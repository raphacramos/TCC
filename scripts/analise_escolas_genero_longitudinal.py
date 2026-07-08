import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
import os
from scipy.stats import chi2_contingency

# Configuração de estilo para os gráficos
sns.set_theme(style="whitegrid")
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Inter', 'Outfit', 'DejaVu Sans', 'Arial']

# Diretório de Artefatos para salvar cópias
ARTIFACT_DIR = "/Users/raphaelramos/.gemini/antigravity/brain/94b82bc2-5022-49cb-9c5e-04358ac9bab8/artifacts"

def salvar_grafico(filename):
    """Salva o gráfico atual no diretório scripts/ e no diretório de artefatos."""
    plt.tight_layout()
    # Salva no diretório de trabalho atual (Cwd)
    plt.savefig(filename, dpi=300)
    # Salva no diretório de artefatos
    artifact_path = os.path.join(ARTIFACT_DIR, filename)
    plt.savefig(artifact_path, dpi=300)
    print(f">>> Gráfico salvo em '{filename}' e cópia em '{artifact_path}'")
    plt.close()

# Dicionário de mapeamento de campeonatos para anos
MAPA_ANOS = {
    'continentais_curta_Complete_Results_Book': 2012,
    'continentais_curta_Get_the_complete_results_book_here-2': 2010,
    'continentais_curta_Get_the_complete_results_book_here': 2011,
    'continentais_curta_RESULTS_BOOK-2': 2024,
    'continentais_curta_europeu_curta2023': 2023,
    'continentais_curta_europeu_curta2025': 2025,
    'continentais_longa_Get_the_complete_results_book_here-3': 2010,
    'continentais_longa_Get_the_complete_results_book_here': 2012,
    'continentais_longa_europeu_longa2020': 2021,
    'continentais_longa_europeu_longa2024': 2024,
    'mundiais_curta_Complete_Results_Book-2': 2012,
    'mundiais_curta_Complete_results_book': 2014,
    'mundiais_curta_Get_the_complete_results_book_here': 2010,
    'mundiais_curta_RESULTS_BOOK-3': 2024,
    'mundiais_curta_mundial_curta2016': 2016,
    'mundiais_curta_mundial_curta2018': 2018,
    'mundiais_curta_mundial_curta2021': 2021,
    'mundiais_curta_mundial_curta2022': 2022,
    'mundiais_curta_mundial_curta2024': 2024,
    'mundiais_longa_COMPLETE_RESULTS_BOOK - cópia': 2015,
    'mundiais_longa_COMPLETE_RESULTS_BOOK - cópia': 2015,
    'mundiais_longa_Complete_Results_Book': 2013,
    'mundiais_longa_Get_the_complete_results_book_here-2': 2011,
    'mundiais_longa_RESULTS_BOOK': 2024,
    'mundiais_longa_mundial_longa2017': 2017,
    'mundiais_longa_mundial_longa2019': 2019,
    'mundiais_longa_mundial_longa2022': 2022,
    'mundiais_longa_mundial_longa2023': 2023,
    'mundiais_longa_mundial_longa2024': 2024,
    'mundiais_longa_mundial_singapura_2025': 2025,
    'olimpiadas_olimpiadas_2012': 2012,
    'olimpiadas_olimpiadas_2016': 2016,
    'olimpiadas_olimpiadas_2021': 2021,
    'olimpiadas_olimpiadas_2024': 2024,
}

def extrair_ano(c):
    if c in MAPA_ANOS:
        return MAPA_ANOS[c]
    m = re.search(r'\b(20\d{2})\b', c)
    if m:
        return int(m.group(1))
    return None

