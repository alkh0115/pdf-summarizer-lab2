import logging
import fitz  # PyMuPDF
import os
from azure.storage.blob import BlobServiceClient

def main(blob_path: str) -> str:
    logging.info(f"Received input type: {type(blob_path)}, content: {blob_path}")

    # Extract blob name from path like "input/sample.pdf"
    blob_name = blob_path.replace("input/", "")

    # Read environment variables
    connection_string = os.environ["AzureWebJobsStorage"]
    container_name = os.environ.get("InputContainerName", "input")

    # Download the PDF from Azure Blob Storage
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

    download_path = f"/tmp/{blob_name}"
    with open(download_path, "wb") as f:
        f.write(blob_client.download_blob().readall())

    # Extract text from the PDF
    doc = fitz.open(download_path)
    extracted_text = ""
    for page in doc:
        extracted_text += page.get_text()
    doc.close()

    # Log and return
    logging.info("PDF text extraction complete.")
    return extracted_text.strip()
