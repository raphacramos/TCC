# Prompt de Entrada para Geração de Slides (TCC - Análise de Pacing na Natação)

> **Instruções para o Gemini (ou outro LLM gerador de slides):**
> Use o conteúdo estruturado abaixo para criar uma apresentação de slides profissional, acadêmica e visualmente atraente sobre o Trabalho de Conclusão de Curso (TCC). Estruture a apresentação em 13 slides, mantendo a clareza dos dados estatísticos, das fórmulas e dos insights biomecânicos apresentados.

---

## Slide 1: Título e Identificação
* **Título Principal:** Inteligência de Dados no Esporte: Análise de Pacing na Natação de Elite usando Machine Learning e Inferência Estatística
* **Subtítulo:** Identificação de Perfis Estratégicos nas Provas de Médio e Longo Fundo (400m, 800m e 1500m Livre) a partir de Dados Oficiais da Omega Timing
* **Contexto:** Trabalho de Conclusão de Curso (TCC) em Ciência da Computação / Engenharia de Dados Esportivos.

---

## Slide 2: Introdução e Contexto Biomecânico
* **O que é Pacing Strategy?** É a distribuição da energia e velocidade de um atleta ao longo de uma prova de resistência. É um fator crítico que separa vencedores de finalistas.
* **Problema:** Tradicionalmente, análises de pacing dependem de observação manual ou datasets pequenos. Falta uma abordagem escalável e estatisticamente validada sobre grandes volumes de dados de elite.
* **Escopo do Trabalho:** Foco nas provas de fundo e meio-fundo da natação: **400m, 800m e 1500m Livre**, tanto em Piscina Longa (50m) quanto em Piscina Curta (25m), abrangendo Olimpíadas, Mundiais e Europeus de 2012 a 2025.

---

## Slide 3: O Pipeline de Engenharia de Dados (ETL)
* **Extração (Extract):** Script em Python com a biblioteca `pdfplumber` realizando o parsing automático de 32 PDFs de relatórios oficiais da Omega Timing (Livros de Resultados completos, contendo milhares de páginas).
* **Transformação (Transform):** 
  * Desenvolvimento de uma **Máquina de Estados (State Machine)** e expressões regulares (`RegEx`) para capturar dinamicamente os nomes dos nadadores, nacionalidades, parciais (splits de 50m ou 25m) e tempos finais.
  * Padronização de dados inconsistentes (ex: correção de nomes com pontuação como initials e correção dinâmica de nomes de campeonatos duplicados por subpastas).
  * Conversão de formato *Wide* (uma coluna por split) para *Long/Tidy Format* via `pandas`.
* **Carga (Load):** Persistência no CSV mestre (`dataset_pacing_completo.csv`) contendo mais de **3.740 performances individuais de elite mundial**.

---

## Slide 4: Engenharia de Features e Fórmulas Analíticas
Para comparar nadadores de diferentes tempos absolutos, criamos métricas relativas normalizadas baseadas na literatura de ciências do esporte (Abbiss & Laursen, 2008):
1. **Velocidade do Trecho ($V_i$):**
   $$V_i = \frac{D_{trecho}}{T_{parcial}}$$
2. **Velocidade Média Global ($V_{media}$):**
   $$V_{media} = \frac{D_{total}}{T_{final}}$$
3. **Velocidade Relativa Normalizada ($V_{relativa}$):** (Indica o percentual da velocidade média da prova adotado em cada trecho)
   $$V_{relativa} = \left( \frac{V_i}{V_{media}} \right) \times 100$$
4. **Percentual de Alocação de Tempo ($Pct_{tempo}$):** (Quanto do tempo total da prova foi gasto naquele trecho específico)
   $$Pct_{tempo} = \left( \frac{T_{parcial}}{T_{final}} \right) \times 100$$

---

## Slide 5: Modelagem de Machine Learning (K-Means Clustering)
* **Abordagem:** Treinamento independente de modelos **K-Means** por distância (400m/800m/1500m) e por tipo de piscina (Curta/Longa) para evitar a armadilha de dimensionalidade (diferentes quantidades de parciais).
* **Justificativa do Hiperparâmetro $K=4$:**
  * **Validação Matemática:** Curva do Cotovelo (Elbow Curve) mostrando clara inflexão da inércia e pico/estabilização do Coeficiente de Silhueta (Silhouette Score) testado de $K=2$ a $K=10$ para o tensor de parciais (Shape do tensor demonstrativo: 1.234 atletas × 8 features para 400m Long Course).
  * **Resultados dos 4 Perfis de Pacing Identificados:**
    1. **Parabólico (Sprint Final):** Início controlado, ritmo estável no meio e forte aceleração nos últimos 50m.
    2. **Uniforme / Estável:** Ritmo altamente constante do início ao fim (menor variabilidade interna).
    3. **Super Agressivo (Fly & Die):** Passagem muito rápida nos primeiros 50m/100m com forte queda de rendimento no terço final.
    4. **Positivo Tradicional:** Perda linear e gradual de velocidade após o primeiro trecho de aceleração inicial.

