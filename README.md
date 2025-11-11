# Educational RAG-Based Chatbot

A Retrieval-Augmented Generation (RAG) chatbot that allows users to upload PDFs and ask questions. The chatbot retrieves relevant text chunks using FAISS and generates answers using a local LLM.

---

## Features
- Upload PDFs and automatically build vector embeddings
- Ask natural language questions
- Retrieve top-k relevant text chunks
- Generate answers using a local LLM
- Optional session memory for context
- Full-stack implementation (React frontend + Flask backend)

---

## Tech Stack
- **Frontend:** React, Dropzone, Axios  
- **Backend:** Flask, Python 3.13+  
- **Vectorization & Retrieval:** LocalOllamaEmbedder, PyMuPDF, FAISS  
- **Storage:** JSON / SQLite (optional)  
- **Version Control:** Git / GitHub  

---

## End-to-End AI Use Case Lifecycle

| Step | Description | Methods / Techniques |
|------|------------|--------------------|
| **Ideation** | Identify the problem and AI solution | Stakeholder interviews, problem analysis, brainstorming educational use cases |
| **Feasibility Analysis** | Check viability of the solution | Data availability check (PDF corpus), technology stack evaluation, cost-benefit analysis |
| **Prototyping** | Build a minimum viable solution | Jupyter notebooks for text extraction, embeddings, similarity search; basic Flask API |
| **Design** | Plan architecture and workflow | Architecture diagrams, data flow charts, API endpoint design, component diagrams |
| **Development** | Implement production-ready system | React frontend, Flask backend, PDF vectorization, embeddings, FAISS index, answer generation logic |
| **Deployment** | Make it accessible to users | Docker containers, local server deployment, optional cloud deployment (AWS/GCP/Azure), CI/CD pipelines |
| **Monitoring & Maintenance** | Ensure reliability | Logging, performance monitoring, error handling, model evaluation |
| **Iteration & Scaling** | Improve and expand system | Feature addition (multi-file support, memory), optimize retrieval and embeddings, scaling backend for concurrency |

---

## System Architecture & Flow

[User Frontend (React)]
|
v
REST API (Flask)
/upload_pdf ---> PDFVectorizer ---> LocalOllamaEmbedder ---> FAISS Index
/ask ---> ChatbotService ---> FAISS Index search ---> CSVChatbot ---> Answer

markdown
Copy code

---

## Layers Breakdown

### User Layer (Frontend)
- **Technologies:** React, Dropzone, Axios  
- Features:
  - Upload PDFs
  - Ask questions
  - Display chat history
- Components:
  - PDF Dropzone
  - Chat input box
  - Chat window (Q&A display)
- Communication:
  - `/upload_pdf` → upload PDFs
  - `/ask` → send question and receive answer

### Backend Layer (Flask)
- Handles API requests
- Manages PDF ingestion and FAISS index
- Generates answers from top-k results

**Routes:**
- `/upload_pdf` → receives PDFs → PDFVectorizer → rebuilds FAISS index
- `/ask` → receives question → fetches top-k results → CSVChatbot generates answer

**ChatbotService (Singleton) Components:**
- LocalOllamaEmbedder → generates embeddings
- PDFVectorizerUnstructured → extracts PDF text & builds FAISS
- CSVChatbot → generates final answer

**Methods:**
- `ask(query, k)` → main entry for generating answer
- `build_faiss_index_from_data()` → builds FAISS index
- `get_faiss_results(query, k)` → retrieves top-k chunks

### Vectorization Layer
- **Technologies:** LocalOllamaEmbedder, PyMuPDF, FAISS  
- Responsibilities:
  - Extract text from PDFs
  - Generate embeddings
  - Build FAISS index for fast similarity search

### Retrieval Layer (FAISS Index)
- Stores embeddings of all PDF chunks
- Performs similarity search
- Returns top-k relevant text chunks + metadata

### Chatbot Layer (QA Model)
- Components: CSVChatbot, LLM  
- Responsibilities:
  - Take top-k chunks from FAISS
  - Combine with user query
  - Generate final answer
  - Optional memory module for session history

### Storage Layer
- PDFs → stored in `chat/data/`
- FAISS index → in-memory (optional disk serialization)
- Chat history → optional JSON or database (SQLite/PostgreSQL)

### Memory Options
| Type | Description |
|------|-------------|
| In-Memory | Python list/dict per session; fast but lost on restart |
| Persistent | Store chat history in JSON or database; survives restarts |
| Hybrid | Last N messages in memory + persistent storage for speed & reliability |

---

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/JhaswinArjunSuresh/EducationalChatBot.git
cd EducationalChatBot
2. Setup Backend
Create a Python virtual environment:

bash
Copy code
python3 -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
Install required Python packages:

bash
Copy code
pip install -r requirements.txt
(Optional) Set environment variables:

bash
Copy code
export KPI_DB_PATH="chat/data/kpi_data.db"
export KPI_SQL_MODEL="google-gla:gemini-2.5-flash"
Start Flask backend:

bash
Copy code
python app.py
Backend runs at: http://localhost:5000

3. Setup Frontend
Navigate to frontend folder:

bash
Copy code
cd frontend
Install dependencies:

bash
Copy code
npm install
Start React app:

bash
Copy code
npm start
Frontend runs at: http://localhost:3000

Ensure backend is running before using frontend.

Usage
Upload PDFs
Go to “Upload PDF(s)” section

Drag & drop PDFs or click to select files

Click Upload & Rebuild Index

PDFs will be indexed for question answering

Ask Questions
Type your question in chat box

Press Enter or click Ask

Answers include references to relevant PDF content

Formatting Results & Answers
Backend combines results used for answering and final answer:

python
Copy code
results_text = "\n\n".join([f"{r['rank']}. {r['text']}" for r in results])
answer = self.chatbot.generate_answer(query, results_text)

final_text = (
    f"Thinking - Content used for answering:\n\n"
    f"{results_text}\n\n"
    f"Answer:\n{answer}"
)
React Frontend Rendering Example:

jsx
Copy code
<p style={{whiteSpace: 'pre-wrap'}}>
  <strong>Answer:</strong> {answer}
</p>
Limitations
Memory is optional; default is session-based

FAISS index rebuilds after each upload (incremental update can improve)

Currently supports PDFs only

Local embeddings may limit scalability; cloud LLM integration possible
