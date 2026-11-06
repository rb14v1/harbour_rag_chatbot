# Search
import os
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()

os.environ["TAVILY_API_KEY"] = os.getenv('TAVILY_API_KEY', '')


class WebSearch:
    def __init__(self, k):
        self.k = k
        self.web_search_tool = TavilySearchResults(k=self.k)


def web_search(state):
    """
    Web search based based on the question

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): Appended web results to documents
    """

    print("---WEB SEARCH---")
    question = state["question"]
    documents = state.get("documents")
    if not os.environ.get("TAVILY_API_KEY"):
        print("TAVILY_API_KEY not set, skipping web search")
        return {"documents": documents or [], "question": question}
    web_search_tool = WebSearch(k=3).web_search_tool

    # Web search
    docs = web_search_tool.invoke({"query": question})
    web_results = "\n".join([d["content"] for d in docs])
    web_results = Document(page_content=web_results)
    if documents is not None:
        documents.append(web_results)
    else:
        documents = [web_results]
    return {"documents": documents, "question": question}
