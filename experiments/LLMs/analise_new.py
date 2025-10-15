import os
import csv
import requests
import json
import time

# Configuração
API_KEY = "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"
MODELS = [
    "meta-llama/llama-3.3-70b-instruct",
    "x-ai/grok-4-fast",
    "openai/gpt-4o-mini",
    "deepseek/deepseek-chat-v3.1:free"
]
BASE_DIR = "code"
OUTPUT_FULL_CSV = "results_full.csv"
OUTPUT_SUMMARY_CSV = "results_summary.csv"
OLD_RESULTS_PATH = "old_results/results_full.csv"

PROMPT_TEMPLATE = """
You are a Python expert. Check the following code and answer:

1. Is there any operation in the code that could fail on a specific operating system (Linux, Mac, Windows)? 
2. If yes, explain why and on which OS it might fail, finish saying "NonPortable!!!" If it is fully portable, finish saying "Portable!!!"

Code:
{}
"""

def call_llm(model, code):
    """Chama a API do OpenRouter e tenta novamente uma vez em caso de erro."""
    headers = {"Authorization": f"Bearer {API_KEY}"}
    data = {
        "model": model,
        "messages": [{"role": "user", "content": PROMPT_TEMPLATE.format(code)}],
    }

    for attempt in range(2):  # tenta no máximo 2 vezes
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            data=json.dumps(data)
        )

        if response.status_code == 200:
            try:
                r_json = response.json()
                return r_json["choices"][0]["message"]["content"].strip()
            except (KeyError, IndexError):
                return "ERROR: no content"
        else:
            print(f"⚠️  {model} returned status {response.status_code}, retrying ({attempt + 1}/2)...")
            time.sleep(3)  # espera antes de tentar novamente

    return f"ERROR: status {response.status_code}"

def classify_response(response_text):
    """Detecta Portable!!! ou NonPortable!!! no texto da LLM"""
    if "NonPortable!!!" in response_text:
        return "nonportable"
    elif "Portable!!!" in response_text:
        return "portable"
    else:
        return "unknown"

def load_old_results(path):
    """Carrega resultados antigos de old_results/results_full.csv em um dict"""
    old_data = {}
    if not os.path.exists(path):
        return old_data

    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = (row["filename"], row["model"])
            old_data[key] = row["response"]
    return old_data

def main():
    # Carrega resultados antigos
    old_results = load_old_results(OLD_RESULTS_PATH)
    print(f"Loaded {len(old_results)} previous results from {OLD_RESULTS_PATH}")

    # Abre os CSVs de saída e escreve header
    f_full = open(OUTPUT_FULL_CSV, "w", newline="", encoding="utf-8")
    f_sum = open(OUTPUT_SUMMARY_CSV, "w", newline="", encoding="utf-8")

    full_writer = csv.DictWriter(f_full, fieldnames=["filename", "class", "model", "response"])
    full_writer.writeheader()

    summary_writer = csv.DictWriter(f_sum, fieldnames=["filename", "class", "model", "predicted"])
    summary_writer.writeheader()

    for cls in ["portable", "nonportable"]:
        folder = os.path.join(BASE_DIR, cls)

        # ✅ se for portable, buscar dentro das subpastas fixed e unrelated
        if cls == "portable":
            subfolders = ["fixed", "unrelated"]
            folders_to_scan = [os.path.join(folder, sub) for sub in subfolders]
        else:
            folders_to_scan = [folder]

        for folder_path in folders_to_scan:
            if not os.path.exists(folder_path):
                continue

            for filename in os.listdir(folder_path):
                if not filename.endswith(".py"):
                    continue

                rel_path = os.path.join(cls, os.path.basename(folder_path), filename) \
                    if cls == "portable" else os.path.join(cls, filename)
                filepath = os.path.join(folder_path, filename)

                with open(filepath, "r", encoding="utf-8") as f:
                    code = f.read()

                for model in MODELS:
                    key = (rel_path, model)

                    # ✅ Verifica se já existe resultado anterior
                    if key in old_results:
                        output = old_results[key]
                        print(f"✅ Using cached result for {rel_path} with {model}")
                    else:
                        print(f"🧠 Processing {rel_path} with {model}...")
                        output = call_llm(model, code)
                        time.sleep(1)

                    classified = classify_response(output)

                    # Salva linha no CSV completo
                    full_writer.writerow({
                        "filename": rel_path,
                        "class": cls,
                        "model": model,
                        "response": output
                    })
                    f_full.flush()

                    # Salva linha no CSV resumido
                    summary_writer.writerow({
                        "filename": rel_path,
                        "class": cls,
                        "model": model,
                        "predicted": classified
                    })
                    f_sum.flush()

    f_full.close()
    f_sum.close()
    print(f"\n✅ Full results saved to {OUTPUT_FULL_CSV}")
    print(f"✅ Summary results saved to {OUTPUT_SUMMARY_CSV}")

if __name__ == "__main__":
    main()
