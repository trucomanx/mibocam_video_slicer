import json
import os

def save_couples(couples,json_file_path):

    DIR=os.path.dirname(json_file_path);
    
    if DIR!='':
        os.makedirs(DIR,exist_ok=True);
    
    couples_list = [list(couple) for couple in couples]

    # Salvar a lista de listas no arquivo JSON
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(couples_list, json_file, ensure_ascii=False, indent=4)
        
def load_couples(json_file_path):
    # Ler os dados do arquivo JSON
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        couples_list = json.load(json_file)

    # Converter a lista de listas de volta para uma lista de tuplas
    couples = [tuple(couple) for couple in couples_list]
    
    return couples;
