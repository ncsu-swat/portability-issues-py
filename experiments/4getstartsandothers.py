import csv
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

GITHUB_TOKEN = ""  # coloque sua API key aqui
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}
THREADS = 5
def get_repo_stats(repo_url):
    try:
        # Extrai "owner/repo" da URL
        parts = repo_url.strip().split("/")
        if len(parts) < 2:
            return repo_url, 0, 0, 0
        owner, repo = parts[-2], parts[-1]

        # 1. Número de commits (contando no branch padrão)
        commits_url = f"https://api.github.com/repos/{owner}/{repo}/commits"
        commits_resp = requests.get(commits_url, headers=HEADERS, params={"per_page": 1})
        if commits_resp.status_code != 200:
            return repo_url, 0, 0, 0

        # O total vem no header "Link" (última página)
        if "Link" in commits_resp.headers:
            links = commits_resp.headers["Link"]
            last_link = [l for l in links.split(",") if 'rel="last"' in l]
            if last_link:
                last_url = last_link[0].split(";")[0].strip(" <>")
                last_page = int(last_url.split("page=")[-1])
                n_commits = last_page
            else:
                n_commits = 1
        else:
            n_commits = 1

        # 2. Idade do repositório em anos
        repo_url_api = f"https://api.github.com/repos/{owner}/{repo}"
        repo_resp = requests.get(repo_url_api, headers=HEADERS)
        if repo_resp.status_code != 200:
            return repo_url, n_commits, 0, 0
        repo_data = repo_resp.json()
        created_at = datetime.strptime(repo_data["created_at"], "%Y-%m-%dT%H:%M:%SZ")
        age_years = (datetime.utcnow() - created_at).days / 365.25

        # 3. Número de estrelas
        stars = repo_data.get("stargazers_count", 0)

        return repo_url, n_commits, round(age_years, 2), stars

    except Exception as e:
        print(f"Erro em {repo_url}: {e}")
        return repo_url, 0, 0, 0

def main():
    input_csv = "projects.csv"   # arquivo com os GitHubs
    output_csv = "projects_stats.csv"

    repos = []
    with open(input_csv, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if row:
                repos.append(row[0])

    results = []
    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        future_to_repo = {executor.submit(get_repo_stats, repo): repo for repo in repos}
        for future in as_completed(future_to_repo):
            repo_url, n_commits, age, stars = future.result()
            print(f"[DONE] {repo_url} -> commits={n_commits}, age={age}, stars={stars}")
            results.append((repo_url, n_commits, age, stars))

    # Salva no CSV
    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Repository", "Commits", "Age (years)", "Stars"])
        writer.writerows(results)

    print(f"\n✅ Finalizado! Resultados salvos em {output_csv}")

if __name__ == "__main__":
    main()
