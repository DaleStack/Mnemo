import google.generativeai as genai
from django.conf import settings
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_embedding(text):
    """Generate embedding for the given text using Gemini API."""
    try:
        result = genai.embed_content(
            model = "models/embedding-001",
            content=text,
            task_type="retrieval_document"
        )
        return result['embedding']
    except Exception as e:
        print(f"Embedding generation failed: {e}")
        return [0.0] * 768 # Return a zero vector on failure