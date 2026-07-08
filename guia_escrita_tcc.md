# Guia de Escrita e Conteúdo para o TCC (Draft Expandido & Guia de Elementos)

Este documento contém textos de rascunho acadêmico aprofundados, sugestões de parágrafos introdutórios (mini-resumos) para o início de cada capítulo do seu TCC, um mapa completo de inserção de imagens com código LaTeX pronto e um guia detalhado sobre como gerenciar as citações e referências bibliográficas.

---

## ESTRUTURA GERAL DO TCC (MAPA DE ELEMENTOS)

A tabela abaixo mostra a relação entre os arquivos `.tex` do seu modelo de TCC, os parágrafos introdutórios que você deve colocar na abertura de cada um, as imagens geradas pelos scripts Python do projeto e as referências bibliográficas aplicáveis.

| Capítulo / Arquivo `.tex` | Imagens Associadas | Referências Recomendadas |
| :--- | :--- | :--- |
| **1. Introdução** (`introducao.tex`) | Nenhum | Nenhuma |
| **2. Fundamentação Teórica** (`fundamentacao.tex`) | Nenhum | `\cite{abbiss2008}`, `\cite{mcgibbon2018}` |
| **3. Metodologia** (`metodologia.tex`) | Nenhum (Lógica do pipeline) | Nenhuma |
| **4. Resultados e Discussão** (`resultados.tex`) | `validacao_kmeans_k.png`, `kmeans_pacing_todas_distancias.png`, `anova_tempo_por_estrategia.png`, `insight_1_heats_vs_finals.png`, `insight_2_genero_pacing.png`, `insight_7_genero_medalhistas_pacing.png`, `insight_4_curta_vs_longa.png`, `insight_5_assinatura_ouro.png`, `insight_8_curva_auge_carreira.png`, `insight_9_trajetorias_individuais.png`, `insight_3_escolas_nacionais.png`, `insight_6_escolas_medalhas.png` | `\cite{abbiss2008}`, `\cite{mcgibbon2018}` |
| **5. Considerações Finais** (`conclusao.tex`) | Nenhum | Nenhuma |

---

## 1. INTRODUÇÃO (`introducao.tex`)

### 📝 Mini-Resumo / Parágrafo Introdutório do Capítulo 1
> **Instrução:** Insira este parágrafo no início do arquivo `introducao.tex`, logo abaixo do título `\section{INTRODUÇÃO}` e antes do primeiro texto. Ele serve para situar o leitor sobre o que será discutido no capítulo.
>
> *"Este capítulo apresenta a introdução ao tema de estudo, contextualizando a importância da análise de dados no esporte de alto rendimento e os desafios envolvidos no gerenciamento do ritmo de prova (pacing) na natação de meio e longo fundo. A seguir, detalha-se a problematização que motivou a pesquisa, a necessidade de normalização relativa de velocidades, os objetivos gerais e específicos que guiaram a investigação, bem como as principais hipóteses estatísticas delineadas para validar a análise tática computacional."*

### 1.1 Contextualização e Introdução
A análise de dados aplicados ao esporte, comumente chamada de *Sports Analytics*, passou de uma atividade de suporte estatístico básico para um pilar estratégico indispensável no esporte de alto rendimento. Com a proliferação de sensores vestíveis, câmeras de alta velocidade e sistemas automatizados de cronometragem, comissões técnicas agora contam com fluxos contínuos de dados para planejar treinamentos e definir táticas de competição. Na natação de elite mundial, onde a diferença entre conquistar a medalha de ouro olímpica e ficar fora do pódio é frequentemente medida em centésimos de segundo, a otimização de cada fase da prova assume uma importância vital. 

Dentre os múltiplos fatores determinantes para o rendimento nas provas de meio e longo fundo (especificamente as distâncias de 400 metros, 800 metros e 1500 metros no estilo Livre), a estratégia de ritmo — conceitualizada na literatura científica como *pacing strategy* — destaca-se como a decisão tática mais crítica que um atleta deve tomar. O *pacing* descreve a forma como um nadador gerencia e distribui seu esforço mecânico e suas reservas energéticas (aeróbicas e anaeróbicas) ao longo da distância da prova. A natação de fundo exige do atleta um equilíbrio refinado: iniciar a prova de forma excessivamente rápida pode desencadear uma fadiga precoce e catastrófica, enquanto um início muito conservador pode distanciar o nadador dos líderes da prova de forma irreversível. 

Historicamente, o estudo científico e empírico do *pacing* tem esbarrado em limitações metodológicas. A principal delas reside na análise dos tempos parciais (*split times*) em termos absolutos. A análise puramente absoluta negligencia o fato de que atletas possuem diferentes capacidades aeróbicas de base, tornando difícil isolar o comportamento tático puro de sua aptidão cardiovascular. Por exemplo, se um nadador de nível olímpico realiza a primeira parcial de 50 metros em 26 segundos e um nadador júnior a realiza em 28 segundos, a diferença absoluta nos diz muito sobre o nível físico de cada um, mas pouco sobre qual dos dois adotou uma estratégia mais agressiva ou conservadora em relação aos seus próprios limites. Para solucionar esta lacuna e permitir uma análise comparativa puramente tática, este trabalho propõe a aplicação de técnicas de engenharia de dados e aprendizado de máquina para modelar o *pacing* em termos relativos, utilizando dados reais de competições de elite mundial.

### 1.2 Problematização
O problema central a ser mitigado neste estudo reside na complexidade fisiológica e física envolvida no gerenciamento do ritmo de prova na água. Do ponto de vista metabólico, o nadador possui uma reserva finita de capacidade anaeróbica alática e lática, além de um sistema aeróbico que leva algum tempo para atingir o seu estado estável de captação de oxigênio (*VO2 kinetics*). Se o nadador inicia a prova com velocidade muito superior à sua velocidade de limiar anaeróbico, ele acumula subprodutos metabólicos (como íons de hidrogênio, que causam a acidose muscular) de forma precoce, comprometendo severamente a eficiência de contração muscular nas fases finais da prova.

