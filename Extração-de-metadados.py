import json

REQUIRED_FIELDS = {
    "Carteira de Identidade": [
        "name",
        "RG",
        "shipping-date",
        "affiliation",
        "naturalness",
        "date-of-birth",
        "original-dock",
        "CPF"
    ],"Passaporte": [
        "type",              
        "issuing-country",   
        "passport-number",   
        "full-name",  
        "nationality",
        "date-of-birth",   
        "sex",               
        "place-of-birth",   
        "issue-date",   
        "expiry-date",   
        "issuing-authority" 
    ],
    "Registro Nacional de Estrangeiros - RNE": [
        "rne-number",      
        "full-name",   
        "affiliation",      
        "date-of-birth",    
        "sex",
        "nationality",      
        "place-of-birth",    
        "arrival-date",
        "migratory-category", 
        "issue-date",      
        "expiry-date",    
        "issuing-authority"    
    ]
}


def validar_documento(json_str: str):
    try:
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        print(f"JSON inválido: {e}")
        return
    
    doc_type = data.get("type")
    if doc_type not in REQUIRED_FIELDS:
        print(f"Tipo de documento '{doc_type}' não reconhecido.")
        return
    
    print(f"Validando documento: {doc_type}")
    required = REQUIRED_FIELDS[doc_type]
    missing = []
    
    for field in required:
        if not data.get(field):  
            missing.append(field)

    if missing:
        print("Campos obrigatórios faltando:")
        for f in missing:
            print(f"- {f}")
    else:
        print("Todos os campos obrigatórios estão presentes.")
    
    

if __name__ == "__main__":
    exemplo_json = '''
    {
        "type": "Passaporte",
        "issuing-country": "BRA",
        "passport-number": "PA9876543",
        "full-name": "Carlos Pereira",
        "nationality": "Brasileira",
        "date-of-birth": "1992-03-15",
        "sex": "M"
    }
    '''.replace("//", "#")

    validar_documento(exemplo_json)