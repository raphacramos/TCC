import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans

def rotular_estrategias_dinamicamente(centroides, k):
    """
    Classifica cada centroide em um estilo de pacing baseado em matemática.
    """
    labels = {}
    dist_inicial = centroides.columns[0]
    dist_final = centroides.columns[-1]
    
    # Extrair métricas de cada cluster
    metricas = []
    for c in centroides.index:
        vel_inicial = centroides.loc[c, dist_inicial]
        vel_final = centroides.loc[c, dist_final]
        std_dev = centroides.loc[c].std()
        vel_meio = centroides.loc[c, centroides.columns[1:-1]].mean()
        queda = vel_inicial - vel_meio
        metricas.append({'id': c, 'vel_ini': vel_inicial, 'vel_fin': vel_final, 'std': std_dev, 'queda': queda})
        
    df_metricas = pd.DataFrame(metricas)
    
    # 1. Uniforme: Menor desvio padrão de velocidade ao longo da prova
    id_uniforme = df_metricas.loc[df_metricas['std'].idxmin(), 'id']
    labels[id_uniforme] = "Uniforme / Estável"
    
    # 2. Parabólico: Dentre os que sobraram, o que tem maior sprint final
    df_restante = df_metricas[df_metricas['id'] != id_uniforme]
    id_parabolico = df_restante.loc[df_restante['vel_fin'].idxmax(), 'id']
    labels[id_parabolico] = "Parabólico (Sprint Final)"
    
    # 3. Super Agressivo: Dentre os que sobraram, o que tem a maior "queda" do início pro meio
    df_restante = df_restante[df_restante['id'] != id_parabolico]
    if not df_restante.empty:
        id_agressivo = df_restante.loc[df_restante['queda'].idxmax(), 'id']
        labels[id_agressivo] = "Super Agressivo (Fly & Die)"
        
        # 4. Positivo Tradicional (e outros se K > 4)
        df_restante = df_restante[df_restante['id'] != id_agressivo]
        for _, row in df_restante.iterrows():
            # Apenas distribui numerações extras se for maior que 4
            labels[row['id']] = f"Positivo (Variante {int(row['id'])})"
            
    # Garantir fallback se a lógica der conflito
    for c in centroides.index:
        if c not in labels:
            labels[c] = f"Estratégia {c}"
            
    return labels

def rodar_pipeline_kmeans():
    print(">>> 1. Carregando os dados consolidados do ETL...")
    try:
        df = pd.read_csv("dataset_pacing_completo.csv")
    except FileNotFoundError:
        print("Erro: Arquivo não encontrado.")
        return
        
    distancias = [400, 800, 1500]
    tipos_piscina = ['Long Course', 'Short Course']
    K_CLUSTERS = 4 
    
    fig, axes = plt.subplots(3, 2, figsize=(20, 18))
    todos_resultados = []
    
    for i, dist in enumerate(distancias):
        for j, tipo in enumerate(tipos_piscina):
            print(f"\n>>> Processando prova de {dist}m ({tipo})...")
            df_dist = df[(df['distancia_prova'] == dist) & (df['tipo_piscina'] == tipo)].copy()
            ax = axes[i, j]
            
            if df_dist.empty:
                print(f"Nenhum dado para {dist}m em {tipo}.")
                ax.set_visible(False)
                continue
                
            df_dist['id_performance'] = df_dist['campeonato'] + " | " + df_dist['atleta'] + " (" + df_dist['genero'] + " " + df_dist['fase'] + ")"
            # Garantir que não haja duplicatas caso o mesmo PDF esteja duplicado na pasta
            df_dist = df_dist.drop_duplicates(subset=['id_performance', 'distancia_parcial'])
            df_pivot = df_dist.pivot(index='id_performance', columns='distancia_parcial', values='velocidade_relativa')
            df_pivot = df_pivot.dropna()
            
            if df_pivot.shape[0] < K_CLUSTERS:
                print(f"Performances válidas ({df_pivot.shape[0]}) menores que K={K_CLUSTERS}. Pulando.")
                ax.set_visible(False)
                continue
                
            print(f"Dados Pivotados: {df_pivot.shape[0]} atletas | Features: {df_pivot.shape[1]} parciais.")
            
            # Treinando K-Means (K=4)
            kmeans = KMeans(n_clusters=K_CLUSTERS, random_state=42, n_init='auto')
            df_pivot['Cluster'] = kmeans.fit_predict(df_pivot)
            
            # Analisando Centroides e Rotulando
            centroides = df_pivot.groupby('Cluster').mean()
            mapa_estrategias = rotular_estrategias_dinamicamente(centroides, K_CLUSTERS)
            df_pivot['Estrategia_Pacing'] = df_pivot['Cluster'].map(mapa_estrategias)
            
            # Guardando para o CSV global
            df_resultados = df_pivot.reset_index()
            df_resultados.insert(1, 'Prova', f"{dist}m Livre ({tipo})")
            todos_resultados.append(df_resultados)
            
            # Plotando no grid 3x2
            cores = sns.color_palette("Set1", K_CLUSTERS) 
            
            for c_idx, cluster_id in enumerate(centroides.index):
                qtd_atletas = sum(df_pivot["Cluster"] == cluster_id)
                nome_estrategia = mapa_estrategias[cluster_id]
                
                sns.lineplot(
                    x=centroides.columns, 
                    y=centroides.loc[cluster_id], 
                    marker='o', 
                    label=f'{nome_estrategia} (N={qtd_atletas})',
                    linewidth=2.5,
                    color=cores[c_idx],
                    ax=ax
                )
                
            ax.axhline(y=100, color='black', linestyle='--', label='Baseline (100%)', alpha=0.5)
            ax.set_title(f'{dist}m Livre - {tipo}', fontsize=15)
            ax.set_xlabel('Distância Parcial (m)', fontsize=11)
            ax.set_ylabel('Velocidade Relativa (%)', fontsize=11)
            ax.legend(title='Estratégia Identificada', bbox_to_anchor=(1.02, 1), loc='upper left')
            ax.grid(True, linestyle=':', alpha=0.7)

    plt.tight_layout()
    plt.savefig('kmeans_pacing_todas_distancias.png', dpi=300)
    print("\n>>> Gráfico global salvo em 'kmeans_pacing_todas_distancias.png'")
    
    # Exportar os resultados consolidados de todas as distâncias
    if todos_resultados:
        df_final_csv = pd.concat(todos_resultados, ignore_index=True)
        # Limpar NaN gerados pelo concat (já que 1500m tem colunas que 400m não tem)
        df_final_csv = df_final_csv.fillna("")
        
        # Colocando colunas importantes na frente
        cols_principais = ['id_performance', 'Prova', 'Estrategia_Pacing']
        outras_cols = [c for c in df_final_csv.columns if c not in cols_principais + ['Cluster']]
        df_final_csv = df_final_csv[cols_principais + outras_cols]
        
        arquivo_saida = "resultados_kmeans_todas_distancias.csv"
        df_final_csv.to_csv(arquivo_saida, index=False)
        print(f">>> Planilha mestre consolidada salva em '{arquivo_saida}'")

if __name__ == '__main__':
    rodar_pipeline_kmeans()
