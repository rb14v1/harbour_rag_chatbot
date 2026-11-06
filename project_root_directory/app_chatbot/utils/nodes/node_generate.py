# Generate

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from app_chatbot.utils.llm import get_llm

class RAGChain:
    def __init__(self, temperature):
        self.llm = get_llm(json_mode=False, temperature=temperature)
        self.prompt_template = PromptTemplate(
            template=""" You are an assistant for question-answering tasks.
            Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know.
            Use three sentences maximum and keep the answer concise 
            Question: {question}
            Context: {context}
            Answer: """,
            input_variables=["question", "context"],
        )
        self.rag_chain = self.prompt_template | self.llm | StrOutputParser()

    def format_docs(self, docs):
        return "\n\n".join(doc.page_content for doc in docs)


def generate(state):
    """
    Generate answer using RAG on retrieved documents

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): New key added to state, generation, that contains LLM generation
    """
    # Chain
    rag_chain = RAGChain(temperature=0).rag_chain
    print("---GENERATE---")
    question = state["question"]
    documents = state["documents"]

    # RAG generation
    generation = rag_chain.invoke({"context": documents, "question": question})
    return {"documents": documents, "question": question, "generation": generation}
