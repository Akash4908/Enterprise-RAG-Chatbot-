import re
import logging

# =========================
# LOGGING SETUP
# =========================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_info(message: str):
    logging.info(message)

def log_error(message: str):
    logging.error(message)

# =========================
# TEXT CLEANING (VERY IMPORTANT FOR RAG)
# =========================
def clean_text(text: str) -> str:
    """
    Cleans raw document text to improve embedding quality
    """
    if not text:
        return ""

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text)

    # Remove weird special characters (keep meaning intact)
    text = re.sub(r"[^\w\s.,;:!?()-]", "", text)

    return text.strip()

# =========================
# RESPONSE CLEANING
# =========================
def format_response(text: str) -> str:
    """
    Ensures chatbot output is clean for UI
    """
    if not text:
        return "No response generated."

    return text.strip()

# =========================
# SIMPLE VALIDATION
# =========================
def is_valid_file(filename: str) -> bool:
    """
    Checks if uploaded file is supported
    """
    allowed_extensions = [".pdf", ".txt", ".md"]

    return any(filename.endswith(ext) for ext in allowed_extensions)