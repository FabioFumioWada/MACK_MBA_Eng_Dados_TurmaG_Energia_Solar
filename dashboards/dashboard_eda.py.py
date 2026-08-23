# Databricks notebook source
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Patch

# ---------- Paleta Nexus (design-foundations) ----------
BG = "#F7F6F2"
SURFACE = "#F9F8F5"
BORDER = "#D4D1CA"
TEXT = "#28251D"
TEXT_MUTED = "#7A7974"
PRIMARY = "#01696F"
COR_BANDEIRA = {
    "Verde": "#437A22",
    "Amarela": "#D19900",
    "Vermelha P1": "#DA7101",
    "Vermelha P2": "#A13544",
    "Escassez Hídrica": "#7A39BB",
}

painel = pd.read_csv("/home/user/workspace/painel_mensal_nacional.csv")
painel["mes_dt"] = pd.to_datetime(painel["mes"])
painel["ano"] = painel["mes_dt"].dt.year

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "text.color": TEXT,
    "axes.labelcolor": TEXT,
    "xtick.color": TEXT_MUTED,
    "ytick.color": TEXT_MUTED,
    "axes.edgecolor": BORDER,
})

fig = plt.figure(figsize=(14, 11), facecolor=BG)
gs = fig.add_gridspec(3, 2, hspace=0.55, wspace=0.28, left=0.07, right=0.96, top=0.93, bottom=0.06)

fig.suptitle(
    "Energia em Dados — EDA Inicial (Brasil, 2015–2026)",
    fontsize=18, fontweight="bold", color=TEXT, x=0.07, ha="left", y=0.985,
)

# ---------- 1. Linha do tempo da bandeira tarifária (histórico completo) ----------
ax1 = fig.add_subplot(gs[0, :])
ax1.set_facecolor(SURFACE)
for cor, hexcode in COR_BANDEIRA.items():
    sub = painel[painel["NomBandeiraAcionada"] == cor]
    ax1.scatter(sub["mes_dt"], sub["nivel"], color=hexcode, s=28, label=cor, zorder=3)
ax1.plot(painel["mes_dt"], painel["nivel"], color=BORDER, linewidth=1, zorder=1)
ax1.set_yticks([0, 1, 2, 3, 4])
ax1.set_yticklabels(["Verde", "Amarela", "Verm. P1", "Verm. P2", "Escassez"])
ax1.set_title("Bandeira tarifária nacional — mês a mês", fontsize=12, fontweight="bold", loc="left", pad=10)
ax1.xaxis.set_major_locator(mdates.YearLocator())
ax1.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
ax1.legend(loc="upper left", bbox_to_anchor=(0, -0.18), ncol=5, frameon=False, fontsize=9)
ax1.grid(axis="y", color=BORDER, linewidth=0.5, alpha=0.6)
for spine in ["top", "right"]:
    ax1.spines[spine].set_visible(False)

# ---------- 2. ENA nacional (% da MLT) x nível da bandeira ----------
ax2 = fig.add_subplot(gs[1, 0])
ax2.set_facecolor(SURFACE)
ax2.plot(painel["mes_dt"], painel["ena_nacional_pct_mlt_media_subsis"], color=PRIMARY, linewidth=1.6)
ax2.axhline(100, color=TEXT_MUTED, linewidth=0.8, linestyle="--", alpha=0.7)
ax2.set_title("ENA nacional (% da média histórica)", fontsize=11, fontweight="bold", loc="left")
ax2.set_ylabel("% da MLT")
ax2.xaxis.set_major_locator(mdates.YearLocator(2))
ax2.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
for spine in ["top", "right"]:
    ax2.spines[spine].set_visible(False)
ax2.grid(axis="y", color=BORDER, linewidth=0.5, alpha=0.6)

# ---------- 3. Crescimento solar acumulado nacional ----------
ax3 = fig.add_subplot(gs[1, 1])
ax3.set_facecolor(SURFACE)
ax3.fill_between(painel["mes_dt"], painel["potencia_acumulada_mw"], color=PRIMARY, alpha=0.15)
ax3.plot(painel["mes_dt"], painel["potencia_acumulada_mw"], color=PRIMARY, linewidth=1.8)
ax3.set_title("Potência solar (GD) acumulada — Brasil", fontsize=11, fontweight="bold", loc="left")
ax3.set_ylabel("MW instalados")
ax3.xaxis.set_major_locator(mdates.YearLocator(2))
ax3.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
for spine in ["top", "right"]:
    ax3.spines[spine].set_visible(False)
ax3.grid(axis="y", color=BORDER, linewidth=0.5, alpha=0.6)

# ---------- 4. Distribuição da bandeira por ano (barras apiladas) ----------
ax4 = fig.add_subplot(gs[2, 0])
ax4.set_facecolor(SURFACE)
dist = painel.groupby(["ano", "NomBandeiraAcionada"]).size().unstack(fill_value=0)
ordem_cols = ["Verde", "Amarela", "Vermelha P1", "Vermelha P2", "Escassez Hídrica"]
dist = dist.reindex(columns=[c for c in ordem_cols if c in dist.columns])
bottom = None
for cor in dist.columns:
    ax4.bar(dist.index, dist[cor], bottom=bottom, color=COR_BANDEIRA[cor], width=0.7, label=cor)
    bottom = dist[cor] if bottom is None else bottom + dist[cor]
ax4.set_title("Meses por cor de bandeira, por ano", fontsize=11, fontweight="bold", loc="left")
ax4.set_ylabel("Meses")
for spine in ["top", "right"]:
    ax4.spines[spine].set_visible(False)
ax4.grid(axis="y", color=BORDER, linewidth=0.5, alpha=0.6)
ax4.tick_params(axis="x", rotation=45)

# ---------- 5. Correlação (nível bandeira x indicadores) ----------
ax5 = fig.add_subplot(gs[2, 1])
ax5.set_facecolor(SURFACE)
corr_vals = {
    "ENA Sul": -0.133,
    "ENA Nacional": -0.095,
    "ENA Sudeste/CO": -0.037,
    "ENA Nordeste": -0.010,
    "ENA Norte": 0.099,
    "Cresc. Solar (MoM %)": 0.118,
}
labels = list(corr_vals.keys())
vals = list(corr_vals.values())
colors_bar = ["#A13544" if v > 0 else "#01696F" for v in vals]
ax5.barh(labels, vals, color=colors_bar, height=0.55)
ax5.axvline(0, color=TEXT, linewidth=0.8)
ax5.set_title("Correlação com o nível da bandeira", fontsize=11, fontweight="bold", loc="left")
ax5.set_xlabel("coeficiente de correlação (r)")
for spine in ["top", "right"]:
    ax5.spines[spine].set_visible(False)
ax5.grid(axis="x", color=BORDER, linewidth=0.5, alpha=0.6)

fig.text(0.07, 0.012,
         "Fontes: ANEEL (Bandeiras Tarifárias, Geração Distribuída) · ONS (ENA Diário por Subsistema) · dadosabertos.aneel.gov.br · dados.ons.org.br",
         fontsize=8, color=TEXT_MUTED)

fig.savefig("/home/user/workspace/dashboard_eda_nacional.png", dpi=180, facecolor=BG)
print("Salvo: dashboard_eda_nacional.png")
