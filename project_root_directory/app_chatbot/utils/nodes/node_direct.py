from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from app_chatbot.utils.llm import get_llm


def direct_answer(state):
    """Answer greetings and general questions without retrieval."""
    print("---DIRECT ANSWER---")
    question = state["question"]
    prompt = PromptTemplate(
        template="""You are a friendly, concise assistant. Answer the user's message directly.
            Message: {question}
            Answer: """,
        input_variables=["question"],
    )
    chain = prompt | get_llm(json_mode=False, temperature=0) | StrOutputParser()
    return {"generation": chain.invoke({"question": question}),
            "question": question, "documents": []}
