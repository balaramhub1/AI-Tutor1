import os
from pypdf import PdfReader

cwd = os.getcwd()
parentDir = os.path.dirname(os.getcwd())
parentDir2 = os.path.dirname(os.path.abspath(__file__))
print(" Current working directory: ", cwd)
print(" Parent folder path : ", parentDir)
print(" path: ",os.path.dirname(os.path.abspath(__file__)))
print(" new path : ", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "sample.pdf"))
newPath = os.path.join(parentDir, "uploaded_pdfs")
print(" new path 1 : ", newPath)
print( " new path 2 : ", os.path.join(parentDir, "uploaded_pdfs"))

for file in os.listdir(newPath):
    if file.endswith(".pdf"):
        pdf_path = os.path.join(newPath, file)
        print(" PDF path : ", pdf_path)

        reader = PdfReader(pdf_path)
        full_text = ""
        for page in reader.pages:
            full_text += page.extract_text() + "\n"

        print(" Extracted text from PDF: ", full_text[:500])  # Print the first 500 characters of the extracted text