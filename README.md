# TCC: Análise de Pacing na Natação 🏊‍♂️📊

Repositório do Trabalho de Conclusão de Curso (TCC) em Ciência da Computação, focado em **Análise de Dados Esportivos** e **Pacing Strategy (Estratégia de Prova)** na natação de médio e longo fundo (400m, 800m e 1500m Livre).

## 🎯 Objetivo do Projeto
O objetivo principal é extrair, processar e analisar dados brutos (relatórios oficias em PDF) gerados pela **Omega Timing / World Aquatics**. Através de técnicas de Data Engineering e extração dinâmica (RegEx e State Machines), convertemos dados empilhados não estruturados em Datasets consolidados (Formato *Long / Tidy Data*).

Com os dados padronizados, aplicamos algoritmos de **Machine Learning (K-Means Clustering)** para identificar diferentes perfis estratégicos de gerenciamento de energia (Pacing) adotados pelos nadadores de elite mundiais.

## ⚙️ Arquitetura e Pipeline ETL
1. **Extração (Extract):** Leitura de PDFs multipáginas com `pdfplumber`. A state machine contextualiza a prova (Distância, Gênero, Fase).
2. **Transformação (Transform):** 
   - Limpeza de anomalias (DNS, DSQ).
   - Extração contínua (com Empilhamento) dos *splits* (voltas) usando `Expressões Regulares`.
   - Conversão de *Wide Format* para *Long Format* via `pandas`.
3. **Engenharia de Features:** Criação das métricas analíticas:
   - *Percentual do Tempo:* Avalia quanto da energia global foi alocada por trecho.
   - *Velocidade Relativa Normalizada:* Define em percentual a velocidade da parcial comparada com a média da prova.
4. **Carga e EDA (Load & Exploratory Data Analysis):** Exportação dos dados prontos para bancos relacionais (PostgreSQL) e plotagem visual com `Seaborn/Matplotlib`.

## 🛠️ Tecnologias Utilizadas
* **Python 3**
* **Pandas:** Transformação de dados, vetorização e cálculos `.diff()`.
* **pdfplumber:** Parsing e leitura profunda dos arquivos PDF da Omega.
* **Regex (re):** Padrões escaláveis para extração de dados tabulares ocultos.
* **Matplotlib & Seaborn:** Visualizações de Análise Exploratória (Gráficos de Pacing).
* *(Futuro)* **Scikit-Learn:** Modelagem de Clusters via K-Means.

## 🚀 Como Executar
1. Instale as dependências:
```bash
pip install pandas pdfplumber matplotlib seaborn openpyxl
```
2. Navegue até a pasta de scripts e execute o ETL Principal:
```bash
cd scripts
python extrair_resultados_omega.py
```
3. O pipeline varrerá a pasta de PDFs e gerará o arquivo consolidado `dataset_pacing_completo.csv` junto com os painéis gráficos `eda_pacing_completo.png`.

## 📁 Estrutura do Repositório
* `/pdfs_omega/`: PDFs brutos oficiais.
* `/scripts/`: Códigos-fonte do Pipeline de Extração e EDA.
  * `extrair_resultados_omega.py`: Core do ETL.
* `/*.md`: Relatórios de status e ideias de reuniões.
