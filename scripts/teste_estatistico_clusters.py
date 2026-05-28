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
    
    distancias = [400, 800, 1500]
    tipos_piscina = ['Long Course', 'Short Course']
    
    fig, axes = plt.subplots(3, 2, figsize=(16, 18))
    
    print("\n======================================================================")
    print("INFERÊNCIA ESTATÍSTICA GLOBAL - CHI-SQUARE & ANOVA")
    print("======================================================================")
    
    for i, dist in enumerate(distancias):
        for j, tipo in enumerate(tipos_piscina):
            nome_prova = f"{dist}m Livre ({tipo})"
            ax = axes[i, j]
            
            df_prova = df_analise[df_analise['Prova'] == nome_prova].copy()
            if df_prova.empty:
                print(f"\nSem dados para {nome_prova}. Pulando.")
                ax.set_visible(False)
                continue
                
            print(f"\n>>> Analisando {len(df_prova)} performances na prova de {nome_prova}...")
            
            # Teste 1: Qui-Quadrado
            tabela_contingencia = pd.crosstab(df_prova['Estrategia_Pacing'], df_prova['medalhista'])
            try:
                chi2, p_valor_chi2, dof, esperada = chi2_contingency(tabela_contingencia)
                print(f"  [Qui-Quadrado] Chi-Square Stat: {chi2:.4f} | p-valor: {p_valor_chi2:.4e} | dof: {dof}")
                if p_valor_chi2 < 0.05:
                    print("  => Conclusão: Relação estatisticamente significante entre pacing e medalha!")
                else:
                    print("  => Conclusão: Relação não significante.")
            except Exception as e:
                print(f"  [Qui-Quadrado] Erro ao rodar teste: {e}")
                
            # Teste 2: ANOVA
            grupos = []
            nomes_grupos = df_prova['Estrategia_Pacing'].unique()
            for estrategia in nomes_grupos:
                tempos = df_prova[df_prova['Estrategia_Pacing'] == estrategia]['tempo_final_seg'].dropna()
                if len(tempos) > 0:
                    grupos.append(tempos)
                    print(f"    - Média {estrategia}: {tempos.mean():.2f}s (n={len(tempos)})")
            
            if len(grupos) > 1:
                f_stat, p_valor_anova = f_oneway(*grupos)
                print(f"  [ANOVA] F-Statistic: {f_stat:.4f} | p-valor: {p_valor_anova:.4e}")
                if p_valor_anova < 0.05:
                    print("  => Conclusão: Diferença de médias altamente significante!")
                else:
                    print("  => Conclusão: Sem diferença significante entre as médias.")
            else:
                print("  [ANOVA] Grupos insuficientes para rodar o teste.")
                
            # Plotar Boxplot no grid 3x2
            sns.boxplot(data=df_prova, x='Estrategia_Pacing', y='tempo_final_seg', ax=ax, palette='Set2', hue='Estrategia_Pacing', legend=False)
            ax.set_title(f'ANOVA: {nome_prova}', fontsize=12, fontweight='bold')
            ax.set_xlabel('Estratégia de Pacing', fontsize=9)
            ax.set_ylabel('Tempo Final (segundos)', fontsize=9)
            ax.tick_params(axis='x', rotation=15, labelsize=8)
            ax.grid(True, linestyle=':', alpha=0.5)

    plt.tight_layout()
    plt.savefig('anova_tempo_por_estrategia.png', dpi=300)
    print("\n>>> Gráfico global de Boxplots ANOVA salvo em 'anova_tempo_por_estrategia.png'")

if __name__ == "__main__":
    rodar_inferencia_estatistica()
