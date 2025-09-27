import pandas as pd

# Ler o CSV
df = pd.read_csv("projects_stats.csv")

# Selecionar apenas as colunas numéricas que você quer
cols = ["Commits", "Age (years)", "Stars"]

# Calcular estatísticas
stats = {
    "Mean": df[cols].mean(),
    "Med": df[cols].median(),
    "Min": df[cols].min(),
    "Max": df[cols].max(),
    "Sum": df[cols].sum()
}

# Transformar em DataFrame para formatar igual ao exemplo
summary = pd.DataFrame(stats).T

summary.to_csv("projects_stats_summary.csv")