---

## Slide 6: Validação Estatística I - Qui-Quadrado (Pacing vs. Medalhas)
* **Pergunta Científica:** A escolha da estratégia de pacing (Cluster) afeta a probabilidade de ganhar uma medalha (Top 3)?
* **Método:** Teste de Independência do Qui-Quadrado ($\chi^2$) aplicado às finais de 400m Livre (Longa).
  * **Hipótese Nula ($H_0$):** A conquista de medalha é independente da estratégia de pacing adotada.
* **Tabela de Contingência Observada ($N = 2.042$ performances finalistas):**
  * *Parabólico (Sprint Final):* 646 não-medalhistas | 90 medalhistas (**Taxa de Sucesso: 12,2%**)
  * *Uniforme / Estável:* 582 não-medalhistas | 42 medalhistas (**Taxa de Sucesso: 6,7%**)
  * *Positivo Tradicional:* 566 não-medalhistas | 17 medalhistas (**Taxa de Sucesso: 2,9%**)
  * *Super Agressivo (Fly & Die):* 99 não-medalhistas | 0 medalhistas (**Taxa de Sucesso: 0,0%**)
* **Resultado:** $\chi^2 = 51,0898$ | **p-valor = 0.0000** ($p < 0.05$)
* **Conclusão:** Rejeita-se $H_0$. Há associação estatística altamente significativa. O nado *Parabólico* e o *Uniforme* são as estratégias mais seguras e vitoriosas. A tática *Super Agressiva (Fly & Die)* possui 0% de aproveitamento em pódios.

---

## Slide 7: Validação Estatística II - ANOVA (Tempos Finais vs. Estratégias)
* **Pergunta Científica:** O tempo final médio da prova difere significativamente de acordo com a estratégia adotada?
* **Método:** ANOVA One-Way (Análise de Variância) para os tempos finais em segundos.
  * **Hipótese Nula ($H_0$):** Os tempos médios das 4 estratégias são idênticos.
* **Resultados das Médias de Tempo por Cluster (400m Livre):**
  * *Super Agressivo (Fly & Die):* 337.93 segundos ($N=99$)
  * *Positivo Tradicional:* 370.10 segundos ($N=583$)
  * *Parabólico (Sprint Final):* 427.53 segundos ($N=736$)
  * *Uniforme / Estável:* 435.81 segundos ($N=624$)
* **Métrica F-Value:** 11.4741 | **p-valor = 0.0000** ($p < 0.05$)
* **Conclusão:** Rejeita-se $H_0$. Há diferença estatística muito significativa entre os grupos. 
  *(Nota Biomecânica: A média inferior do Super Agressivo reflete que esta tática de alto risco é adotada principalmente por nadadores de altíssimo nível em eliminatórias rápidas, porém é a menos provável de conquistar pódios na final, onde o controle de energia prevalece).*

---

## Slide 8: Insight 1 - O Fator Eliminatória (Heats vs. Finals)
* **Análise:** Comparação das táticas adotadas nas Eliminatórias (Heats) vs. Finais (Final).
* **Descoberta:** Nadadores de ponta adotam uma postura conservadora ("escondem o jogo") nas eliminatórias. Eles usam predominantemente estratégias **Uniforme / Estável** e **Positivo** para garantir classificação com menor desgaste fisiológico.
* **Nas Finais:** Ocorre uma transição nítida para a estratégia **Parabólica (Sprint Final)**. Os atletas aumentam drasticamente a intensidade do ritmo e utilizam o sprint final de forma explosiva nos últimos 50 metros para decidir a colocação.

---