Sob a ótica computacional, o desafio consiste em modelar esse comportamento dinâmico através de uma base de dados robusta e limpa, e classificar os padrões de ritmo sem introduzir vieses subjetivos. A maioria dos estudos na literatura esportiva limita-se a amostras pequenas (dezenas de atletas) e ambientes de laboratório ou competições locais. Para obter conclusões generalizáveis sobre o comportamento da elite mundial, é preciso minerar dados de centenas de PDFs oficiais de resultados (publicados pela Omega Timing e World Aquatics) e converter esses documentos não estruturados em uma estrutura de dados de formato *long/tidy* apta a algoritmos de aprendizado de máquina. 

Com os dados estruturados, surge a necessidade de modelagem não supervisionada. O algoritmo de agrupamento *K-Means* apresenta-se como uma ferramenta eficaz, mas sua aplicação exige uma validação criteriosa: a definição de quantos perfis de pacing realmente existem e como classificá-los matematicamente. Adicionalmente, faz-se necessário integrar a modelagem computacional a testes de inferência estatística para provar se as estratégias de *pacing* identificadas possuem correlação significativa com métricas de sucesso competitivo (conquista de medalhas) e tempos finais de prova. Há também a problematização de como variáveis externas, tais como gênero (masculino vs. feminino), fase da prova (eliminatórias vs. finais), formato da piscina (curta de 25m vs. longa de 50m) e potências esportivas (escolas nacionais) afetam o comportamento tático adotado.

### 1.3 Objetivos

#### Objetivo Geral
Modelar e analisar de forma comparativa as estratégias de distribuição de esforço (*pacing*) de nadadores de elite mundial nas provas de 400m, 800m e 1500m Livre, utilizando um pipeline de engenharia de dados integrado a algoritmos de agrupamento não supervisionado (*K-Means*) e testes de inferência estatística (Qui-Quadrado e ANOVA).

#### Objetivos Específicos
*   Desenvolver um pipeline automatizado de extração, tratamento e consolidação de dados de parciais a partir de livros de resultados oficiais da Omega Timing / World Aquatics.
*   Implementar a normalização das velocidades relativas para permitir a análise tática livre do viés de tempo absoluto.
*   Modelar perfis estratégicos de distribuição de esforço via algoritmo de agrupamento não supervisionado *K-Means*, validando matematicamente o número ideal de perfis.
*   Aplicar testes estatísticos de independência (Qui-Quadrado) e análise de variância (ANOVA) para mensurar o impacto dos perfis de *pacing* na conquista de medalhas e nos tempos finais.
*   Investigar a influência de variáveis externas, como o gênero do atleta, a fase da competição (eliminatórias vs. finais), a geopolítica esportiva (escolas nacionais) e a configuração da piscina (curta vs. longa) no comportamento tático.

---

## 2. FUNDAMENTAÇÃO TEÓRICA (`fundamentacao.tex`)

### 📝 Mini-Resumo / Parágrafo Introdutório do Capítulo 2
> **Instrução:** Insira este parágrafo no início do arquivo `fundamentacao.tex`, logo abaixo do título `\section{FUNDAMENTAÇÃO TEÓRICA}`.
>
> *"Este capítulo estabelece a base teórica necessária para o desenvolvimento do estudo. Primeiramente, revisam-se os conceitos fundamentais de pacing descritos na literatura esportiva e a aplicabilidade de tais estratégias no contexto da natação clássica de piscina. Em seguida, abordam-se os mecanismos fisiológicos de fornecimento de energia (aeróbicos e anaeróbicos) e a dinâmica do limiar de fadiga. Por fim, descreve-se a modelagem física do arrasto hidrodinâmico e sua influência biomecânica na eficiência energética do nado."*

### 2.1 Citações Bibliográficas neste Capítulo
> [!TIP]
> Use os comandos de citação nas seguintes sentenças:
> *   Ao mencionar o trabalho conceitual de Abbiss e Laursen, insira `\cite{abbiss2008}`.
> *   Ao citar a revisão sistemática sobre pacing na natação, insira `\cite{mcgibbon2018}`.

#### Texto da Seção:
O estudo científico de *pacing* foi amplamente sistematizado por Abbiss e Laursen (2008) `\cite{abbiss2008}`, que identificaram seis perfis principais de distribuição de energia em esportes de endurance. Na natação de piscina de meio e longo fundo, contudo, dois desses perfis são biologicamente ou ambientalmente inviáveis: a tática *All-Out* (restrita a tiros curtos por esgotamento imediato do sistema ATP-CP) e a tática *Variable* (ritmo oscilante), ineficiente pela natureza estável da piscina.

Dessa forma, a análise teórica foca nas quatro estratégias restantes aplicáveis à piscina, amplamente documentadas na revisão sistemática de McGibbon et al. (2018) `\cite{mcgibbon2018}`:
*   **Uniforme (Estável):** Velocidade constante, otimizando o arrasto.
*   **Positivo Tradicional:** Velocidade inicial alta com declínio gradual.
*   **Parabólico (U-Shape):** Início e final rápidos com controle intermediário.
*   **Super Agressivo (Fly \& Die):** Esforço excessivo no início que colapsa o nado subsequente.

### 2.2 Fisiologia do Exercício de Endurance na Natação
O desempenho em provas de natação de meio e longo fundo é governado pela interação metabólica entre os sistemas de transferência de energia. As provas de 400m Livre duram tipicamente entre 3,5 e 4,5 minutos, as de 800m entre 7,5 e 8,5 minutos, e as de 1500m entre 14,3 e 16 minutos para a elite. Fisiologicamente, essas janelas temporais colocam as provas na categoria de exercício de intensidade alta a severa, exigindo contribuição massiva tanto das vias aeróbicas quanto anaeróbicas.

