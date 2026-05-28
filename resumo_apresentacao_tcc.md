# Guia de Slides: Análise de Dados e Insights de Pacing (TCC Natação)

> **Instruções para o Gemini (ou outro LLM gerador de slides):**
> Você receberá este texto estruturado junto com os gráficos em formato PNG correspondentes aos scripts. Monte os slides focando nas **perguntas científicas (indagações)**, nas respostas extraídas dos dados e nas justificativas biomecânicas. Use os nomes das imagens indicadas abaixo para vincular o texto ao slide correto.

---

## Slide 1: Introdução ao Problema
* **Indagação Central:** Como os atletas de elite mundial de natação gerenciam a sua velocidade ao longo de provas de longa distância (400m, 800m e 1500m Livre) para maximizar o rendimento?
* **O Desafio dos Dados:** Tradicionalmente, as parciais são analisadas apenas em tempo absoluto. Para comparar atletas de níveis diferentes de forma puramente estratégica, normalizamos todas as parciais usando a **Velocidade Relativa (%)** em relação à média global de cada nadador na prova.
* **O Dataset:** Dados 100% reais de **3.923 performances** e mais de 100.000 parciais extraídos via Python dos relatórios oficiais da Omega Timing (Olimpíadas, Mundiais e Europeus de 2012 a 2025).

---

## Slide 2: Validação Matemática da Estruturação dos Dados
* **Imagem de Referência:** `validacao_kmeans_k.png`
* **Indagação Científica:** Como provar matematicamente que o comportamento estratégico dos atletas de elite se agrupa em exatamente 4 perfis distintos, sem depender de palpites ou viés humano?
* **O que o gráfico mostra:**
  * **Método do Cotovelo (Elbow Curve):** Queda acentuada da inércia que se estabiliza a partir de $K=4$ clusters.
  * **Coeficiente de Silhueta (Silhouette Score):** Pico local indicando que a coesão interna e separação dos grupos é maximizada com $K=4$ em um tensor demonstrativo de 1.234 atletas por 8 parciais.
* **Conclusão:** Os nadadores de elite não nadam de forma aleatória; eles adotam 4 assinaturas táticas claras: *Uniforme/Estável*, *Parabólico (Sprint Final)*, *Super Agressivo (Fly & Die)* e *Positivo Tradicional*.

---

## Slide 3: Pacing vs. Medalhas (Qui-Quadrado)
* **Indagação Científica:** A estratégia de distribuição de energia adotada pelo nadador determina se ele subirá ao pódio ou se ele está fadado a perder nas Finais de elite?
* **Análise Estatística:** Teste de Independência do Qui-Quadrado ($\chi^2$) aplicado a 2.042 finalistas de 400m Livre (Longa).
  * **Hipótese Nula ($H_0$):** Conquistar uma medalha é independente do perfil de pacing adotado.
* **Os Resultados dos Dados:**
  * **Parabólico (Sprint Final):** 90 medalhistas de 736 performances (**12,2% de sucesso**)
  * **Uniforme / Estável:** 42 medalhistas de 624 performances (**6,7% de sucesso**)
  * **Positivo Tradicional:** 17 medalhistas de 583 performances (**2,9% de sucesso**)
  * **Super Agressivo (Fly & Die):** 0 medalhistas de 99 performances (**0% de sucesso**)
* **Decisão Estatística:** $\chi^2 = 51,0898$ | **p-valor = 0.0000** ($p < 0.05$)
* **Conclusão:** Rejeita-se $H_0$. O pacing determina diretamente a probabilidade de pódio. O nado Parabólico e o Uniforme são os mais bem-sucedidos. A estratégia Super Agressiva na final resulta em colapso muscular precoce e aproveitamento nulo de pódios.

---

## Slide 4: O Risco das Táticas (ANOVA de Tempos Finais)
* **Imagem de Referência:** `anova_tempo_por_estrategia.png`
* **Indagação Científica:** Se a tática "Super Agressiva (Fly & Die)" tem 0% de aproveitamento em medalhas nas finais, por que ela apresenta os tempos médios finais mais baixos e rápidos nas estatísticas gerais?
* **O que o gráfico boxplot mostra:**
  * Distribuição dos tempos finais de prova em segundos para as 4 estratégias.
  * Média de tempo do cluster *Super Agressivo*: 337,93s ($N=99$)
  * Média de tempo do cluster *Parabólico*: 427,53s ($N=736$)
* **Decisão Estatística:** $F = 11,4741$ | **p-valor = 0.0000** (Diferença de médias altamente significante)
* **Resposta Biomecânica:** A tática *Super Agressiva* é de altíssimo risco e alto custo energético. Ela só é sustentada e adotada por nadadores com capacidades físicas excepcionais em eliminatórias muito rápidas. No entanto, sob a pressão de uma final competitiva, os atletas que controlam a energia (*Parabólico* e *Uniforme*) levam a melhor sobre aqueles que tentam "vencer a prova no início".

---

