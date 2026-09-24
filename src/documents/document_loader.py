import os
from pathlib import Path

# pip install pypdf
from pypdf import PdfReader


def load_pdf(file_path):
    reader = PdfReader(file_path)
    all_text = ""
    for page in reader.pages:
        text = page.extract_text()
        if text:
            all_text += text + "\n"
    return all_text


def load_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def load_document(file_path):
    if not os.path.exists(file_path):
        print("File not found:", file_path)
        return ""

    ext = Path(file_path).suffix.lower()

    if ext == ".pdf":
        print("Loading PDF...")
        return load_pdf(file_path)
    elif ext == ".txt":
        print("Loading TXT file...")
        return load_txt(file_path)
    else:
        print("Unsupported file type:", ext)
        return ""


# test
if __name__ == "__main__":
    text = load_document("../../data/safety_manual.pdf")
    print("Characters loaded:", len(text))
    print(text[:300])
