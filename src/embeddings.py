from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

def split_text_into_chunks(text, chunk_size=200):
    """Split text into chunks of specified word size."""
    words = text.split()
    chunks = [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]
    return chunks

def generate_embeddings(chunks):
    """Generate embeddings for a list of text chunks."""
    embeddings = model.encode(chunks)
    return embeddings