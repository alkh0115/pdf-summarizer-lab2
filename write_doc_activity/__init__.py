import os
import logging
from azure.storage.blob import BlobServiceClient
from datetime import datetime

def main(input: dict) -> None:
    logging.info(f"Received input type: {type(input)}, content: {input}")

    # Extract summary and blob name from input
    summary_text = input.get("summary", "")
    blob_name = input.get("blobName", "unknown.pdf")
    
    # Get container name from environment variable
    container_name = os.environ.get("OutputContainerName", "output")

    # Get connection string from environment variable
    connection_string = os.environ["AzureWebJobsStorage"]

    # Initialize blob client
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)

    # Create a new blob name for the summary
    output_blob_name = blob_name.replace("input/", "").replace(".pdf", "-summary.txt")

    # Optional: include timestamp
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    summary_content = f"Summary generated on {timestamp}:\n\n{summary_text}"

    # Upload the summary text
    blob_client = container_client.get_blob_client(output_blob_name)
    blob_client.upload_blob(summary_content, overwrite=True)

    logging.info(f"Summary written to blob: {container_name}/{output_blob_name}")
