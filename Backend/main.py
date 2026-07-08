from fastapi import FastAPI
from processor import extract_text_from_pdfs
import google.generativeai as genai
import networkx as nx
import os
from fastapi.middleware.cors import CORSMiddleware

# Initialize the API
app = FastAPI()

# 1. Configure CORS (Crucial for Vercel <-> Render connection)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Configure the AI 
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

# 3. Configure the Graph (Causal Digital Twin Spine)
twin_graph = nx.DiGraph()
entities = ["PowerTech Inc.", "Backup Generator A", "Install-Task", "System Testing"]
twin_graph.add_nodes_from(entities)
causal_relationships = [
    ("PowerTech Inc.", "Backup Generator A"),  
    ("Backup Generator A", "Install-Task"),    
    ("Install-Task", "System Testing")         
]
twin_graph.add_edges_from(causal_relationships)

# --- API ENDPOINTS ---

@app.get("/")
def home():
    return {"message": "Causal Digital Twin Backend is Live!"}

# ONLY ONE DEFINITION OF /view-twin
@app.get("/view-twin")
def view_twin():
    """Returns the in-memory graph structure"""
    return {
        "nodes": list(twin_graph.nodes()),
        "edges": list(twin_graph.edges())
    }

@app.get("/simulate-delay/{node_name}")
def simulate_delay(node_name: str):
    """Traces the Domino Effect of a delay"""
    if node_name not in twin_graph:
        return {"error": f"Entity '{node_name}' not found in the Digital Twin."}
    
    impacted_nodes = list(nx.descendants(twin_graph, node_name))
    return {
        "delayed_entity": node_name,
        "downstream_impact": impacted_nodes,
        "warning": f"Delaying {node_name} will impact {len(impacted_nodes)} subsequent steps."
    }

@app.get("/analyze")
def analyze_data():
    """Extracts PDFs and uses Gemini to analyze causal impacts"""
    docs = extract_text_from_pdfs()
    
    if "error" in docs:
        return {"error": docs["error"]}

    combined_text = ""
    for filename, text in docs.items():
        combined_text += f"\n--- {filename} ---\n{text}\n"

    prompt = f"""
    You are a Causal AI Digital Twin for an EPC Supply Chain. 
    Review the following extracted project documents and identify the causal chain of events.
    If there is a delay or quality issue, explain exactly HOW it impacts the rest of the project.
    Provide a structured summary of risks and actionable recommendations.
    
    Documents:
    {combined_text}
    """

    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return {"insights": response.text}
    except Exception as e:
        return {"error": f"AI generation failed: {str(e)}"}
