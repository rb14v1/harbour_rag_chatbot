from app_chatbot.utils.llm import get_llm
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate

# LLM



class QuestionRouter:
    def __init__(self, temperature):
        self.llm = get_llm(json_mode=True, temperature=temperature)
        self.prompt_template = PromptTemplate(
            template=""" You are an expert at routing a user question to a vectorstore, web search, or a direct answer.
            The vectorstore holds the user's own uploaded documents and ingested web pages. Use 'vectorstore' for any factual, technical or topical question,
            even if you are unsure the documents cover it. Use 'web_search' only for news, current events, live prices, or things that change daily.
            Use 'direct' only for greetings, thanks and small talk. Return a JSON with a single key 'datasource' whose value is
            'vectorstore', 'web_search' or 'direct', with no preamble or explanation. Question to route: {question} """,
            input_variables=["question"],
        )
        self.question_router = self.prompt_template | self.llm | JsonOutputParser()


def route_question(state):
    """
    Route question to web search or RAG.

    Args:
        state (dict): The current graph state

    Returns:
        str: Next node to call
    """
    question_router = QuestionRouter(
        temperature=0).question_router
    print("---ROUTE QUESTION---")
    question = state["question"]
    print(question)
    source = question_router.invoke({"question": question})
    print(source)
    print(source["datasource"])
    if source["datasource"] == "web_search":
        print("---ROUTE QUESTION TO WEB SEARCH---")
        return "websearch"
    elif source["datasource"] == "vectorstore":
        print("---ROUTE QUESTION TO RAG---")
        return "vectorstore"
    print("---ROUTE QUESTION TO DIRECT ANSWER---")
    return "direct"
