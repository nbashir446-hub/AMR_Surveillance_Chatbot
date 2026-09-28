import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
PERSIST_DIR = BASE_DIR / "storage"

# ECDC PDF Settings
ECDC_PDF_URL = "https://www.ecdc.europa.eu/sites/default/files/documents/antimicrobial-resistance-eu-annual-epidemiological-report-2024.pdf"
ECDC_PDF_FILENAME = "amr-ears-net-2024.pdf"

# Model & Index Settings
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")
EMBED_MODEL = "BAAI/bge-small-en-v1.5"
DEFAULT_TOP_K = 3

# UI Examples
EXAMPLE_QUESTIONS = [
    "What is the trend in E. coli resistance to 3rd-generation cephalosporins?",
    "Which countries have the highest AMR rates?",
    "How does resistance in Germany compare to other EU countries?",
]
