import pdfplumber
import pandas as pd
import numpy as np
import re
import os
import glob
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Dict, Optional

def converte_para_segundos(tempo_str: str) -> float:
    """
    Converte uma string de tempo ('mm:ss.cc', 'ss.cc', ou 'hh:mm:ss.cc') para segundos (float).
    """
    try:
        if not tempo_str or pd.isna(tempo_str) or tempo_str in ['DSQ', 'DNS']: ## desclassificado ou nao largou
            return 0.0
            
        tempo_str = str(tempo_str).strip()
        if ':' in tempo_str:
            partes = tempo_str.split(':')
            if len(partes) == 2: # mm:ss.cc
                return float(partes[0]) * 60 + float(partes[1])
           ## elif len(partes) == 3: # hh:mm:ss.cc (Raro, mas possível em maratonas aquáticas)
           ##     return float(partes[0]) * 3600 + float(partes[1]) * 60 + float(partes[2])
        return float(tempo_str)
    except Exception as e:
        print(f"Erro ao converter tempo '{tempo_str}': {e}")
        return 0.0

def extrair_contexto_pagina(texto_pagina: str) -> Optional[Dict]:
    """
    State Machine (Contexto):
    Varre o texto da página buscando as palavras-chave que identificam o Evento.
    Exemplo: "Event 102 Men's 400m Freestyle Final"
    """
    genero_match = re.search(r"(Men's|Women's)", texto_pagina, re.IGNORECASE)
    distancia_match = re.search(r"(400|800|1500)m\s+Freestyle", texto_pagina, re.IGNORECASE)
    fase_match = re.search(r"(Heats|Final|Semifinal)", texto_pagina, re.IGNORECASE)
    
    if genero_match and distancia_match and fase_match:
        return {
            "genero": genero_match.group(1).capitalize(),
            "distancia_prova": int(distancia_match.group(1)),
            "fase": fase_match.group(1).capitalize()
        }
    return None

def extrair_dados_pdf_escalavel(caminho_pdf: str) -> List[Dict]:
    """
    Itera por todas as páginas do PDF, identificando o contexto da prova e extraindo
    dinamicamente as parciais empilhadas (400m, 800m, 1500m).
    """
    # Regex 1: Identifica a linha inicial do atleta (suporta Formato Heats com Data de Nascimento e Heat Number)
    padrao_atleta = re.compile(r'^(\d+)\s+(?:(\d+)\s+)?(\d+)\s+([A-Za-z\s\-\']+?)\s+([A-Z]{3})\s+(?:\d{1,2}\s+[A-Z]{3}\s+\d{4}\s+)?([\d.]+)?\s*([\d:.]+|DSQ|DNS)')
    
    # Regex 2: Captura qualquer padrão de split na linha (Com ou sem posição entre parênteses)
    padrao_parciais = re.compile(r'(\d+)m\s+(?:\([^)]+\)\s+)?([\d:.]+)')
    
    resultados = []
    
    with pdfplumber.open(caminho_pdf) as pdf:
        for num_pagina, pagina in enumerate(pdf.pages):
            texto = pagina.extract_text()
            if not texto: continue
            
            # Atualiza o Estado/Contexto baseado na página atual
            contexto = extrair_contexto_pagina(texto)
            if not contexto:
                continue # Pula páginas que não são Freestyle 400/800/1500
                
            linhas = texto.split('\n')
            nadador_atual = None
            
            for linha in linhas:
                linha = linha.strip()
                match_atleta = padrao_atleta.match(linha)
                
                # Gatilho: Novo atleta encontrado
                if match_atleta:
                    rank, heat_opcional, lane, nome, nat, rt_opcional, tempo_final = match_atleta.groups()
                    nadador_atual = {
                        "campeonato": os.path.basename(caminho_pdf).replace('.pdf', ''),
                        "tipo_piscina": "Short Course" if "curta" in caminho_pdf.lower() else "Long Course",
                        "genero": contexto["genero"],
                        "distancia_prova": contexto["distancia_prova"],
                        "fase": contexto["fase"],
                        "rank": int(rank) if rank and rank.isdigit() else 999,
                        "atleta": nome.strip(),
                        "nacionalidade": nat,
                        "tempo_final": tempo_final,
                        "parciais": {} # Armazena chaves dinâmicas: {50: "24.77", 100: "51.95"}
                    }
                    resultados.append(nadador_atual)
                    continue
                
                # Loop Contínuo: Adiciona splits dinamicamente ao atleta atual
                if nadador_atual:
                    matches_parciais = padrao_parciais.finditer(linha)
                    for m in matches_parciais:
                        distancia, tempo_cumulativo = m.groups()
                        nadador_atual["parciais"][int(distancia)] = tempo_cumulativo

    return resultados

