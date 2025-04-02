import os
from document_loader import load_pdf, load_docx, load_txt, load_html
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface.embeddings import HuggingFaceEmbeddings

DATA_PATH = "data/"
CHROMA_PATH = "docs_index/"
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

print("Current working directory:", os.getcwd())

def load_all_documents():
    documents = []
    for root, _, files in os.walk(DATA_PATH):
        print(f"Checking directory: {root}")
        print(f"Found files: {files}")
        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith('.pdf'):
                documents.append(load_pdf(file_path))
            elif file.endswith('.docx'):
                documents.append(load_docx(file_path))
            elif file.endswith('.txt') or file.endswith('.md'):
                documents.append(load_txt(file_path))
            elif file.endswith('.html'):
                documents.append(load_html(file_path))
    return documents


def main():
    documents = load_all_documents()
    if not documents:
        raise FileNotFoundError("No documents found!")

    # Split the text into chunks using langchain
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(documents)

    # Save the chunks as embeddings in the vector db
    db = Chroma.from_documents(chunks, embeddings, persist_directory=CHROMA_PATH)
    db.persist()
    print("✅ Documents indexed successfully!")

if __name__ == "__main__":
    main()
