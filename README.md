Educational RAG-Based Chatbot

A Retrieval-Augmented Generation (RAG) chatbot that allows users to upload PDFs and ask questions. The chatbot retrieves relevant text chunks using FAISS and generates answers using a local LLM.

Features

Upload PDFs and automatically build vector embeddings

Ask natural language questions

Retrieve top-k relevant text chunks

Generate answers using a local LLM

Optional session memory for context

Full-stack implementation (React frontend + Flask backend)

Tech Stack

Frontend: React, Dropzone, Axios

Backend: Flask, Python 3.13+

Vectorization & Retrieval: LocalOllamaEmbedder, PyMuPDF, FAISS

Storage: JSON / SQLite (optional)

Version Control: Git / GitHub

Installation
1. Clone the Repository
git clone https://github.com/JhaswinArjunSuresh/EducationalChatBot.git
cd EducationalChatBot

2. Setup Backend

Create a Python virtual environment (recommended):

python3 -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows


Install required Python packages:

pip install -r requirements.txt


(Optional) Set environment variables:

export KPI_DB_PATH="chat/data/kpi_data.db"
export KPI_SQL_MODEL="google-gla:gemini-2.5-flash"


Start the Flask backend:

python app.py


By default, backend runs at: http://localhost:5000

3. Setup Frontend

Navigate to frontend folder:

cd frontend


Install dependencies:

npm install


Start React app:

npm start


By default, frontend runs at: http://localhost:3000

Ensure the backend (http://localhost:5000) is running before using the frontend.

Usage
Upload PDFs

Go to the “Upload PDF(s)” section

Drag & drop PDFs or click to select files

Click Upload & Rebuild Index

PDFs will be indexed in FAISS for question answering

Ask Questions

Type your question in the chat box

Press Enter or click Ask

Answers will include references to relevant PDF content

Memory Options

In-memory: session-based, lost on restart

Persistent: store chat history in JSON or database

Hybrid: combination of in-memory + persistent storage

Formatting Answers

Results used for answering are shown before the final answer

Multi-line answers preserved using \n or white-space: pre-wrap in React

Example in backend:

results_text = "\n\n".join([f"{r['rank']}. {r['text']}" for r in results])
answer = self.chatbot.generate_answer(query, results_text)

final_text = (
    f"Thinking - Content used for answering:\n\n"
    f"{results_text}\n\n"
    f"Answer:\n{answer}"
)

GitHub Repository

https://github.com/JhaswinArjunSuresh/EducationalChatBot
