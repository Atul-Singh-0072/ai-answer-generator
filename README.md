# ai-answer-generator
Developed an AI-powered answer generation system leveraging LLMs and RAG architecture to deliver accurate, context-aware responses. Designed with modular components including retriever, generator, and API integration.
# 🤖 AI Answer Generator

An AI-powered answer generation system that leverages Large Language Models (LLMs) and Retrieval-Augmented Generation (RAG) to deliver accurate, context-aware responses from custom documents.

---

## 🚀 Features

- 🔍 Retrieval-Augmented Generation (RAG)
- 📄 Upload and process custom PDF documents
- 🧠 Context-aware answer generation using LLMs
- 📊 Automatic diagram/flowchart generation
- 🌐 Simple and interactive web interface (Flask)
- ⚡ Fast inference using Groq API

---

## 🏗️ Architecture Overview

The system is built using a modular agent-based architecture:

- **Retriever Agent** → Fetches relevant document chunks  
- **Generator Agent** → Generates answers using LLM  
- **Critic Agent** → Refines and improves responses  
- **Diagram Agent** → Generates flowcharts/visual outputs  

---

## 🛠️ Tech Stack

- Python 🐍  
- Flask 🌐  
- LangChain 🔗  
- ChromaDB 📦  
- Sentence Transformers 🤗  
- Groq API ⚡  

---

## 📂 Project Structure
answer_generator-master/
│── agents/
│── chroma_db/ # (ignored in Git)
│── data/ # (ignored in Git)
│── uploads/ # (ignored in Git)
│── templates/
│── static/
│── utils/
│── app.py
│── main.py
│── config.py
│── create_kb.py
## ⚙️ Setup Instructions

1️⃣ Clone the Repository
2️⃣ Create Virtual Environment
3️⃣ Install Dependencies
4️⃣ Set Environment Variable
▶️ Run the Project

🧪 How It Works
Upload a PDF document
Text is split into chunks
Relevant context is retrieved
LLM generates an answer
Optional diagram is generated

👨‍💻 Author
Atul Singh
GitHub: https://github.com/Atul-Singh-0072