def transformar_e_calcular_features(dados_brutos: List[Dict]) -> pd.DataFrame:
    """
    Processa os dados em formato consolidado, aplica Data Cleaning (remove exceções)
    e calcula a Engenharia de Features agrupando por contexto.
    """
    linhas_long = []
    
    # Expandindo dicionários agrupados para Long Format nativo
    for d in dados_brutos:
        # Data Cleaning: Remoção de DSQ/DNS
        if d['tempo_final'] in ['DSQ', 'DNS']:
            continue
            
        dist_prova = d['distancia_prova']
        # Adicionar o tempo da prova como a última parcial de todas (caso não esteja no Regex da página)
        if dist_prova not in d['parciais'] and d['tempo_final'] not in ['DSQ', 'DNS']:
            d['parciais'][dist_prova] = d['tempo_final']
            
        for dist, tempo_str in d['parciais'].items():
            linhas_long.append({
                "campeonato": d["campeonato"],
                "tipo_piscina": d["tipo_piscina"],
                "genero": d["genero"],
                "distancia_prova": d["distancia_prova"],
                "fase": d["fase"],
                "rank": d["rank"],
                "atleta": d["atleta"],
                "nacionalidade": d["nacionalidade"],
                "distancia_parcial": dist,
                "tempo_acumulado_str": tempo_str,
                "tempo_final_str": d["tempo_final"]
            })
            
    df_long = pd.DataFrame(linhas_long)
    if df_long.empty: return df_long
    
    # Ordenação estrita por evento e por trecho
    df_long = df_long.sort_values(
        by=['campeonato', 'tipo_piscina', 'genero', 'distancia_prova', 'fase', 'atleta', 'distancia_parcial']
    ).reset_index(drop=True)
    
    # Conversões
    df_long['tempo_acumulado_seg'] = df_long['tempo_acumulado_str'].apply(converte_para_segundos)
    df_long['tempo_final_seg'] = df_long['tempo_final_str'].apply(converte_para_segundos)
    
    # Cálculo Vetorizado do Delta de cada Parcial (Agrupado por Evento/Atleta)
    agrupamento = ['campeonato', 'tipo_piscina', 'genero', 'distancia_prova', 'fase', 'atleta']
    
    df_long['tempo_parcial_seg'] = df_long.groupby(agrupamento)['tempo_acumulado_seg'].diff()
    df_long['tempo_parcial_seg'] = df_long['tempo_parcial_seg'].fillna(df_long['tempo_acumulado_seg'])
    
    df_long['distancia_trecho'] = df_long.groupby(agrupamento)['distancia_parcial'].diff()
    df_long['distancia_trecho'] = df_long['distancia_trecho'].fillna(df_long['distancia_parcial'])
    
    # Engenharia de Features (Fórmulas Esportivas de Pacing)
    df_long['percentual_tempo'] = (df_long['tempo_parcial_seg'] / df_long['tempo_final_seg']) * 100
    
    df_long['velocidade_trecho'] = df_long['distancia_trecho'] / df_long['tempo_parcial_seg']
    df_long['velocidade_media'] = df_long['distancia_prova'] / df_long['tempo_final_seg']
    df_long['velocidade_relativa'] = (df_long['velocidade_trecho'] / df_long['velocidade_media']) * 100
    
    # Criacao da Variavel Alvo: Medalhista (Apenas Finais, Top 3)
    df_long['medalhista'] = (df_long['fase'].str.lower() == 'final') & (df_long['rank'] <= 3)
    
    # Filtragem das colunas requeridas pelo usuário
    colunas_finais = [
        'campeonato', 'tipo_piscina', 'genero', 'distancia_prova', 'fase', 'rank', 'medalhista', 'atleta', 'nacionalidade', 
        'distancia_parcial', 'tempo_acumulado_seg', 'tempo_parcial_seg', 
        'percentual_tempo', 'velocidade_relativa'
    ]
    
    df_final = df_long[colunas_finais].copy()
    
    # Arredondamentos acadêmicos
    df_final['tempo_acumulado_seg'] = df_final['tempo_acumulado_seg'].round(2)
    df_final['tempo_parcial_seg'] = df_final['tempo_parcial_seg'].round(2)
    df_final['percentual_tempo'] = df_final['percentual_tempo'].round(2)
    df_final['velocidade_relativa'] = df_final['velocidade_relativa'].round(2)
    
    return df_final

