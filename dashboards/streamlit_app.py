import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Energia em Dados",
    layout="wide"
)

st.title("Energia em Dados")
st.subheader("Diagnóstico das bases")

arquivos = {
    "Bandeiras": "../trusted/bandeira_mensal.parquet",
    "ENA": "../trusted/ena_mensal.parquet",
    "Solar": "../trusted/solar_mensal_nacional.parquet"
}

for nome, caminho in arquivos.items():

    st.header(nome)

    try:
        df = pd.read_parquet(caminho)

        st.write("Dimensões:", df.shape)

        st.write("Colunas:")
        st.write(list(df.columns))

        st.dataframe(df.head())

    except Exception as e:
        st.error(f"Erro ao carregar {nome}: {e}")
