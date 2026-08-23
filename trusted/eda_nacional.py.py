# Databricks notebook source
import duckdb
import pandas as pd

con = duckdb.connect()

# ---------- 1. Bandeira tarifária (alvo, nacional, mensal, desde 2015) ----------
bandeira = pd.read_csv(
    "/home/user/workspace/bandeira_acionamento.csv",
    sep=";",
    decimal=",",
    encoding="utf-8",
)
bandeira.columns = [c.strip() for c in bandeira.columns]
bandeira["DatCompetencia"] = pd.to_datetime(bandeira["DatCompetencia"])
bandeira["mes"] = bandeira["DatCompetencia"].dt.to_period("M")
bandeira["NomBandeiraAcionada"] = bandeira["NomBandeiraAcionada"].str.strip()

ordem = {"Verde": 0, "Amarela": 1, "Vermelha P1": 2, "Vermelha P2": 3, "Escassez Hídrica": 4}
bandeira["nivel"] = bandeira["NomBandeiraAcionada"].map(ordem)
bandeira = bandeira.sort_values("DatCompetencia").drop_duplicates("mes", keep="last")

print("=== Distribuição histórica da bandeira (2015-2026) ===")
print(bandeira["NomBandeiraAcionada"].value_counts())
print(f"\nTotal de meses: {len(bandeira)}")
print(f"Período: {bandeira['DatCompetencia'].min().date()} a {bandeira['DatCompetencia'].max().date()}")

bandeira.to_parquet("/home/user/workspace/bandeira_mensal.parquet")

# ---------- 2. ENA por subsistema -> agregado mensal nacional ----------
ena = con.execute("""
    SELECT
        nom_subsistema,
        ena_data::DATE AS data,
        ena_bruta_regiao_mwmed,
        ena_bruta_regiao_percentualmlt,
        ena_armazenavel_regiao_mwmed,
        ena_armazenavel_regiao_percentualmlt
    FROM read_csv('/home/user/workspace/ena_subsistema/ena_*.csv', delim=';', header=true, decimal_separator='.',
                   columns={
                     'id_subsistema': 'VARCHAR',
                     'nom_subsistema': 'VARCHAR',
                     'ena_data': 'VARCHAR',
                     'ena_bruta_regiao_mwmed': 'DOUBLE',
                     'ena_bruta_regiao_percentualmlt': 'DOUBLE',
                     'ena_armazenavel_regiao_mwmed': 'DOUBLE',
                     'ena_armazenavel_regiao_percentualmlt': 'DOUBLE'
                   })
""").df()

ena["mes"] = pd.to_datetime(ena["data"]).dt.to_period("M")

# Média mensal por subsistema (% da MLT - Média de Longo Termo)
ena_mensal_sub = ena.groupby(["nom_subsistema", "mes"]).agg(
    ena_pct_mlt=("ena_bruta_regiao_percentualmlt", "mean"),
    ena_mwmed=("ena_bruta_regiao_mwmed", "mean"),
).reset_index()

# Pivot: uma coluna por subsistema
ena_pivot = ena_mensal_sub.pivot(index="mes", columns="nom_subsistema", values="ena_pct_mlt")
ena_pivot.columns = [f"ena_pct_mlt_{c.lower()}" for c in ena_pivot.columns]
ena_pivot = ena_pivot.reset_index()

# ENA nacional = soma de MWmed de todos os subsistemas / média simples do % MLT
ena_nacional_mwmed = ena.groupby("mes")["ena_bruta_regiao_mwmed"].sum().rename("ena_nacional_mwmed")
ena_nacional_pct = ena.groupby("mes")["ena_bruta_regiao_percentualmlt"].mean().rename("ena_nacional_pct_mlt_media_subsis")

ena_final = ena_pivot.merge(ena_nacional_mwmed, on="mes").merge(ena_nacional_pct, on="mes")
ena_final.to_parquet("/home/user/workspace/ena_mensal.parquet")

print("\n=== ENA mensal nacional (amostra) ===")
print(ena_final.tail(8).to_string())

# ---------- 3. GD Solar nacional (UFV) - crescimento acumulado mensal ----------
solar = con.execute("""
    SELECT
        DthAtualizaCadastralEmpreend AS data_conexao,
        MdaPotenciaInstaladaKW AS potencia_kw,
        SigUF AS uf
    FROM read_csv('/home/user/workspace/gd_extracted/empreendimento-geracao-distribuida.csv',
                   delim=';', header=true, ignore_errors=true, strict_mode=false)
    WHERE SigTipoGeracao = 'UFV'
""").df()

solar["data_conexao"] = pd.to_datetime(solar["data_conexao"], errors="coerce")
solar = solar[solar["data_conexao"] > "2005-01-01"]  # remove placeholders tipo 1900-01-01
solar["potencia_kw"] = (
    solar["potencia_kw"].astype(str).str.replace(",", ".", regex=False)
)
solar["potencia_kw"] = pd.to_numeric(solar["potencia_kw"], errors="coerce")
solar = solar.dropna(subset=["data_conexao", "potencia_kw"])
solar["mes"] = solar["data_conexao"].dt.to_period("M")

print(f"\n=== GD Solar nacional: {len(solar):,} registros válidos ===")
print(f"Potência total instalada (nacional): {solar['potencia_kw'].sum()/1000:,.1f} MW")

# Novas conexões por mês (fluxo) + acumulado (estoque)
fluxo_mensal = solar.groupby("mes")["potencia_kw"].agg(["count", "sum"]).rename(
    columns={"count": "novas_conexoes", "sum": "potencia_nova_kw"}
).reset_index().sort_values("mes")

fluxo_mensal["potencia_acumulada_kw"] = fluxo_mensal["potencia_nova_kw"].cumsum()
fluxo_mensal["potencia_acumulada_mw"] = fluxo_mensal["potencia_acumulada_kw"] / 1000
fluxo_mensal["conexoes_acumuladas"] = fluxo_mensal["novas_conexoes"].cumsum()

fluxo_mensal.to_parquet("/home/user/workspace/solar_mensal_nacional.parquet")

print("\n=== Crescimento solar nacional (últimos 8 meses) ===")
print(fluxo_mensal.tail(8)[["mes", "novas_conexoes", "potencia_acumulada_mw"]].to_string())

print("\nOK - todos os parquets salvos.")