def plotar_eda_dupla(df: pd.DataFrame):
    """
    Gera painel de Visualização de Dados Duplo filtrando como exemplo (Men's 400m Final).
    Subplot 1: Percentual do Tempo
    Subplot 2: Velocidade Relativa
    """
    # Filtro contextual
    filtro = (df['genero'] == "Men's") & (df['distancia_prova'] == 400) & (df['fase'] == "Final")
    df_plot = df[filtro].copy()
    
    if df_plot.empty:
        print("Aviso: Dados filtrados para o Plot ('Men's 400m Final') vazios. Utilizando dataset inteiro.")
        df_plot = df.copy()
        
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    # Subplot 1: Percentual do Tempo vs Distância
    sns.lineplot(
        data=df_plot, x='distancia_parcial', y='percentual_tempo', 
        hue='atleta', marker='o', ax=axes[0], legend=False
    )
    axes[0].set_title('Pacing: Percentual do Tempo (%)', fontsize=14)
    axes[0].set_xlabel('Distância Parcial (m)', fontsize=12)
    axes[0].set_ylabel('Percentual do Tempo (%)', fontsize=12)
    axes[0].grid(True, linestyle=':', alpha=0.7)
    
    # Subplot 2: Velocidade Relativa vs Distância
    sns.lineplot(
        data=df_plot, x='distancia_parcial', y='velocidade_relativa', 
        hue='atleta', marker='o', ax=axes[1]
    )
    axes[1].axhline(y=100, color='red', linestyle='--', label='Baseline (100%)')
    axes[1].set_title('Pacing: Velocidade Relativa (%)', fontsize=14)
    axes[1].set_xlabel('Distância Parcial (m)', fontsize=12)
    axes[1].set_ylabel('Velocidade Relativa (%)', fontsize=12)
    axes[1].grid(True, linestyle=':', alpha=0.7)
    
    # Ajuste e Salve
    axes[1].legend(title='Atleta', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig('eda_pacing_completo.png', dpi=300)
    print(">>> 4. EDA: Gráfico salvo em 'eda_pacing_completo.png'")

def main():
    arquivos_pdf = glob.glob("../pdfs_omega/**/*.pdf", recursive=True)
    if not arquivos_pdf:
        print("Nenhum arquivo PDF encontrado na pasta '../pdfs_omega/'")
        return
        
    arquivo_saida_csv = "dataset_pacing_completo.csv"
    campeonatos_processados = set()
    df_antigo = None
    
    if os.path.exists(arquivo_saida_csv):
        df_antigo = pd.read_csv(arquivo_saida_csv)
        campeonatos_processados = set(df_antigo['campeonato'].unique())
        print(f">>> Modo Incremental Ativo: O CSV atual tem {len(campeonatos_processados)} campeonatos. Eles serão ignorados no parsing.")
    
    novos_pdfs = []
    for caminho in arquivos_pdf:
        nome_camp = os.path.basename(caminho).replace('.pdf', '')
        if nome_camp not in campeonatos_processados:
            novos_pdfs.append(caminho)
            
    if not novos_pdfs:
        print(">>> Nenhum PDF novo encontrado. Todos já estão no CSV!")
        if df_antigo is not None and not df_antigo.empty:
            plotar_eda_dupla(df_antigo)
        return
    
    print(f">>> 1. Iniciando Extração Escalável ({len(novos_pdfs)} arquivos novos)...")
    dados_extraidos = []
    
    for caminho in novos_pdfs:
        print(f"Lendo: {os.path.basename(caminho)}...")
        dados = extrair_dados_pdf_escalavel(caminho)
        dados_extraidos.extend(dados)
    
    print(f"\n>>> 2. Transformando dados novos extraídos...")
    df_etl = transformar_e_calcular_features(dados_extraidos)
    
    if not df_etl.empty:
        if df_antigo is not None and not df_antigo.empty:
            df_final = pd.concat([df_antigo, df_etl], ignore_index=True)
            print(">>> Merge com o histórico antigo realizado com sucesso.")
        else:
            df_final = df_etl
            
        print("\n>>> 3. Exportando (Load)...")
        df_final.to_csv(arquivo_saida_csv, index=False)
        print(f"Dataset atualizado: '{arquivo_saida_csv}'")
        
        plotar_eda_dupla(df_final)
    else:
        print("Nenhum dado válido foi extraído dos PDFs novos.")

if __name__ == "__main__":
    main()