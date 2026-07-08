import fitz  # PyMuPDF
import os

def extract_text_from_pdfs(data_folder="data"):
    """
    Reads all PDF documents in the specified folder and extracts their text.
    """
    extracted_data = {}
    
    # Check if the data folder exists
    if not os.path.exists(data_folder):
        return {"error": f"Folder '{data_folder}' not found."}

    # Loop through the 5-10 PDF test cases
    for filename in os.listdir(data_folder):
        if filename.endswith(".pdf"):
            filepath = os.path.join(data_folder, filename)
            
            # Open the PDF and extract text via OCR/Parsing
            doc = fitz.open(filepath)
            text = ""
            for page in doc:
                text += page.get_text()
                
            extracted_data[filename] = text
            doc.close()
            
    return extracted_data

# Quick test to ensure it works
if __name__ == "__main__":
    docs = extract_text_from_pdfs()
    print(f"Successfully extracted text from {len(docs)} documents.")
