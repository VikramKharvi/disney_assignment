from langchain_core.prompts import ChatPromptTemplate
def generate_unstructured_response(llm,vector_store,question):
    template = """<s>[INST] Provide answer to the question in short based on the context provided below:

    **Question:** {question}

    **Context:** {context}
    [/INST] </s>
    """

    prompt = ChatPromptTemplate.from_template(template)

    chain = prompt | llm
    results = vector_store.similarity_search(
        question,
        k=1,
    )
    answer = chain.invoke({"question": question,"context": results[0].page_content})
    return answer
