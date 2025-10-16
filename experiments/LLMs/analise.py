import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score, confusion_matrix

# Ler o CSV
df = pd.read_csv('3results_summary.csv')

# Modelos a analisar
MODELS = [
    "meta-llama/llama-3.3-70b-instruct", 
    "x-ai/grok-4-fast", 
    "openai/gpt-4o-mini", 
    # "deepseek/deepseek-chat-v3.1:free"
]

# Calcular métricas para cada modelo
results = []

for model in MODELS:
    # Filtrar dados do modelo
    model_data = df[df['model'] == model]
    
    if len(model_data) == 0:
        print(f"Aviso: Nenhum dado encontrado para {model}")
        continue
    
    # Extrair valores reais e preditos
    y_true = model_data['class'].values
    y_pred = model_data['predicted'].values
    
    # Agora "nonportable" é o caso positivo (TP)
    pos_label = 'nonportable'
    
    precision = precision_score(y_true, y_pred, pos_label=pos_label, zero_division=0)
    recall = recall_score(y_true, y_pred, pos_label=pos_label, zero_division=0)
    f1 = f1_score(y_true, y_pred, pos_label=pos_label, zero_division=0)
    accuracy = accuracy_score(y_true, y_pred)
    
    # Armazenar resultados
    results.append({
        'Model': model.split('/')[-1],  # Nome curto
        'Precision': precision,
        'Recall': recall,
        'F1-Score': f1,
        'Accuracy': accuracy,
        'Samples': len(model_data)
    })

# Criar DataFrame com resultados
results_df = pd.DataFrame(results)

# Exibir tabela formatada para o paper
print("\n" + "="*80)
print("MÉTRICAS DE DESEMPENHO POR MODELO (NonPort = Positivo)")
print("="*80 + "\n")

# Tabela em formato LaTeX
print("Formato LaTeX:")
print("-" * 80)
print(results_df.to_latex(index=False, float_format="%.3f"))

# Tabela em formato Markdown
print("\nFormato Markdown:")
print("-" * 80)
print(results_df.to_markdown(index=False, floatfmt=".3f"))

# Tabela simples para visualização
print("\nTabela Simples:")
print("-" * 80)
print(results_df.to_string(index=False, float_format=lambda x: f'{x:.3f}'))

# Estatísticas adicionais
print("\n" + "="*80)
print("ANÁLISE COMPARATIVA")
print("="*80)
print(f"\nMelhor Precision: {results_df.loc[results_df['Precision'].idxmax(), 'Model']} "
      f"({results_df['Precision'].max():.3f})")
print(f"Melhor Recall: {results_df.loc[results_df['Recall'].idxmax(), 'Model']} "
      f"({results_df['Recall'].max():.3f})")
print(f"Melhor F1-Score: {results_df.loc[results_df['F1-Score'].idxmax(), 'Model']} "
      f"({results_df['F1-Score'].max():.3f})")
print(f"Melhor Accuracy: {results_df.loc[results_df['Accuracy'].idxmax(), 'Model']} "
      f"({results_df['Accuracy'].max():.3f})")

# Matrizes de confusão para cada modelo
print("\n" + "="*80)
print("MATRIZES DE CONFUSÃO (NonPort = Positivo)")
print("="*80)

for model in MODELS:
    model_data = df[df['model'] == model]
    
    if len(model_data) == 0:
        continue
    
    y_true = model_data['class'].values
    y_pred = model_data['predicted'].values
    
    cm = confusion_matrix(y_true, y_pred, labels=['portable', 'nonportable'])
    
    print(f"\n{model.split('/')[-1]}:")
    print(f"                 Predicted")
    print(f"               Port  NonPort")
    print(f"Actual Port    {cm[0][0]:4d}    {cm[0][1]:4d}")
    print(f"       NonPort {cm[1][0]:4d}    {cm[1][1]:4d}")
