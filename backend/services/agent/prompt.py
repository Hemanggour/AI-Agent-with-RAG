from langchain.prompts import PromptTemplate


def get_prompt_template():
    return PromptTemplate(
        input_variables=["context", "question"],
        template="""
You are a professional accounting assistant.

You have access to the following document snippets from accounting standards and explanations. These snippets may be fragmented. Use only the *relevant information* to answer the user's question accurately and completely.
- Give detailed answers.

Context:
{context}

Question:
{question}

Answer:
""".strip(),  # noqa
    )
