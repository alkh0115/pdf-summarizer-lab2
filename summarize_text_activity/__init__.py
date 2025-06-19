import os
from openai import AzureOpenAI

def main(input: dict) -> dict:
    client = AzureOpenAI(
        api_key=os.environ["AZURE_OPENAI_KEY"],
        api_version="2023-05-15",
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"]
    )

    deployment_name = os.environ["CHAT_MODEL_DEPLOYMENT_NAME"]

    response = client.chat.completions.create(
        model=deployment_name,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes text."},
            {"role": "user", "content": input["text"]}
        ]
    )

    return {
        "summary": response.choices[0].message.content,
        "blobName": input["blobName"]
    }
