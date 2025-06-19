import azure.durable_functions as df

def orchestrator_function(context: df.DurableOrchestrationContext):
    # Get the blob name from the trigger input
    input_data = context.get_input()
    blob_name = input_data["blobName"]

    # Step 1: Analyze the PDF
    extracted_text = yield context.call_activity("analyze_pdf_activity", blob_name)

    # Step 2: Summarize the extracted text, pass both text and blob name
    summarize_input = {
        "text": extracted_text,
        "blobName": blob_name
    }

    summary_result = yield context.call_activity("summarize_text_activity", summarize_input)

    # Step 3: Write the summary to Table Storage
    yield context.call_activity("write_doc_activity", summary_result)

    # Final result returned by the orchestration
    return summary_result["summary"]

main = df.Orchestrator.create(orchestrator_function)
