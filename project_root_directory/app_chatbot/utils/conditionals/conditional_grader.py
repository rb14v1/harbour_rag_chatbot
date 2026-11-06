from pprint import pprint
from app_chatbot.utils.llm import get_llm
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate

# LLM



class HallucinationGrader:
    def __init__(self, temperature):
        self.llm = get_llm(json_mode=True, temperature=temperature)
        self.prompt_template = PromptTemplate(
            template=""" You are a grader assessing whether
            an answer is grounded in / supported by a set of facts. Give a binary 'yes' or 'no' score to indicate
            whether the answer is grounded in / supported by a set of facts. Provide the binary score as a JSON with a
            single key 'score' and no preamble or explanation. 
            Here are the facts:
            \n ------- \n
            {documents}
            \n ------- \n
            Here is the answer: {generation}  """,
            input_variables=["generation", "documents"],
        )
        self.hallucination_grader = self.prompt_template | self.llm | JsonOutputParser()


class AnswerGrader:
    def __init__(self, temperature):
        self.llm = get_llm(json_mode=True, temperature=temperature)
        self.prompt_template = PromptTemplate(
            template=""" You are a grader assessing whether an
            answer is useful to resolve a question. Give a binary score 'yes' or 'no' to indicate whether the answer is
            useful to resolve a question. Provide the binary score as a JSON with a single key 'score' and no preamble or explanation.
              Here is the answer:
            \n ------- \n
            {generation}
            \n ------- \n
            Here is the question: {question} """,
            input_variables=["generation", "question"],
        )
        self.answer_grader = self.prompt_template | self.llm | JsonOutputParser()


def _normalise(score):
    value = score.get("score", "") if isinstance(score, dict) else score
    return str(value).strip().strip("'\"").lower()


def grade_generation_v_documents_and_question(state):
    """
    Determines whether the generation is grounded in the document and answers question.

    Args:
        state (dict): The current graph state

    Returns:
        str: Decision for next node to call
    """
    hallucination_grader = HallucinationGrader(
        temperature=0).hallucination_grader
    answer_grader = AnswerGrader(
        temperature=0).answer_grader
    print("---CHECK HALLUCINATIONS---")
    question = state["question"]
    documents = state["documents"]
    generation = state["generation"]

    docs_text = "\n\n".join(
        getattr(d, "page_content", str(d)) for d in documents)
    score = hallucination_grader.invoke(
        {"documents": docs_text, "generation": generation}
    )
    grade = _normalise(score)
    print(f"---HALLUCINATION GRADER RAW: {score}---")

    # Check hallucination
    if grade == "yes":
        print("---DECISION: GENERATION IS GROUNDED IN DOCUMENTS---")
        # Check question-answering
        print("---GRADE GENERATION vs QUESTION---")
        score = answer_grader.invoke(
            {"question": question, "generation": generation})
        grade = _normalise(score)
        if grade == "yes":
            print("---DECISION: GENERATION ADDRESSES QUESTION---")
            return "useful"
        else:
            print("---DECISION: GENERATION DOES NOT ADDRESS QUESTION---")
            return "not useful"
    else:
        pprint("---DECISION: GENERATION IS NOT GROUNDED IN DOCUMENTS, RE-TRY---")
        return "not supported"
