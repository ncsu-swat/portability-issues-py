import os
import subprocess
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

projects_path = './projects'
num_threads = 9

# Função para contar número de funções de teste usando bash
def count_tests_bash(project_path):
    try:
        cmd = f"grep -rho 'def test_' {project_path} --include '*.py' | wc -l"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return int(result.stdout.strip())
    except Exception as e:
        print(f"Erro ao contar testes em {project_path}: {e}")
        return 0

# Função para calcular SLOC usando cloc (saída padrão, não CSV)
def get_sloc_cloc(project_path):
    try:
        cmd = f"cloc {project_path} --include-lang=Python --quiet"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        total = 0
        for line in result.stdout.splitlines():
            if line.strip().startswith('Python'):
                parts = line.split()
                total = int(parts[-1])  # última coluna é 'code'
                break
        return total
    except Exception as e:
        print(f"Erro ao calcular SLOC em {project_path}: {e}")
        return 0

# Função que processa um projeto
def process_project(project_dir):
    project_path = os.path.join(projects_path, project_dir)
    if os.path.isdir(project_path):
        print(f"Processando projeto: {project_dir}")
        total_tests = count_tests_bash(project_path)
        total_sloc = get_sloc_cloc(project_path)
        print(f"-> {project_dir} concluído: {total_tests} testes, {total_sloc} SLOC")
        return {'Project': project_dir, '#Tests': total_tests, 'SLOC': total_sloc}
    return None

# Lista de projetos
project_dirs = [d for d in os.listdir(projects_path) if os.path.isdir(os.path.join(projects_path, d))]

# ThreadPoolExecutor para paralelizar
with ThreadPoolExecutor(max_workers=num_threads) as executor:
    results = list(executor.map(process_project, project_dirs))

# Filtra resultados válidos
results = [r for r in results if r is not None]

# Contabiliza projetos com SLOC = 0 ou #Tests = 0
discarded = [r for r in results if r['#Tests'] == 0 or r['SLOC'] == 0]
print(f"\nProjetos descartados por terem SLOC=0 ou #Tests=0: {len(discarded)}")

# Mantém apenas os válidos
results = [r for r in results if r['#Tests'] > 0 and r['SLOC'] > 0]

# Converte para DataFrame
df = pd.DataFrame(results)

# Calcula estatísticas agregadas
table = pd.DataFrame({
    'Mean': df[['#Tests', 'SLOC']].mean(),
    'Med': df[['#Tests', 'SLOC']].median(),
    'Min': df[['#Tests', 'SLOC']].min(),
    'Max': df[['#Tests', 'SLOC']].max(),
    'Sum': df[['#Tests', 'SLOC']].sum()
}).transpose()

print("\n=== Tabela final ===")
print(table)

# Salvar em CSV
table.to_csv('table1.csv', index=True)
