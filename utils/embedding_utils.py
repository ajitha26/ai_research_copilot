import os
from pinecone import Pinecone, ServerlessSpec
from langchain.text_splitter import RecursiveCharacterTextSplitter
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()

# Initialize Pinecone
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index_name = "researchindex"

def get_or_create_index(dimension=768):
    """Create or connect to Pinecone index"""
    if index_name not in [i.name for i in pc.list_indexes()]:
        pc.create_index(
            name=index_name,
            dimension=dimension,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1")
        )
    return pc.Index(index_name)

def chunk_text(text, chunk_size=500, overlap=50):
    """Split text into smaller chunks"""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=overlap
    )
    return splitter.split_text(text)

def embed_and_upsert(chunks):
    """Embed text chunks with Gemini and store in Pinecone"""
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    embed_model = "models/text-embedding-004"
    index = get_or_create_index()

    vectors = []
    for i, chunk in enumerate(chunks):
        emb = genai.embed_content(model=embed_model, content=chunk)
        vectors.append((f"chunk-{i}", emb["embedding"], {"text": chunk}))
    index.upsert(vectors=vectors)

def query_pinecone(question, top_k=3):
    """Query Pinecone and return retrieved context"""
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    embed_model = "models/text-embedding-004"
    index = get_or_create_index()

    q_emb = genai.embed_content(model=embed_model, content=question)["embedding"]
    results = index.query(vector=q_emb, top_k=top_k, include_metadata=True)
    context = "\n".join([m["metadata"]["text"] for m in results["matches"]])
    return context
