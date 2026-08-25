import streamlit as st
import pandas as pd
from pathlib import Path


# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================

st.set_page_config(
    page_title="Energia em Dados",
    page_icon="☀️",
    layout="wide"
)


# ============================================================
# ESTILO VISUAL
# ============================================================

st.markdown(
    """
    <style>
        .main {
            background-color: #f7f9fc;
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        h1 {
            font-size: 2.5rem;
            font-weight: 700;
        }

        h2, h3 {
            font-weight: 600;
        }

        .metric-card {
            background-color: white;
            padding: 20px;
            border-radius: 12px;
            border: 1px solid #e6e9ef;
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        }

        .subtitle {
            color: #667085;
            font-size: 1.05rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# CAMINHO DAS BASES
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
TRUSTED_DIR = BASE_DIR / "trusted"


arquivos = {
    "Bandeiras": TRUSTED_DIR / "bandeira_mensal.parquet",
    "ENA": TRUSTED_DIR / "ena_mensal.parquet",
    "Solar": TRUSTED_DIR / "solar_mensal_nacional.parquet"
}


# ============================================================
# CABEÇALHO
# ============================================================

st.title("☀️ Energia em Dados")

st.markdown(
    '<p class="subtitle">'
    'Painel exploratório das bases do setor elétrico brasileiro'
    '</p>',
    unsafe_allow_html=True
)

st.divider()


# ============================================================
# CARREGAMENTO DAS BASES
# ============================================================

bases = {}

for nome, caminho in arquivos.items():

    try:
        df = pd.read_parquet(caminho)
        bases[nome] = df

    except Exception as e:

        st.error(
            f"Não foi possível carregar a base {nome}: {e}"
        )


# ============================================================
# INDICADORES GERAIS
# ============================================================

st.subheader("Visão geral das bases")

col1, col2, col3 = st.columns(3)


if "Bandeiras" in bases:

    with col1:
        st.metric(
            "Bandeiras",
            f"{len(bases['Bandeiras']):,}".replace(",", ".")
        )


if "ENA" in bases:

    with col2:
        st.metric(
            "ENA",
            f"{len(bases['ENA']):,}".replace(",", ".")
        )


if "Solar" in bases:

    with col3:
        st.metric(
            "Solar",
            f"{len(bases['Solar']):,}".replace(",", ".")
        )


st.divider()


# ============================================================
# EXPLORAÇÃO DAS BASES
# ============================================================

st.subheader("Exploração dos dados")


abas = st.tabs(
    [
        "☀️ Solar",
        "💧 ENA",
        "⚡ Bandeiras"
    ]
)


# ============================================================
# SOLAR
# ============================================================

with abas[0]:

    if "Solar" in bases:

        df = bases["Solar"]

        st.markdown("### Base Solar")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Registros",
                f"{len(df):,}".replace(",", ".")
            )

        with col2:
            st.metric(
                "Colunas",
                len(df.columns)
            )

        st.markdown("#### Prévia dos dados")

        st.dataframe(
            df.head(10),
            use_container_width=True
        )

        with st.expander("Ver estrutura da base"):

            st.write("Colunas:")

            st.write(
                list(df.columns)
            )

            st.write("Tipos de dados:")

            st.dataframe(
                pd.DataFrame(
                    {
                        "Coluna": df.columns,
                        "Tipo": df.dtypes.astype(str).values
                    }
                ),
                use_container_width=True
            )


# ============================================================
# ENA
# ============================================================

with abas[1]:

    if "ENA" in bases:

        df = bases["ENA"]

        st.markdown("### Energia Natural Afluente — ENA")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Registros",
                f"{len(df):,}".replace(",", ".")
            )

        with col2:
            st.metric(
                "Colunas",
                len(df.columns)
            )

        st.markdown("#### Prévia dos dados")

        st.dataframe(
            df.head(10),
            use_container_width=True
        )

        with st.expander("Ver estrutura da base"):

            st.write("Colunas:")

            st.write(
                list(df.columns)
            )

            st.write("Tipos de dados:")

            st.dataframe(
                pd.DataFrame(
                    {
                        "Coluna": df.columns,
                        "Tipo": df.dtypes.astype(str).values
                    }
                ),
                use_container_width=True
            )


# ============================================================
# BANDEIRAS
# ============================================================

with abas[2]:

    if "Bandeiras" in bases:

        df = bases["Bandeiras"]

        st.markdown("### Bandeiras Tarifárias")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Registros",
                f"{len(df):,}".replace(",", ".")
            )

        with col2:
            st.metric(
                "Colunas",
                len(df.columns)
            )

        st.markdown("#### Prévia dos dados")

        st.dataframe(
            df.head(10),
            use_container_width=True
        )

        with st.expander("Ver estrutura da base"):

            st.write("Colunas:")

            st.write(
                list(df.columns)
            )

            st.write("Tipos de dados:")

            st.dataframe(
                pd.DataFrame(
                    {
                        "Coluna": df.columns,
                        "Tipo": df.dtypes.astype(str).values
                    }
                ),
                use_container_width=True
            )


# ============================================================
# RODAPÉ
# ============================================================

st.divider()

st.caption(
    "Projeto MBA Engenharia de Dados — Energia Solar | "
    "Dados organizados na camada Trusted"
)
