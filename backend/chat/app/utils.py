import os
import logging
from logging.handlers import RotatingFileHandler

def setup_logger(name: str, log_file: str = "logs/app.log"):
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            "%Y-%m-%d %H:%M:%S",
        )
        file_handler = RotatingFileHandler(log_file, maxBytes=5_000_000, backupCount=5)
        console_handler = logging.StreamHandler()

        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger


def ensure_models_ready():
    pass
    # logger = setup_logger("utils")
    # logger.info("Checking Ollama models availability...")
    # os.system("ollama pull llama3")
    # os.system("ollama pull nomic-embed-text")
    # logger.info("Model pull check complete.")
