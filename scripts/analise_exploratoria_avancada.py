import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

def gerar_graficos_fase_2():
    print(">>> Iniciando Análise Exploratória Avançada (Fase 2)...")
    sns.set_theme(style="whitegrid")
    
    # Carregar Dados
    try:
        df_completo = pd.read_csv("dataset_pacing_completo.csv")
        df_kmeans = pd.read_csv("resultados_kmeans_todas_distancias.csv")
    except Exception as e:
        print("Erro: rode o ETL e o K-Means antes de iniciar as analises avancadas.")
        return
        
    # Preparar Dados Consolidados (Última linha por performance)
    df_consolidado = df_completo.drop_duplicates(subset=['campeonato', 'tipo_piscina', 'genero', 'distancia_prova', 'fase', 'atleta'], keep='last').copy()
    df_consolidado['id_performance'] = df_consolidado['campeonato'] + " | " + df_consolidado['atleta'] + " (" + df_consolidado['genero'] + " " + df_consolidado['fase'] + " " + df_consolidado['distancia_prova'].astype(str) + "m " + df_consolidado['tipo_piscina'] + ")"
    
    # Merge
    df_analise = df_kmeans.merge(df_consolidado, on='id_performance', how='inner')
    
    # ---------------------------------------------------------
    # 1. Heats vs Finals (O Fator Eliminatória)
    # ---------------------------------------------------------
    print("Gerando Análise 1: Heats vs Finals...")
    plt.figure(figsize=(10, 6))
    props = df_analise.groupby('fase')['Estrategia_Pacing'].value_counts(normalize=True).unstack()
    props.plot(kind='bar', stacked=True, colormap='viridis', figsize=(10, 6))
    plt.title('Distribuição de Estratégias: Eliminatórias vs Finais', fontsize=14)
    plt.ylabel('Proporção Adotada (%)')
    plt.xlabel('Fase da Competição')
    plt.legend(title='Estratégia K-Means', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig('insight_1_heats_vs_finals.png', dpi=300)
    plt.close()

    # ---------------------------------------------------------
    # 2. Homens vs Mulheres (Assinatura de Gênero)
    # Vamos avaliar o Desvio Padrão da Velocidade Relativa (Constância)
    # ---------------------------------------------------------
    print("Gerando Análise 2: Assinatura de Gênero (Constância de Pacing)...")
    # Agrupamos as parciais inteiras para calcular o desvio padrao de cada nadador
    df_completo['id_performance'] = df_completo['campeonato'] + " | " + df_completo['atleta'] + " (" + df_completo['genero'] + " " + df_completo['fase'] + " " + df_completo['distancia_prova'].astype(str) + "m " + df_completo['tipo_piscina'] + ")"
    std_pacing = df_completo.groupby(['id_performance', 'genero'])['velocidade_relativa'].std().reset_index()
    std_pacing.rename(columns={'velocidade_relativa': 'std_velocidade'}, inplace=True)
    
    plt.figure(figsize=(8, 6))
    sns.violinplot(data=std_pacing, x='genero', y='std_velocidade', palette='Set2')
    plt.title('Variabilidade do Pacing (Menos = Mais Constante)', fontsize=14)
    plt.ylabel('Desvio Padrão da Velocidade Relativa')
    plt.xlabel('Gênero')
    plt.tight_layout()
    plt.savefig('insight_2_genero_pacing.png', dpi=300)
    plt.close()

    # ---------------------------------------------------------
    # 3. Escolas Nacionais de Natação (TOP 5 Países)
    # ---------------------------------------------------------
    print("Gerando Análise 3: Escolas Nacionais (EUA, AUS, GBR, CHN, ITA)...")
    top_paises = ['USA', 'AUS', 'GBR', 'CHN', 'ITA']
    df_paises = df_analise[df_analise['nacionalidade'].isin(top_paises)]
    
    ct = pd.crosstab(df_paises['nacionalidade'], df_paises['Estrategia_Pacing'], normalize='index') * 100
    plt.figure(figsize=(10, 5))
    sns.heatmap(ct, annot=True, fmt=".1f", cmap="YlGnBu", cbar_kws={'label': '% de Adoção'})
    plt.title('Mapa de Calor Tático: Escolas Nacionais de Natação', fontsize=14)
    plt.ylabel('Nacionalidade')
    plt.xlabel('Estratégia de Pacing')
    plt.tight_layout()
    plt.savefig('insight_3_escolas_nacionais.png', dpi=300)
    plt.close()

    # ---------------------------------------------------------
    # 4. Piscina Curta vs Piscina Longa (Fator Virada/Fadiga)
    # Foco na prova de 1500m Livre
    # ---------------------------------------------------------
    print("Gerando Análise 4: Curva de Fadiga (Short Course vs Long Course)...")
    df_1500 = df_completo[df_completo['distancia_prova'] == 1500].copy()
    # Criar "buckets" percentuais de prova (0-10%, 10-20%...) para comparar distancias diferentes de viradas
    df_1500['progresso_prova'] = (df_1500['distancia_parcial'] / df_1500['distancia_prova']) * 100
    # Arredondar para a dezena mais proxima
    df_1500['progresso_buck'] = df_1500['progresso_prova'].round(0)
    
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df_1500, x='progresso_buck', y='velocidade_relativa', hue='tipo_piscina', palette=['blue', 'red'], errorbar=None)
    plt.title('Curva Média de Fadiga: 1500m Livre (Curta vs Longa)', fontsize=14)
    plt.ylabel('Velocidade Relativa (%)')
    plt.xlabel('Progresso da Prova (%)')
    plt.axhline(100, color='gray', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig('insight_4_curta_vs_longa.png', dpi=300)
    plt.close()

    # ---------------------------------------------------------
    # 5. A Assinatura do Ouro (Rank 1 vs Outros na última parcial)
    # ---------------------------------------------------------
    print("Gerando Análise 5: O Sprint Final do Campeão Olímpico/Mundial...")
    df_finais = df_completo[df_completo['fase'].str.lower() == 'final'].copy()
    
    # Classificar Rank em Categorias
    def classificar_rank(r):
        if r == 1: return 'Ouro (1º)'
        elif r in [2, 3]: return 'Pódio (2º e 3º)'
        else: return 'Finalista (4º+)'
    
    df_finais['categoria_rank'] = df_finais['rank'].apply(classificar_rank)
    
    # Pegar apenas a última parcial
    ultimas_parciais = df_finais.drop_duplicates(subset=['id_performance'], keep='last')
    
    plt.figure(figsize=(9, 6))
    sns.boxplot(data=ultimas_parciais, x='categoria_rank', y='velocidade_relativa', order=['Ouro (1º)', 'Pódio (2º e 3º)', 'Finalista (4º+)'], palette='flare')
    plt.title('O Segredo do Ouro: Força do Sprint Final (Última Parcial)', fontsize=14)
    plt.ylabel('Velocidade Relativa da Última Parcial (%)')
    plt.xlabel('Colocação')
    plt.axhline(100, color='gray', linestyle='--', label='Velocidade Média Absoluta')
    plt.legend()
    plt.tight_layout()
    plt.savefig('insight_5_assinatura_ouro.png', dpi=300)
    plt.close()
    
    print(">>> FASE 2 CONCLUÍDA! As 5 imagens de insights foram geradas com sucesso.")

if __name__ == "__main__":
    gerar_graficos_fase_2()
