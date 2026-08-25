import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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

st.markdown("""
<style>

    /* ---------- FUNDO ---------- */

    .stApp {
        background:
            radial-gradient(circle at 10% 10%,
                rgba(30, 136, 229, 0.06),
                transparent 25%),
            radial-gradient(circle at 90% 80%,
                rgba(255, 193, 7, 0.06),
                transparent 25%),
            #f6f9fc;
        color: #102a43;
    }

    /* ---------- CONTAINER ---------- */

    .block-container {
        max-width: 1400px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* ---------- TÍTULOS ---------- */

    h1, h2, h3 {
        color: #102a43 !important;
        letter-spacing: -0.5px;
    }

    h1 {
        font-size: 2.4rem !important;
        font-weight: 750 !important;
    }

    h2 {
        font-size: 1.35rem !important;
        font-weight: 700 !important;
    }

    /* ---------- HEADER ---------- */

    .hero {
        padding: 10px 0 25px 0;
        border-bottom: 1px solid #d9e2ec;
        margin-bottom: 25px;
    }

    .hero-title {
        font-size: 38px;
        font-weight: 800;
        color: #102a43;
        letter-spacing: -1.5px;
    }

    .hero-subtitle {
        color: #627d98;
        font-size: 15px;
        margin-top: 3px;
    }

    .sun {
        font-size: 38px;
        vertical-align: middle;
    }

    /* ---------- KPI CARDS ---------- */

    .kpi {
        background: white;
        border: 1px solid #d9e2ec;
        border-radius: 14px;
        padding: 20px 22px;
        box-shadow: 0 5px 18px rgba(16, 42, 67, 0.06);
        min-height: 120px;
    }

    .kpi-label {
        color: #627d98;
        font-size: 13px;
        font-weight: 600;
        margin-bottom: 10px;
    }

    .kpi-value {
        color: #102a43;
        font-size: 28px;
        font-weight: 800;
        letter-spacing: -0.8px;
    }

    .kpi-caption {
        color: #829ab1;
        font-size: 12px;
        margin-top: 5px;
    }

    /* ---------- SEÇÃO ---------- */

    .section-title {
        font-size: 20px;
        font-weight: 750;
        color: #102a43;
        margin-top: 35px;
        margin-bottom: 4px;
    }

    .section-description {
        color: #627d98;
        font-size: 13px;
        margin-bottom: 18px;
    }

    .accent-line {
        border-left: 4px solid #f9c74f;
        padding-left: 12px;
    }

    /* ---------- BANNER ---------- */

    .solar-banner {
        background:
            radial-gradient(circle at 90% 10%,
                rgba(42, 157, 244, 0.18),
                transparent 30%),
            linear-gradient(135deg, #071d35, #0b2d4d);
        color: white;
        border-radius: 16px;
        padding: 25px 28px;
        margin: 20px 0 25px 0;
        box-shadow: 0 10px 30px rgba(7, 29, 53, 0.15);
    }

    .solar-banner-title {
        font-size: 20px;
        font-weight: 750;
        color: #ffd166;
    }

    .solar-banner-text {
        color: #d9e8f5;
        font-size: 14px;
        line-height: 1.6;
        margin-top: 8px;
        max-width: 800px;
    }

    /* ---------- CHART CARDS ---------- */

    .chart-card {
        background: white;
        border: 1px solid #d9e2ec;
        border-radius: 14px;
        padding: 8px 10px 2px 10px;
        box-shadow: 0 5px 18px rgba(16, 42, 67, 0.05);
    }

    /* ---------- TABELA ---------- */

    .data-card {
        background: white;
        border: 1px solid #d9e2ec;
        border-radius: 14px;
        padding: 20px;
        box-shadow: 0 5px 18px rgba(16, 42, 67, 0.05);
    }

    /* ---------- INFO CARD ---------- */

    .info-card {
        background: linear-gradient(145deg, #071d35, #0c3559);
        color: white;
        border-radius: 14px;
        padding: 24px;
        min-height: 250px;
        box-shadow: 0 8px 25px rgba(7, 29, 53, 0.15);
    }

    .info-title {
        color: #ffd166;
        font-size: 18px;
        font-weight: 750;
        margin-bottom: 18px;
    }

    .info-item {
        margin: 14px 0;
    }

    .info-label {
        color: #9fb3c8;
        font-size: 12px;
    }

    .info-value {
        color: white;
        font-size: 14px;
        font-weight: 600;
    }

    /* ---------- TABS ---------- */

    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
        border-bottom: 1px solid #d9e2ec;
    }

    .stTabs [data-baseweb="tab"] {
        color: #627d98;
        font-weight: 600;
        padding-left: 5px;
        padding-right: 5px;
    }

    .stTabs [aria-selected="true"] {
        color: #102a43 !important;
    }

    /* ---------- FOOTER ---------- */

    .footer {
        text-align: center;
        color: #829ab1;
        font-size: 12px;
        padding-top: 40px;
        padding-bottom: 15px;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# CARREGAMENTO DAS BASES
# ============================================================

arquivos = {
    "Bandeiras": "./trusted/bandeiras_mensal.parquet",
    "ENA": "./trusted/ena_mensal.parquet",
    "Solar": "./trusted/solar_mensal.parquet"
}


@st.cache_data
def carregar_base(caminho):
    try:
        return pd.read_parquet(caminho)
    except Exception:
        return None


df_solar = carregar_base(arquivos["Solar"])
df_ena = carregar_base(arquivos["ENA"])
df_bandeiras = carregar_base(arquivos["Bandeiras"])


# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div class="hero">

<div class="hero-title">
<span class="sun">☀️</span> ENERGIA EM DADOS
</div>

<div class="hero-subtitle">
Intelligence for the Brazilian Energy Sector
</div>

</div>
""", unsafe_allow_html=True)


