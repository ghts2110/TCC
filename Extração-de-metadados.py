import json

CAMPOS_OBRIGATORIOS = {
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
        "name",
        "passport-number",
        "date-of-birth",
        "validity",
        "nationality"
    ],
    "Registro Nacional de Estrangeiros - RNE": [
        "name",
        "RNE",
        "date-of-birth",
        "country-of-origin",
        "validity"
    ]
}


def validar_documento(json_str):
    try:
        dados = json.loads(json_str)
    except json.JSONDecodeError as e:
        print(f"JSON inválido: {e}")
        return
    
    tipo = dados.get("type")
    if tipo not in CAMPOS_OBRIGATORIOS:
        print(f"Tipo de documento '{tipo}' não reconhecido.")
        return
    
    print(f"Validando documento: {tipo}")
    obrigatorios = CAMPOS_OBRIGATORIOS[tipo]
    faltando = []
    
    for campo in obrigatorios:
        if not dados.get(campo):  
            faltando.append(campo)

    if faltando:
        print("Campos obrigatórios faltando:")
        for f in faltando:
            print(f)
    else:
        print("Todos os campos obrigatórios estão presentes.")
    
    

if __name__ == "__main__":
    exemplo_json = '''
    {
        "type": "Carteira de Identidade",
        "name": "",
        "RG": "",
        "shipping-date": "",
        "affiliation": "",
        "naturalness": "",
        "date-of-birth": "",
        "original-dock": "",
        "CPF": ""
    }
    '''.replace("//", "#")

    validar_documento(exemplo_json)