def rodar_novas_analises():
    print(">>> 1. Carregando dados consolidando para novas análises...")
    try:
        df_completo = pd.read_csv("dataset_pacing_completo.csv")
        df_kmeans = pd.read_csv("resultados_kmeans_todas_distancias.csv")
    except FileNotFoundError:
        print("Erro: rode o ETL e o modelo K-Means primeiro.")
        return
        
    df_perf = df_completo.drop_duplicates(subset=['campeonato', 'tipo_piscina', 'genero', 'distancia_prova', 'fase', 'atleta'], keep='last').copy()
    
    # ------------------------------------------------------------------
    # ANÁLISE 1: SUCESSO DE MEDALHAS POR ESCOLA NACIONAL (Insight 6)
    # ------------------------------------------------------------------
    print("\n>>> Executando Análise 1: Sucesso de Medalhas por País...")
    df_med = df_perf[df_perf['medalhista'] == True].copy()
    
    # Classificar tipo de medalha
    df_med['medalha'] = df_med['rank'].map({1: 'Ouro', 2: 'Prata', 3: 'Bronze'})
    
    # Cruzamento para contar medalhas por país
    cruzamento_medalhas = pd.crosstab(df_med['nacionalidade'], df_med['medalha'])
    
    # Garantir a ordem das colunas
    colunas_medalhas = [c for c in ['Ouro', 'Prata', 'Bronze'] if c in cruzamento_medalhas.columns]
    cruzamento_medalhas = cruzamento_medalhas[colunas_medalhas]
    
    # Adicionar coluna total e ordenar
    cruzamento_medalhas['Total'] = cruzamento_medalhas.sum(axis=1)
    top_paises_medalhas = cruzamento_medalhas.sort_values(by='Total', ascending=False).head(10)
    
    # Plotar
    plt.figure(figsize=(10, 6))
    cores_medalhas = {'Ouro': '#FFD700', 'Prata': '#C0C0C0', 'Bronze': '#CD7F32'}
    
    # Plot stacked bar
    top_paises_medalhas[colunas_medalhas].plot(
        kind='bar', stacked=True, color=[cores_medalhas[c] for c in colunas_medalhas], 
        edgecolor='black', linewidth=0.5, figsize=(10, 6)
    )
    plt.title('Geopolítica da Natação: TOP 10 Escolas Nacionais por Medalhas (2010 - 2025)', fontsize=14, fontweight='bold')
    plt.xlabel('Nacionalidade (País)', fontsize=11)
    plt.ylabel('Quantidade de Medalhas', fontsize=11)
    plt.xticks(rotation=0)
    plt.legend(title='Medalha')
    salvar_grafico('insight_6_escolas_medalhas.png')

    # ------------------------------------------------------------------
    # ANÁLISE 2: PACING DE MEDALHISTAS POR GÊNERO (Insight 7)
    # ------------------------------------------------------------------
    print("\n>>> Executando Análise 2: Pacing de Medalhistas por Gênero...")
    df_consolidado = df_perf.copy()
    df_consolidado['id_performance'] = df_consolidado['campeonato'] + ' | ' + df_consolidado['atleta'] + ' (' + df_consolidado['genero'] + ' ' + df_consolidado['fase'] + ' ' + df_consolidado['distancia_prova'].astype(str) + 'm ' + df_consolidado['tipo_piscina'] + ')'
    
    # Merge com resultados K-Means
    df_analise = df_kmeans.merge(df_consolidado[['id_performance', 'medalhista', 'genero']], on='id_performance', how='inner')
    df_med_pacing = df_analise[df_analise['medalhista'] == True].copy()
    
    # Proporções de pacing por gênero
    frequencias = pd.crosstab(df_med_pacing['Estrategia_Pacing'], df_med_pacing['genero'], normalize='columns') * 100
    df_plot_gen = frequencias.reset_index().melt(id_vars='Estrategia_Pacing', var_name='Gênero', value_name='Taxa de Adoção (%)')
    
    # Teste de Independência do Qui-Quadrado
    tabela_contingencia = pd.crosstab(df_med_pacing['Estrategia_Pacing'], df_med_pacing['genero'])
    print("Tabela de Contingência (Gênero vs Pacing entre Medalhistas):")
    print(tabela_contingencia)
    try:
        chi2, p_valor, dof, exp = chi2_contingency(tabela_contingencia)
        print(f"Teste Qui-Quadrado (Gênero vs Pacing Medalhistas): stat={chi2:.4f}, p-valor={p_valor:.4e}")
    except Exception as e:
        print(f"Erro ao rodar Qui-Quadrado de gênero: {e}")
        
    # Plotar
    plt.figure(figsize=(10, 6))
    sns.barplot(
        data=df_plot_gen, x='Estrategia_Pacing', y='Taxa de Adoção (%)', hue='Gênero',
        palette=['#3498db', '#e74c3c'], edgecolor='black', linewidth=0.5
    )
    plt.title('Diferença de Pacing por Gênero entre Medalhistas de Elite', fontsize=14, fontweight='bold')
    plt.xlabel('Estratégia de Pacing (Cluster)', fontsize=11)
    plt.ylabel('Taxa de Adoção (%)', fontsize=11)
    plt.xticks(rotation=15, ha='right')
    plt.legend(title='Gênero')
    salvar_grafico('insight_7_genero_medalhistas_pacing.png')

    # ------------------------------------------------------------------
    # ANÁLISE 3: LONGITUDINAL - CURVA DE AUGE DE CARREIRA (Insight 8)
    # ------------------------------------------------------------------
    print("\n>>> Executando Análise 3: Análise Longitudinal de Carreira (Curva de Auge)...")
    df_perf['ano'] = df_perf['campeonato'].apply(extrair_ano)
    df_perf_anos = df_perf.dropna(subset=['ano']).copy()
    
    # Agrupar no nível de ano: melhor tempo por atleta por prova por piscina por ano
    df_event_year = df_perf_anos.groupby(['atleta', 'genero', 'distancia_prova', 'tipo_piscina', 'ano'])['tempo_acumulado_seg'].min().reset_index()
    df_event_year.rename(columns={'tempo_acumulado_seg': 'tempo_final'}, inplace=True)
    
    # Identificar atleta-eventos com 3 ou mais anos de dados
    event_counts = df_event_year.groupby(['atleta', 'distancia_prova', 'tipo_piscina'])['ano'].nunique()
    valid_events = event_counts[event_counts >= 3].index
    
    # Filtrar
    df_event_year['event_key'] = list(zip(df_event_year['atleta'], df_event_year['distancia_prova'], df_event_year['tipo_piscina']))
    df_long = df_event_year[df_event_year['event_key'].isin(valid_events)].copy()
    
    # Encontrar melhor tempo histórico (Personal Best - PB) por prova
    pb = df_long.groupby(['atleta', 'distancia_prova', 'tipo_piscina'])['tempo_final'].min().reset_index()
    pb.rename(columns={'tempo_final': 'tempo_pb'}, inplace=True)
    
    df_long = df_long.merge(pb, on=['atleta', 'distancia_prova', 'tipo_piscina'], how='inner')
    
    # Encontrar o primeiro ano em que atingiu o PB (Ano de Auge)
    df_pb_year = df_long[df_long['tempo_final'] == df_long['tempo_pb']].groupby(['atleta', 'distancia_prova', 'tipo_piscina'])['ano'].min().reset_index()
    df_pb_year.rename(columns={'ano': 'ano_pb'}, inplace=True)
    
    df_long = df_long.merge(df_pb_year, on=['atleta', 'distancia_prova', 'tipo_piscina'], how='inner')
    
    # Definir anos relativos e Índice de Rendimento (%)
    df_long['anos_rel_pb'] = df_long['ano'] - df_long['ano_pb']
    df_long['indice_performance'] = (df_long['tempo_pb'] / df_long['tempo_final']) * 100
    
    # Filtrar janela de relevância temporal (-4 a +4 anos) onde há quantidade estatística de amostras
    df_janela = df_long[(df_long['anos_rel_pb'] >= -4) & (df_long['anos_rel_pb'] <= 4)].copy()
    
    print("Amostragem por Ano Relativo ao Auge:")
    print(df_janela.groupby('anos_rel_pb')['indice_performance'].count())
    
    # Plotar Curva Média de Carreira
    plt.figure(figsize=(10, 6))
    sns.lineplot(
        data=df_janela, x='anos_rel_pb', y='indice_performance', 
        marker='o', markersize=8, color='#8e44ad', linewidth=2.5, errorbar=('ci', 95)
    )
    plt.title('Curva Longitudinal de Carreira: Evolução e Declínio Fisiológico', fontsize=14, fontweight='bold')
    plt.xlabel('Anos em Relação ao Auge de Carreira (0 = Personal Best)', fontsize=11)
    plt.ylabel('Índice de Rendimento (% do PB)', fontsize=11)
    plt.axvline(x=0, color='gray', linestyle='--', alpha=0.5)
    plt.ylim(92, 101)
    plt.grid(True, linestyle=':', alpha=0.7)
    salvar_grafico('insight_8_curva_auge_carreira.png')

    # ------------------------------------------------------------------
    # ANÁLISE 4: TRAJETÓRIAS INDIVIDUAIS DE ELITE (Insight 9)
    # ------------------------------------------------------------------
    print("\n>>> Executando Análise 4: Trajetórias Individuais de Atletas (Insight 9)...")
    
    # Função auxiliar para gerar e salvar gráficos individuais para o TCC
    def gerar_e_salvar_individual(distancia, titulo, nome_arquivo, atletas_info):
        plt.figure(figsize=(8, 5))
        df_sub = df_perf_anos[(df_perf_anos['distancia_prova'] == distancia) & (df_perf_anos['tipo_piscina'] == 'Long Course')].copy()
        for nome_busca, label, cor, marker in atletas_info:
            df_ath = df_sub[df_sub['atleta'].str.contains(nome_busca, na=False, case=False)].copy()
            if not df_ath.empty:
                df_ath['tempo_final_min'] = df_ath['tempo_acumulado_seg'] / 60
                df_g = df_ath.groupby('ano')['tempo_final_min'].min().reset_index().sort_values('ano')
                plt.plot(df_g['ano'], df_g['tempo_final_min'], marker=marker, markersize=6, color=cor, linewidth=2, label=label)
        
        plt.title(titulo, fontsize=12, fontweight='bold')
        plt.ylabel("Melhor Tempo no Ano (Minutos)", fontsize=11)
        plt.xlabel("Ano Calendário", fontsize=11)
        plt.legend(fontsize=9)
        plt.grid(True, linestyle=':', alpha=0.6)
        plt.gca().invert_yaxis()
        salvar_grafico(nome_arquivo)

    # 1. Gerar os 4 gráficos individuais primeiro
    atletas_1500m_masc = [
        ("PALTRINIERI", "Gregorio Paltrinieri (ITA)", "#2c3e50", "s"),
        ("ROMANCHUK", "Mykhailo Romanchuk (UKR)", "#2980b9", "o"),
        ("WELLBROCK", "Florian Wellbrock (GER)", "#e67e22", "^"),
        ("CHRISTIANSEN", "Henrik Christiansen (NOR)", "#27ae60", "d")
    ]
    gerar_e_salvar_individual(1500, "Trajetória Individual: 1500m Livre Masculino (Long Course)", "insight_9a_trajetoria_1500m_masc.png", atletas_1500m_masc)

    atletas_1500m_fem = [
        ("LEDECKY", "Katie Ledecky (USA)", "#8e44ad", "s"),
        ("QUADARELLA", "Simona Quadarella (ITA)", "#c0392b", "o"),
        ("KOBRICH", "Kristel Köbrich (CHI)", "#16a085", "^")
    ]
    gerar_e_salvar_individual(1500, "Trajetória Individual: 1500m Livre Feminino (Long Course)", "insight_9b_trajetoria_1500m_fem.png", atletas_1500m_fem)

    atletas_800m = [
        ("LEDECKY", "Katie Ledecky (USA - Fem)", "#8e44ad", "s"),
        ("PALTRINIERI", "Gregorio Paltrinieri (ITA - Masc)", "#2c3e50", "o"),
        ("QUADARELLA", "Simona Quadarella (ITA - Fem)", "#c0392b", "^")
    ]
    gerar_e_salvar_individual(800, "Trajetória Individual: 800m Livre (Long Course)", "insight_9c_trajetoria_800m.png", atletas_800m)

    atletas_400m = [
        ("SUN Yang", "Sun Yang (CHN - Masc)", "#d35400", "s"),
        ("TITMUS", "Ariarne Titmus (AUS - Fem)", "#27ae60", "o"),
        ("LEDECKY", "Katie Ledecky (USA - Fem)", "#8e44ad", "^")
    ]
    gerar_e_salvar_individual(400, "Trajetória Individual: 400m Livre (Long Course)", "insight_9d_trajetoria_400m.png", atletas_400m)

    # 2. Gerar o gráfico em grade (combined panel) para manter compatibilidade com o relatório HTML
    fig, axs = plt.subplots(2, 2, figsize=(14, 10))
    
    def plotar_atleta_eixo(ax, nome_busca, distancia, label, cor, marker):
        df_sub = df_perf_anos[(df_perf_anos['distancia_prova'] == distancia) & (df_perf_anos['tipo_piscina'] == 'Long Course')].copy()
        df_ath = df_sub[df_sub['atleta'].str.contains(nome_busca, na=False, case=False)].copy()
        if not df_ath.empty:
            df_ath['tempo_final_min'] = df_ath['tempo_acumulado_seg'] / 60
            df_g = df_ath.groupby('ano')['tempo_final_min'].min().reset_index().sort_values('ano')
            ax.plot(df_g['ano'], df_g['tempo_final_min'], marker=marker, markersize=6, color=cor, linewidth=2, label=label)
            return True
        return False

    # Subplot 1 (Top-Left): 1500m Livre Masculino (Long Course)
    plotar_atleta_eixo(axs[0, 0], "PALTRINIERI", 1500, "Gregorio Paltrinieri (ITA)", "#2c3e50", "s")
    plotar_atleta_eixo(axs[0, 0], "ROMANCHUK", 1500, "Mykhailo Romanchuk (UKR)", "#2980b9", "o")
    plotar_atleta_eixo(axs[0, 0], "WELLBROCK", 1500, "Florian Wellbrock (GER)", "#e67e22", "^")
    plotar_atleta_eixo(axs[0, 0], "CHRISTIANSEN", 1500, "Henrik Christiansen (NOR)", "#27ae60", "d")
    axs[0, 0].set_title("1500m Livre Masculino (Long Course)", fontsize=11, fontweight='bold')
    axs[0, 0].set_ylabel("Melhor Tempo no Ano (Minutos)", fontsize=10)
    axs[0, 0].legend(fontsize=8)
    axs[0, 0].grid(True, linestyle=':', alpha=0.6)
    axs[0, 0].invert_yaxis()
    
    # Subplot 2 (Top-Right): 1500m Livre Feminino (Long Course)
    plotar_atleta_eixo(axs[0, 1], "LEDECKY", 1500, "Katie Ledecky (USA)", "#8e44ad", "s")
    plotar_atleta_eixo(axs[0, 1], "QUADARELLA", 1500, "Simona Quadarella (ITA)", "#c0392b", "o")
    plotar_atleta_eixo(axs[0, 1], "KOBRICH", 1500, "Kristel Köbrich (CHI)", "#16a085", "^")
    axs[0, 1].set_title("1500m Livre Feminino (Long Course)", fontsize=11, fontweight='bold')
    axs[0, 1].set_ylabel("Melhor Tempo no Ano (Minutos)", fontsize=10)
    axs[0, 1].legend(fontsize=8)
    axs[0, 1].grid(True, linestyle=':', alpha=0.6)
    axs[0, 1].invert_yaxis()

    # Subplot 3 (Bottom-Left): 800m Livre (Long Course)
    plotar_atleta_eixo(axs[1, 0], "LEDECKY", 800, "Katie Ledecky (USA - Fem)", "#8e44ad", "s")
    plotar_atleta_eixo(axs[1, 0], "PALTRINIERI", 800, "Gregorio Paltrinieri (ITA - Masc)", "#2c3e50", "o")
    plotar_atleta_eixo(axs[1, 0], "QUADARELLA", 800, "Simona Quadarella (ITA - Fem)", "#c0392b", "^")
    axs[1, 0].set_title("800m Livre (Long Course)", fontsize=11, fontweight='bold')
    axs[1, 0].set_xlabel("Ano Calendário", fontsize=10)
    axs[1, 0].set_ylabel("Melhor Tempo no Ano (Minutos)", fontsize=10)
    axs[1, 0].legend(fontsize=8)
    axs[1, 0].grid(True, linestyle=':', alpha=0.6)
    axs[1, 0].invert_yaxis()

    # Subplot 4 (Bottom-Right): 400m Livre (Long Course)
    plotar_atleta_eixo(axs[1, 1], "SUN Yang", 400, "Sun Yang (CHN - Masc)", "#d35400", "s")
    plotar_atleta_eixo(axs[1, 1], "TITMUS", 400, "Ariarne Titmus (AUS - Fem)", "#27ae60", "o")
    plotar_atleta_eixo(axs[1, 1], "LEDECKY", 400, "Katie Ledecky (USA - Fem)", "#8e44ad", "^")
    axs[1, 1].set_title("400m Livre (Long Course)", fontsize=11, fontweight='bold')
    axs[1, 1].set_xlabel("Ano Calendário", fontsize=10)
    axs[1, 1].set_ylabel("Melhor Tempo no Ano (Minutos)", fontsize=10)
    axs[1, 1].legend(fontsize=8)
    axs[1, 1].grid(True, linestyle=':', alpha=0.6)
    axs[1, 1].invert_yaxis()

    plt.suptitle("Trajetórias Individuais de Elite: Evolução Temporal de Tempos Anuais (2010 - 2025)\n(Eixo Y Invertido: Tempos mais rápidos / melhores aparecem no topo)", fontsize=13, fontweight='bold', y=0.98)
    salvar_grafico('insight_9_trajetorias_individuais.png')

    print("\n>>> Pipeline de Expansão de Análises Executado com Sucesso!")

if __name__ == '__main__':
    rodar_novas_analises()