# ============================================================
# ABAS
# ============================================================

tab_solar, tab_ena, tab_bandeiras, tab_metodologia = st.tabs([
    "☀ Solar",
    "⚡ ENA",
    "🏭 Bandeiras",
    "📚 Metodologia"
])


# ============================================================
# SOLAR
# ============================================================

with tab_solar:

    if df_solar is None:

        st.error(
            "Não foi possível carregar a base Solar. "
            "Verifique o arquivo em ./trusted/solar_mensal.parquet"
        )

    else:

        # ----------------------------------------------------
        # PREPARAÇÃO
        # ----------------------------------------------------

        df = df_solar.copy()

        if "mes" in df.columns:
            df["mes"] = pd.to_datetime(df["mes"], errors="coerce")

        df = df.sort_values("mes")

        # ----------------------------------------------------
        # KPIs
        # ----------------------------------------------------

        ultima_linha = df.iloc[-1]

        conexoes = ultima_linha.get("conexoes_acumuladas", 0)

        potencia_mw = ultima_linha.get(
            "potencia_acumulada_mw", 0
        )

        periodo = (
            df["mes"].min().strftime("%Y")
            + " – "
            + df["mes"].max().strftime("%Y")
        )

        nova_potencia = df["potencia_nova_kw"].max() / 1000

        # ----------------------------------------------------
        # PANORAMA
        # ----------------------------------------------------

        st.markdown("""
        <div class="solar-banner">

        <div class="solar-banner-title">
        ☀ PANORAMA SOLAR
        </div>

        <div class="solar-banner-text">
        A geração distribuída fotovoltaica no Brasil apresenta forte
        expansão ao longo da série histórica, permitindo acompanhar
        a evolução das conexões e da capacidade instalada.
        </div>

        </div>
        """, unsafe_allow_html=True)

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.markdown(f"""
            <div class="kpi">
                <div class="kpi-label">CONEXÕES ACUMULADAS</div>
                <div class="kpi-value">{conexoes:,.0f}</div>
                <div class="kpi-caption">último período disponível</div>
            </div>
            """.replace(",", "."), unsafe_allow_html=True)

        with c2:
            st.markdown(f"""
            <div class="kpi">
                <div class="kpi-label">POTÊNCIA ACUMULADA</div>
                <div class="kpi-value">{potencia_mw:,.1f} MW</div>
                <div class="kpi-caption">capacidade instalada</div>
            </div>
            """.replace(",", "X").replace(".", ",").replace("X", "."), unsafe_allow_html=True)

        with c3:
            st.markdown(f"""
            <div class="kpi">
                <div class="kpi-label">PERÍODO DA SÉRIE</div>
                <div class="kpi-value">{periodo}</div>
                <div class="kpi-caption">dados mensais</div>
            </div>
            """, unsafe_allow_html=True)

        with c4:
            st.markdown(f"""
            <div class="kpi">
                <div class="kpi-label">MAIOR NOVA POTÊNCIA MENSAL</div>
                <div class="kpi-value">{nova_potencia:,.1f} MW</div>
                <div class="kpi-caption">pico observado</div>
            </div>
            """.replace(",", "X").replace(".", ",").replace("X", "."), unsafe_allow_html=True)

        # ----------------------------------------------------
        # EVOLUÇÃO
        # ----------------------------------------------------

        st.markdown("""
        <div class="section-title accent-line">
        EVOLUÇÃO DA GERAÇÃO DISTRIBUÍDA SOLAR
        </div>

        <div class="section-description">
        Série histórica mensal de conexões e potência fotovoltaica
        </div>
        """, unsafe_allow_html=True)

        # ----------------------------------------------------
        # GRÁFICO 1
        # ----------------------------------------------------

        fig_conexoes = go.Figure()

        fig_conexoes.add_trace(
            go.Scatter(
                x=df["mes"],
                y=df["conexoes_acumuladas"],
                mode="lines",
                name="Conexões",
                line=dict(
                    color="#1677ff",
                    width=3
                ),
                fill="tozeroy",
                fillcolor="rgba(22,119,255,0.10)"
            )
        )

        fig_conexoes.update_layout(
            title="Conexões acumuladas",
            height=390,
            margin=dict(l=20, r=20, t=55, b=20),
            plot_bgcolor="white",
            paper_bgcolor="white",
            hovermode="x unified",
            font=dict(
                family="Arial",
                color="#102a43"
            ),
            xaxis=dict(
                showgrid=False,
                title=""
            ),
            yaxis=dict(
                gridcolor="#edf2f7",
                title=""
            )
        )

        # ----------------------------------------------------
        # GRÁFICO 2
        # ----------------------------------------------------

        fig_potencia = go.Figure()

        fig_potencia.add_trace(
            go.Scatter(
                x=df["mes"],
                y=df["potencia_acumulada_mw"],
                mode="lines",
                name="Potência",
                line=dict(
                    color="#1f9d8b",
                    width=3
                ),
                fill="tozeroy",
                fillcolor="rgba(31,157,139,0.10)"
            )
        )

        fig_potencia.update_layout(
            title="Potência acumulada (MW)",
            height=390,
            margin=dict(l=20, r=20, t=55, b=20),
            plot_bgcolor="white",
            paper_bgcolor="white",
            hovermode="x unified",
            font=dict(
                family="Arial",
                color="#102a43"
            ),
            xaxis=dict(
                showgrid=False,
                title=""
            ),
            yaxis=dict(
                gridcolor="#edf2f7",
                title=""
            )
        )

        c1, c2 = st.columns(2)

        with c1:
            st.plotly_chart(
                fig_conexoes,
                use_container_width=True,
                config={"displayModeBar": False}
            )

        with c2:
            st.plotly_chart(
                fig_potencia,
                use_container_width=True,
                config={"displayModeBar": False}
            )

        # ----------------------------------------------------
        # GRÁFICO 3
        # ----------------------------------------------------

        fig_nova = px.bar(
            df,
            x="mes",
            y="potencia_nova_kw",
            title="Nova potência por período (kW)"
        )

        fig_nova.update_traces(
            marker_color="#1677ff"
        )

        fig_nova.update_layout(
            height=360,
            margin=dict(l=20, r=20, t=55, b=20),
            plot_bgcolor="white",
            paper_bgcolor="white",
            font=dict(
                family="Arial",
                color="#102a43"
            ),
            xaxis=dict(showgrid=False),
            yaxis=dict(gridcolor="#edf2f7")
        )

        # ----------------------------------------------------
        # GRÁFICO 4
        # ----------------------------------------------------

        fig_acumulada = go.Figure()

        fig_acumulada.add_trace(
            go.Scatter(
                x=df["mes"],
                y=df["potencia_acumulada_mw"],
                mode="lines",
                line=dict(
                    color="#f9b233",
                    width=3
                ),
                fill="tozeroy",
                fillcolor="rgba(249,178,51,0.15)"
            )
        )

        fig_acumulada.update_layout(
            title="Potência acumulada (MW)",
            height=360,
            margin=dict(l=20, r=20, t=55, b=20),
            plot_bgcolor="white",
            paper_bgcolor="white",
            font=dict(
                family="Arial",
                color="#102a43"
            ),
            xaxis=dict(showgrid=False),
            yaxis=dict(gridcolor="#edf2f7")
        )

        c1, c2 = st.columns(2)

        with c1:
            st.plotly_chart(
                fig_nova,
                use_container_width=True,
                config={"displayModeBar": False}
            )

        with c2:
            st.plotly_chart(
                fig_acumulada,
                use_container_width=True,
                config={"displayModeBar": False}
            )

        # ----------------------------------------------------
        # DADOS CONSOLIDADOS
        # ----------------------------------------------------

        st.markdown("""
        <div class="section-title accent-line">
        DADOS CONSOLIDADOS
        </div>

        <div class="section-description">
        Últimos registros disponíveis na base tratada
        </div>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns([2.1, 1])

        with c1:

            st.markdown(
                '<div class="data-card">',
                unsafe_allow_html=True
            )

            st.dataframe(
                df.tail(10).sort_values(
                    "mes",
                    ascending=False
                ),
                use_container_width=True,
                hide_index=True
            )

            st.markdown("</div>", unsafe_allow_html=True)

        with c2:

            st.markdown("""
            <div class="info-card">

            <div class="info-title">
            ☀ SOBRE A BASE SOLAR
            </div>

            <div class="info-item">
            <div class="info-label">PERIODICIDADE</div>
            <div class="info-value">Mensal</div>
            </div>

            <div class="info-item">
            <div class="info-label">FONTE</div>
            <div class="info-value">
            ANEEL — Geração Distribuída
            </div>
            </div>

            <div class="info-item">
            <div class="info-label">DADOS</div>
            <div class="info-value">
            Conexões e potência instalada
            </div>
            </div>

            <div class="info-item">
            <div class="info-label">ÚLTIMO PERÍODO</div>
            <div class="info-value">
            """ + df["mes"].max().strftime("%B/%Y") + """
            </div>
            </div>

            </div>
            """, unsafe_allow_html=True)


# ============================================================
# ENA
# ============================================================

with tab_ena:

    st.markdown("""
    <div class="section-title accent-line">
    ENERGIA NATURAL AFLUENTE
    </div>

    <div class="section-description">
    Indicadores históricos de Energia Natural Afluente.
    </div>
    """, unsafe_allow_html=True)

    if df_ena is not None:

        st.metric(
            "Registros disponíveis",
            f"{len(df_ena):,}".replace(",", ".")
        )

        st.dataframe(
            df_ena.tail(20),
            use_container_width=True,
            hide_index=True
        )

    else:

        st.warning(
            "Base ENA não encontrada em ./trusted/ena_mensal.parquet"
        )


# ============================================================
# BANDEIRAS
# ============================================================

with tab_bandeiras:

    st.markdown("""
    <div class="section-title accent-line">
    BANDEIRAS TARIFÁRIAS
    </div>

    <div class="section-description">
    Histórico de bandeiras tarifárias do setor elétrico brasileiro.
    </div>
    """, unsafe_allow_html=True)

    if df_bandeiras is not None:

        st.metric(
            "Registros disponíveis",
            f"{len(df_bandeiras):,}".replace(",", ".")
        )

        st.dataframe(
            df_bandeiras.tail(20),
            use_container_width=True,
            hide_index=True
        )

    else:

        st.warning(
            "Base de bandeiras não encontrada em ./trusted/bandeiras_mensal.parquet"
        )


# ============================================================
# METODOLOGIA
# ============================================================

with tab_metodologia:

    st.markdown("""
    <div class="section-title accent-line">
    METODOLOGIA
    </div>

    <div class="section-description">
    Estrutura de dados utilizada no projeto.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    ### Arquitetura de dados

    O projeto utiliza uma organização em camadas para tratamento
    e disponibilização dos dados.

    **Raw → Trusted → Dashboard**

    ### Fontes

    - ANEEL
    - Dados públicos do setor elétrico brasileiro

    ### Tecnologias

    - Python
    - Pandas
    - Parquet
    - Streamlit
    - Plotly
    - GitHub

    ### Objetivo

    Transformar dados públicos do setor elétrico em informações
    estruturadas para exploração, análise e visualização.
    """)


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">

Energia em Dados &nbsp;•&nbsp;
MBA Engenharia de Dados &nbsp;•&nbsp;
Projeto de análise do setor elétrico brasileiro

</div>
""", unsafe_allow_html=True)
