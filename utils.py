import google.generativeai as genai
from django.conf import settings
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_embedding(text):
    """Generate embedding for the given text using Gemini API."""
    if not text or not text.strip():
        return [0.0] * 768
    
    try:
        result = genai.embed_content(
            model="models/embedding-001",
            content=text,
            task_type="retrieval_document"
        )
        
        # Debug: Print the result structure
        print(f"DEBUG: Result type: {type(result)}")
        print(f"DEBUG: Result keys: {dir(result)}")
    
        embedding = result.embedding 
        
        print(f"DEBUG: Successfully generated embedding with {len(embedding)} dimensions")
        print(f"DEBUG: First 5 values: {embedding[:5]}")
        
        return embedding
        
    except Exception as e:
        print(f"Embedding generation failed: {e}")
        import traceback
        traceback.print_exc()  # Print full error details
        return [0.0] * 768
