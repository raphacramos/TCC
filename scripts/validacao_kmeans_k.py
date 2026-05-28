import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import seaborn as sns

def rodar_validacao_matematica_k():
    print(">>> Iniciando Validação Matemática do Hiperparâmetro K...")
    
    # Carregar dados
    df = pd.read_csv("dataset_pacing_completo.csv")
    
    # Filtrar uma prova específica para a demonstração do teorema
    # (Não se mistura dimensões na hora de calcular Inércia e Silhouette)
    df_400 = df[(df['distancia_prova'] == 400) & (df['tipo_piscina'] == 'Long Course')].copy()
    
    # Montar Tensor de Pacing
    df_400['id_performance'] = df_400['campeonato'] + " | " + df_400['atleta'] + " (" + df_400['genero'] + " " + df_400['fase'] + " " + df_400['distancia_prova'].astype(str) + "m " + df_400['tipo_piscina'] + ")"
    df_400 = df_400.drop_duplicates(subset=['id_performance', 'distancia_parcial'])
    df_pivot = df_400.pivot(index='id_performance', columns='distancia_parcial', values='velocidade_relativa').dropna()
    
    X = df_pivot.values
    
    inercia = []
    silhouette_scores = []
    k_valores = range(2, 11)
    
    print(f"Testando Tensor (Shape: {X.shape}) para K de 2 até 10...")
    for k in k_valores:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = kmeans.fit_predict(X)
        
        inercia.append(kmeans.inertia_)
        sil_score = silhouette_score(X, labels)
        silhouette_scores.append(sil_score)
        
    # Plotar Resultados
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # 1. Curva do Cotovelo (Inércia)
    sns.lineplot(x=list(k_valores), y=inercia, marker='o', ax=axes[0], color='blue', linewidth=2)
    axes[0].set_title('Método do Cotovelo (Elbow Curve)', fontsize=14)
    axes[0].set_xlabel('Número de Clusters (K)', fontsize=12)
    axes[0].set_ylabel('Inércia (Soma dos Quadrados das Distâncias)', fontsize=12)
    axes[0].axvline(x=4, color='red', linestyle='--', label='Escolha K=4')
    axes[0].legend()
    axes[0].grid(True, linestyle=':', alpha=0.7)
    
    # 2. Silhouette Score
    sns.lineplot(x=list(k_valores), y=silhouette_scores, marker='s', ax=axes[1], color='green', linewidth=2)
    axes[1].set_title('Análise de Silhueta (Silhouette Score)', fontsize=14)
    axes[1].set_xlabel('Número de Clusters (K)', fontsize=12)
    axes[1].set_ylabel('Coeficiente de Silhueta (Mais próximo de 1 é melhor)', fontsize=12)
    axes[1].axvline(x=4, color='red', linestyle='--', label='Escolha K=4')
    axes[1].legend()
    axes[1].grid(True, linestyle=':', alpha=0.7)
    
    plt.tight_layout()
    plt.savefig('validacao_kmeans_k.png', dpi=300)
    print(">>> Validação Salva em 'validacao_kmeans_k.png'")

if __name__ == "__main__":
    rodar_validacao_matematica_k()
