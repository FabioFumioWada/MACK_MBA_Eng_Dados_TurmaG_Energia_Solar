# MACK_MBA_Eng_Dados_TurmaG_Energia_Solar

Repositório com a estrutura técnica da análise de dados da Energia Solar.

Universidade Presbiteriana Mackenzie
MBA em Engenharia de Dados

Grupo:
Alberto Oliveira Chaves (RA1015803)
Fabio Fumio Wada (RA10741479)
Laiane Ressurreição (RA10739799)
Sweeli Suzuki (RA10423319)
Tatiane Silva Santos (RA10747108)

## Sobre o projeto

Análise nacional da relação entre bandeira tarifária, Energia Natural Afluente (ENA) e crescimento da geração distribuída solar no Brasil- Projeto Hands-On de Big Data Analytics.

## Estrutura do repositório

- `/raw` - arquivos brutos, sem transformação (ANEEL bandeira, ANEEL GD solar, ONS ENA por subsistema).
- `/trusted` - `eda_nacional.py`: limpeza, tipagem e nível ordinal da bandeira (0–4).
- `/refined` - `eda_correlacao.py` + painéis consolidados mensal/trimestral (`painel_mensal_nacional.csv`, `painel_trimestral_nacional.csv`).
- `/dashboards` - `dashboard_eda.py` e o painel de gráficos (Excel editável e PNG).
- `/docs` - documentos das Fases 1 e 2 (Word/PDF).
- `/databricks` - Asset Bundle (databricks.yml) e definição dos jobs Raw → Trusted → Refined.
- `/.github/workflows` - pipeline de CI/CD (GitHub Actions).

## Janela temporal

Histórico completo: jan/2015 a ago/2026 (140 meses / 11,7 anos), usado para 
sazonalidade e stress-test. Modelo preditivo: treinado com todo o histórico 
disponível, exceto o último trimestre completo, reservado como período de 
teste/validação (recorte de livre escolha do grupo, dentro do critério 
orientado).
