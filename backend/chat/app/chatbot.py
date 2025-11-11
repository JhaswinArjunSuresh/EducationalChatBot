import os
if os.name == "nt" or "KMP_DUPLICATE_LIB_OK" not in os.environ:
    os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from langchain_ollama import OllamaLLM
from chat.app.utils import setup_logger

class CSVChatbot:
    def __init__(self, model_name="llama3"):
        self.logger = setup_logger("chatbot")
        self.llm = OllamaLLM(model=model_name)
        self.logger.info(f"Chatbot initialized with model {model_name}")

    def generate_answer(self, query, retrieved_context):
        self.logger.info(f"Generating answer for query: {query}")

        # Make sure retrieved_context is string
        if isinstance(retrieved_context, list):
            context = "\n".join([str(item) for item in retrieved_context])
        else:
            context = str(retrieved_context)

        prompt = f"""You are a teacher answering the student's question.
                    Context:
                    {context}
                    Question:
                    {query}
                    Answer:"""

        try:
            response = self.llm.invoke(prompt)
            self.logger.info("Response generated successfully.")
            return response.strip()
        except Exception as e:
            self.logger.error(f"Failed to generate answer: {e}")
            return "⚠️ Failed to generate answer from LLaMA model."
