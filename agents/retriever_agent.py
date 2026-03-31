import os
from langchain_community.document_loaders import (
    DirectoryLoader,
    TextLoader,
    PyPDFLoader
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


class MyRetriever:
    def __init__(self, persist_dir="chroma_db"):
        print("[INFO] Initializing Retriever...")

        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        self.persist_dir = persist_dir
        self.vectorstore = None

        print("[INFO] Retriever initialized successfully.")

    # 🔥 LOAD TXT + PDF (Supports Upload File)
    def load_docs(self, data_dir="data", custom_file=None):

        documents = []

        # ✅ If uploaded file is provided
        if custom_file:
            print(f"[INFO] Loading custom file: {custom_file}")

            if custom_file.endswith(".pdf"):
                loader = PyPDFLoader(custom_file)
                documents.extend(loader.load())

            elif custom_file.endswith(".txt"):
                loader = TextLoader(custom_file)
                documents.extend(loader.load())

            return documents

        # ✅ Otherwise load from data folder
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
            print(f"[INFO] '{data_dir}' created. Add .txt or .pdf files and rerun.")
            return []

        # Load TXT files
        txt_loader = DirectoryLoader(
            data_dir,
            glob="*.txt",
            loader_cls=TextLoader
        )
        documents.extend(txt_loader.load())

        # Load PDF files
        pdf_loader = DirectoryLoader(
            data_dir,
            glob="*.pdf",
            loader_cls=PyPDFLoader
        )
        documents.extend(pdf_loader.load())

        print(f"[INFO] Loaded {len(documents)} documents.")
        return documents

    def split_docs(self, docs):
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=100
        )

        split_documents = splitter.split_documents(docs)
        print(f"[INFO] Split into {len(split_documents)} chunks.")
        return split_documents

    def create_vectorstore(self, docs):
        if not docs:
            print("[WARN] No documents to create vectorstore.")
            return None

        print("[INFO] Creating vectorstore...")

        vectorstore = Chroma.from_documents(
            docs,
            embedding=self.embeddings,
            persist_directory=self.persist_dir
        )

        vectorstore.persist()

        print("[INFO] Vectorstore created and persisted.")
        return vectorstore

    def get_relevant_texts(self, query):
        if not self.vectorstore:
            print("[WARN] Vectorstore not initialized.")
            return []

        results = self.vectorstore.similarity_search(query, k=3)

        return [doc.page_content for doc in results]


# ✅ Updated create_retriever
def create_retriever(custom_file=None):

    retriever = MyRetriever()

    docs = retriever.load_docs(custom_file=custom_file)

    if not docs:
        print("[WARN] No documents found.")
        return retriever

    split_docs = retriever.split_docs(docs)

    retriever.vectorstore = retriever.create_vectorstore(split_docs)

    print(f"[INFO] Retriever created successfully.")

    return retriever