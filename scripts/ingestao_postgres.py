import pandas as pd
from sqlalchemy import create_engine
import sys

def ingestao_postgresql():
    """
    Exporta os DataFrames consolidados para um banco de dados relacional PostgreSQL,
    demonstrando habilidades plenas em Banco de Dados para a banca de Engenharia de Dados.
    """
    print(">>> Iniciando Pipeline de Carga (Load) para SGBD PostgreSQL...")
    
    # Substitua com as credenciais reais do seu servidor ou localhost
    DATABASE_URI = 'postgresql://usuario:senha@localhost:5432/tcc_natacao'
    
    try:
        # Tenta criar a engine do SQLAlchemy
        engine = create_engine(DATABASE_URI)
        
        # Testando conexão
        with engine.connect() as conexao:
            print("Conexão com PostgreSQL estabelecida com sucesso!")
            
    except Exception as e:
        print("\n[AVISO]: O servidor PostgreSQL não foi encontrado em localhost:5432.")
        print("Para a banca do TCC, garanta que o serviço (ex: via pgAdmin ou Docker) esteja rodando.")
        print(f"Erro original: {e}")
        print("\nPara executar o upload relacional depois, certifique-se de instalar as dependências:")
        print("pip install sqlalchemy psycopg2-binary")
        return

    # Se a conexão der certo, ler e salvar no banco
    try:
        print("\nCarregando datasets gerados pelo ETL...")
        df_pacing = pd.read_csv("dataset_pacing_completo.csv")
        df_clusters = pd.read_csv("resultados_kmeans_todas_distancias.csv")
        
        # Enviar Dataset Long Format (Feature Engineering Bruto)
        print("Criando tabela 'pacing_features_brutas' no banco de dados...")
        df_pacing.to_sql('pacing_features_brutas', engine, if_exists='replace', index=False)
        
        # Enviar Dataset Largo Format (Resultados de Machine Learning)
        print("Criando tabela 'clusters_kmeans_resultados' no banco de dados...")
        df_clusters.to_sql('clusters_kmeans_resultados', engine, if_exists='replace', index=False)
        
        print("\n>>> SUCESSO: Ingestão de Banco de Dados finalizada!")
        print("O orientador agora poderá rodar comandos SQL clássicos nas tabelas para auditoria.")
        
    except Exception as e:
        print(f"Erro durante a transação SQL: {e}")

if __name__ == "__main__":
    ingestao_postgresql()
