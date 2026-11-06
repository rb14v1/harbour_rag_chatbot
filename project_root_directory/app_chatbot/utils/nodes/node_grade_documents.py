# Retrieval Grader

from app_chatbot.utils.llm import get_llm
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate

# LLM



class RetrievalGrader:
    def __init__(self, temperature):
        self.llm = get_llm(json_mode=True, temperature=temperature)
        self.prompt_template = PromptTemplate(
            template=""" You are a grader assessing relevance
            of a retrieved document to a user question. If the document contains keywords related to the user question,
            grade it as relevant. It does not need to be a stringent test. The goal is to filter out erroneous retrievals. \n
            Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question. \n
            Provide the binary score as a JSON with a single key 'score' and no preamble or explanation.
             
            Here is the retrieved document: \n\n {document} \n\n
            Here is the user question: {question} \n 
            """,
            input_variables=["question", "document"],
        )
        self.retrieval_grader = self.prompt_template | self.llm | JsonOutputParser()


def grade_documents(state):
    """
    Determines whether the retrieved documents are relevant to the question
    If any document is not relevant, we will set a flag to run web search

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): Filtered out irrelevant documents and updated web_search state
    """

    retrieval_grader = RetrievalGrader(
        temperature=0).retrieval_grader
    print("---CHECK DOCUMENT RELEVANCE TO QUESTION---")
    question = state["question"]
    documents = state["documents"]

    # Score each doc
    filtered_docs = []
    web_search = "No"
    for d in documents:
        score = retrieval_grader.invoke(
            {"question": question, "document": d.page_content}
        )
        grade = str(score.get("score", "") if isinstance(score, dict) else score).strip().lower()
        # Document relevant
        if grade == "yes":
            print("---GRADE: DOCUMENT RELEVANT---")
            filtered_docs.append(d)
        # Document not relevant
        else:
            print("---GRADE: DOCUMENT NOT RELEVANT---")
            # We do not include the document in filtered_docs
            # We set a flag to indicate that we want to run web search
            web_search = "Yes"
            continue
    return {"documents": filtered_docs, "question": question, "web_search": web_search}