Nos primeiros instantes da prova, o corpo utiliza as reservas intramusculares de trifosfato de adenosina (ATP) e fosfocreatina (CP) pela via anaeróbica alática. À medida que essas reservas se esgotam nos primeiros 10 a 15 segundos, a glicólise anaeróbica (via lática) acelera rapidamente para suprir a demanda contínua de ATP, quebrando o glicogênio intramuscular em piruvato e gerando lactato e íons de hidrogênio ($H^+$) como subprodutos. Simultaneamente, a captação de oxigênio pelo sistema cardiovascular (via aeróbica) entra em uma fase de aceleração exponencial (*VO2 kinetics*), levando de 90 a 120 segundos para atingir um estado de fornecimento energético estável que cubra a maior parte da ordem de trabalho da prova.

O principal limitador fisiológico do ritmo está associado ao acúmulo intracelular de íons $H^+$. O excesso de hidrogênio reduz o pH citoplasmático das fibras musculares (acidose muscular), o que interfere diretamente nas pontes cruzadas de actina e miocina e inibe enzimas-chave da via glicolítica, como a fosfofructocinase (PFK). Se um nadador adota um pacing excessivamente rápido no início (estilo *Fly \& Die*), a via glicolítica opera em taxa máxima antes que o sistema aeróbico atinja sua capacidade de platô. O resultado é o acúmulo descontrolado de íons $H^+$ precocemente na prova. Uma vez atingido o ponto de acidose severa, a capacidade contrátil do músculo decai vertiginosamente, forçando o nadador a uma desaceleração severa para que os sistemas de tamponamento consigam clarear o ambiente celular.

### 2.3 Biomecânica e Arrastos Hidrodinâmicos
A locomoção na água difere radicalmente do deslocamento terrestre devido à alta densidade e viscosidade do meio. A física hidrodinâmica define que um corpo em movimento na água sofre uma força de arrasto ($F_D$) contrária ao deslocamento, expressa pela equação:
\begin{equation}
    F_D = \frac{1}{2} C_D \rho A v^2
\end{equation}
Nesta equação, $C_D$ é o coeficiente de arrasto (que reflete o alinhamento corporal e a técnica do nadador), $\rho$ é a densidade da água (aproximadamente $1000 \text{ kg/m}^3$), $A$ é a área de seção transversal projetada do nadador contra a água, e $v$ é a velocidade de deslocamento.

Como a força de arrasto hidrodinâmico cresce com o quadrado da velocidade ($v^2$), a potência mecânica ($P_D$) necessária para vencer esse arrasto e manter o corpo em movimento cresce de forma cúbica:
\begin{equation}
    P_D = F_D \cdot v = \frac{1}{2} C_D \rho A v^3
\end{equation}
Esta relação cúbica tem implicações biomecânicas profundas sobre o *pacing*. Qualquer variação na velocidade de nado exige um custo energético exponencialmente maior para acelerar o corpo de volta contra a barreira viscosa da água. Por exemplo, se um nadador oscila constantemente sua velocidade acima e abaixo de sua média, a energia extra gasta para acelerar nos trechos mais rápidos supera significativamente a energia poupada nos trechos mais lentos. Portanto, do ponto de vista puramente físico e mecânico, a estratégia de pacing mais eficiente para nado contínuo em superfície é a **Uniforme** (velocidade constante), pois ela minimiza o custo total de transporte de energia da prova.

No entanto, a piscina de natação não é um canal contínuo de nado em superfície. A cada 50 metros (ou 25 metros), o nadador encontra a parede, realiza uma virada e executa um impulso vigoroso com as pernas. Nesta fase de saída da parede, o nadador atinge velocidades muito superiores à velocidade máxima de nado em superfície. Ao manter o corpo em posição de *streamline* (braços esticados e travados atrás das orelhas, corpo rígido e estreito), o nadador minimiza a área de seção transversal ($A$) e o coeficiente de arrasto ($C_D$). Esta fase de deslizamento subaquático representa um momento de altíssima eficiência mecânica e serve como um breve período de recuperação ativa para a musculatura propulsora dos membros superiores (ombros, peitoral e costas), o que altera a dinâmica de fadiga quando comparado à corrida ou ciclismo.

---

## 3. METODOLOGIA (`metodologia.tex`)

### 📝 Mini-Resumo / Parágrafo Introdutório do Capítulo 3
> **Instrução:** Insira este parágrafo no início do arquivo `metodologia.tex`, logo abaixo de `\section{METODOLOGIA}`.
>
> *"Este capítulo descreve de forma estruturada as etapas metodológicas que compõem o pipeline de análise do projeto. A seção inicia com a descrição do processo de ETL e extração dos dados tabulares a partir dos PDFs oficiais. Em seguida, detalha-se o tratamento matemático de conversão temporal para velocidades relativas normalizadas. Por fim, apresenta-se a formulação do modelo de agrupamento K-Means, os critérios de validação matemática do parâmetro K, as equações dos testes estatísticos de hipótese (ANOVA e Qui-Quadrado) e a rotina de alinhamento temporal para a análise longitudinal."*

### 3.1 Coleta e Tratamento de Dados (Dataset)
A base de dados utilizada neste estudo foi extraída de relatórios digitais oficiais publicados em formato PDF pela organizadora de cronometragem oficial, a *Omega Timing*, sob tutela da *World Aquatics*. O dataset cobre competições globais de elite realizadas entre 2012 e 2025.

