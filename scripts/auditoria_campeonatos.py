import pandas as pd

def rodar_auditoria():
    try:
        df = pd.read_csv("dataset_pacing_completo.csv")
    except Exception as e:
        print("Arquivo 'dataset_pacing_completo.csv' ainda não existe ou não foi atualizado. Aguarde o fim do script ETL!")
        return

    print("\n=== AUDITORIA DE ATLETAS POR CAMPEONATO ===")
    print("Objetivo: Detectar arquivos PDF que tiveram seus dados pulados devido a formatação diferente.\n")
    
    # Para cada campeonato, quantos atletas distintos extraímos?
    # (Como o dataset é Long Format, contamos apenas as performances únicas, agrupando para não contar a mesma pessoa 30 vezes)
    df['id_performance_unica'] = df['atleta'] + " " + df['genero'] + " " + df['fase'] + " " + df['distancia_prova'].astype(str)
    
    resumo = df.groupby('campeonato')['id_performance_unica'].nunique().reset_index()
    resumo.columns = ['Campeonato (Arquivo PDF)', 'Qtd de Performances Únicas Extraídas']
    
    # Ordenar pelos que extraíram MENOS para detectar falhas do Regex
    resumo = resumo.sort_values(by='Qtd de Performances Únicas Extraídas')
    
    print(resumo.to_string(index=False))
    
    total = resumo['Qtd de Performances Únicas Extraídas'].sum()
    print(f"\nTotal Geral de Performances Extraídas: {total}")
    print("\n--- DIAGNÓSTICO ---")
    print("Se você enviou 32 PDFs e apenas 10 apareceram nesta lista (ou se algum tem 0 atletas),")
    print("isso confirma que o Regex não encontrou o padrão Omega padrão neles.")

if __name__ == '__main__':
    rodar_auditoria()
