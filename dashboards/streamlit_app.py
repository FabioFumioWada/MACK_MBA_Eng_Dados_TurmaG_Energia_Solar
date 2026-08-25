import streamlit as st
import pandas as pd
from pathlib import Path


# ============================================================
# CONFIGURAÇÃO
# ============================================================

st.set_page_config(
    page_title="Energia em Dados",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# IDENTIDADE VISUAL
# ============================================================

st.markdown(
    """
    <style>

    /* ---------- FUNDO ---------- */

    .stApp {
        background-color: #F7F9FC;
    }

    .block-container {
        max-width: 1400px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }


    /* ---------- TÍTULOS ---------- */

    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        letter-spacing: -1.5px;
        color: #102A43;
        margin-bottom: 0.2rem;
    }

    .hero-subtitle {
        font-size: 1.1rem;
        color: #627D98;
        margin-bottom: 2rem;
    }


    /* ---------- SEÇÕES ---------- */

    .section-title {
        font-size: 1.45rem;
        font-weight: 700;
        color: #102A43;
        margin-top: 1rem;
        margin-bottom: 0.8rem;
    }

    .section-subtitle {
        color: #627D98;
        font-size: 0.95rem;
        margin-bottom: 1.2rem;
    }


    /* ---------- CARDS ---------- */

    .metric-card {
        background: #FFFFFF;
        border: 1px solid #E6ECF2;
        border-radius: 16px;
        padding: 1.25rem 1.4rem;
        min-height: 130px;
        box-shadow: 0 4px 14px rgba(16, 42, 67, 0.05);
    }

    .metric-label {
        color: #627D98;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 0.55rem;
    }

    .metric-value {
        color: #102A43;
        font-size: 2rem;
        font-weight: 800;
        line-height: 1.1;
    }

    .metric-description {
        color: #829AB1;
        font-size: 0.78rem;
        margin-top: 0.5rem;
    }


    /* ---------- HERO SOLAR ---------- */

    .solar-banner {
        background: linear-gradient(
            135deg,
            #FFF8E1 0%,
            #FFFDF5 55%,
            #FFFFFF 100%
        );

        border: 1px solid #F4E7B5;
        border-radius: 20px;
        padding: 1.8rem 2rem;
        margin: 1rem 0 1.5rem 0;
    }

    .solar-banner-title {
        color: #102A43;
        font-size: 1.35rem;
        font-weight: 750;
        margin-bottom: 0.35rem;
    }

    .solar-banner-text {
        color: #627D98;
        font-size: 0.92rem;
    }


    /* ---------- DIVISORES ---------- */

    hr {
        border: none;
        border-top: 1px solid #E6ECF2;
        margin: 1.8rem 0;
    }


    /* ---------- TABS ---------- */

    button[data-baseweb="tab"] {
        font-weight: 650;
        color: #486581;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: #D99000;
    }


    /* ---------- TABELAS ---------- */

    .dataframe {
        border-radius: 12px;
    }


    /* ---------- RODAPÉ ---------- */

    .footer {
        text-align: center;
        color: #829AB1;
        font-size: 0.8rem;
        padding-top: 2rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# CAMINHOS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
TRUSTED_DIR = BASE_DIR / "trusted"

ARQUIVOS = {
    "Bandeiras": TRUSTED_DIR / "bandeira_mensal.parquet",
    "ENA": TRUSTED_DIR / "ena_mensal.parquet",
    "Solar": TRUSTED_DIR / "solar_mensal_nacional.parquet"
}


# ============================================================
# FUNÇÕES
# ============================================================

@st.cache_data
def carregar_base(caminho):
    return pd.read_parquet(caminho)


def formatar_numero(valor):
    if pd.isna(valor):
        return "—"

    valor = float(valor)

    if abs(valor) >= 1_000_000:
        return f"{valor / 1_000_000:.1f} mi"

    if abs(valor) >= 1_000:
        return f"{valor / 1_000:.1f} mil"

    return f"{valor:,.0f}".replace(",", ".")


def card(label, value, description=""):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-description">{description}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def encontrar_coluna(df, possibilidades):

    for coluna in possibilidades:

        if coluna in df.columns:
            return coluna

    return None


# ============================================================
# CARREGAMENTO
# ============================================================

bases = {}
erros = {}

for nome, caminho in ARQUIVOS.items():

    try:
        bases[nome] = carregar_base(caminho)

    except Exception as erro:

        erros[nome] = str(erro)


# ============================================================
# CABEÇALHO
# ============================================================

st.markdown(
    '<div class="hero-title">☀️ Energia em Dados</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="hero-subtitle">'
    'Inteligência de dados aplicada ao setor elétrico brasileiro'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# ALERTAS DE CARREGAMENTO
# ============================================================

if erros:

    for nome, erro in erros.items():

        st.warning(
            f"A base {nome} não pôde ser carregada: {erro}"
        )


# ============================================================
# VISÃO GERAL
# ============================================================

st.markdown(
    '<div class="section-title">Visão geral</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">'
    'Panorama das bases disponíveis na camada Trusted.'
    '</div>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)


with col1:

    if "Solar" in bases:

        card(
            "Base Solar",
            formatar_numero(len(bases["Solar"])),
            "registros mensais"
        )

    else:

        card("Base Solar", "—")


with col2:

    if "ENA" in bases:

        card(
            "Base ENA",
            formatar_numero(len(bases["ENA"])),
            "registros"
        )

    else:

        card("Base ENA", "—")


with col3:

    if "Bandeiras" in bases:

        card(
            "Base Tarifária",
            formatar_numero(len(bases["Bandeiras"])),
            "registros"
        )

    else:

        card("Base Tarifária", "—")


# ============================================================
# NAVEGAÇÃO
# ============================================================

st.markdown("<hr>", unsafe_allow_html=True)

abas = st.tabs(
    [
        "☀️ Solar",
        "💧 ENA",
        "⚡ Bandeiras",
        "📚 Metodologia"
    ]
)


# ============================================================
# ABA SOLAR
# ============================================================

with abas[0]:

    if "Solar" not in bases:

        st.error("A base Solar não está disponível.")

    else:

        df = bases["Solar"].copy()

        # ----------------------------------------------------
        # IDENTIFICAÇÃO DAS COLUNAS
        # ----------------------------------------------------

        col_mes = encontrar_coluna(
            df,
            ["mes", "Mes", "data", "Data"]
        )

        col_novas = encontrar_coluna(
            df,
            ["novas_conexoes", "NovasConexoes"]
        )

        col_pot_nova = encontrar_coluna(
            df,
            ["potencia_nova_kw", "PotenciaNovaKW"]
        )

        col_pot_acum_kw = encontrar_coluna(
            df,
            ["potencia_acumulada_kw", "PotenciaAcumuladaKW"]
        )

        col_pot_acum_mw = encontrar_coluna(
            df,
            ["potencia_acumulada_mw", "PotenciaAcumuladaMW"]
        )

        col_conexoes_acum = encontrar_coluna(
            df,
            ["conexoes_acumuladas", "ConexoesAcumuladas"]
        )


        # ----------------------------------------------------
        # DATA
        # ----------------------------------------------------

        if col_mes:

            df[col_mes] = pd.to_datetime(
                df[col_mes].astype(str),
                errors="coerce"
            )

            df = df.sort_values(col_mes)

        # ----------------------------------------------------
        # BANNER
        # ----------------------------------------------------

        st.markdown(
            """
            <div class="solar-banner">

                <div class="solar-banner-title">
                    Panorama da geração distribuída fotovoltaica
                </div>

                <div class="solar-banner-text">
                    Evolução das conexões e da potência fotovoltaica
                    registrada na base nacional.
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


        # ----------------------------------------------------
        # KPIs
        # ----------------------------------------------------

        k1, k2, k3, k4 = st.columns(4)


        with k1:

            if col_conexoes_acum:

                valor = df[col_conexoes_acum].iloc[-1]

                card(
                    "Conexões acumuladas",
                    formatar_numero(valor),
                    "último período disponível"
                )


        with k2:

            if col_pot_acum_mw:

                valor = df[col_pot_acum_mw].iloc[-1]

                card(
                    "Potência acumulada",
                    f"{valor:,.1f} MW".replace(",", "X")
                    .replace(".", ",")
                    .replace("X", "."),
                    "último período disponível"
                )


        with k3:

            if col_novas:

                valor = df[col_novas].sum()

                card(
                    "Novas conexões",
                    formatar_numero(valor),
                    "total registrado na série"
                )


        with k4:

            if col_pot_nova:

                valor = df[col_pot_nova].sum()

                card(
                    "Nova potência",
                    f"{valor:,.1f} kW".replace(",", "X")
                    .replace(".", ",")
                    .replace("X", "."),
                    "total registrado na série"
                )


        # ----------------------------------------------------
        # GRÁFICO — CONEXÕES
        # ----------------------------------------------------

        if col_mes and col_conexoes_acum:

            st.markdown(
                '<div class="section-title">'
                'Evolução das conexões fotovoltaicas'
                '</div>',
                unsafe_allow_html=True
            )

            grafico = df[
                [col_mes, col_conexoes_acum]
            ].dropna()

            grafico = grafico.set_index(col_mes)

            st.line_chart(
                grafico,
                height=400
            )


        # ----------------------------------------------------
        # GRÁFICOS DE POTÊNCIA
        # ----------------------------------------------------

        col_a, col_b = st.columns(2)


        with col_a:

            if col_mes and col_pot_acum_mw:

                st.markdown(
                    '<div class="section-title">'
                    'Potência acumulada'
                    '</div>',
                    unsafe_allow_html=True
                )

                grafico = df[
                    [col_mes, col_pot_acum_mw]
                ].dropna()

                grafico = grafico.set_index(col_mes)

                st.area_chart(
                    grafico,
                    height=350
                )


        with col_b:

            if col_mes and col_pot_nova:

                st.markdown(
                    '<div class="section-title">'
                    'Nova potência por período'
                    '</div>',
                    unsafe_allow_html=True
                )

                grafico = df[
                    [col_mes, col_pot_nova]
                ].dropna()

                grafico = grafico.set_index(col_mes)

                st.bar_chart(
                    grafico,
                    height=350
                )


        # ----------------------------------------------------
        # TABELA
        # ----------------------------------------------------

        st.markdown(
            '<div class="section-title">'
            'Dados consolidados'
            '</div>',
            unsafe_allow_html=True
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# ABA ENA
# ============================================================

with abas[1]:

    if "ENA" not in bases:

        st.error("A base ENA não está disponível.")

    else:

        df = bases["ENA"].copy()

        st.markdown(
            """
            <div class="solar-banner">

                <div class="solar-banner-title">
                    Energia Natural Afluente
                </div>

                <div class="solar-banner-text">
                    Base de apoio para análise do contexto energético
                    brasileiro.
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


        col1, col2 = st.columns(2)

        with col1:

            card(
                "Registros",
                formatar_numero(len(df)),
                "base ENA"
            )

        with col2:

            card(
                "Variáveis",
                str(len(df.columns)),
                "colunas disponíveis"
            )


        st.markdown(
            '<div class="section-title">Prévia dos dados</div>',
            unsafe_allow_html=True
        )

        st.dataframe(
            df.head(20),
            use_container_width=True,
            hide_index=True
        )


        with st.expander("Ver estrutura da base"):

            st.dataframe(
                pd.DataFrame(
                    {
                        "Coluna": df.columns,
                        "Tipo": [
                            str(tipo)
                            for tipo in df.dtypes
                        ]
                    }
                ),
                use_container_width=True,
                hide_index=True
            )


# ============================================================
# ABA BANDEIRAS
# ============================================================

with abas[2]:

    if "Bandeiras" not in bases:

        st.error("A base de Bandeiras não está disponível.")

    else:

        df = bases["Bandeiras"].copy()

        st.markdown(
            """
            <div class="solar-banner">

                <div class="solar-banner-title">
                    Bandeiras Tarifárias
                </div>

                <div class="solar-banner-text">
                    Informações tarifárias utilizadas como contexto
                    para o setor elétrico.
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


        col1, col2 = st.columns(2)

        with col1:

            card(
                "Registros",
                formatar_numero(len(df)),
                "base de bandeiras"
            )

        with col2:

            card(
                "Variáveis",
                str(len(df.columns)),
                "colunas disponíveis"
            )


        st.markdown(
            '<div class="section-title">Prévia dos dados</div>',
            unsafe_allow_html=True
        )

        st.dataframe(
            df.head(20),
            use_container_width=True,
            hide_index=True
        )


        with st.expander("Ver estrutura da base"):

            st.dataframe(
                pd.DataFrame(
                    {
                        "Coluna": df.columns,
                        "Tipo": [
                            str(tipo)
                            for tipo in df.dtypes
                        ]
                    }
                ),
                use_container_width=True,
                hide_index=True
            )


# ============================================================
# ABA METODOLOGIA
# ============================================================

with abas[3]:

    st.markdown(
        '<div class="section-title">'
        'Metodologia e arquitetura dos dados'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        ### Arquitetura

        O dashboard utiliza dados disponibilizados na camada
        **Trusted** do projeto.

        As bases são armazenadas em formato **Parquet** e
        consumidas pelo aplicativo desenvolvido em **Streamlit**.

        ### Bases utilizadas

        **Solar**
        - Série mensal de geração distribuída fotovoltaica.
        - Conexões novas e acumuladas.
        - Potência nova e acumulada.

        **ENA**
        - Base de Energia Natural Afluente.

        **Bandeiras**
        - Base de bandeiras tarifárias.

        ### Objetivo

        O painel tem como objetivo transformar as bases tratadas
        em uma interface visual para exploração e comunicação
        dos principais indicadores do setor energético.
        """
    )


# ============================================================
# RODAPÉ
# ============================================================

st.markdown(
    """
    <div class="footer">
        Energia em Dados · MBA Engenharia de Dados ·
        Projeto de análise do setor elétrico brasileiro
    </div>
    """,
    unsafe_allow_html=True
)
