import logging
import azure.functions as func
from azure.durable_functions import DurableOrchestrationClient

async def main(blob: func.InputStream, starter: str) -> None:
    client = DurableOrchestrationClient(starter)
    instance_id = await client.start_new("orchestrator_function", None, {
        "blobName": blob.name,
        "blobUrl": blob.uri
    })

    logging.info(f"Started orchestration with ID = '{instance_id}'.")
