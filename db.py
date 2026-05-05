import json
import os
from datetime import datetime,timezone

FILE="mapping.json"

def load_mapping():
    if os.path.exists(FILE):
        with open(FILE,"r") as f:
            return json.load(f)
        
    return {}

def save_mapping(mapping):
    with open(FILE,"w") as f:
        json.dump(mapping,f,indent=4)

def add_mapping(nome, id, params=None):
    mapping=load_mapping()

    if(nome not in mapping):
        mapping[nome]=[]

    mapping[nome].append({
        "id": id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "params": params or {},
    })

    save_mapping(mapping)
