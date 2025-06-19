# Intelligent PDF Summarizer (Azure Durable Functions)

This project is a **serverless PDF summarization pipeline** built with **Azure Durable Functions**, **Cognitive Services**, and **Azure Storage**. The app is designed to automatically extract and summarize content from PDF documents uploaded to a Blob Storage container.

---

## Project Structure

This solution follows Azure Functions best practices, with each function defined in a **separate folder** for clarity and modularity.

| Folder | Function Name | Type | Description |
|--------|---------------|------|-------------|
| `starter_function` | `starter_function` | `blobTrigger` | Triggers when a new PDF is uploaded to the `input/` container. Starts the orchestration. |
| `orchestrator_function` | `orchestrator_function` | `orchestrationTrigger` | Coordinates the workflow: analyze → summarize → write. |
| `analyze_pdf_activity` | `analyze_pdf_activity` | `activityTrigger` | Uses Azure Form Recognizer to extract text content from the uploaded PDF. |
| `summarize_text_activity` | `summarize_text_activity` | `activityTrigger` | Sends extracted text to Azure OpenAI (GPT-3.5-turbo) to generate a summary. |
| `write_doc_activity` | `write_doc_activity` | `activityTrigger` | Saves the summary as a `.txt` file into the `output/` Blob container. |

---

## How It Works

1. A PDF is uploaded to the **`input/`** container.
2. `starter_function` triggers and starts a **Durable Orchestration**.
3. `orchestrator_function` calls:
   - `analyze_pdf_activity` to extract raw text using **Form Recognizer**.
   - `summarize_text_activity` to summarize the text using **Azure OpenAI**.
   - `write_doc_activity` to store the summary in the **`output/`** container.
4. The output is saved as `filename-summary.txt`.

---

## Local Setup

### 0. Requirements
- Python 3.10
- Azure Functions Core Tools v4
- Azure Storage Blob SDK
- Azure OpenAI and Form Recognizer resources

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### 2. Create a Virtual Environment

```bash
python3.10 -m venv venv
```

Then activate it using:

```bash
source venv/bin/activate        # For Linux/macOS
# OR
.\venv\Scripts\activate        # For Windows
```

### 3. Install Dependencies

Run:

```bash
pip install -r requirements.txt
```

Ensure that `azure-functions`, `azure-storage-blob`, and `openai` are included.

### 4. Setup Configuration (`local.settings.json`)

Create a `local.settings.json` file in the root directory with the following:

```json
{
  "IsEncrypted": false,
  "Values": {
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "AzureWebJobsStorage": "<your_connection_string>",
    "STORAGE_ACCOUNT_NAME": "<your_account_name>",
    "STORAGE_ACCOUNT_KEY": "<your_account_key>",
    "OPENAI_API_KEY": "<your_openai_key>",
    "AzureWebJobsFeatureFlags": "EnableWorkerIndexing",
    "InputContainerName": "input",
    "OutputContainerName": "output",
    "COGNITIVE_SERVICES_ENDPOINT": "<your_form_recognizer_endpoint>",
    "COGNITIVE_SERVICES_KEY": "<your_form_recognizer_key>",
    "AZURE_OPENAI_ENDPOINT": "<your_azure_openai_endpoint>",
    "AZURE_OPENAI_KEY": "<your_azure_openai_key>",
    "CHAT_MODEL_DEPLOYMENT_NAME": "gpt-35-turbo"
  }
}
```

Replace all placeholders with your actual credentials and endpoints.

### 5. Start the Function App

Use this command:

```bash
func start --verbose
```

You should see all functions loaded correctly:
- `starter_function`
- `orchestrator_function`
- `analyze_pdf_activity`
- `summarize_text_activity`
- `write_doc_activity`

### 6. Upload a Test PDF

Upload a test file like `sample.pdf` to the `input/` container in your Azure Blob Storage.

The summarization pipeline will:
1. Extract the content using **Form Recognizer**
2. Send it to **OpenAI** for summarization
3. Write the result to the `output/` container as `sample-summary.txt`

---
## YouTube demo link








