import streamlit as st
import pandas as pd
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

.stApp {
    background:
        radial-gradient(
            circle at 10% 0%,
            rgba(255, 193, 7, 0.10),
            transparent 28%
        ),
        radial-gradient(
            circle at 90% 15%,
            rgba(0, 119, 255, 0.08),
            transparent 30%
        ),
        linear-gradient(
            180deg,
            #f5f8fc 0%,
            #eef3f8 100%
        );
    color: #102a43;
}

.block-container {
    max-width: 1450px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

/* HEADER */

.hero {
    padding: 12px 0 28px 0;
    border-bottom: 1px solid #d8e2ec;
    margin-bottom: 25px;
}

.hero-title {
    font-size: 38px;
    font-weight: 850;
    letter-spacing: -1.8px;
    color: #102a43;
}

.hero-subtitle {
    color: #627d98;
    font-size: 14px;
    margin-top: 4px;
}

.sun {
    font-size: 36px;
}

/* SECTION */

.section-title {
    font-size: 21px;
    font-weight: 800;
    color: #102a43;
    margin-top: 30px;
    margin-bottom: 5px;
}

.section-description {
    color: #627d98;
    font-size: 13px;
    margin-bottom: 18px;
}

/* KPI */

.kpi {
    background: rgba(255,255,255,0.94);
    border: 1px solid #d9e2ec;
    border-radius: 16px;
    padding: 20px;
    min-height: 125px;
    box-shadow: 0 8px 25px rgba(16,42,67,0.06);
}

.kpi:hover {
    border-color: #b7c8d9;
}

.kpi-label {
    color: #627d98;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 0.8px;
    margin-bottom: 10px;
}

.kpi-value {
    color: #102a43;
    font-size: 28px;
    font-weight: 850;
    letter-spacing: -1px;
}

.kpi-caption {
    color: #829ab1;
    font-size: 11px;
    margin-top: 6px;
}

/* BANNER */

.banner {
    background:
        radial-gradient(
            circle at 90% 20%,
            rgba(255,209,102,0.22),
            transparent 25%
        ),
        linear-gradient(
            135deg,
            #071d35,
            #0b3559
        );

    border-radius: 18px;
    padding: 25px 30px;
    margin: 25px 0;

    box-shadow:
        0 12px 35px rgba(7,29,53,0.15);
}

.banner-title {
    color: #ffd166;
    font-size: 20px;
    font-weight: 800;
}

.banner-text {
    color: #d9e8f5;
    font-size: 13px;
    line-height: 1.7;
    max-width: 900px;
    margin-top: 8px;
}

/* CHART CONTAINER */

.chart-header {
    font-size: 15px;
    font-weight: 750;
    color: #102a43;
    margin-top: 15px;
}

/* TABS */

.stTabs [data-baseweb="tab-list"] {
    gap: 24px;
    border-bottom: 1px solid #d9e2ec;
}

.stTabs [data-baseweb="tab"] {
    font-weight: 700;
    color: #627d98;
}

.stTabs [aria-selected="true"] {
    color: #102a43 !important;
}

/* INFO */

.info-box {
    background: white;
    border: 1px solid #d9e2ec;
    border-radius: 16px;
    padding: 22px;
    box-shadow: 0 8px 25px rgba(16,42,67,0.05);
}

.footer {
    text-align: center;
    color: #829ab1;
    font-size: 11px;
    padding-top: 45px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# CAMINHOS DAS BASES
# ============================================================

arquivos = {
    "Solar": "./trusted/solar_mensal_nacional.parquet",
    "ENA": "./trusted/ena_mensal.parquet",
    "Bandeiras": "./trusted/bandeira_mensal.parquet"
}


# ============================================================
# CARREGAMENTO
# ============================================================

@st.cache_data
def carregar_base(caminho):
    try:
        return pd.read_parquet(caminho)
    except Exception as erro:
        return None


df_solar = carregar_base(arquivos["Solar"])
df_ena = carregar_base(arquivos["ENA"])
df_bandeiras = carregar_base(arquivos["Bandeiras"])


# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def formatar_numero(valor):
    if pd.isna(valor):
        return "—"

    return f"{valor:,.0f}".replace(",", ".")


def formatar_decimal(valor, casas=1):
    if pd.isna(valor):
        return "—"

    return f"{valor:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def estilo_grafico(fig, altura=400):

    fig.update_layout(
        height=altura,
        margin=dict(l=20, r=20, t=55, b=30),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.75)",
        font=dict(
            family="Arial",
            color="#102a43"
        ),
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0
        ),
        xaxis=dict(
            showgrid=False
        ),
        yaxis=dict(
            gridcolor="#e6edf3"
        )
    )

    return fig


# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div class="hero">

    <div class="hero-title">
        <span class="sun">☀️</span>
        ENERGIA EM DADOS
    </div>

    <div class="hero-subtitle">
        Inteligência de dados aplicada ao setor elétrico brasileiro
    </div>

</div>
""", unsafe_allow_html=True)


# ============================================================
# ABAS
# ============================================================

tab_solar, tab_ena, tab_bandeiras, tab_metodologia = st.tabs(
    [
        "☀ Solar",
        "⚡ ENA",
        "🏭 Bandeiras",
        "📚 Metodologia"
    ]
)


# ============================================================
# ABA SOLAR
# ============================================================

with tab_solar:

    if df_solar is None:

        st.error(
            "Não foi possível carregar a base Solar."
        )

    else:

    df = df_solar.copy()

st.write("DEBUG - colunas:", df.columns.tolist())
st.write("DEBUG - quantidade de linhas:", len(df))
st.write("DEBUG - primeiros valores de mes:", df["mes"].head(10).tolist())
st.write("DEBUG - tipo original de mes:", df["mes"].dtype)

        # ----------------------------------------------------
        # VARIÁVEIS
        # ----------------------------------------------------

        ultima = df.iloc[-1]

        conexoes = ultima.get(
            "conexoes_acumuladas",
            0
        )

        potencia_mw = ultima.get(
            "potencia_acumulada_mw",
            0
        )

        periodo_inicio = (
            df["mes"].min().strftime("%m/%Y")
            if "mes" in df.columns
            else "—"
        )

        periodo_fim = (
            df["mes"].max().strftime("%m/%Y")
            if "mes" in df.columns
            else "—"
        )

        periodo = (
            f"{periodo_inicio} – {periodo_fim}"
        )

        # ----------------------------------------------------
        # BANNER
        # ----------------------------------------------------

        st.markdown("""
        <div class="banner">

            <div class="banner-title">
                ☀ PANORAMA DA GERAÇÃO DISTRIBUÍDA SOLAR
            </div>

            <div class="banner-text">
                Acompanhe a evolução das conexões fotovoltaicas,
                da potência instalada e dos principais indicadores
                da série histórica disponível.
            </div>

        </div>
        """, unsafe_allow_html=True)

        # ----------------------------------------------------
        # KPIs
        # ----------------------------------------------------

        c1, c2, c3, c4 = st.columns(4)

        with c1:

            st.markdown(f"""
            <div class="kpi">

                <div class="kpi-label">
                    CONEXÕES ACUMULADAS
                </div>

                <div class="kpi-value">
                    {formatar_numero(conexoes)}
                </div>

                <div class="kpi-caption">
                    último período disponível
                </div>

            </div>
            """, unsafe_allow_html=True)

        with c2:

            st.markdown(f"""
            <div class="kpi">

                <div class="kpi-label">
                    POTÊNCIA ACUMULADA
                </div>

                <div class="kpi-value">
                    {formatar_decimal(potencia_mw)} MW
                </div>

                <div class="kpi-caption">
                    capacidade instalada
                </div>

            </div>
            """, unsafe_allow_html=True)

        with c3:

            st.markdown(f"""
            <div class="kpi">

                <div class="kpi-label">
                    PERÍODO ANALISADO
                </div>

                <div class="kpi-value">
                    {periodo}
                </div>

                <div class="kpi-caption">
                    série mensal
                </div>

            </div>
            """, unsafe_allow_html=True)

        with c4:

            total_registros = len(df)

            st.markdown(f"""
            <div class="kpi">

                <div class="kpi-label">
                    REGISTROS MENSAIS
                </div>

                <div class="kpi-value">
                    {formatar_numero(total_registros)}
                </div>

                <div class="kpi-caption">
                    observações disponíveis
                </div>

            </div>
            """, unsafe_allow_html=True)

        # ----------------------------------------------------
        # EVOLUÇÃO
        # ----------------------------------------------------

        st.markdown("""
        <div class="section-title">
            Evolução da geração distribuída
        </div>

        <div class="section-description">
            Crescimento acumulado das conexões e da potência
            fotovoltaica ao longo da série histórica.
        </div>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns(2)

        # ----------------------------------------------------
        # CONEXÕES
        # ----------------------------------------------------

        with c1:

            if "conexoes_acumuladas" in df.columns:

                fig = go.Figure()

                fig.add_trace(
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

                fig.update_layout(
                    title="Conexões acumuladas"
                )

                fig = estilo_grafico(fig)

                st.plotly_chart(
                    fig,
                    use_container_width=True,
                    config={"displayModeBar": False}
                )

        # ----------------------------------------------------
        # POTÊNCIA
        # ----------------------------------------------------

        with c2:

            if "potencia_acumulada_mw" in df.columns:

                fig = go.Figure()

                fig.add_trace(
                    go.Scatter(
                        x=df["mes"],
                        y=df["potencia_acumulada_mw"],
                        mode="lines",
                        name="Potência",
                        line=dict(
                            color="#18a999",
                            width=3
                        ),
                        fill="tozeroy",
                        fillcolor="rgba(24,169,153,0.10)"
                    )
                )

                fig.update_layout(
                    title="Potência acumulada (MW)"
                )

                fig = estilo_grafico(fig)

                st.plotly_chart(
                    fig,
                    use_container_width=True,
                    config={"displayModeBar": False}
                )

        # ----------------------------------------------------
        # NOVA POTÊNCIA
        # ----------------------------------------------------

        if "potencia_nova_kw" in df.columns:

            st.markdown("""
            <div class="section-title">
                Expansão da capacidade
            </div>

            <div class="section-description">
                Potência adicionada em cada período da série.
            </div>
            """, unsafe_allow_html=True)

            fig = go.Figure()

            fig.add_trace(
                go.Bar(
                    x=df["mes"],
                    y=df["potencia_nova_kw"],
                    name="Nova potência",
                    marker_color="#f4b942"
                )
            )

            fig.update_layout(
                title="Nova potência instalada por período (kW)"
            )

            fig = estilo_grafico(fig, 380)

            st.plotly_chart(
                fig,
                use_container_width=True,
                config={"displayModeBar": False}
            )

        # ----------------------------------------------------
        # RESUMO ANUAL
        # ----------------------------------------------------

        if (
            "mes" in df.columns
            and "novas_conexoes" in df.columns
        ):

            st.markdown("""
            <div class="section-title">
                Visão anual
            </div>

            <div class="section-description">
                Consolidação anual das novas conexões.
            </div>
            """, unsafe_allow_html=True)

            df["ano"] = df["mes"].dt.year

            anual = (
                df.groupby("ano")["novas_conexoes"]
                .sum()
                .reset_index()
            )

            fig = go.Figure()

            fig.add_trace(
                go.Bar(
                    x=anual["ano"],
                    y=anual["novas_conexoes"],
                    name="Novas conexões",
                    marker_color="#1677ff"
                )
            )

            fig.update_layout(
                title="Novas conexões por ano",
                xaxis_title="Ano",
                yaxis_title="Conexões"
            )

            fig = estilo_grafico(fig, 400)

            st.plotly_chart(
                fig,
                use_container_width=True,
                config={"displayModeBar": False}
            )

        # ----------------------------------------------------
        # DADOS
        # ----------------------------------------------------

        st.markdown("""
        <div class="section-title">
            Dados consolidados
        </div>
        """, unsafe_allow_html=True)

        st.dataframe(
            df.tail(12),
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# ABA ENA
# ============================================================

with tab_ena:

    if df_ena is None:

        st.error(
            "Não foi possível carregar a base ENA."
        )

    else:

        df = df_ena.copy()

        if "mes" in df.columns:

            df["mes"] = pd.to_datetime(
                df["mes"],
                errors="coerce"
            )

            df = df.sort_values("mes")

        st.markdown("""
        <div class="banner">

            <div class="banner-title">
                ⚡ ENERGIA NATURAL AFLUENTE
            </div>

            <div class="banner-text">
                Exploração visual dos indicadores disponíveis
                na base ENA.
            </div>

        </div>
        """, unsafe_allow_html=True)

        st.markdown(
            f"**Registros disponíveis:** {len(df):,}".replace(",", ".")
        )

        # Seleciona colunas numéricas
        colunas_numericas = df.select_dtypes(
            include="number"
        ).columns.tolist()

        if colunas_numericas:

            coluna_principal = None

            # Prioriza indicador nacional
            for coluna in colunas_numericas:

                if "nacional" in coluna.lower():

                    coluna_principal = coluna
                    break

            if coluna_principal is None:

                coluna_principal = colunas_numericas[0]

            fig = go.Figure()

            fig.add_trace(
                go.Scatter(
                    x=df["mes"] if "mes" in df.columns else df.index,
                    y=df[coluna_principal],
                    mode="lines",
                    name=coluna_principal,
                    line=dict(
                        color="#1677ff",
                        width=3
                    )
                )
            )

            fig.update_layout(
                title=coluna_principal
            )

            fig = estilo_grafico(fig)

            st.plotly_chart(
                fig,
                use_container_width=True,
                config={"displayModeBar": False}
            )

        st.dataframe(
            df.tail(15),
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# ABA BANDEIRAS
# ============================================================

with tab_bandeiras:

    if df_bandeiras is None:

        st.error(
            "Não foi possível carregar a base de bandeiras."
        )

    else:

        df = df_bandeiras.copy()

        if "mes" in df.columns:

            df["mes"] = pd.to_datetime(
                df["mes"],
                errors="coerce"
            )

            df = df.sort_values("mes")

        st.markdown("""
        <div class="banner">

            <div class="banner-title">
                🏭 BANDEIRAS TARIFÁRIAS
            </div>

            <div class="banner-text">
                Visualização dos dados disponíveis na base
                de bandeiras tarifárias.
            </div>

        </div>
        """, unsafe_allow_html=True)

        colunas_numericas = df.select_dtypes(
            include="number"
        ).columns.tolist()

        if colunas_numericas:

            coluna = colunas_numericas[0]

            fig = go.Figure()

            fig.add_trace(
                go.Scatter(
                    x=df["mes"] if "mes" in df.columns else df.index,
                    y=df[coluna],
                    mode="lines+markers",
                    name=coluna,
                    line=dict(
                        color="#f4b942",
                        width=3
                    )
                )
            )

            fig.update_layout(
                title=coluna
            )

            fig = estilo_grafico(fig)

            st.plotly_chart(
                fig,
                use_container_width=True,
                config={"displayModeBar": False}
            )

        st.dataframe(
            df.tail(15),
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# METODOLOGIA
# ============================================================

with tab_metodologia:

    st.markdown("""
    <div class="section-title">
        Metodologia e estrutura
    </div>

    <div class="section-description">
        Visão geral da organização dos dados utilizados no dashboard.
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:

        st.markdown("""
        <div class="info-box">

        ### Camada de dados

        O dashboard utiliza arquivos em formato Parquet
        armazenados na camada **Trusted** do projeto.

        <br>

        **Bases utilizadas:**

        - Solar
        - ENA
        - Bandeiras tarifárias

        </div>
        """, unsafe_allow_html=True)

    with c2:

        st.markdown("""
        <div class="info-box">

        ### Visualização

        A aplicação foi construída em **Streamlit**,
        utilizando gráficos interativos e componentes
        visuais para facilitar a exploração dos dados.

        <br>

        O objetivo é transformar as bases tratadas em
        uma camada visual de apoio à análise.

        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="section-title">
        Arquitetura simplificada
    </div>
    """, unsafe_allow_html=True)

    st.code(
        """
Fontes de dados
       ↓
Camada Raw
       ↓
Camada Trusted
       ↓
Dados consolidados
       ↓
Dashboard Streamlit
       ↓
Visualização e análise
        """,
        language="text"
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">

ENERGIA EM DADOS · MBA Engenharia de Dados · Projeto acadêmico

</div>
""", unsafe_allow_html=True)
