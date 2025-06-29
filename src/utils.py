import re
import json

def clean_and_parse_json(raw_output):
    try:
        clean_output = re.sub(r'[\r\n]+', ' ', raw_output).strip()
        return json.loads(clean_output)
    except json.JSONDecodeError as e:
        print(f"Erro de JSON: {e}")
        return {"opinion": "Erro ao interpretar resposta do modelo."}