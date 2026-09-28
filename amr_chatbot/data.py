import os
import requests
from amr_chatbot.config import DATA_DIR, ECDC_PDF_URL, ECDC_PDF_FILENAME


def download_ecdc_report() -> str:
    """Downloads the ECDC AMR report to data/ if it doesn't exist."""
    os.makedirs(DATA_DIR, exist_ok=True)
    pdf_path = os.path.join(DATA_DIR, ECDC_PDF_FILENAME)

    if not os.path.exists(pdf_path):
        print(f"Downloading ECDC AMR report from {ECDC_PDF_URL}...")
        response = requests.get(ECDC_PDF_URL, timeout=30)
        response.raise_for_status()
        with open(pdf_path, "wb") as f:
            f.write(response.content)
        print("Download completed successfully.")
    else:
        print("ECDC report already present in data directory.")

    return pdf_path