## Slide 9: Insight 2 - Assinatura de Gênero (Masculino vs. Feminino)
* **Análise:** Variabilidade de velocidade (desvio padrão das parciais) por gênero em provas de fundo.
* **Descoberta:** O gênero feminino apresenta um desvio padrão da velocidade significativamente menor que o masculino nas provas de 800m e 1500m Livre.
* **Explicação Fisiológica/Biomecânica:** 
  * As mulheres exibem maior **estabilidade e constância no pacing**.
  * Fatores relacionados a um limiar aeróbico mais estável e melhor economia de nado na flutuação e eficiência hidrodinâmica ajudam o gênero feminino a evitar oscilações bruscas de velocidade ao longo das parciais da prova, em comparação com a propulsão mais intermitente e dependente de força anaeróbica dos homens.

---

## Slide 10: Insight 3 - Escolas Nacionais de Natação (Análise Geopolítica)
* **Análise:** Mapa de calor cruzando a nacionalidade (TOP 5 países) com a adoção das táticas.
* **Descoberta:** Identificamos assinaturas táticas culturais de treinamento:
  * **Estados Unidos (USA):** Apresentam forte equilíbrio entre a estratégia Parabólica e a Uniforme, mostrando nadadores taticamente completos.
  * **Austrália (AUS):** Escola tradicional com maior concentração histórica no nado Parabólico, focando em um final de prova devastador.
  * **Itália (ITA):** Escola muito técnica, focada no nado Uniforme/Estável em provas longas (escola de Gregorio Paltrinieri).
  * **China (CHN):** Distribuição equilibrada, com nadadores muito fortes em estratégias de transição rápida (sprints).

---

## Slide 11: Insight 4 - O Fator Piscina Curta (25m) vs. Longa (50m)
* **Análise:** Comparação das curvas médias de velocidade relativa normalizada (Decay Rate/Fadiga) ao longo da prova de 1500m Livre.
* **Descoberta:** Nadadores de Piscina Curta (25m) conseguem manter uma velocidade relativa significativamente maior no terço médio e final da prova, apresentando uma **taxa de fadiga menor** (curva mais plana).
* **Explicação Física/Biomecânica:**
  * Na piscina curta de 1500m, o nadador realiza **60 viradas** (contra 30 na piscina longa).
  * Cada virada e deslize subaquático subsequente (filamento hidrodinâmico em posição *streamline*) funciona como um **micro-descanso ativo**.
  * A impulsão na parede e o nado ondulatório subaquático poupam a musculatura da braçada (propulsão superior), reduzindo o acúmulo de lactato e retardando a fadiga periférica.

---

## Slide 12: Insight 5 - O Segredo do Ouro (O Sprint dos Campeões)
* **Análise:** Velocidade relativa normalizada isolada nos últimos 50 metros da final entre o Campeão (Ouro / 1º), o Pódio (2º e 3º) e os demais Finalistas (4º ao 8º).
* **Descoberta:** O nadador que ganha o **Ouro (1º)** possui uma aceleração final estatisticamente isolada em relação a todos os concorrentes. 
* **Explicação Tática:** Enquanto os atletas do pódio e finalistas aceleram para velocidades em torno de 103% a 105% de suas médias nos últimos 50m, o medalhista de ouro atinge picos de **108% a 110%**.
* **Implicação:** O campeão olímpico/mundial não se destaca apenas por nadar mais rápido ao longo da prova inteira, mas sim pela sua impressionante capacidade anaeróbica residual (reserva de emergência de glicogênio) para disparar um sprint insustentável para os adversários nos metros decisivos da prova.

---

## Slide 13: Conclusão, Contribuições e Próximos Passos
* **Conclusões:** Perfis de pacing não são aleatórios; são agrupados matematicamente em 4 assinaturas distintas. A tática Parabólica e a Uniforme são estatisticamente associadas à obtenção de medalhas. Fatores como gênero, país, piscina e fase da competição moldam diretamente essas táticas.
* **Contribuições do TCC:**
  * Pipeline ETL robusto capaz de extrair dados de relatórios complexos em PDF da Omega.
  * Dataset inédito consolidado com mais de 3.900 performances e 100.000 splits de natação de elite.
  * Validação matemática e estatística completa para dar sustentação científica às conclusões biomecânicas.
* **Próximos Passos (Trabalhos Futuros):**
  * Desenvolvimento de um **Dashboard Web interativo em Streamlit** para que treinadores possam fazer o upload de PDFs da Omega e visualizar em tempo real a classificação do atleta e suas curvas de pacing.
  * Implementação de redes neurais recorrentes (LSTM) para predizer o tempo final do nadador a partir das parciais dos primeiros 100m.
