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

/* =========================================================
   FUNDO GERAL
   ========================================================= */

.stApp {
    background:
        radial-gradient(
            circle at 5% 0%,
            rgba(255, 193, 7, 0.10),
            transparent 25%
        ),
        radial-gradient(
            circle at 95% 5%,
            rgba(0, 119, 255, 0.08),
            transparent 28%
        ),
        repeating-linear-gradient(
            90deg,
            rgba(16,42,67,0.018) 0px,
            rgba(16,42,67,0.018) 1px,
            transparent 1px,
            transparent 80px
        ),
        linear-gradient(
            180deg,
            #f7f9fc 0%,
            #eef3f8 100%
        );
}

.block-container {
    max-width: 1450px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}


/* =========================================================
   HEADER PRINCIPAL
   ========================================================= */

.hero {
    padding: 10px 0 30px 0;
    border-bottom: 1px solid #d8e2ec;
    margin-bottom: 22px;
}

.hero-topline {
    color: #1677ff;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 8px;
}

.hero-title {
    font-size: 40px;
    font-weight: 850;
    letter-spacing: -2px;
    color: #102a43;
    line-height: 1.05;
}

.hero-subtitle {
    color: #627d98;
    font-size: 14px;
    margin-top: 8px;
}

.sun {
    font-size: 36px;
}


/* =========================================================
   CABEÇALHOS DE SEÇÃO
   ========================================================= */

.section-header {
    margin-top: 34px;
    margin-bottom: 18px;
    padding-left: 15px;
    border-left: 4px solid #f4b942;
}

.section-number {
    color: #1677ff;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 1.8px;
    margin-bottom: 4px;
}

.section-title {
    font-size: 23px;
    font-weight: 850;
    color: #102a43;
    letter-spacing: -0.5px;
}

.section-description {
    color: #627d98;
    font-size: 13px;
    margin-top: 5px;
}


/* =========================================================
   BANNER
   ========================================================= */

.banner {
    position: relative;
    overflow: hidden;

    background:
        radial-gradient(
            circle at 92% 15%,
            rgba(255,209,102,0.20),
            transparent 24%
        ),
        radial-gradient(
            circle at 70% 100%,
            rgba(22,119,255,0.12),
            transparent 35%
        ),
        linear-gradient(
            135deg,
            #071d35,
            #0b3559
        );

    border-radius: 20px;
    padding: 28px 32px;
    margin: 25px 0;

    box-shadow:
        0 14px 40px rgba(7,29,53,0.14);
}

.banner-label {
    color: #8ec5ff;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 7px;
}

.banner-title {
    color: #ffd166;
    font-size: 21px;
    font-weight: 850;
}

.banner-text {
    color: #d9e8f5;
    font-size: 13px;
    line-height: 1.7;
    max-width: 900px;
    margin-top: 9px;
}


/* =========================================================
   KPIs
   ========================================================= */

.kpi {
    background: rgba(255,255,255,0.96);
    border: 1px solid #d9e2ec;
    border-radius: 17px;
    padding: 20px;
    min-height: 130px;

    box-shadow:
        0 8px 25px rgba(16,42,67,0.055);
}

.kpi:hover {
    border-color: #b7c8d9;
}

.kpi-label {
    color: #627d98;
    font-size: 10px;
    font-weight: 850;
    letter-spacing: 1px;
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
    margin-top: 7px;
}


/* =========================================================
   CARDS DE METODOLOGIA
   ========================================================= */

.info-box {
    background: rgba(255,255,255,0.94);
    border: 1px solid #d9e2ec;
    border-radius: 17px;
    padding: 23px;
    min-height: 170px;

    box-shadow:
        0 8px 25px rgba(16,42,67,0.045);
}

.info-label {
    color: #1677ff;
    font-size: 10px;
    font-weight: 850;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    margin-bottom: 10px;
}

.info-title {
    color: #102a43;
    font-size: 18px;
    font-weight: 800;
    margin-bottom: 10px;
}

.info-text {
    color: #627d98;
    font-size: 12px;
    line-height: 1.7;
}


/* =========================================================
   TABS
   ========================================================= */

.stTabs [data-baseweb="tab-list"] {
    gap: 28px;
    border-bottom: 1px solid #d9e2ec;
}

