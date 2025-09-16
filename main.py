import argparse
from google.cloud import documentai_v1 as documentai

def process_document(project_id, location, processor_id, file_path):
    client = documentai.DocumentProcessorServiceClient(
        client_options={"api_endpoint": f"{location}-documentai.googleapis.com"}
    )
    name = client.processor_path(project_id, location, processor_id)

    with open(file_path, "rb") as f:
        raw_document = documentai.RawDocument(content=f.read(), mime_type="image/jpeg")

    request = documentai.ProcessRequest(name=name, raw_document=raw_document)
    result = client.process_document(request=request)

    print("Texto extraído (início):")
    print(result.document.text[:500])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Processar documento com Document AI")
    parser.add_argument("--project_id", required=True, help="ID do projeto GCP")
    parser.add_argument("--location", required=True, help="Região (ex: us, eu, us-latin1)")
    parser.add_argument("--processor_id", required=True, help="ID do processador Document AI")
    parser.add_argument("--file", required=True, help="Caminho do arquivo de imagem/PDF")

    args = parser.parse_args()

    process_document(args.project_id, args.location, args.processor_id, args.file)
