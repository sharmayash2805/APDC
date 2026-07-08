from fastapi import FastAPI
from processor import extract_text_from_pdfs
import google.generativeai as genai
import os

# Initialize the API
app = FastAPI()

# Configure the AI using an environment variable (secure!)
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

@app.get("/")
def home():
    return {"message": "Causal Digital Twin Backend is Live!"}

@app.get("/analyze")
def analyze_data():
    """
    1. Extracts text from PDFs
    2. Sends to AI for causal analysis
    3. Returns the insights
    """
    # Step 1: Extract the data using the script you already wrote!
    docs = extract_text_from_pdfs()
    
    if "error" in docs:
        return {"error": docs["error"]}

    # Step 2: Combine all the document text into one big string
    combined_text = ""
    for filename, text in docs.items():
        combined_text += f"\n--- {filename} ---\n{text}\n"

    # Step 3: The "Causal AI" Prompt
    prompt = f"""
    You are a Causal AI Digital Twin for an EPC Supply Chain. 
    Review the following extracted project documents and identify the causal chain of events.
    If there is a delay or quality issue, explain exactly HOW it impacts the rest of the project.
    Provide a structured summary of risks and actionable recommendations.
    
    Documents:
    {combined_text}
    """

    # Step 4: Ask the AI
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return {"insights": response.text}
    except Exception as e:
        return {"error": f"AI generation failed: {str(e)}"}
