from langchain_openai import ChatOpenAI

def load_llm():

    llm = ChatOpenAI(
        model="gpt-4.1-mini",
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