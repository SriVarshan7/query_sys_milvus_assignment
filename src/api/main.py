from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import numpy as np
from src.data_extraction import extract_text_from_url, extract_text_from_image, extract_text_from_pdf
from src.embeddings import split_text_into_chunks, generate_embeddings
from src.milvus_ops import create_collection, insert_data, search
from src.generative_ai import generate_answer

app = FastAPI()

class Source(BaseModel):
    type: str  # "url", "image", "pdf"
    value: str  # URL or file path

class InsertRequest(BaseModel):
    sources: List[Source]

class QueryRequest(BaseModel):
    question: str

@app.on_event("startup")
def startup_event():
    global collection
    collection = create_collection()

@app.post("/insert")
def insert_sources(request: InsertRequest):
    for source in request.sources:
        print(f"Processing source: type={source.type}, value={source.value}")
        if source.type == "url":
            text = extract_text_from_url(source.value)
        elif source.type == "image":
            print(f"Attempting to access image file: {source.value}")
            text = extract_text_from_image(source.value)
        elif source.type == "pdf":
            print(f"Attempting to access PDF file: {source.value}")
            text = extract_text_from_pdf(source.value)
        else:
            raise HTTPException(status_code=400, detail="Invalid source type")
        
        if text is None:
            print(f"No text extracted from source: {source.value}")
            continue
        
        print(f"Extracted text: {text[:100]}...")  # Log first 100 chars of extracted text
        chunks = split_text_into_chunks(text)
        embeddings = generate_embeddings(chunks)
        source_types = [source.type] * len(chunks)
        source_urls = [source.value] * len(chunks)
        insert_data(collection, embeddings, chunks, source_types, source_urls)
    
    return {"message": "Sources inserted successfully"}

@app.post("/query")
def query_system(request: QueryRequest):
    question = request.question
    print(f"Received query: {question}")
    question_embedding = generate_embeddings([question])[0]
    results = search(collection, question_embedding, prioritize_recent=True)  # Prioritize recent uploads
    
    context = ""
    sources = set()
    for hit in results[0]:
        context += hit.entity.get("text") + "\n"
        sources.add(hit.entity.get("source_url"))
    
    print(f"Context for query: {context[:100]}...")  # Log first 100 chars of context
    answer = generate_answer(question, context)
    print(f"Generated answer: {answer}")
    
    return {"answer": answer, "sources": list(sources)}

@app.post("/clear")
def clear_collection():
    global collection
    from pymilvus import utility
    # Drop the existing collection
    utility.drop_collection("demo_collection")
    # Recreate the collection
    collection = create_collection()
    return {"message": "Collection cleared successfully"}