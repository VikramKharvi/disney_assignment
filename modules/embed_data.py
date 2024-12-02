from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import CacheBackedEmbeddings,HuggingFaceEmbeddings
from langchain.storage import LocalFileStore
from langchain_chroma import Chroma
from uuid import uuid4

def run_embeddings(extracted_data):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500,
                                        chunk_overlap=20,)
    splitted_documents = text_splitter.transform_documents(extracted_data)

    store = LocalFileStore("./cache/")
    embed_model_id = 'BAAI/bge-small-en-v1.5'
    core_embeddings_model = HuggingFaceEmbeddings(model_name=embed_model_id)
    embedder = CacheBackedEmbeddings.from_bytes_store(core_embeddings_model,
                                                    store,
                                                    namespace=embed_model_id)

    vector_store = Chroma(
        collection_name="disney",
        embedding_function=embedder,
        persist_directory="database/chroma_langchain_db",  # Where to save data locally
    )

    # uuids = [str(uuid4()) for _ in range(len(splitted_documents))]
    # vector_store.add_documents(documents=splitted_documents, ids=uuids)

    def add_documents_in_batches(vector_store, documents, batch_size=2):
        for i in range(0, len(documents), batch_size):
            batch_documents = documents[i:i + batch_size]
            uuids = [str(uuid4()) for _ in range(len(batch_documents))]  # Generate UUIDs for this batch

            # Add documents to the vector store with their corresponding UUIDs
            vector_store.add_documents(documents=batch_documents, ids=uuids)
            print(f"Added batch {i // batch_size + 1}: {uuids}")

    add_documents_in_batches(vector_store,splitted_documents)
    print('embed complete')
    return vector_store