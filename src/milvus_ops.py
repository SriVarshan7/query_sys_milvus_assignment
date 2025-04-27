from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType, utility
import time

MILVUS_HOST = 'localhost'
MILVUS_PORT = '19530'

def connect_to_milvus():
    """Connect to Milvus server."""
    connections.connect(host=MILVUS_HOST, port=MILVUS_PORT)

def create_collection():
    """Create a Milvus collection if it doesn't exist."""
    connect_to_milvus()
    if not utility.has_collection("demo_collection"):
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
            FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=384),
            FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=65535),
            FieldSchema(name="source_type", dtype=DataType.VARCHAR, max_length=10),
            FieldSchema(name="source_url", dtype=DataType.VARCHAR, max_length=1000),
            FieldSchema(name="timestamp", dtype=DataType.DOUBLE)  # New field for timestamp
        ]
        schema = CollectionSchema(fields, description="Text chunks with embeddings")
        collection = Collection(name="demo_collection", schema=schema)
        index_params = {
            "index_type": "IVF_FLAT",
            "metric_type": "L2",
            "params": {"nlist": 128}
        }
        collection.create_index(field_name="vector", index_params=index_params)
    else:
        collection = Collection("demo_collection")
    
    # Load the collection into memory
    collection.load()
    return collection

def insert_data(collection, embeddings, texts, source_types, source_urls):
    """Insert data into Milvus collection."""
    current_time = time.time()
    entities = [
        {"vector": emb.tolist(), "text": txt, "source_type": st, "source_url": su, "timestamp": current_time}
        for emb, txt, st, su in zip(embeddings, texts, source_types, source_urls)
    ]
    collection.insert(entities)

def search(collection, query_embedding, top_k=5, prioritize_recent=True):
    """Search Milvus collection for similar embeddings, optionally prioritizing recent entries."""
    search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
    if prioritize_recent:
        # Get the current timestamp and calculate a threshold (e.g., last 1 hour)
        current_time = time.time()
        time_threshold = current_time - 3600  # 1 hour ago
        expr = f"timestamp >= {time_threshold}"
        results = collection.search(
            [query_embedding], "vector", search_params, limit=top_k,
            output_fields=["text", "source_url"], expr=expr
        )
    else:
        results = collection.search(
            [query_embedding], "vector", search_params, limit=top_k,
            output_fields=["text", "source_url"]
        )
    return results