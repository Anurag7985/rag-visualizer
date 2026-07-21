from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

def load_llm():

    llm = ChatGroq(
       model="llama-3.1-8b-instant",
       temperature=0
    )

    return llm


def generate_answer(llm, context, query):

    prompt = f"""
You are a helpful assistant.

Use only the following context.

Context:
{context}

Question:
{query}

If the answer is not present in the context, say "I don't know."
"""

    response = llm.invoke(prompt)

    return response.content