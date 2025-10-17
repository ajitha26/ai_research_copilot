import os
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()

def ask_gemini(question, context):
    """Send context + question to Gemini and get an answer"""
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-2.5-flash")

    prompt = f"""Answer the question based on the context below:

Context:
{context}

Question:
{question}
"""
    response = model.generate_content(prompt)
    return response.text
