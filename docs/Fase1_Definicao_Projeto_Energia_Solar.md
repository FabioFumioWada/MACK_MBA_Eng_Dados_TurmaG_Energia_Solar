# Fase 1: Definição do Projeto
## Tema: Impacto da Geração Distribuída Solar na Tarifa de Energia Elétrica (Conta de Luz) no Brasil

**Disciplina:** Hands-On Fundamentos de Dados e Analytics: MBA em Engenharia de Dados (Mackenzie)
**Data:** 15/08/2026

---

## 1. Definição do problema e escolha do caso de uso

### 1.1 Contexto (por que o tema é atual)

- O Brasil ultrapassou **4 milhões de sistemas fotovoltaicos** em operação na geração distribuída (GD), somando **44,6 GW** de potência instalada e beneficiando mais de **7,1 milhões de unidades consumidoras**, marca atingida em 2026 ([Canal Solar](https://canalsolar.com.br/brasil-quatro-milhoes-sistemas-energia-solar/), [PV Magazine Brasil](https://www.pv-magazine-brasil.com/2026/02/27/geracao-distribuida-ultrapassa-4-milhoes-de-sistemas-no-brasil/)).
- Só no 1º trimestre de 2026 foram conectados **2.177 MW** em GD solar, com uma média de **8,8 mil novos sistemas por dia** ([PV Magazine Brasil](https://www.pv-magazine-brasil.com/2026/05/14/brasil-adiciona-44-gw-de-capacidade-solar-no-primeiro-trimestre/)).
- Esse crescimento acelera o debate sobre quem paga a manutenção da rede elétrica (o chamado "Fio B", regulado pela Lei 14.300) à medida que mais consumidores geram sua própria energia e reduzem o consumo faturado pelas distribuidoras, um problema real de sustentabilidade financeira do setor.
- Paralelamente, o valor da conta de luz de quem **não** tem painel solar depende do acionamento mensal das **bandeiras tarifárias**, definido pelas condições hidrológicas do Sistema Interligado Nacional (SIN) ([ANEEL Dados Abertos](https://dadosabertos.aneel.gov.br/dataset/bandeiras-tarifarias)).

### 1.2 Problema de negócio

Distribuidoras, reguladores e o próprio consumidor final têm dificuldade em antecipar como a expansão acelerada da geração distribuída solar e as condições hidrológicas do país vão pressionar o valor da tarifa de energia (conta de luz) nos próximos meses/anos, hoje essa leitura é fragmentada entre diferentes fontes e não é combinada de forma sistemática.

### 1.3 Impacto para o negócio

A distorção tarifária afeta diretamente o caixa das distribuidoras (que perdem receita de consumidores com GD, mas mantêm o custo fixo da rede) e o bolso dos consumidores sem geração própria, que absorvem parte do custo via bandeiras tarifárias e realocação de tarifas. Sem visibilidade preditiva, decisões de política tarifária e de investimento em energia solar são tomadas de forma reativa.

### 1.4 Objetivo geral

Construir um pipeline de dados e um modelo preditivo que relacione a evolução da geração distribuída solar, as condições hidrológicas e a estrutura tarifária das distribuidoras, permitindo antecipar o comportamento da conta de luz no Brasil.

### 1.5 Objetivos específicos (sugestão de 4)

1. Consolidar em uma única base histórica o crescimento da geração distribuída solar por estado/região e sua relação com a tarifa (TE/TUSD) praticada pelas distribuidoras locais.
2. Modelar a relação entre o nível de Energia Natural Afluente (ENA/hidrologia) e o acionamento histórico das bandeiras tarifárias (classificação: verde, amarela, vermelha P1/P2).
3. Identificar clusters de estados/distribuidoras por perfil de penetração solar x estrutura tarifária (quem já sente mais impacto da GD na receita).
4. Construir um dashboard que estime, para os próximos meses, a probabilidade de acionamento de bandeira e a tendência tarifária por região.

### 1.6 Setor de atuação

**Energia** (regulado / setor público-privado), se o formulário do briefing não tiver essa opção nativa, marcar "Outro: Energia".

---

## 2. Seleção e avaliação das bases de dados

| Base | Fonte | Formato | Granularidade | Cobertura temporal | Atualização | Avaliação |
|---|---|---|---|---|---|---|
| **Bandeiras Tarifárias** (acionamento, adicional, conta bandeira) | [ANEEL Dados Abertos](https://dadosabertos.aneel.gov.br/dataset/bandeiras-tarifarias) | CSV + dicionário PDF | Nacional, mensal | Desde jan/2015 | Mensal (últ. atualização: 10/ago/2026) | Boa: série longa e oficial, mas granularidade nacional única, precisa ser enriquecida para gerar features suficientes |
| **Relação de Empreendimentos de Geração Distribuída** | [ANEEL Dados Abertos](https://dadosabertos.aneel.gov.br/dataset/relacao-de-empreendimentos-de-geracao-distribuida) | CSV, ZIP e **Parquet** (já otimizado para big data) | Por empreendimento (potência, fonte, data de conexão) | Desde dez/2008 | **Diária** | Excelente: alto volume (milhões de registros dado o marco de 4M+ sistemas), formato Parquet nativo, atualizado todo dia. Ponto de atenção de governança: avaliar se há identificação de unidade consumidora e, se sim, tratar/agregar por município para reduzir sensibilidade |
| **Tarifas Homologadas das Distribuidoras (TE e TUSD)** | [ANEEL Dados Abertos](https://dadosabertos.aneel.gov.br/dataset/tarifas-distribuidoras-energia-eletrica) | CSV + XML | Por distribuidora, por processo de reajuste | Histórico dos reajustes tarifários | Conforme homologação da ANEEL | Boa: permite calcular o valor efetivo da conta de luz por distribuidora/região ao longo do tempo |
| **ENA Diário por Reservatório / por Bacia** (Energia Natural Afluente) | [ONS Dados Abertos](https://dados.ons.org.br/dataset/ena-diario-por-reservatorio) | CSV, XLSX e Parquet | Diária, por reservatório e por bacia hidroenergética | Desde 2005 | Diária | Excelente: é o principal driver técnico por trás do acionamento das bandeiras, combinação direta com a base de bandeiras para a modelagem preditiva |
| **(complementar) Malha municipal / população: IBGE** | IBGE | CSV/API | Município | Censo/estimativas anuais | Anual | Útil para normalizar penetração de GD per capita por região, se necessário |

**Conclusão da avaliação:** as quatro bases principais (bandeiras, GD, tarifas, ENA) são todas públicas, gratuitas, em formatos processáveis (CSV/Parquet), com granularidade diária ou mensal e séries longas o suficiente para modelagem, atendem bem ao requisito de "Big Data Analytics" tanto pelo volume (GD com atualização diária desde 2008) quanto pela necessidade real de integração de múltiplas fontes heterogêneas.

**Limitação identificada:** as páginas de metadados da ANEEL não expõem publicamente o dicionário de campos nem o volume exato de linhas, isso só é confirmado baixando o arquivo. Recomendo que o grupo baixe uma amostra de cada base já na próxima etapa (avaliação técnica) para validar schema antes de fechar a arquitetura definitiva.

---

## 3. Desenho inicial da arquitetura

```
                    ┌─────────────────────────────────────────┐
                    │              FONTES (Ingestão)            │
                    │  ANEEL (Bandeiras, GD, Tarifas) · ONS (ENA) │
                    └───────────────────┬─────────────────────┘
                                        │  download / API (CSV, Parquet, XML)
                                        ▼
                    ┌─────────────────────────────────────────┐
                    │   CAMADA RAW (dados brutos, como estão)   │
                    │   Armazenamento: pasta/bucket por fonte   │
                    │   e data de ingestão (partição diária)    │
                    └───────────────────┬─────────────────────┘
                                        │  limpeza, padronização de tipos,
                                        │  normalização de nomes de campos/UF
                                        ▼
                    ┌─────────────────────────────────────────┐
                    │  CAMADA TRUSTED (dados validados)         │
                    │  Junção por data + UF/distribuidora,      │
                    │  deduplicação, checagem de qualidade      │
                    └───────────────────┬─────────────────────┘
                                        │  agregações e features
                                        ▼
                    ┌─────────────────────────────────────────┐
                    │ CAMADA CURATED/REFINED (modelo analítico) │
                    │ Tabela mensal: UF x tarifa média x        │
                    │ penetração solar x ENA x bandeira         │
                    └───────────────────┬─────────────────────┘
                                        │
                          ┌─────────────┴─────────────┐
                          ▼                           ▼
              ┌───────────────────┐        ┌───────────────────────┐
              │  MODELAGEM (ML)    │        │  DASHBOARD (consumo)   │
              │ Classificação      │        │  Power BI / Looker     │
              │ (bandeira) +       │        │  Studio - visão        │
              │ Clusterização (UF) │        │  executiva e regional  │
              └───────────────────┘        └───────────────────────┘
```

Governança aplicada: catálogo de dados simples (planilha com fonte, dono, frequência), classificação de sensibilidade da base de GD (avaliar se há UC/CPF/CNPJ e, se houver, mascarar ou agregar por município), e política de acesso básica (camada raw só para o time de dados, curated liberada para todo o grupo).

---

## 4. Ferramentas e tecnologias sugeridas

| Etapa | Ferramenta sugerida | Por quê |
|---|---|---|
| Ingestão/ETL | **Python** (pandas + requests) | Simples, roda em qualquer máquina do grupo, suficiente para o volume do projeto acadêmico |
| Orquestração | **Prefect** ou scripts agendados (cron), evitar Airflow completo a menos que o grupo já tenha familiaridade, pelo custo de setup | Foco no tempo do semestre; Airflow é overkill para 4 fontes de dados |
| Armazenamento | **Parquet local + DuckDB** (ou PostgreSQL, se preferirem SQL tradicional) | DuckDB lê Parquet nativamente e é leve, ótimo para simular camadas Raw/Trusted/Curated sem precisar de infraestrutura em nuvem |
| Modelagem | **Python (scikit-learn)**: Árvore de Decisão / Random Forest para classificação da bandeira, K-Means para clusterização de UFs | Alinhado às opções já previstas no briefing do projeto |
| Dashboard | **Power BI** ou **Google Looker Studio** (gratuito) | Looker Studio é gratuito e conecta direto em CSV/Google Sheets; Power BI é mais robusto se alguém do grupo já tiver licença |
| Versionamento/documentação | **GitHub** (repositório com README, notebooks, código-fonte) | Exigido na seção 9 do briefing |
| Gestão do projeto | **Trello** ou **Jira** | Ver quadro Kanban sugerido abaixo |

---

## 5. Kanban inicial (estrutura sugerida para Trello/Jira)

**Colunas:** `Backlog` → `A Fazer` → `Em Andamento` → `Em Revisão` → `Concluído`

**Cartões da Fase 1 (a mover para "Concluído" ao fechar esta etapa):**
- [ ] Definir problema de negócio e caso de uso
- [ ] Levantar e validar as 4 bases de dados (baixar amostras, checar dicionários)
- [ ] Desenhar arquitetura de camadas (raw/trusted/curated)
- [ ] Definir stack de ferramentas
- [ ] Criar repositório GitHub inicial (README + estrutura de pastas)

**Cartões da Fase 2 (próxima etapa: Ingestão e Preparação):**
- [ ] Escrever scripts de ingestão (download automatizado ANEEL + ONS)
- [ ] Padronizar schemas e nomes de colunas entre fontes
- [ ] Implementar camada Trusted (joins por data/UF)
- [ ] Documentar dicionário de dados consolidado

**Cartões da Fase 3 (Modelagem e Dashboard):**
- [ ] EDA (estatística descritiva, correlação ENA x bandeira)
- [ ] Treinar modelo de classificação de bandeira
- [ ] Treinar clusterização de UFs
- [ ] Construir dashboard executivo
- [ ] Preparar apresentação final e slides

*Posso criar esse quadro diretamente no Trello ou Jira se vocês conectarem a conta, é só avisar qual das duas preferem.*

---

## Fontes consultadas
- [ANEEL Dados Abertos: Bandeiras Tarifárias](https://dadosabertos.aneel.gov.br/dataset/bandeiras-tarifarias)
- [ANEEL Dados Abertos: Geração Distribuída](https://dadosabertos.aneel.gov.br/dataset/relacao-de-empreendimentos-de-geracao-distribuida)
- [ANEEL Dados Abertos: Tarifas das Distribuidoras](https://dadosabertos.aneel.gov.br/dataset/tarifas-distribuidoras-energia-eletrica)
- [ONS Dados Abertos: ENA Diário por Reservatório](https://dados.ons.org.br/dataset/ena-diario-por-reservatorio)
- [Canal Solar: Brasil ultrapassa 4 milhões de sistemas de energia solar distribuída](https://canalsolar.com.br/brasil-quatro-milhoes-sistemas-energia-solar/)
- [PV Magazine Brasil: Geração distribuída ultrapassa 4 milhões de sistemas](https://www.pv-magazine-brasil.com/2026/02/27/geracao-distribuida-ultrapassa-4-milhoes-de-sistemas-no-brasil/)
- [PV Magazine Brasil: Brasil adiciona 4,4 GW de capacidade solar no 1º trimestre](https://www.pv-magazine-brasil.com/2026/05/14/brasil-adiciona-44-gw-de-capacidade-solar-no-primeiro-trimestre/)