A extração de dados de arquivos PDF foi realizada com o uso da biblioteca `pdfplumber`, estruturada como uma Máquina de Estados Finita (FSM). O fluxo do script opera da seguinte maneira:
1.  **Estado de Busca de Prova:** O script lê o arquivo PDF linha por linha. Ao detectar palavras-chave específicas (ex: "Men's 1500m Freestyle - Final"), ele extrai os metadados da prova (Distância: 1500, Gênero: Masculino, Fase: Final, Tipo de Piscina: Piscina Longa) e transita para o estado de extração de resultados.
2.  **Estado de Extração de Atletas:** O script detecta a presença de nomes de atletas e seus respectivos países. Por meio de Expressões Regulares (`re.compile`), o extrator captura a estrutura tabular contendo raia, atleta, país e parciais acumuladas.
3.  **Estado de Processamento de Parciais:** Para cada nadador, o extrator varre as colunas horizontais de tempos de virada e reconstrói o vetor temporal, descartando performances com desclassificação (DSQ) ou ausência (DNS).

Após a varredura, o dataset consolidado foi formatado no modelo *Long Data* via biblioteca `Pandas`. O dataset final é composto por 5.665 performances completas de elite e mais de 100.000 tempos de parciais individuais.

### 3.2 Métrica de Normalização e Velocidade Relativa
Com os dados de parciais acumuladas extraídos, procedeu-se ao cálculo do tempo líquido de cada parcial de 50 metros ($\Delta t_i$). O tempo líquido da parcial $i$ é calculado como a diferença entre o tempo acumulado no ponto $i$ ($T_i$) e o tempo acumulado no ponto anterior ($T_{i-1}$):
\begin{equation}
    \Delta t_i = T_i - T_{i-1} \quad (\text{com } T_0 = 0)
\end{equation}
A velocidade média de deslocamento em cada parcial $i$ ($v_i$, expressa em metros por segundo) é calculada dividindo-se a distância do trecho (normalmente $\Delta d_i = 50\text{m}$) pelo tempo líquido correspondente:
\begin{equation}
    v_i = \frac{50}{\Delta t_i}
\end{equation}

A velocidade média global da performance de prova do atleta ($\bar{v}$, expressa em m/s) é obtida dividindo-se a distância total da prova ($d_{\text{total}}$) pelo tempo final de prova ($t_{\text{final}}$):
\begin{equation}
    \bar{v} = \frac{d_{\text{total}}}{t_{\text{final}}}
\end{equation}

A transformação para a métrica de Velocidade Relativa Normalizada ($V_{rel, i}$, expressa em percentual) é dada por:
\begin{equation}
    V_{rel, i} = \left( \frac{v_i}{\bar{v}} \right) \times 100\%
\end{equation}

### 3.3 Modelagem Computacional: K-Means Clustering
O agrupamento e classificação automática dos estilos de *pacing* foram realizados através do algoritmo não supervisionado *K-Means*. Cada performance de prova foi mapeada como um vetor multidimensional $X = [V_{rel, 1}, V_{rel, 2}, \dots, V_{rel, D}]$, onde a dimensão $D$ varia de acordo com a prova ($D=8$ para 400m Livre; $D=16$ para 800m Livre; $D=30$ para 1500m Livre).

O algoritmo de clusterização computacional opera iterativamente com o objetivo de minimizar a Soma dos Quadrados Intra-Cluster (Inércia térmica ou WCSS - *Within-Cluster Sum of Squares*):
\begin{equation}
    WCSS = \sum_{j=1}^{K} \sum_{X_i \in C_j} || X_i - \mu_j ||^2
\end{equation}
Onde $K$ representa o número de clusters, $C_j$ representa o conjunto de amostras atribuídas ao cluster $j$, e $\mu_j$ representa o centroide (vetor médio) do cluster $j$.

*   **Método do Cotovelo (Elbow Method):** Rastreou-se o comportamento da inércia (WCSS) para valores de $K$ de 1 a 10. Observou-se uma queda acentuada na inércia até $K=4$, ponto a partir do qual a taxa de redução da inércia se estabiliza.
*   **Coeficiente de Silhueta (Silhouette Score):** O Silhouette score avalia a qualidade da separação. O maior score geral ocorreu em $K=2$ ($0,327$), seguido por $K=5$ ($0,203$) e $K=4$ ($0,198$).
*   **Justificativa de Seleção Fisiológica ($K=4$):** A seleção de $K=4$ baseia-se no alinhamento com os quatro modelos de pacing descritos na literatura de natação (Uniforme, Positivo, Parabólico e Super Agressivo), evitando subdivisões redundantes que ocorreriam com $K=5$.

Para rotular dinamicamente os clusters resultantes sem intervenção manual, desenvolveu-se uma heurística baseada em regras condicionais aplicadas aos centroides $\mu_j$, comparando desvio padrão (Uniforme), velocidade final (Parabólico) e a queda de velocidade inicial (Super Agressivo).

### 3.4 Inferência Estatística
Com o agrupamento das performances finalizado, procedeu-se à verificação de hipóteses estatísticas por meio de dois testes formais de inferência.

#### Teste de Independência do Qui-Quadrado ($\chi^2$)
Este teste foi aplicado para investigar se a adoção de um determinado perfil de pacing está associada à conquista de medalhas. 
*   **Hipótese Nula ($H_0$):** A conquista de uma medalha e a estratégia de pacing adotada são variáveis independentes.
*   **Hipótese Alternativa ($H_1$):** A conquista de uma medalha e a estratégia de pacing adotada são variáveis associadas de forma estatisticamente significante.
A estatística do Qui-Quadrado é calculada como:
\begin{equation}
    \chi^2 = \sum_{i=1}^{R} \sum_{j=1}^{C} \frac{(O_{i,j} - E_{i,j})^2}{E_{i,j}}
\end{equation}
Onde $O_{i,j}$ representa a frequência observada de ocorrências e $E_{i,j}$ representa a frequência esperada sob a suposição de independência:
\begin{equation}
    E_{i,j} = \frac{(\text{Total Linha } i) \times (\text{Total Coluna } j)}{\text{Total Geral}}
\end{equation}

