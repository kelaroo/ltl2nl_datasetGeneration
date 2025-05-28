import json 

PROMPT = "Given these LTL formulas <ltl>, whre y, y1, y2, etc. are possbile locations, and the following translations in natural language for reference, try to generate as many as possible(20 or more) unique and diverse natural language translations, trying to use terms related to the field of mobile robots but also generic terms for move commands, keeping the wording as second person imperative:\n<nl>"

def load_dataset(json_path: str) -> list[dict]:
    with open(json_path, 'r') as file:
        dataset = json.loads(file.read())
    return dataset

def save_dataset(dataset: list[dict], json_path: str):
    with open(json_path, 'w') as file:
        file.write(json.dumps(dataset))

def create_prompt(entry: dict) -> str:
    ltl = ', '.join(entry["ltl"])
    nlp = "NL: " + "\nNL: ".join(entry["nlp"])

    return PROMPT.replace("<ltl>", ltl).replace("<nl>", nlp)

