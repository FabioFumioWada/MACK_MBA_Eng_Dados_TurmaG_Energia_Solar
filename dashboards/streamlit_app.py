import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(
    page_title="Energia em Dados",
    page_icon="☀️",
    layout="wide"
)

# Título
st.title("☀️ Energia em Dados")
st.markdown("### Panorama nacional da geração de energia")

st.divider()

# Carregamento das bases
@st.cache_data
def carregar_dados():

    bandeiras = pd.read_parquet(
        "trusted/bandeira_mensal.parquet"
    )

    ena = pd.read_parquet(
        "trusted/ena_mensal.parquet"
    )

    solar = pd.read_parquet(
        "trusted/solar_mensal_nacional.parquet"
    )

    return bandeiras, ena, solar


bandeiras, ena, solar = carregar_dados()

st.success("Bases de dados carregadas com sucesso.")

# Informações iniciais
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Registros — Bandeiras",
        f"{len(bandeiras):,}"
    )

with col2:
    st.metric(
        "Registros — ENA",
        f"{len(ena):,}"
    )

with col3:
    st.metric(
        "Registros — Solar",
        f"{len(solar):,}"
    )