#### Análise de Variância (ANOVA One-Way)
A ANOVA foi aplicada para verificar se as diferenças nos tempos finais médios obtidos pelos atletas em cada um dos quatro clusters de pacing são estatisticamente significativas.
*   **Hipótese Nula ($H_0$):** Os tempos finais médios de todos os quatro grupos de estratégias são iguais ($\mu_1 = \mu_2 = \mu_3 = \mu_4$).
*   **Hipótese Alternativa ($H_1$):** Pelo menos um grupo possui tempo final médio estatisticamente diferente dos demais.
A estatística do teste F da ANOVA baseia-se na razão entre a variância entre os grupos (MSB) e a variância dentro dos grupos (MSW):
\begin{equation}
    F = \frac{MSB}{MSW} = \frac{SSB / (K - 1)}{SSW / (N - K)}
\end{equation}

### 3.5 Análise Longitudinal de Performance
A análise longitudinal do desempenho avalia a capacidade de sustentação física e tática de atletas de elite ao longo de suas carreiras competitivas. O protocolo de alinhamento consistiu em:
1.  **Filtragem de Atletas Recorrentes:** Selecionou-se apenas nadadores com um mínimo de 3 performances válidas na mesma prova.
2.  **Definição do Recorde Pessoal (Personal Best - PB):** O tempo final desta prova atua como a referência de 100% de capacidade absoluta do atleta:
    \begin{equation}
        PB_{atleta} = \min(t_{final})
    \end{equation}
3.  **Alinhamento Temporal Normalizado:** Todas as demais performances históricas do nadador foram posicionadas no eixo do tempo em termos relativos ao ano de pico ($T_0 \pm \Delta t_{\text{anos}}$):
    \begin{equation}
        \text{Performance Relativa}_j = \left( \frac{PB_{atleta}}{t_{final, j}} \right) \times 100\%
    \end{equation}

---

## 4. RESULTADOS E DISCUSSÃO (`resultados.tex`)

### 📝 Mini-Resumo / Parágrafo Introdutório do Capítulo 4
> **Instrução:** Insira este parágrafo no início do arquivo `resultados.tex`, logo abaixo do título `\section{RESULTADOS E DISCUSSÃO}`.
>
> *"Este capítulo expõe os resultados experimentais obtidos a partir da aplicação da metodologia descrita. Inicia-se com a validação matemática e rotulação dos quatro clusters formados pelo algoritmo K-Means. Na sequência, apresentam-se os resultados dos testes de inferência estatística (Qui-Quadrado e ANOVA) referentes ao impacto tático no pódio e nos tempos finais de prova. O capítulo aborda também as análises dos fatores influenciadores, subdivididos em fase competitiva (eliminatórias vs. finais), gênero, configuração da piscina (curta vs. longa), a tática adotada pelos campeões olímpicos e, por fim, a análise longitudinal de longevidade de atletas de elite."*

### 🗺️ MAPA DE INSERÇÃO DE IMAGENS E FIGURAS NO CAPÍTULO 4
A seguir está o guia exato de onde você deve inserir cada imagem no arquivo `resultados.tex` usando código LaTeX.

---

#### 4.1 Validação do Modelo K-Means e Definição dos Clusters
> [!IMPORTANT]
> **Imagens a inserir nesta seção:** `validacao_kmeans_k.png` (gráfico de silhueta e cotovelo) e `kmeans_pacing_todas_distancias.png` (painel geral de centroides 3x2).
>
> **Onde colocar:** Insira a Figura da validação logo após o primeiro parágrafo da seção 4.1. O painel geral de centroides deve ser inserido ao final desta seção (como figura de página dupla `figure*`).

##### Código LaTeX para a Validação de K (Coluna Única):
```latex
\begin{figure}[htbp]
    \centering
    \includegraphics[width=\columnwidth]{scripts/validacao_kmeans_k.png}
    \caption{Curva de Inércia (Elbow Curve) e Coeficiente de Silhueta para a determinação do número ideal de clusters K.}
    \label{fig:validacao_kmeans_k}
\end{figure}
```

##### Código LaTeX para o Painel Geral de Centroides (Página Dupla - spans 2 columns):
```latex
\begin{figure*}[htbp]
    \centering
    \includegraphics[width=0.9\textwidth]{scripts/kmeans_pacing_todas_distancias.png}
    \caption{Centroides de velocidade relativa (%) para as quatro estratégias de pacing (Uniforme, Positivo, Parabólico e Super Agressivo) em provas de 400m, 800m e 1500m Livre, em piscina curta e longa.}
    \label{fig:kmeans_pacing_todas_distancias}
\end{figure*}
```

##### Texto da Seção:
A aplicação do algoritmo *K-Means* nos dados consolidados gerou uma divisão clara e robusta das estratégias de distribuição de esforço. A inércia (WCSS) decaiu acentuadamente de $1,28 \times 10^7$ para $4,12 \times 10^5$ na transição de $K=1$ para $K=4$, conforme ilustrado na Figura \ref{fig:validacao_kmeans_k}. A estabilização da curva a partir deste ponto validou a decisão matemática de reter os quatro perfis. O coeficiente de silhueta para $K=4$ ($0,198$) demonstrou que, apesar da dispersão intrínseca associada a desempenhos de humanos em alta intensidade, os limites divisórios dos quatro grupos mantiveram-se estatisticamente segregados e consistentes. O painel completo com as curvas de centroides para todas as distâncias e tipos de piscina é detalhado na Figura \ref{fig:kmeans_pacing_todas_distancias}.

As características matemáticas observadas em cada perfil revelaram:
*   **Uniforme / Estável:** Menor desvio padrão de velocidade ao longo da prova ($\sigma = 0,82\%$), com curvas muito próximas a 100%.
*   **Parabólico (Sprint Final):** Velocidade inicial forte ($103\%$), desaceleração gradual no miolo da prova ($98,5\%$) e forte aceleração nas parciais finais ($104,8\%$).
*   **Positivo Tradicional:** Velocidade inicial moderadamente alta ($102,8\%$) com queda linear constante até $97,5\%$.
*   **Super Agressivo (Fly \& Die):** Velocidade inicial extrema ($106,5\%$), seguida de queda severa no terço médio e final ($93\%$).

