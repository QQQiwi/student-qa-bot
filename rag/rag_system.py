from rag.model import LlamaModel
from qdrant.vector_storage import get_vectors

model = LlamaModel()

def format_docs(docs):
    return "\n\n".join(f"Title: {doc['title']}\nContent: {doc['content']}" for doc in docs)

def get_response(query):
    vectors = get_vectors(query)
    context = format_docs(vectors)
    prompt = f"Context: {context}\nQuestion: {query}\nAnswer:"
    return model.generate_response(prompt)
