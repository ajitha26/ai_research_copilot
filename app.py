import streamlit as st
from utils.pdf_utils import extract_text_from_pdf
from utils.embedding_utils import chunk_text, embed_and_upsert, query_pinecone
from utils.llm_utils import ask_gemini

st.title("📘 AI Research Copilot (RAG with Pinecone + Gemini)")

# Upload PDFs
uploaded_files = st.file_uploader("Upload PDFs", type=["pdf"], accept_multiple_files=True)

if uploaded_files:
    st.write("Processing documents...")
    for file in uploaded_files:
        raw_text = extract_text_from_pdf(file)
        chunks = chunk_text(raw_text)
        embed_and_upsert(chunks)
    st.success("Documents uploaded and indexed in Pinecone ✅")

# Ask a question
question = st.text_input("Ask a question about your documents:")
if st.button("Get Answer") and question:
    context = query_pinecone(question)
    answer = ask_gemini(question, context)
    st.write("### 📌 Answer")
    st.write(answer)