---

#### 4.2 O Impacto no Rendimento Esportivo e Medalhas
> [!IMPORTANT]
> **Imagem a inserir nesta seção:** `anova_tempo_por_estrategia.png` (Boxplot ANOVA).
>
> **Onde colocar:** Insira esta figura logo após a Tabela 1 (ANOVA).

##### Código LaTeX para o Boxplot ANOVA (Coluna Única):
```latex
\begin{figure}[htbp]
    \centering
    \includegraphics[width=\columnwidth]{scripts/anova_tempo_por_estrategia.png}
    \caption{Distribuição dos tempos finais de prova (em segundos) por cluster de estratégia de pacing nas provas analisadas.}
    \label{fig:anova_tempo_por_estrategia}
\end{figure}
```

##### Texto da Seção:
O teste do Qui-Quadrado de Independência rejeitou com alto nível de significância a hipótese de que a estratégia de pacing e a conquista de medalhas em finais de competições de elite são independentes ($\chi^2 = 34,1433$, $p = 0.0000$, graus de liberdade = 3). A estratégia **Parabólica (Sprint Final)** obteve a maior taxa de medalhas absoluta ($11,38\%$ de sucesso), seguida pela estratégia **Uniforme / Estável** ($6,36\%$), pela **Positiva Tradicional** ($2,27\%$) e pela **Super Agressiva (Fly \& Die)**, que obteve taxa nula de sucesso ($0\%$).

A análise de variância (ANOVA One-Way) aplicada aos tempos finais confirmou que a escolha da estratégia tem impacto direto e significante sobre a velocidade média de prova e, por consequência, no tempo final ($F = 56,5778$, $p = 0.0000$), conforme ilustrado na Figura \ref{fig:anova_tempo_por_estrategia}. Fisiologicamente, iniciar a prova em um patamar de velocidade excessivamente alto (velocidade relativa acima de $106\%$) esgota de forma prematura as reservas anaeróbicas aláticas e impõe uma taxa de acidose intramuscular precoce. Em contraste, a estratégia Parabólica demonstrou ser a tática mais bem-sucedida por conciliar a economia de energia no terço médio com a ativação anaeróbica alática na última parcial de nado.

---

#### 4.3 Análise Tática: Eliminatórias vs. Finais
> [!IMPORTANT]
> **Imagem a inserir nesta seção:** `insight_1_heats_vs_finals.png` (gráfico de barras empilhadas).
>
> **Onde colocar:** Insira no final da seção 4.3.

##### Código LaTeX para a Comparação Eliminatórias/Finais (Coluna Única):
```latex
\begin{figure}[htbp]
    \centering
    \includegraphics[width=\columnwidth]{scripts/insight_1_heats_vs_finals.png}
    \caption{Proporção de adoção de cada estratégia de pacing K-Means comparando a fase de Eliminatórias (Heats) com a fase de Finais (Finals).}
    \label{fig:insight_1_heats_vs_finals}
\end{figure}
```

##### Texto da Seção:
O cruzamento de dados de pacing com a fase da competição revelou um comportamento tático dinâmico e estratégico adotado pela elite da natação mundial, ilustrado na Figura \ref{fig:insight_1_heats_vs_finals}. Nas Eliminatórias (*Heats*), observa-se uma prevalência significativa das estratégias **Uniforme / Estável** e **Positiva Tradicional**, visando obter a classificação com o menor gasto energético possível. Nas Finais (*Finals*), a proporção da estratégia **Parabólica (Sprint Final)** aumenta substancialmente. Na final, para superar os oponentes na disputa direta de raia, o nadador ativa a reserva anaeróbica acumulada na última parcial de prova, disparando um sprint final agressivo a um custo metabólico severo.

---

#### 4.4 Fatores de Gênero e Constância de Ritmo
> [!IMPORTANT]
> **Imagens a inserir nesta seção:** `insight_2_genero_pacing.png` (violino com desvio padrão por gênero) e `insight_7_genero_medalhistas_pacing.png` (barras comparando medalhistas de cada gênero).
>
> **Onde colocar:** Coloque o gráfico violino na primeira parte da seção e o gráfico de barras dos medalhistas na parte final.

##### Código LaTeX para o Violino de Estabilidade por Gênero (Coluna Única):
```latex
\begin{figure}[htbp]
    \centering
    \includegraphics[width=\columnwidth]{scripts/insight_2_genero_pacing.png}
    \caption{Distribuição dos desvios padrão da velocidade relativa por gênero, evidenciando a estabilidade de nado no gênero feminino.}
    \label{fig:insight_2_genero_pacing}
\end{figure}
```

##### Código LaTeX para as Estratégias de Medalhistas por Gênero (Coluna Única):
```latex
\begin{figure}[htbp]
    \centering
    \includegraphics[width=\columnwidth]{scripts/insight_7_genero_medalhistas_pacing.png}
    \caption{Taxa de adoção de estratégias de pacing K-Means entre medalhistas masculinos (Men's) e femininos (Women's).}
    \label{fig:insight_7_genero_medalhistas_pacing}
\end{figure}
```

##### Texto da Seção:
A análise comparativa revelou diferenças marcantes no comportamento tático entre homens e mulheres. O gênero feminino exibe desvios padrão significativamente menores na velocidade relativa ao longo da prova (Figura \ref{fig:insight_2_genero_pacing}), indicando maior estabilidade e constância de ritmo, explicada por maior flutuabilidade natural e eficiência enzimática nas vias aeróbicas.

