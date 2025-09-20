import argparse
from google.cloud import documentai_v1 as documentai
from src.identidade import extract_fields

def process_document(project_id, location, processor_id, file_path):
    client = documentai.DocumentProcessorServiceClient(
        client_options={"api_endpoint": f"{location}-documentai.googleapis.com"}
    )
    name = client.processor_path(project_id, location, processor_id)

    with open(file_path, "rb") as f:
        raw_document = documentai.RawDocument(content=f.read(), mime_type="image/png")

    request = documentai.ProcessRequest(name=name, raw_document=raw_document)
    result = client.process_document(request=request)
    doc = result.document

    print("Texto extraído (início):")
    print(doc.text[:400])  # só uma prévia

    # aqui chama a função do outro arquivo
    fields = extract_fields(doc.text)

    print("\nCampos organizados:")
    print(fields)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Processar documento com Document AI")
    parser.add_argument("--project_id", required=True)
    parser.add_argument("--location", required=True)
    parser.add_argument("--processor_id", required=True)
    parser.add_argument("--file", required=True)
    args = parser.parse_args()
    process_document(args.project_id, args.location, args.processor_id, args.file)
