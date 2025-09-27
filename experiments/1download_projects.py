import csv
import os
import requests
import zipfile
import io

# Configuração
CSV_FILE = "repos.csv"       # seu arquivo CSV
OUTPUT_DIR = "projects"      # pasta de saída
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # exporte seu token: export GITHUB_TOKEN=xxxx

os.makedirs(OUTPUT_DIR, exist_ok=True)

success = []
fail = []

headers = {}
if GITHUB_TOKEN:
    headers["Authorization"] = f"token {GITHUB_TOKEN}"

with open(CSV_FILE, newline='', encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if len(row) < 2:
            continue
        repo_url, sha = row[0].strip(), row[1].strip()
        if not repo_url or not sha:
            continue

        # Extrai o owner e repo do URL
        try:
            parts = repo_url.rstrip("/").split("/")
            owner, repo = parts[-2], parts[-1]
        except Exception as e:
            print(f"[ERRO] URL inválida: {repo_url}")
            fail.append((repo_url, sha))
            continue

        folder_name = f"{repo}__{sha}"
        target_dir = os.path.join(OUTPUT_DIR, folder_name)

        if os.path.exists(target_dir):
            print(f"[SKIP] Já existe: {target_dir}")
            success.append((repo_url, sha))
            continue

        zip_url = f"https://api.github.com/repos/{owner}/{repo}/zipball/{sha}"
        print(f"[BAIXANDO] {repo_url}@{sha}")

        try:
            resp = requests.get(zip_url, headers=headers, stream=True, timeout=60)
            if resp.status_code != 200:
                print(f"[ERRO] Falhou {repo_url}@{sha} -> HTTP {resp.status_code}")
                fail.append((repo_url, sha))
                continue

            with zipfile.ZipFile(io.BytesIO(resp.content)) as z:
                z.extractall(target_dir)

            print(f"[OK] {repo_url}@{sha}")
            success.append((repo_url, sha))

        except Exception as e:
            print(f"[ERRO] {repo_url}@{sha} -> {e}")
            fail.append((repo_url, sha))

# Relatório final
print("\n===== RELATÓRIO FINAL =====")
print(f"Sucesso: {len(success)}")
print(f"Falha: {len(fail)}")

if fail:
    print("\nProjetos com falha:")
    for url, sha in fail:
        print(f"- {url} @ {sha}")
