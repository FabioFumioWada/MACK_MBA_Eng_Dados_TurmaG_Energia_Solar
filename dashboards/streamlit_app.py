import streamlit as st
import pandas as pd

# ============================================================
# CONFIGURAÇÃO
# ============================================================

st.set_page_config(
    page_title="Energia em Dados",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================
# IDENTIDADE VISUAL
# ============================================================

st.markdown(
    """
    <style>
    .stApp {
        background:
            radial-gradient(circle at 4% 0%, rgba(255,193,7,.11), transparent 24%),
            radial-gradient(circle at 96% 4%, rgba(0,119,255,.09), transparent 28%),
            repeating-linear-gradient(
                90deg,
                rgba(16,42,67,.018) 0px,
                rgba(16,42,67,.018) 1px,
                transparent 1px,
                transparent 80px
            ),
            linear-gradient(180deg, #f7f9fc 0%, #eef3f8 100%);
    }

    .block-container {
        max-width: 1450px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    .hero {
        padding: 10px 0 28px 0;
        border-bottom: 1px solid #d8e2ec;
        margin-bottom: 18px;
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

    .section {
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
        letter-spacing: -.5px;
    }

    .section-description {
        color: #627d98;
        font-size: 13px;
        margin-top: 5px;
    }

    .banner {
        background:
            radial-gradient(circle at 92% 15%, rgba(255,209,102,.20), transparent 24%),
            radial-gradient(circle at 70% 100%, rgba(22,119,255,.13), transparent 35%),
            linear-gradient(135deg, #071d35, #0b3559);
        border-radius: 20px;
        padding: 28px 32px;
        margin: 24px 0;
        box-shadow: 0 14px 40px rgba(7,29,53,.14);
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
        max-width: 950px;
        margin-top: 9px;
    }

    .kpi {
        background: rgba(255,255,255,.96);
        border: 1px solid #d9e2ec;
        border-radius: 17px;
        padding: 20px;
        min-height: 125px;
        box-shadow: 0 8px 25px rgba(16,42,67,.055);
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
        font-size: 27px;
        font-weight: 850;
        letter-spacing: -1px;
    }

    .kpi-caption {
        color: #829ab1;
        font-size: 11px;
        margin-top: 7px;
    }

    .info-box {
        background: rgba(255,255,255,.94);
        border: 1px solid #d9e2ec;
        border-radius: 17px;
        padding: 23px;
        min-height: 170px;
        box-shadow: 0 8px 25px rgba(16,42,67,.045);
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

    div[data-testid="stDataFrame"] {
        border: 1px solid #d9e2ec;
        border-radius: 14px;
        overflow: hidden;
    }

    .footer {
        text-align: center;
        color: #829ab1;
        font-size: 10px;
        padding-top: 50px;
        letter-spacing: .3px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# CAMINHOS DAS BASES
# ============================================================

ARQUIVOS = {
    "Solar": "./trusted/solar_mensal_nacional.parquet",
    "ENA": "./trusted/ena_mensal.parquet",
    "Bandeiras": "./trusted/bandeira_mensal.parquet",
}

# ============================================================
# FUNÇÕES
# ============================================================

@st.cache_data
def carregar_base(caminho):
    try:
        return pd.read_parquet(caminho)
    except Exception:
        return None


def preparar_data(df, coluna="mes"):
    if df is None:
        return None

    df = df.copy()

    if coluna in df.columns:
        df[coluna] = pd.to_datetime(
            df[coluna].astype(str),
            errors="coerce"
        )
        df = df.dropna(subset=[coluna])
        df = df.sort_values(coluna).reset_index(drop=True)

    return df


def numero(valor, casas=0):
    if valor is None or pd.isna(valor):
        return "—"

    if casas == 0:
        return f"{valor:,.0f}".replace(",", ".")
    return (
        f"{valor:,.{casas}f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )


def secao(numero_secao, titulo, descricao):
    st.markdown(
        f"""
        <div class="section">
            <div class="section-number">{numero_secao}</div>
            <div class="section-title">{titulo}</div>
            <div class="section-description">{descricao}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def kpi(coluna, titulo, valor, legenda):
    with coluna:
        st.markdown(
            f"""
            <div class="kpi">
                <div class="kpi-label">{titulo}</div>
                <div class="kpi-value">{valor}</div>
                <div class="kpi-caption">{legenda}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def banner(label, titulo, texto):
    st.markdown(
        f"""
        <div class="banner">
            <div class="banner-label">{label}</div>
            <div class="banner-title">{titulo}</div>
            <div class="banner-text">{texto}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def grafico(df, coluna_data, coluna_valor, titulo, tipo="line"):
    if df is None or coluna_data not in df.columns or coluna_valor not in df.columns:
        st.info(f"Dados insuficientes para o gráfico: {titulo}.")
        return

    dados = df[[coluna_data, coluna_valor]].copy()
    dados[coluna_valor] = pd.to_numeric(dados[coluna_valor], errors="coerce")
    dados = dados.dropna()

    if dados.empty:
        st.info(f"Não há dados válidos para: {titulo}.")
        return

    dados = dados.set_index(coluna_data)

    if tipo == "bar":
        st.bar_chart(dados[coluna_valor], use_container_width=True)
    else:
        st.line_chart(dados[coluna_valor], use_container_width=True)


# ============================================================
# CARREGAMENTO
# ============================================================

df_solar = preparar_data(carregar_base(ARQUIVOS["Solar"]))
df_ena = preparar_data(carregar_base(ARQUIVOS["ENA"]))
df_bandeiras = preparar_data(carregar_base(ARQUIVOS["Bandeiras"]))

# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="hero">
        <div class="hero-topline">DATA INTELLIGENCE • ENERGY</div>
        <div class="hero-title">
            <span class="sun">☀️</span> ENERGIA EM DADOS
        </div>
        <div class="hero-subtitle">
            Inteligência de dados aplicada ao setor elétrico brasileiro
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# ABAS
# ============================================================

tab_solar, tab_ena, tab_bandeiras, tab_metodologia = st.tabs(
    ["☀ Solar", "⚡ ENA", "🏭 Bandeiras", "📚 Metodologia"]
)

# ============================================================
# SOLAR
# ============================================================

with tab_solar:

    if df_solar is None or df_solar.empty:
        st.error(
            "A base Solar não pôde ser carregada ou não possui registros válidos. "
            "Verifique ./trusted/solar_mensal_nacional.parquet."
        )
    else:
        banner(
            "01 / GERAÇÃO DISTRIBUÍDA",
            "☀ PANORAMA DA ENERGIA SOLAR",
            "Acompanhe a expansão da geração distribuída fotovoltaica "
            "por meio da evolução das conexões, da capacidade instalada "
            "e dos principais indicadores da série histórica."
        )

        ultima = df_solar.iloc[-1]

        conexoes = ultima.get("conexoes_acumuladas", None)
        potencia_mw = ultima.get("potencia_acumulada_mw", None)

        inicio = df_solar["mes"].min().strftime("%m/%Y")
        fim = df_solar["mes"].max().strftime("%m/%Y")

        secao(
            "01",
            "Visão executiva",
            "Principais indicadores da série histórica disponível."
        )

        c1, c2, c3, c4 = st.columns(4)

        kpi(c1, "CONEXÕES ACUMULADAS", numero(conexoes), "último período disponível")
        kpi(c2, "POTÊNCIA ACUMULADA", f"{numero(potencia_mw, 1)} MW", "capacidade instalada")
        kpi(c3, "PERÍODO ANALISADO", f"{inicio} – {fim}", "série mensal")
        kpi(c4, "REGISTROS MENSAIS", numero(len(df_solar)), "observações disponíveis")

        secao(
            "02",
            "Evolução da geração distribuída",
            "Crescimento acumulado das conexões e da capacidade fotovoltaica."
        )

        a, b = st.columns(2)

        with a:
            st.markdown("**Conexões acumuladas**")
            grafico(
                df_solar,
                "mes",
                "conexoes_acumuladas",
                "Conexões acumuladas"
            )

        with b:
            st.markdown("**Potência acumulada (MW)**")
            grafico(
                df_solar,
                "mes",
                "potencia_acumulada_mw",
                "Potência acumulada"
            )

        secao(
            "03",
            "Expansão da capacidade",
            "Potência adicionada em cada período da série histórica."
        )

        st.markdown("**Nova potência instalada por período (kW)**")
        grafico(
            df_solar,
            "mes",
            "potencia_nova_kw",
            "Nova potência",
            tipo="bar"
        )

        secao(
            "04",
            "Visão anual",
            "Consolidação das novas conexões por ano."
        )

        anual = (
            df_solar
            .assign(ano=df_solar["mes"].dt.year)
            .groupby("ano", as_index=False)["novas_conexoes"]
            .sum()
        )

        anual["ano"] = anual["ano"].astype(str)
        anual = anual.set_index("ano")

        st.bar_chart(
            anual["novas_conexoes"],
            use_container_width=True
        )

        secao(
            "05",
            "Dados consolidados",
            "Amostra da base utilizada para a visualização."
        )

        st.dataframe(
            df_solar.tail(12),
            use_container_width=True,
            hide_index=True
        )

# ============================================================
# ENA
# ============================================================

with tab_ena:

    if df_ena is None or df_ena.empty:
        st.error(
            "A base ENA não pôde ser carregada ou não possui registros válidos."
        )
    else:
        banner(
            "02 / ENERGIA NATURAL AFLUENTE",
            "⚡ ENERGIA NATURAL AFLUENTE",
            "Exploração visual dos indicadores de Energia Natural Afluente "
            "disponíveis na base consolidada."
        )

        secao(
            "01",
            "Visão da base ENA",
            "Indicadores disponíveis e comportamento da série histórica."
        )

        c1, c2, c3 = st.columns(3)

        kpi(c1, "REGISTROS", numero(len(df_ena)), "observações disponíveis")
        kpi(c2, "VARIÁVEIS", numero(len(df_ena.columns)), "colunas na base")
        kpi(
            c3,
            "PERÍODO",
            f"{df_ena['mes'].min().strftime('%m/%Y')} – {df_ena['mes'].max().strftime('%m/%Y')}",
            "série disponível"
        )

        secao(
            "02",
            "Indicadores ENA",
            "Evolução temporal dos principais indicadores percentuais."
        )

        colunas_ena = [
            c for c in df_ena.columns
            if c != "mes" and pd.api.types.is_numeric_dtype(df_ena[c])
        ]

        if colunas_ena:
            selecionadas = st.multiselect(
                "Selecione os indicadores",
                colunas_ena,
                default=colunas_ena[:min(3, len(colunas_ena))]
            )

            if selecionadas:
                dados_ena = df_ena[["mes"] + selecionadas].copy()
                dados_ena = dados_ena.set_index("mes")
                st.line_chart(dados_ena, use_container_width=True)
        else:
            st.info("Não foram encontradas colunas numéricas na base ENA.")

        secao(
            "03",
            "Dados consolidados",
            "Amostra dos registros mais recentes."
        )

        st.dataframe(
            df_ena.tail(12),
            use_container_width=True,
            hide_index=True
        )

# ============================================================
# BANDEIRAS
# ============================================================

with tab_bandeiras:

    if df_bandeiras is None or df_bandeiras.empty:
        st.error(
            "A base de Bandeiras não pôde ser carregada ou não possui registros válidos."
        )
    else:
        banner(
            "03 / BANDEIRAS TARIFÁRIAS",
            "🏭 BANDEIRAS TARIFÁRIAS",
            "Visualização dos dados históricos de bandeiras tarifárias "
            "e dos respectivos adicionais registrados."
        )

        secao(
            "01",
            "Visão da base",
            "Panorama dos registros disponíveis."
        )

        c1, c2, c3 = st.columns(3)

        kpi(c1, "REGISTROS", numero(len(df_bandeiras)), "observações disponíveis")
        kpi(c2, "VARIÁVEIS", numero(len(df_bandeiras.columns)), "colunas na base")

        if "NomBandeiraAcionada" in df_bandeiras.columns:
            categorias = df_bandeiras["NomBandeiraAcionada"].nunique()
        else:
            categorias = 0

        kpi(c3, "CATEGORIAS", numero(categorias), "bandeiras identificadas")

        secao(
            "02",
            "Evolução das bandeiras",
            "Comportamento temporal do adicional registrado."
        )

        coluna_valor = "VlrAdicionalBandeira"

        if coluna_valor in df_bandeiras.columns:
            dados_bandeiras = df_bandeiras[
                ["mes", coluna_valor]
            ].copy()

            dados_bandeiras[coluna_valor] = pd.to_numeric(
                dados_bandeiras[coluna_valor],
                errors="coerce"
            )

            dados_bandeiras = (
                dados_bandeiras
                .dropna()
                .set_index("mes")
            )

            st.line_chart(
                dados_bandeiras[coluna_valor],
                use_container_width=True
            )
        else:
            st.info(
                "A coluna VlrAdicionalBandeira não está disponível "
                "na base atual."
            )

        secao(
            "03",
            "Dados consolidados",
            "Amostra dos registros mais recentes."
        )

        st.dataframe(
            df_bandeiras.tail(12),
            use_container_width=True,
            hide_index=True
        )

# ============================================================
# METODOLOGIA
# ============================================================

with tab_metodologia:

    banner(
        "04 / ARQUITETURA DE DADOS",
        "📚 METODOLOGIA E ESTRUTURA",
        "Visão geral das bases utilizadas e da arquitetura simplificada "
        "adotada para disponibilizar os dados em uma camada visual."
    )

    secao(
        "01",
        "Camada de dados",
        "Bases utilizadas na construção do dashboard."
    )

    c1, c2 = st.columns(2)

    with c1:
        st.markdown(
            """
            <div class="info-box">
                <div class="info-label">DATA LAYER</div>
                <div class="info-title">Camada Trusted</div>
                <div class="info-text">
                    Os dados utilizados pelo dashboard são arquivos
                    em formato Parquet armazenados na camada Trusted
                    do projeto.
                    <br><br>
                    <b>Bases utilizadas:</b><br>
                    • Solar<br>
                    • ENA<br>
                    • Bandeiras tarifárias
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            """
            <div class="info-box">
                <div class="info-label">VISUALIZATION LAYER</div>
                <div class="info-title">Streamlit</div>
                <div class="info-text">
                    A aplicação foi construída em Streamlit,
                    utilizando componentes nativos para facilitar
                    a exploração visual e a leitura dos indicadores.
                    <br><br>
                    O objetivo é transformar as bases tratadas em
                    uma camada visual de apoio à análise.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    secao(
        "02",
        "Arquitetura simplificada",
        "Fluxo conceitual entre dados e visualização."
    )

    st.code(
        """Fontes de dados
        ↓
Camada Raw
        ↓
Camada Trusted
        ↓
Dados consolidados
        ↓
Dashboard Streamlit
        ↓
Visualização e análise""",
        language="text",
    )

    secao(
        "03",
        "Transparência da análise",
        "Indicadores apresentados a partir das bases disponíveis no repositório."
    )

    st.info(
        "O dashboard é uma camada de visualização. "
        "As métricas e gráficos dependem diretamente das bases "
        "Parquet existentes na camada Trusted."
    )

# ============================================================
# RODAPÉ
# ============================================================

st.markdown(
    """
    <div class="footer">
        ENERGIA EM DADOS • MBA EM ENGENHARIA DE DADOS •
        Projeto de análise do setor elétrico brasileiro
    </div>
    """,
    unsafe_allow_html=True,
)
