
def search(vector_store, query):

    results = vector_store.similarity_search(
        query,
        k=5
    )

    return results