# Metrop db compiler

import os
import json
import base64
import random

def generate_base64_id() -> str:
    num = random.randint(1, 1_000_000_000)
    return base64.urlsafe_b64encode(num.to_bytes(4, 'big')).decode('utf-8').rstrip('=')

file_list = [os.path.join(dirpath, file) for (dirpath, dirnames, filenames) in os.walk("./content") for file in filenames]
file_list = [i.replace('\\', '/').removeprefix('./content/') for i in file_list]

alreadyTakenId = []

# --- START ---

for file_rel_path in file_list:
    if file_rel_path.endswith('.json'):
        full_path = os.path.join("./content", file_rel_path)
        
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                card_data = json.load(f)
            
            if "cardInfo" in card_data and isinstance(card_data["cardInfo"], dict):
                if "card_key_id" in card_data["cardInfo"]:
                    alreadyTakenId.append(card_data["cardInfo"]["card_key_id"])
                else:
                    new_id = generate_base64_id()
                    while new_id in alreadyTakenId:
                        new_id = generate_base64_id()
            
                    card_data["cardInfo"]["card_key_id"] = new_id
                    alreadyTakenId.append(new_id)

                with open(full_path, 'w', encoding='utf-8') as f:
                    json.dump(card_data, f, indent=4, ensure_ascii=False)
                    
        except (json.JSONDecodeError, IOError) as e:
            print(f"Erreur lors du traitement de {full_path} : {e}")

# --- END ---
with open('dbinfo.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

data['QUIZ_LIST'] = [f for f in file_list if f.endswith('.json')]

with open('dbinfo.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)