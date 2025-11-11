from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
from chat.app.services.chatbot_service import ask, get_faiss_results, rebuild_index
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = os.path.join("chat", "data")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {"pdf"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/ask", methods=["POST"])
def api_ask():
    data = request.get_json()
    query = data.get("query")
    k = data.get("k", 5)
    answer = ask(query, k)
    return jsonify({"answer": answer})

@app.route("/upload_pdf", methods=["POST"])
def upload_pdf():
    if "files" not in request.files:
        return jsonify({"error": "No files uploaded"}), 400
    files = request.files.getlist("files")
    saved_files = []
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            saved_files.append(filename)
        else:
            return jsonify({"error": f"File not allowed: {file.filename}"}), 400
    message = rebuild_index()
    return jsonify({"message": f"Uploaded {len(saved_files)} PDF(s). {message}", "files": saved_files})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