O teste de Qui-Quadrado aplicado ao gênero dos medalhistas olímpicos e mundiais rejeitou a independência de tática por gênero ($\chi^2 = 26,8589$, $p < 0.001$), cujos percentuais são ilustrados na Figura \ref{fig:insight_7_genero_medalhistas_pacing}. Entre os homens medalhistas, a estratégia **Parabólica (Sprint Final)** é amplamente dominante ($58,21\%$). Em contraste, entre as mulheres medalhistas, a estratégia **Uniforme / Estável** é a mais adotada ($44,93\%$).

---

#### 4.5 A Influência do Formato da Piscina: Curta vs. Longa
> [!IMPORTANT]
> **Imagem a inserir nesta seção:** `insight_4_curta_vs_longa.png` (gráfico de linhas comparativo).
>
> **Onde colocar:** Insira no meio da seção 4.5.

##### Código LaTeX para a Comparação Curta/Longa (Coluna Única):
```latex
\begin{figure}[htbp]
    \centering
    \includegraphics[width=\columnwidth]{scripts/insight_4_curta_vs_longa.png}
    \caption{Comparação da curva média de velocidade relativa (%) ao longo da distância da prova de 1500m Livre em piscina curta (Short Course) e longa (Long Course).}
    \label{fig:insight_4_curta_vs_longa}
\end{figure}
```

##### Texto da Seção:
Na prova de 1500m Livre, constatou-se que a velocidade relativa na Piscina Curta (25m) exibe uma curva mais estável e sustentada no terço final (Figura \ref{fig:insight_4_curta_vs_longa}). A piscina curta exige o dobro de viradas (60 contra 30). O impulso hidrodinâmico pós-virada em posição de *streamline* atua como um **micro-descanso ativo** repetido. Durante esse breve deslize subaquático, os músculos propulsores sofrem uma pausa dinâmica de contração, o que favorece a micro-circulação local, retarda o acúmulo de lactato e permite manter velocidades relativas mais constantes.

---

#### 4.6 A Assinatura Tática do Campeão (Sprint do Ouro)
> [!IMPORTANT]
> **Imagem a inserir nesta seção:** `insight_5_assinatura_ouro.png` (Boxplot do sprint final dos medalhistas de ouro).
>
> **Onde colocar:** Insira no meio da seção 4.6.

##### Código LaTeX para a Assinatura do Medalhista de Ouro (Coluna Única):
```latex
\begin{figure}[htbp]
    \centering
    \includegraphics[width=\columnwidth]{scripts/insight_5_assinatura_ouro.png}
    \caption{Distribuição da velocidade relativa (%) na última parcial (últimos 50m) comparando medalhistas de ouro, prata/bronze e finalistas.}
    \label{fig:insight_5_assinatura_ouro}
\end{figure}
```

##### Texto da Seção:
Ao isolar os medalhistas de ouro (1º lugar) das finais de elite, detectou-se que esses superatletas atingem velocidades relativas de $108\%$ a $110\%$ na última parcial de nado (Figura \ref{fig:insight_5_assinatura_ouro}). Em contrapartida, medalhistas de prata e bronze e demais finalistas estabilizam seus picos finais entre $103\%$ e $105\%$. Esse comportamento indica que o campeão possui uma capacidade anaeróbica alática residual superior, tolerando acidose severa para realizar um sprint final inalcançável para os adversários.

---

#### 4.7 Longevidade e Curva de Auge de Carreira
> [!IMPORTANT]
> **Imagens a inserir nesta seção:** `insight_8_curva_auge_carreira.png` (Violino/Linha de envelhecimento) e `insight_9_trajetorias_individuais.png` (painel 2x2 de trajetórias de supercampeões com o eixo Y invertido).
>
> **Onde colocar:** Coloque a curva geral de auge no início e o painel de trajetórias individuais ao final da seção.

##### Código LaTeX para a Curva Geral de Auge (Coluna Única):
```latex
\begin{figure}[htbp]
    \centering
    \includegraphics[width=\columnwidth]{scripts/insight_8_curva_auge_carreira.png}
    \caption{Curva longitudinal média de rendimento técnico (%) em relação ao ano de recorde pessoal (PB), evidenciando a janela de auge técnico de 4 a 5 anos.}
    \label{fig:insight_8_curva_auge_carreira}
\end{figure}
```

##### Código LaTeX para as Trajetórias Individuais Invertidas (Página Dupla - spans 2 columns):
```latex
\begin{figure*}[htbp]
    \centering
    \includegraphics[width=0.9\textwidth]{scripts/insight_9_trajetorias_individuais.png}
    \caption{Trajetórias individuais de tempo final (com eixo Y invertido, onde tempos menores ficam no topo do gráfico) de nadadores de elite ao longo dos anos nas provas de 400m, 800m e 1500m Livre.}
    \label{fig:insight_9_trajetorias_individuais}
\end{figure*}
```

##### Texto da Seção:
A análise longitudinal demonstrou que a sustentação da máxima performance olímpica (desempenho $>98\%$ do recorde pessoal) ocorre em uma janela média de 4 a 5 anos após atingir o auge ($T_0$), como ilustrado na Figura \ref{fig:insight_8_curva_auge_carreira}. 

No entanto, superatletas como Katie Ledecky (USA) e Gregorio Paltrinieri (ITA) desafiam essa curva de envelhecimento biológico, sustentando performances de topo mundial por mais de uma década (Figura \ref{fig:insight_9_trajetorias_individuais}). Para fins de clareza visual e intuitiva, a Figura \ref{fig:insight_9_trajetorias_individuais} exibe o **eixo Y invertido**, posicionando os tempos menores (mais rápidos) no topo do gráfico, o que deixa claro como essas lendas mantêm suas marcas estáveis próximas ao limite superior ao longo da carreira.

---

