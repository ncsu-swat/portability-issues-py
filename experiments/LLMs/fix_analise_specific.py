import pandas as pd

# === 1. Ler o arquivo CSV ===
print("🔹 Lendo arquivo CSV com resultados dos fixes...\n")
df = pd.read_csv("fix_specific_summary.csv")

print("Prévia dos dados:")
print(df.head(), "\n")

# === 2. Normalizar a coluna fixed_correctly ===
df["fixed_correctly"] = df["fixed_correctly"].str.strip().str.upper()

# === 3. Estatísticas gerais ===
total = len(df)
total_fixed = (df["fixed_correctly"] == "YES").sum()
accuracy = total_fixed / total

print("=== Estatísticas gerais ===")
print(f"Total de amostras: {total}")
print(f"Total corrigidas corretamente: {total_fixed}")
print(f"Taxa de acerto geral: {accuracy:.2%}\n")

# === 4. Estatísticas por modelo ===
print("=== Resultados por modelo ===")
results_by_model = (
    df.groupby("model")["fixed_correctly"]
    .value_counts()
    .unstack(fill_value=0)
    .reset_index()
)

# adiciona colunas com total e taxa de acerto
results_by_model["Total"] = results_by_model["YES"] + results_by_model["NO"]
results_by_model["Accuracy"] = results_by_model["YES"] / results_by_model["Total"]

# ordena por melhor desempenho
results_by_model = results_by_model.sort_values("Accuracy", ascending=False)

print(results_by_model, "\n")

# === 5. Exibir ranking resumido ===
print("=== Ranking dos modelos por taxa de acerto ===")
for _, row in results_by_model.iterrows():
    print(f"{row['model']}: {row['Accuracy']:.2%} ({int(row['YES'])}/{int(row['Total'])} corretos)")

# # === 6. (Opcional) Exportar tabela LaTeX ===
# results_by_model.to_latex(
#     "fix_results_table.tex",
#     index=False,
#     float_format="%.2f",
#     caption="LLM performance in generating correct portability fixes.",
#     label="tab:llm_fix_results"
# )

# print("\nTabela LaTeX salva como 'fix_results_table.tex'")
