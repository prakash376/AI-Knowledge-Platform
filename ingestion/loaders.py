from pypdf import PdfReader

def load_text(file_path:str)-> str:
    with open(file_path, "r", encoding="utf-8", errors="ignore")as f:
        return f.read()

def load_pdf(file_path:str)-> str:
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
        return text


def load_document(file_path:str)-> str:
    if file_path.endswith(".pdf"):
        return load_pdf(file_path)
    else:
        return load_text(file_path)    