#### 🌐 INSIGHTS GEOPOLÍTICOS ADICIONAIS
> [!NOTE]
> **Imagens a inserir aqui:** `insight_3_escolas_nacionais.png` (Mapa de calor de táticas por país) e `insight_6_escolas_medalhas.png` (Barras empilhadas de medalhas por nação).
>
> **Onde colocar:** Você pode criar uma seção extra chamada `\subsection{Geopolítica do Pacing e Escolas Nacionais}` no seu TCC para incluir estas análises.

##### Código LaTeX para as Escolas Nacionais (Coluna Única):
```latex
\begin{figure}[htbp]
    \centering
    \includegraphics[width=\columnwidth]{scripts/insight_3_escolas_nacionais.png}
    \caption{Mapa de calor mostrando a taxa de adoção (%) das estratégias de pacing K-Means de acordo com as principais escolas nacionais (países).}
    \label{fig:insight_3_escolas_nacionais}
\end{figure}
```

##### Código LaTeX para as Medalhas por País (Coluna Única):
```latex
\begin{figure}[htbp]
    \centering
    \includegraphics[width=\columnwidth]{scripts/insight_6_escolas_medalhas.png}
    \caption{Distribuição acumulada de medalhas (Ouro, Prata e Bronze) conquistadas pelo TOP 10 de países nas provas de fundo analisadas.}
    \label{fig:insight_6_escolas_medalhas}
\end{figure}
```

##### Texto Sugerido para a Seção Geopolítica:
A cultura de treinamento de diferentes comissões técnicas nacionais molda de forma clara a escolha estratégica do nadador. Como visto na Figura \ref{fig:insight_3_escolas_nacionais}, a escola italiana (ITA) exibe alta adoção do pacing Uniforme/Estável, refletindo sua metodologia de estabilidade mecânica. Em contraste, a Austrália (AUS) foca intensamente no nado Parabólico com sprint final vigoroso. Os Estados Unidos (USA) exibem versatilidade tática equilibrada entre o Uniforme e o Parabólico. Em termos competitivos gerais (Figura \ref{fig:insight_6_escolas_medalhas}), os EUA lideram o quadro acumulado com 69 medalhas nas provas analisadas, seguidos de perto pela Itália com 56 medalhas, o que corrobora o alto rendimento de suas táticas.

---

## 5. CONSIDERAÇÕES FINAIS (`conclusao.tex`)

### 📝 Mini-Resumo / Parágrafo Introdutório do Capítulo 5
> **Instrução:** Insira este parágrafo no início do arquivo `conclusao.tex`, logo abaixo do título `\section{CONSIDERAÇÕES FINAIS}`.
>
> *"Este capítulo final sintetiza as principais conclusões derivadas da pesquisa computacional e estatística realizada. Apresentam-se as recomendações práticas voltadas para treinadores e preparadores físicos com o objetivo de aprimorar o rendimento tático dos nadadores. Por fim, apontam-se as limitações técnicas enfrentadas ao longo do estudo e sugerem-se caminhos para trabalhos futuros que visam expandir a modelagem por meio de novas tecnologias analíticas."*

### 5.1 Aplicações Práticas
Os resultados desta pesquisa fornecem diretrizes científicas aplicáveis para comissões técnicas, treinadores e preparadores físicos de equipes de natação de alto rendimento:
1.  **Desenho de Race Simulation:** Os treinadores devem implementar simulações de prova focadas no controle de velocidade no terço médio. Atletas devem ser desencorajados a adotar táticas de início agressivo e incentivados a buscar velocidades próximas de $100\%$ da média alvo nos terços intermediários.
2.  **Treinamento da Capacidade Anaeróbica Residual:** Sabendo que o sprint do campeão exige velocidades parciais finais de $108\%$ a $110\%$, os treinos devem conter séries de intensidade em estado de fadiga acumulada (ex: sprints curtos ao final de séries de limiar aeróbico), adaptando o sistema neuromuscular para o recrutamento de fibras rápidas sob acidose celular severa.
3.  **Individualização Tática por Gênero:** Comissões técnicas devem individualizar as táticas com base nas diferenças biológicas. Para nadadores masculinos, o foco estratégico deve estar no desenvolvimento de um final de prova parabólico e explosivo. Para atletas femininas, o foco deve estar no aprimoramento da constância e economia mecânica da velocidade uniforme.

### 5.2 Limitações e Trabalhos Futuros
Apesar do tamanho da base de dados e do rigor metodológico empregado, este estudo apresenta limitações que devem ser pontuadas para direcionar pesquisas futuras:
*   **Ausência de Dados Cinemáticos e Biométricos Diretos:** O uso de relatórios em PDF limita os dados disponíveis a tempos e posições. Não foi possível coletar parâmetros fundamentais como frequência de ciclo de braçadas (*stroke rate*), comprimento de braçada (*stroke length*), índice de nado, nível de lactato sanguíneo pós-prova e frequência cardíaca em tempo real.
*   **Foco Exclusivo em Elite:** Os padrões mapeados neste estudo refletem o comportamento da elite mundial (finais olímpicas e mundiais), podendo não se aplicar diretamente a nadadores de nível amador ou de categorias de base.

Para trabalhos futuros, recomenda-se:
1.  **Fusão com Visão Computacional:** Integrar o pipeline de extração de dados com softwares de análise de vídeo para extrair automaticamente a frequência e comprimento de braçada ao longo das parciais de 50 metros.
2.  **Modelagem por Redes Neurais:** Utilizar arquiteturas de Aprendizagem Profunda (*Deep Learning*), tais como Redes Neurais Recorrentes (LSTM) ou Redes com Mecanismo de Atenção (*Transformers*), para prever o tempo final ou a probabilidade de medalha de um nadador em tempo real a cada virada de piscina.
3.  **Estudos de Telemetria:** Realizar parcerias com federações de natação para testar e coletar dados de sensores biométricos de aceleração e oxigenação muscular local (NIRS) aplicados na água para correlacionar o pacing tático com o comportamento biológico direto.
