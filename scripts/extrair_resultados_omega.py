import pdfplumber
import pandas as pd
import re
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Dict, Optional

def converte_para_segundos(tempo_str: str) -> float:
    """
    Converte uma string de tempo ('mm:ss.cc', 'ss.cc', ou 'hh:mm:ss.cc') para segundos (float).
    """
    try:
        if not tempo_str or pd.isna(tempo_str) or tempo_str in ['DSQ', 'DNS']:
            return 0.0
            
        tempo_str = str(tempo_str).strip()
        if ':' in tempo_str:
            partes = tempo_str.split(':')
            if len(partes) == 2: # mm:ss.cc
                return float(partes[0]) * 60 + float(partes[1])
            elif len(partes) == 3: # hh:mm:ss.cc (Raro, mas possível em maratonas aquáticas)
                return float(partes[0]) * 3600 + float(partes[1]) * 60 + float(partes[2])
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
                        "genero": contexto["genero"],
                        "distancia_prova": contexto["distancia_prova"],
                        "fase": contexto["fase"],
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
                "genero": d["genero"],
                "distancia_prova": d["distancia_prova"],
                "fase": d["fase"],
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
        by=['genero', 'distancia_prova', 'fase', 'atleta', 'distancia_parcial']
    ).reset_index(drop=True)
    
    # Conversões
    df_long['tempo_acumulado_seg'] = df_long['tempo_acumulado_str'].apply(converte_para_segundos)
    df_long['tempo_final_seg'] = df_long['tempo_final_str'].apply(converte_para_segundos)
    
    # Cálculo Vetorizado do Delta de cada Parcial (Agrupado por Evento/Atleta)
    agrupamento = ['genero', 'distancia_prova', 'fase', 'atleta']
    df_long['tempo_parcial_seg'] = df_long.groupby(agrupamento)['tempo_acumulado_seg'].diff()
    df_long['tempo_parcial_seg'] = df_long['tempo_parcial_seg'].fillna(df_long['tempo_acumulado_seg'])
    
    # Engenharia de Features (Fórmulas Esportivas de Pacing)
    df_long['percentual_tempo'] = (df_long['tempo_parcial_seg'] / df_long['tempo_final_seg']) * 100
    
    comprimento_piscina = 50.0
    df_long['velocidade_trecho'] = comprimento_piscina / df_long['tempo_parcial_seg']
    df_long['velocidade_media'] = df_long['distancia_prova'] / df_long['tempo_final_seg']
    df_long['velocidade_relativa'] = (df_long['velocidade_trecho'] / df_long['velocidade_media']) * 100
    
    # Filtragem das colunas requeridas pelo usuário
    colunas_finais = [
        'genero', 'distancia_prova', 'fase', 'atleta', 'nacionalidade', 
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
    caminho_arquivo_pdf = "../pdfs_omega/mundial_singapura_2025.pdf"
    
    print(">>> 1. Iniciando Extração Escalável com State Machine...")
    dados_extraidos = extrair_dados_pdf_escalavel(caminho_arquivo_pdf)
    
    print(f">>> 2. Transformando dados extraídos...")
    df_etl = transformar_e_calcular_features(dados_extraidos)
    
    if not df_etl.empty:
        print("\n>>> Pipeline ETL Consolidado: Visualização do Long Format:")
        print(df_etl.head(10).to_string(index=False))
        
        print("\n>>> 3. Exportando (Load)...")
        arquivo_saida_csv = "dataset_pacing_completo.csv"
        df_etl.to_csv(arquivo_saida_csv, index=False)
        print(f"Dataset consolidado para Banco de Dados gerado: '{arquivo_saida_csv}'")
        
        plotar_eda_dupla(df_etl)
    else:
        print("Nenhum dado válido foi extraído ou transformado.")

if __name__ == "__main__":
    main()