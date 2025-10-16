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
    # "deepseek/deepseek-chat-v3.1:free"
]
BASE_DIR = "code/nonportable"
OUTPUT_SUMMARY = "fix_generic_summary.csv"
FIXES_BASE = "fixes/generic"

# PROMPT_TEMPLATE = """
# You are a Python expert. The following code has portability issues (it may fail on Linux, macOS or Windows).

# Your task:
# - Identify the problem(s) related to portability.
# - Produce a corrected version of the code that is portable across major OSes.
# - Return ONLY the corrected code, nothing else.

# Code to fix:
# {}
# """

PROMPT_TEMPLATE = """
You are a Python expert. The following code has portability issues (it may fail on Linux, macOS or Windows).

Your task:
- Analyze the code carefully.
- Explain what should be changed or adjusted to make it portable across all major operating systems.
- Do NOT rewrite or show the entire fixed code. Only show the changes needed to make it portable in a simple way.

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

    for attempt in range(2):
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
            time.sleep(3)
    return f"ERROR: status {response.status_code}"

def ensure_dir(path):
    """Cria diretório se não existir."""
    os.makedirs(path, exist_ok=True)

def main():
    ensure_dir(FIXES_BASE)

    with open(OUTPUT_SUMMARY, "w", newline="", encoding="utf-8") as f_sum:
        writer = csv.DictWriter(f_sum, fieldnames=["filename", "model", "fixed_file", "fixed_correctly"])
        writer.writeheader()

        for filename in os.listdir(BASE_DIR):
            if not filename.endswith(".py"):
                continue

            filepath = os.path.join(BASE_DIR, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                code = f.read()

            for model in MODELS:
                print(f"🧠 Fixing {filename} with {model}...")
                fixed_code = call_llm(model, code)

                # Cria diretório de saída do modelo
                model_dir_name = model.replace("/", "_").replace(":", "_")
                out_dir = os.path.join(FIXES_BASE, model_dir_name)
                ensure_dir(out_dir)

                # Caminho do arquivo corrigido
                out_file = os.path.join(out_dir, filename)

                # change .py to .md if the output is markdown
                if fixed_code.startswith("```"):    
                    out_file = out_file.replace(".py", ".md")
                # Salva o código corrigido
                with open(out_file, "w", encoding="utf-8") as f_out:
                    f_out.write(fixed_code)

                # Registra no CSV resumo
                writer.writerow({
                    "filename": filename,
                    "model": model,
                    "fixed_file": out_file,
                    "fixed_correctly": ""  # campo para você preencher manualmente
                })
                f_sum.flush()

                # Evita sobrecarga da API
                time.sleep(0.5)

    print(f"\n✅ All fixes saved under {FIXES_BASE}")
    print(f"✅ Summary written to {OUTPUT_SUMMARY}")

if __name__ == "__main__":
    main()