.stTabs [data-baseweb="tab"] {
    font-weight: 750;
    color: #627d98;
}

.stTabs [aria-selected="true"] {
    color: #102a43 !important;
}


/* =========================================================
   RODAPÉ
   ========================================================= */

.footer {
    text-align: center;
    color: #829ab1;
    font-size: 10px;
    padding-top: 50px;
    letter-spacing: 0.3px;
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
    except Exception:
        return None


df_solar = carregar_base(arquivos["Solar"])
df_ena = carregar_base(arquivos["ENA"])
df_bandeiras = carregar_base(arquivos["Bandeiras"])


# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def preparar_data(df, coluna="mes"):

    if df is None:
        return None

    df = df.copy()

    if coluna not in df.columns:
        return df

    df[coluna] = pd.to_datetime(
        df[coluna],
        errors="coerce"
    )

    df = df.dropna(subset=[coluna])

    return df.sort_values(coluna).reset_index(drop=True)


def formatar_numero(valor):

    if pd.isna(valor):
        return "—"

    return f"{valor:,.0f}".replace(",", ".")


def formatar_decimal(valor, casas=1):

    if pd.isna(valor):
        return "—"

    return (
        f"{valor:,.{casas}f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )


def grafico_base(fig, altura=400):

    fig.update_layout(
        height=altura,
        margin=dict(
            l=15,
            r=15,
            t=55,
            b=25
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.78)",

        font=dict(
            family="Arial",
            color="#102a43"
        ),

        hovermode="x unified",

        xaxis=dict(
            showgrid=False,
            linecolor="#d9e2ec"
        ),

        yaxis=dict(
            gridcolor="#e6edf3",
            zeroline=False
        ),

        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0
        )
    )

    return fig


def cabecalho_secao(numero, titulo, descricao):

    st.markdown(
        f"""
        <div class="section-header">

            <div class="section-number">
                {numero}
            </div>

            <div class="section-title">
                {titulo}
            </div>

            <div class="section-description">
                {descricao}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="hero">

        <div class="hero-topline">
            DATA INTELLIGENCE • ENERGY
        </div>

        <div class="hero-title">
            <span class="sun">☀️</span>
            ENERGIA EM DADOS
        </div>

        <div class="hero-subtitle">
            Inteligência de dados aplicada ao setor elétrico brasileiro
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


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
            "Não foi possível carregar a base Solar. "
            "Verifique o arquivo na camada Trusted."
        )

    else:

        df = preparar_data(df_solar)

        if df.empty:

            st.error(
                "A base Solar foi carregada, mas não possui "
                "registros válidos."
            )

        else:

            # ------------------------------------------------
            # DADOS PRINCIPAIS
            # ------------------------------------------------

            ultima = df.iloc[-1]

            conexoes = ultima.get(
                "conexoes_acumuladas",
                0
            )

            potencia_mw = ultima.get(
                "potencia_acumulada_mw",
                0
            )

            periodo_inicio = df["mes"].min().strftime("%m/%Y")
            periodo_fim = df["mes"].max().strftime("%m/%Y")

            periodo = (
                f"{periodo_inicio} – {periodo_fim}"
            )

            total_registros = len(df)


            # ------------------------------------------------
            # BANNER
            # ------------------------------------------------

            st.markdown(
                """
                <div class="banner">

                    <div class="banner-label">
                        01 / GERAÇÃO DISTRIBUÍDA
                    </div>

                    <div class="banner-title">
                        ☀ PANORAMA DA ENERGIA SOLAR
                    </div>

                    <div class="banner-text">
                        Acompanhe a expansão da geração distribuída
                        fotovoltaica por meio da evolução das conexões,
                        da capacidade instalada e dos principais
                        indicadores da série histórica.
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


            # ------------------------------------------------
            # KPIs
            # ------------------------------------------------

            cabecalho_secao(
                "01",
                "Visão executiva",
                "Principais indicadores da série histórica disponível."
            )

            c1, c2, c3, c4 = st.columns(4)


            with c1:

                st.markdown(
                    f"""
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
                    """,
                    unsafe_allow_html=True
                )


            with c2:

                st.markdown(
                    f"""
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
                    """,
                    unsafe_allow_html=True
                )


            with c3:

                st.markdown(
                    f"""
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
                    """,
                    unsafe_allow_html=True
                )


            with c4:

                st.markdown(
                    f"""
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
                    """,
                    unsafe_allow_html=True
                )


            # ------------------------------------------------
            # EVOLUÇÃO
            # ------------------------------------------------

            cabecalho_secao(
                "02",
                "Evolução da geração distribuída",
                "Crescimento acumulado das conexões e da potência fotovoltaica."
            )

            c1, c2 = st.columns(2)


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

                    st.plotly_chart(
                        grafico_base(fig),
                        use_container_width=True,
                        config={"displayModeBar": False}
                    )


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

                    st.plotly_chart(
                        grafico_base(fig),
                        use_container_width=True,
                        config={"displayModeBar": False}
                    )


            # ------------------------------------------------
            # EXPANSÃO DA CAPACIDADE
            # ------------------------------------------------

            if "potencia_nova_kw" in df.columns:

                cabecalho_secao(
                    "03",
                    "Expansão da capacidade",
                    "Potência adicionada em cada período da série."
                )

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

                st.plotly_chart(
                    grafico_base(fig, 390),
                    use_container_width=True,
                    config={"displayModeBar": False}
                )


            # ------------------------------------------------
            # VISÃO ANUAL
            # ------------------------------------------------

            if "novas_conexoes" in df.columns:

                cabecalho_secao(
                    "04",
                    "Visão anual",
                    "Consolidação das novas conexões por ano."
                )

                df["ano"] = df["mes"].dt.year

                anual = (
                    df
                    .groupby("ano")["novas_conexoes"]
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

                st.plotly_chart(
                    grafico_base(fig, 390),
                    use_container_width=True,
                    config={"displayModeBar": False}
                )


            # ------------------------------------------------
            # DADOS
            # ------------------------------------------------

            cabecalho_secao(
                "05",
                "Dados consolidados",
                "Prévia da camada utilizada na visualização."
            )

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

        df = preparar_data(df_ena)

        if df.empty:

            st.error(
                "A base ENA não possui registros válidos."
            )

        else:

            st.markdown(
                """
                <div class="banner">

                    <div class="banner-label">
                        02 / ENERGIA NATURAL AFLUENTE
                    </div>

                    <div class="banner-title">
                        ⚡ ENERGIA NATURAL AFLUENTE
                    </div>

                    <div class="banner-text">
                        Exploração visual dos indicadores de Energia
                        Natural Afluente e sua relação com o histórico
                        do sistema elétrico brasileiro.
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

            cabecalho_secao(
                "01",
                "Indicadores da ENA",
                "Evolução dos principais indicadores disponíveis na base."
            )

            st.metric(
                "Registros disponíveis",
                formatar_numero(len(df))
            )

            colunas_ena = [
                coluna
                for coluna in df.columns
                if coluna != "mes"
                and pd.api.types.is_numeric_dtype(df[coluna])
            ]

            if colunas_ena:

                coluna_principal = (
                    "ena_nacional_mwmed"
                    if "ena_nacional_mwmed" in df.columns
                    else colunas_ena[0]
                )

                fig = go.Figure()

                fig.add_trace(
                    go.Scatter(
                        x=df["mes"],
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

                st.plotly_chart(
                    grafico_base(fig, 420),
                    use_container_width=True,
                    config={"displayModeBar": False}
                )


            cabecalho_secao(
                "02",
                "Dados consolidados",
                "Prévia dos indicadores disponíveis na camada Trusted."
            )

            st.dataframe(
                df.tail(12),
                use_container_width=True,
                hide_index=True
            )


# ============================================================
# ABA BANDEIRAS
# ============================================================

with tab_bandeiras:

    if df_bandeiras is None:

        st.error(
            "Não foi possível carregar a base de Bandeiras Tarifárias."
        )

    else:

        df = preparar_data(df_bandeiras)

        if df.empty:

            st.error(
                "A base de Bandeiras não possui registros válidos."
            )

        else:

            st.markdown(
                """
                <div class="banner">

                    <div class="banner-label">
                        03 / SINALIZAÇÃO TARIFÁRIA
                    </div>

                    <div class="banner-title">
                        🏭 BANDEIRAS TARIFÁRIAS
                    </div>

                    <div class="banner-text">
                        Visualização da evolução das bandeiras tarifárias
                        e dos indicadores associados ao período analisado.
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

            cabecalho_secao(
                "01",
                "Evolução das bandeiras",
                "Histórico do indicador disponível na base."
            )

            coluna_valor = None

            for candidato in [
                "VlrAdicionalBandeira",
                "nivel"
            ]:

                if candidato in df.columns:

                    coluna_valor = candidato
                    break


            if coluna_valor:

                fig = go.Figure()

                fig.add_trace(
                    go.Scatter(
                        x=df["mes"],
                        y=df[coluna_valor],
                        mode="lines",
                        name=coluna_valor,
                        line=dict(
                            color="#f4b942",
                            width=3
                        )
                    )
                )

                fig.update_layout(
                    title=coluna_valor
                )

                st.plotly_chart(
                    grafico_base(fig, 420),
                    use_container_width=True,
                    config={"displayModeBar": False}
                )


            cabecalho_secao(
                "02",
                "Dados consolidados",
                "Prévia dos registros disponíveis."
            )

            st.dataframe(
                df.tail(12),
                use_container_width=True,
                hide_index=True
            )


# ============================================================
# ABA METODOLOGIA
# ============================================================

with tab_metodologia:

    st.markdown(
        """
        <div class="banner">

            <div class="banner-label">
                04 / DATA ARCHITECTURE
            </div>

            <div class="banner-title">
                📚 METODOLOGIA E ESTRUTURA
            </div>

            <div class="banner-text">
                Visão geral da organização dos dados e da arquitetura
                utilizada para transformar bases tratadas em uma
                camada visual de apoio à análise.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    cabecalho_secao(
        "01",
        "Camada de dados",
        "Organização das bases utilizadas pelo dashboard."
    )

    c1, c2 = st.columns(2)


    with c1:

        st.markdown(
            """
            <div class="info-box">

                <div class="info-label">
                    DATA LAYER
                </div>

                <div class="info-title">
                    Camada Trusted
                </div>

                <div class="info-text">
                    Os dados utilizados na visualização são
                    disponibilizados em arquivos Parquet na camada
                    Trusted do projeto.
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with c2:

        st.markdown(
            """
            <div class="info-box">

                <div class="info-label">
                    VISUAL LAYER
                </div>

                <div class="info-title">
                    Streamlit
                </div>

                <div class="info-text">
                    A aplicação utiliza Streamlit para estruturar
                    a interface e Plotly para construir as
                    visualizações interativas.
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    cabecalho_secao(
        "02",
        "Bases utilizadas",
        "Principais conjuntos de dados apresentados no dashboard."
    )

    c1, c2, c3 = st.columns(3)


    with c1:

        st.markdown(
            """
            <div class="info-box">

                <div class="info-label">
                    BASE 01
                </div>

                <div class="info-title">
                    ☀ Solar
                </div>

                <div class="info-text">
                    Indicadores mensais da geração distribuída
                    fotovoltaica.
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with c2:

        st.markdown(
            """
            <div class="info-box">

                <div class="info-label">
                    BASE 02
                </div>

                <div class="info-title">
                    ⚡ ENA
                </div>

                <div class="info-text">
                    Indicadores de Energia Natural Afluente
                    utilizados na análise do setor elétrico.
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with c3:

        st.markdown(
            """
            <div class="info-box">

                <div class="info-label">
                    BASE 03
                </div>

                <div class="info-title">
                    🏭 Bandeiras
                </div>

                <div class="info-text">
                    Informações relacionadas às bandeiras
                    tarifárias e seus respectivos indicadores.
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    cabecalho_secao(
        "03",
        "Arquitetura simplificada",
        "Fluxo conceitual utilizado para disponibilização dos dados."
    )

    st.markdown(
        """
        <div class="info-box">

            <div class="info-text"
                 style="font-family: monospace; line-height: 2.2;">

                Fontes de dados
                <br>
                ↓
                <br>
                Camada Raw
                <br>
                ↓
                <br>
                Camada Trusted
                <br>
                ↓
                <br>
                Dados consolidados
                <br>
                ↓
                <br>
                Dashboard Streamlit
                <br>
                ↓
                <br>
                Visualização e análise

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        ENERGIA EM DADOS • MBA EM ENGENHARIA DE DADOS
        • Projeto de análise do setor elétrico brasileiro
    </div>
    """,
    unsafe_allow_html=True
)
