import pandas as pd
from scipy.stats import chi2_contingency, f_oneway
import seaborn as sns
import matplotlib.pyplot as plt

def rodar_inferencia_estatistica():
    print(">>> Iniciando Inferência Estatística sobre os Clusters de Pacing...")
    
    try:
        df_resultados = pd.read_csv("resultados_kmeans_todas_distancias.csv")
        df_completo = pd.read_csv("dataset_pacing_completo.csv")
    except Exception as e:
        print("Erro ao carregar datasets. Rode o ETL e o modelo K-Means primeiro.")
        return
        
    # Extrair informacao de medalha do dataset completo e mesclar com resultados do kmeans
    # Pegamos apenas a última parcial (onde tempo acumulado = tempo final) para ter o registro consolidado do atleta
    # e também extraímos as colunas 'medalhista' e 'tempo_final_seg'
    df_consolidado = df_completo.drop_duplicates(subset=['campeonato', 'tipo_piscina', 'genero', 'distancia_prova', 'fase', 'atleta'], keep='last').copy()
    
    # Criar id_performance para o merge
    df_consolidado['id_performance'] = df_consolidado['campeonato'] + " | " + df_consolidado['atleta'] + " (" + df_consolidado['genero'] + " " + df_consolidado['fase'] + " " + df_consolidado['distancia_prova'].astype(str) + "m " + df_consolidado['tipo_piscina'] + ")"
    
    # O tempo final é o tempo acumulado da última parcial
    df_consolidado['tempo_final_seg'] = df_consolidado['tempo_acumulado_seg']
    
    # Merge com os resultados do kmeans
    df_analise = df_resultados.merge(df_consolidado[['id_performance', 'medalhista', 'tempo_final_seg']], on='id_performance', how='inner')
    
    # Vamos focar na prova de 400m Livre (Long Course) para a prova estatística
    df_prova = df_analise[df_analise['Prova'] == '400m Livre (Long Course)'].copy()
    if df_prova.empty:
        print("Sem dados de 400m Long Course para realizar o teste. Abortando.")
        return
        
    print(f"Analisando {len(df_prova)} performances na prova de 400m Livre (Long Course).")
    
    # -------------------------------------------------------------
    # Teste 1: Qui-Quadrado (Chi-Square) - Variáveis Categóricas
    # Pergunta: A escolha da estratégia (Cluster) afeta a probabilidade de ganhar medalha?
    # -------------------------------------------------------------
    print("\n--- TESTE 1: Qui-Quadrado (Associação entre Estratégia e Medalha) ---")
    tabela_contingencia = pd.crosstab(df_prova['Estrategia_Pacing'], df_prova['medalhista'])
    print("Tabela de Contingência (Frequência Observada):")
    print(tabela_contingencia)
    
    chi2, p_valor_chi2, dof, esperada = chi2_contingency(tabela_contingencia)
    print(f"\nEstatística Chi-Square: {chi2:.4f}")
    print(f"P-Valor: {p_valor_chi2:.4f}")
    if p_valor_chi2 < 0.05:
        print("=> CONCLUSÃO: Rejeitamos a Hipótese Nula (H0). Existe relação estatisticamente significante entre o Pacing e a chance de medalha!")
    else:
        print("=> CONCLUSÃO: Falha ao rejeitar H0. Não há evidência estatística de que o Pacing afeta diretamente a chance de medalha neste recorte.")

    # -------------------------------------------------------------
    # Teste 2: ANOVA (One-Way Analysis of Variance) - Variável Contínua
    # Pergunta: O tempo final médio difere significativamente entre os diferentes Clusters?
    # -------------------------------------------------------------
    print("\n--- TESTE 2: ANOVA (Tempo Final vs Estratégia) ---")
    
    grupos = []
    nomes_grupos = df_prova['Estrategia_Pacing'].unique()
    for estrategia in nomes_grupos:
        tempos = df_prova[df_prova['Estrategia_Pacing'] == estrategia]['tempo_final_seg'].dropna()
        grupos.append(tempos)
        print(f"Média de Tempo - {estrategia}: {tempos.mean():.2f}s (n={len(tempos)})")
        
    f_stat, p_valor_anova = f_oneway(*grupos)
    print(f"\nEstatística F (ANOVA): {f_stat:.4f}")
    print(f"P-Valor: {p_valor_anova:.4f}")
    if p_valor_anova < 0.05:
        print("=> CONCLUSÃO: Rejeitamos a Hipótese Nula (H0). Pelo menos uma das estratégias de Pacing resulta em um tempo final estatisticamente diferente!")
    else:
        print("=> CONCLUSÃO: Falha ao rejeitar H0. Os tempos finais médios não são estatisticamente diferentes entre as estratégias.")

    # Gerar Boxplot para visualização da ANOVA
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df_prova, x='Estrategia_Pacing', y='tempo_final_seg', palette='Set2')
    plt.title('ANOVA: Distribuição do Tempo Final por Estratégia de Pacing (400m Livre)', fontsize=14)
    plt.xlabel('Estratégia de Pacing', fontsize=12)
    plt.ylabel('Tempo Final (segundos)', fontsize=12)
    plt.xticks(rotation=15)
    plt.tight_layout()
    plt.savefig('anova_tempo_por_estrategia.png', dpi=300)
    print("\n>>> Gráfico Boxplot da ANOVA salvo em 'anova_tempo_por_estrategia.png'")

if __name__ == "__main__":
    rodar_inferencia_estatistica()
