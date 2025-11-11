import React, { useState } from "react";
import { useDropzone } from "react-dropzone";
import axios from "axios";
import "./App.css";

function App() {
  const [pdfFiles, setPdfFiles] = useState([]);
  const [question, setQuestion] = useState("");
  const [chatHistory, setChatHistory] = useState([]);
  const [loading, setLoading] = useState(false);

  // Dropzone
  const { getRootProps, getInputProps } = useDropzone({
    accept: { "application/pdf": [".pdf"] },
    onDrop: (acceptedFiles) => setPdfFiles(acceptedFiles),
  });

  const handleUpload = async () => {
    if (!pdfFiles.length) return;
    const formData = new FormData();
    pdfFiles.forEach((file) => formData.append("files", file)); // "files" matches backend

    setLoading(true);
    try {
      await axios.post("http://localhost:5000/upload_pdf", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      alert("PDF(s) uploaded and FAISS index rebuilt!");
      setPdfFiles([]);
    } catch (err) {
      console.error(err);
      alert("Failed to upload PDF(s).");
    } finally {
      setLoading(false);
    }
  };

  const handleAsk = async () => {
    if (!question.trim()) return;

    setLoading(true);
    try {
      const response = await axios.post("http://localhost:5000/ask", {
        query: question,
      });
      setChatHistory([...chatHistory, { question, answer: response.data.answer }]);
      setQuestion("");
    } catch (err) {
      console.error(err);
      alert("Failed to get answer from chatbot.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <h1 className="title">📚 Educational PDF Chatbot</h1>

      <div className="upload-section card">
        <h2>Upload PDF(s)</h2>
        <div {...getRootProps({ className: "dropzone" })}>
          <input {...getInputProps()} />
          {pdfFiles.length === 0
            ? "Drag & drop PDFs here, or click to select files"
            : pdfFiles.map((file) => <p key={file.name}>{file.name}</p>)}
        </div>
        <button onClick={handleUpload} disabled={!pdfFiles.length || loading}>
          {loading ? "Uploading..." : "Upload & Rebuild Index"}
        </button>
      </div>

      <div className="chat-section card">
        <h2>Ask Questions</h2>
        <div className="chat-box">
          {chatHistory.map((item, idx) => (
            <div key={idx} className="chat-item">
              <p className="user-msg">👤 {item.question}</p>
              <p className="bot-msg">
                🤖 <strong>Answer:</strong><br />
                {item.answer.split("\n").map((line, idx) => (
                  <span key={idx}>
                    {line}
                    <br />
                  </span>
                ))}
              </p>
            </div>
          ))}
        </div>

        <div className="input-section">
          <input
            type="text"
            placeholder="Ask a question..."
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleAsk()}
          />
          <button onClick={handleAsk} disabled={!question.trim() || loading}>
            Ask
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;
