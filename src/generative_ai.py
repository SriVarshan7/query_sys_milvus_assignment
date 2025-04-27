import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load API key from environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# Initialize the Gemini model
model = genai.GenerativeModel('gemini-1.5-pro')

def generate_answer(question, context):
    print(f"Question: {question}")
    print(f"Context: {context}")
    prompt = f"Based on the following context, answer the question.\n\nContext:\n{context}\n\nQuestion: {question}\n\nAnswer:"
    response = model.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(
            temperature=0.7,
            max_output_tokens=1024,
        )
    )
    answer = response.text
    print(f"Gemini response: {answer}")
    return answer