## Slide 5: Insight 1 - Eliminatórias vs. Finais (Heats vs. Finals)
* **Imagem de Referência:** `insight_1_heats_vs_finals.png`
* **Indagação Científica:** Os nadadores de elite se comportam de forma diferente dependendo da fase da competição, ou seja, eles "escondem o jogo" nas eliminatórias para poupar energia?
* **O que o gráfico de barras empilhadas mostra:**
  * **Nas Eliminatórias (Heats):** Adoção maciça de estratégias controladas e lineares (*Uniforme* e *Positivo*) para garantir a classificação com o menor desgaste físico possível.
  * **Nas Finais (Finals):** Há uma migração tática evidente. A proporção do cluster **Parabólico (Sprint Final)** dispara.
* **Conclusão:** Existe uma adaptação tática consciente baseada na fase. Nas eliminatórias, o objetivo é a eficiência energética; nas finais, o objetivo é a vitória a qualquer custo, ativando o sprint final.

---

## Slide 6: Insight 2 - Assinatura de Gênero (Constância de Ritmo)
* **Imagem de Referência:** `insight_2_genero_pacing.png`
* **Indagação Científica:** Nadadores homens e mulheres gerenciam o ritmo de prova da mesma forma? Quem é mais constante e estável sob a fadiga em provas de fundo?
* **O que o gráfico violino mostra:**
  * O desvio padrão da velocidade relativa por nadador (indica o nível de oscilação do ritmo).
  * O gênero **Feminino (Women's)** concentra-se em desvios padrão significativamente menores.
* **Explicação Biomecânica e Fisiológica:**
  * As mulheres exibem **maior estabilidade de nado**.
  * Fatores fisiológicos como um limiar aeróbico mais estável e melhor eficiência hidrodinâmica natural (flutuação e distribuição de gordura corporal periférica) contribuem para que o nado feminino sofra menos acelerações e desacelerações bruscas em relação ao masculino.

---

## Slide 7: Insight 3 - Escolas Nacionais (Geopolítica do Pacing)
* **Imagem de Referência:** `insight_3_escolas_nacionais.png`
* **Indagação Científica:** Existe uma "cultura tática regional" na natação? Como os métodos de treinamento das grandes potências (EUA, Austrália, Itália...) moldam a escolha do pacing?
* **O que o mapa de calor mostra:**
  * A taxa de adoção percentual das 4 estratégias de pacing para nadadores de diferentes países.
* **Os Padrões Culturais Revelados:**
  * **Itália (ITA):** Foco extremo no pacing *Uniforme/Estável*. Reflete a escola italiana de longa distância clássica (escola técnica de Paltrinieri).
  * **Austrália (AUS):** Alta taxa de adoção do nado *Parabólico*, visando um encerramento de prova explosivo.
  * **Estados Unidos (USA):** Perfil equilibrado entre o *Uniforme* e o *Parabólico*, revelando atletas taticamente versáteis e adaptáveis.

---

## Slide 8: Insight 4 - O Impacto das Viradas (Curta vs. Longa)
* **Imagem de Referência:** `insight_4_curta_vs_longa.png`
* **Indagação Científica:** Como o número de viradas na Piscina Curta (25m) altera a taxa de fadiga de um atleta ao longo de uma prova exaustiva como os 1500m Livre?
* **O que o gráfico de linha mostra:**
  * Comparação da curva média de velocidade relativa (%) ao longo do progresso da prova.
  * A curva da **Piscina Curta (Short Course)** é muito mais plana e preserva velocidades mais altas no terço final da prova em comparação com a **Piscina Longa (Long Course)**.
* **Explicação Física/Biomecânica:**
  * Nos 1500m em piscina curta, o nadador realiza **60 viradas** (o dobro da piscina longa).
  * Cada impulso na parede seguido pelo deslize subaquático em *streamline* funciona como um **micro-descanso ativo**.
  * Esse intervalo dinâmico poupa a musculatura propulsiva superior (braços), retarda o acúmulo de lactato e diminui a perda de velocidade relativa.

---

## Slide 9: Insight 5 - O Segredo do Ouro (O Sprint do Campeão)
* **Imagem de Referência:** `insight_5_assinatura_ouro.png`
* **Indagação Científica:** O que separa o nadador que ganha o Ouro (1º) do restante do pódio e dos outros finalistas no momento de decisão da prova?
* **O que o gráfico boxplot mostra:**
  * A velocidade relativa (%) alcançada na última parcial (últimos 50m) em finais de elite.
  * O medalhista de **Ouro (1º)** apresenta uma aceleração final estatisticamente superior, alcançando picos entre **108% e 110%** da sua velocidade média global.
  * Medalhistas de Prata/Bronze e finalistas estabilizam entre 103% e 105%.
* **Explicação Tática:** O campeão olímpico/mundial possui uma **capacidade anaeróbica residual superior**. Ele consegue suportar a acidose muscular nos últimos metros e liberar uma reserva de emergência fisiológica para disparar um sprint final que os adversários não conseguem acompanhar.
