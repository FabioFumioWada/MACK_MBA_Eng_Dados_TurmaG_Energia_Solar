# Databricks notebook source
import pandas as pd
import numpy as np

bandeira = pd.read_parquet("/home/user/workspace/bandeira_mensal.parquet")[["mes", "NomBandeiraAcionada", "nivel"]]
ena = pd.read_parquet("/home/user/workspace/ena_mensal.parquet")
solar = pd.read_parquet("/home/user/workspace/solar_mensal_nacional.parquet")

# Padroniza tipo do período
bandeira["mes"] = bandeira["mes"].astype(str)
ena["mes"] = ena["mes"].astype(str)
solar["mes"] = solar["mes"].astype(str)

painel = bandeira.merge(ena, on="mes", how="left").merge(solar, on="mes", how="left")
painel = painel.sort_values("mes").reset_index(drop=True)
painel["potencia_acumulada_mw"] = painel["potencia_acumulada_mw"].ffill()
painel["conexoes_acumuladas"] = painel["conexoes_acumuladas"].ffill()
painel = painel.dropna(subset=["nivel", "ena_nacional_pct_mlt_media_subsis", "potencia_acumulada_mw"])

painel.to_csv("/home/user/workspace/painel_mensal_nacional.csv", index=False)

print(f"=== Painel mensal consolidado: {len(painel)} meses ({painel['mes'].min()} a {painel['mes'].max()}) ===\n")

# ---------- Correlações (nível cru) ----------
cols_corr = [
    "nivel",
    "ena_nacional_pct_mlt_media_subsis",
    "ena_pct_mlt_sudeste",
    "ena_pct_mlt_sul",
    "ena_pct_mlt_nordeste",
    "ena_pct_mlt_norte",
    "potencia_acumulada_mw",
]
corr = painel[cols_corr].corr(numeric_only=True)
print("=== Matriz de correlação (nível bruto, com tendência) ===")
print(corr["nivel"].sort_values())

# ---------- Correlação controlando tendência (variação mês a mês) ----------
painel["d_nivel"] = painel["nivel"].diff()
painel["d_ena_nacional"] = painel["ena_nacional_pct_mlt_media_subsis"].diff()
painel["d_potencia_solar"] = painel["potencia_acumulada_mw"].pct_change() * 100  # % crescimento MoM

corr_var = painel[["nivel", "ena_nacional_pct_mlt_media_subsis", "d_potencia_solar"]].dropna().corr()
print("\n=== Correlação nível bandeira x % crescimento mensal do solar (sem viés de tendência conjunta) ===")
print(corr_var["nivel"])

# ---------- Agregação trimestral (pra validar a lógica "prever próximo trimestre") ----------
painel["mes_dt"] = pd.to_datetime(painel["mes"])
painel["trimestre"] = painel["mes_dt"].dt.to_period("Q").astype(str)

trim = painel.groupby("trimestre").agg(
    nivel_max=("nivel", "max"),
    nivel_medio=("nivel", "mean"),
    ena_medio=("ena_nacional_pct_mlt_media_subsis", "mean"),
    ena_sudeste_medio=("ena_pct_mlt_sudeste", "mean"),
    potencia_fim_trimestre_mw=("potencia_acumulada_mw", "last"),
).reset_index()

trim["crescimento_solar_trim_pct"] = trim["potencia_fim_trimestre_mw"].pct_change() * 100

print(f"\n=== Agregado trimestral: {len(trim)} trimestres ===")
print(trim.tail(10).to_string(index=False))

trim.to_csv("/home/user/workspace/painel_trimestral_nacional.csv", index=False)

# ---------- Distribuição da bandeira por ano (pra mostrar desbalanceamento) ----------
painel["ano"] = painel["mes_dt"].dt.year
dist_ano = painel.groupby(["ano", "NomBandeiraAcionada"]).size().unstack(fill_value=0)
print("\n=== Bandeira por ano (contagem de meses) ===")
print(dist_ano.to_string())

print("\nOK - painel consolidado salvo em painel_mensal_nacional.csv e painel_trimestral_nacional.csv")
