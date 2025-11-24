import streamlit as st
import pandas as pd
import plotly.express as px
import unicodedata
from pyairtable import Api

# =============================================================================
# CONFIGURACIÓN
# =============================================================================

API_KEY = st.secrets["airtable_mexico_investment"]["api_key"]      #Api key de nuestro airtable
BASE_ID = st.secrets["airtable_mexico_investment"]["base_id"]     #base id del CRM
TABLE_ID_EM = st.secrets["airtable_mexico_investment"]["table_id_em"]     #Tabla con el feedback de los EM's
TABLE_ID_DD = st.secrets["airtable_mexico_investment"]["table_id_team"]      #Tabla con el feedback del equipo de los forms

THRESHOLD = 0.9
TWO_METRIC_THRESHOLD = 0.8

PROGRAM_YEAR = "2025"
PROGRAM_NAME = "Mexico 2025"

# Configuración de Streamlit
st.set_page_config(
    page_title="Informe de Outliers",
    layout="wide"
)

if "selected_year" not in st.session_state:
    st.session_state.selected_year = PROGRAM_YEAR

# Título con logo
st.markdown("""
<style>
.outer-container {
    display: flex;
    justify-content: center;
    width: 100%;
}
.container {
    display: flex;
    align-items: center;
}
.logo-img {
    width: 80px;
    height: 80px;
    margin-right: 20px;
}
.title-text {
    font-size: 2.5em;
    font-weight: bold;
}
.logo-img-card {
    width: 30px;
    height: 30px;
    margin-right: 5px;
}
h4 {
    font-size: 1.2em;
    margin-top: 0.5rem;
    margin-bottom: 0.5rem;
}
</style>
<div class="outer-container">
    <div class="container">
        <img class="logo-img" src="https://images.squarespace-cdn.com/content/v1/67811e8fe702fd5553c65249/c5500619-9712-4b9b-83ee-a697212735ae/Disen%CC%81o+sin+ti%CC%81tulo+%2840%29.png">
        <h1 class="title-text">Decelera Program<br>Informe de Outliers</h1>
    </div>
</div>
""", unsafe_allow_html=True)

# =============================================================================
# SIDEBAR CONFIGURATION
# =============================================================================

# Hide default Streamlit navigation elements
st.markdown("""
    <style>
        [data-testid="stSidebarNav"] {
            display: none;
        }
    </style>
""", unsafe_allow_html=True)

# Custom hierarchical navigation
with st.sidebar:
    # Home button at the top
    if st.button("🏠 Home", key="home_btn", use_container_width=True):
        st.switch_page("Home.py")
    
    st.markdown("---")
    
    # Mexico (Title 1)
    st.markdown("#### Mexico")
    
    # Year selection in sidebar
    st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;**{st.session_state.selected_year}**")

    # Outliers section
    if st.button("Outliers", key="mx_outliers", use_container_width=True):
        st.switch_page(f"pages/Mexico_Outliers_{st.session_state.selected_year}.py")
    
    # Investment section (Title 4)
    st.markdown("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Investment**")
    
    # Investment pages (Title 5)
    if st.button("Risk-Reward Matrix", key="mx_inv_general", use_container_width=True):
        st.switch_page(f"pages/Mexico_Risk_Reward_{st.session_state.selected_year}.py")
    
    if st.button("Individual, Team and Business DD", key="mx_inv_startup", use_container_width=True):
        st.switch_page(f"pages/Mexico_Feedback_Details_{st.session_state.selected_year}.py")
    
    # Program section (Title 4)
    st.markdown("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Program**")
    
    # Program pages (Title 5)
    if st.button("Guests feedback", key="mx_prog_general", use_container_width=True):
        st.switch_page(f"pages/Mexico_Guests_Feedback_{st.session_state.selected_year}.py")
    
    if st.button("Breathe-Focus-Grow", key="mx_prog_agenda", use_container_width=True):
        st.switch_page(f"pages/Mexico_Breathe-Focus-Grow_{st.session_state.selected_year}.py")
    
    st.markdown("---")
    
    # Menorca (Title 1)
    st.markdown("#### Menorca")
    
    # Year selection in sidebar
    st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;**{st.session_state.selected_year}**")
    
    # Investment section (Title 4)
    st.markdown("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Investment**")
    
    # Investment pages (Title 5)
    if st.button("Risk-Reward Matrix", key="mn_inv_general", use_container_width=True):
        st.switch_page(f"pages/Menorca_Risk_Reward_{st.session_state.selected_year}.py")
    
    if st.button("Individual, Team and Business DD", key="mn_inv_startup", use_container_width=True):
        st.switch_page(f"pages/Menorca_Feedback_Details_{st.session_state.selected_year}.py")
    
    # Program section (Title 4)
    st.markdown("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Program**")
    
    # Program pages (Title 5)
    if st.button("Guests feedback", key="mn_prog_general", use_container_width=True):
        st.switch_page(f"pages/Menorca_Guests_Feedback_{st.session_state.selected_year}.py")
    
    if st.button("Breathe-Focus-Grow", key="mn_prog_agenda", use_container_width=True):
        st.switch_page(f"pages/Menorca_Breathe-Focus-Grow_{st.session_state.selected_year}.py")


# =============================================================================
# DATOS ESTÁTICOS
# =============================================================================

startup_founders = {
    "ROOK": ["Marco Benitez", "Jonas Ducker", "Daniel Martinez"],
    "Figuro": ["Juan Camilo Gonzalez"],
    "Admina": ["David Gomez", "Andres Gomez"],
    "Ecosis": ["Enrique Arredondo", "Roberto Riveroll"],
    "CALMIO": ["Andrés Ospina", "Camilo Ospina"],
    "Pitz": ["Natalia Salcedo"],
    "BondUP": ["Michelle Schnitzer"],
    "Jelt": ["Sergio Ramirez"],
    "Moabits SL": ["Alejandro Ortiz", "David Santibanez", "Juan Martin Pawluszek"],
    "Ximple": ["Daniel Sujo", "Joao Ramos", "Clarissa Morrisson"],
    "Kuri": ["Ludwig Pucha Cofrep"],
    "CROMODATA": ["Juan Pablo  Merea Otermin", "Keila Barral Masri", "Matias  Karlsson"],
    "Ternadia": ["Angel Sanchez", "Raul Merino"],
    "Tu Cambio": ["Luis Saavedra", "Carla Leal"],
    "Airbag": ["Adrian Trucios"],
    "Handit.ai": ["Jose Manuel Ramirez", "Cristhian Camilo Gomez"],
    "Verticcal": ["Santiago Gallo Restrepo", "Pablo Sanchez Villamarin"],
    "Neat": ["Nicolas Chacon", "Javier Benavides"],
    "CIFRATO": ["Yerson Cacua", "Juan Pisco"],
    "Konvex": ["Andres Cristobal Sosa Tellez"]
}

founder_list = []
for startup in startup_founders.keys():
    founder_list.extend(startup_founders[startup])

fields = {
    "team": [
        "Castle Contest | Conflict resolution (Team)",
        "Castle Contest | Clear vision and alignment (Team)",
        "Castle Contest | Confidence and respect between founders (Team)",
        "Castle Contest | Clear roles",
        "Castle Contest | Complementary hard skills between founders",
        "Castle Contest | Execution and speed (Team)",
        "1:1's | Team ambition (Team)",
        "1:1's | Product and customer focus (Team)"
    ],
    "individual": [
        "Workstations | Integrity and honesty (Individual)",
        "Workstations | Relevant experience and network (Individual)",
        "Paellas contest | Visionary leadership (Individual)",
        "Paellas contest | Active listening (Individual)",
        "Paellas contest | Flexibility (Individual)",
        "Paellas contest | Self awareness and management of emotions (Individual)",
        "Openness",
        "Purpose",
        "Dilema 1",
        "Dilema 2"
    ],
    "risk_reward": [
        "RISK | State of development_Score",
        "RISK | Momentum_Score",
        "RISK | Management_Score",
        "Reward | Market_Score",
        "Reward | Team_Score",
        "Reward | Pain_Score",
        "Reward | Scalability_Score"
    ],
    "workstations": [
        "Workstations | Challenge clearness (Bussiness)",
        "Workstations | Challenge importance (Bussiness)"
    ]
}

METRICS = {
    "individual": {
        "mean_col": "media_individual",
        "z_col": "z_media_individual",
        "label": "Individual",
    },
    "team": {
        "mean_col": "media_equipo",
        "z_col": "z_media_equipo",
        "label": "Equipo",
    },
    "business": {
        "mean_col": "media_business",
        "z_col": "z_media_business",
        "label": "Business",
    }
}

# =============================================================================
# FUNCIONES AUXILIARES
# =============================================================================

def fix_cell(val):
    """Corrige valores NaN especiales de Airtable"""
    if isinstance(val, dict) and "specialValue" in val:
        return float("nan")
    return val


def normalize_name(s: str) -> str:
    """Normaliza nombres eliminando acentos y estandarizando formato"""
    if not isinstance(s, str):
        return ""
    
    s = unicodedata.normalize("NFKD", s)
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    s = s.lower()
    s = s.replace("\u00A0", " ").replace("\u200b", " ")
    s = " ".join(s.split())
    s = s.strip()
    return s


def metricas_agrupadas(df_to_check, columns_list, field_to_group_by, mean_field_name):
    """
    Calcula la media de las columnas especificadas y agrupa por un campo.
    
    Args:
        df_to_check: DataFrame con los datos
        columns_list: Lista de columnas a promediar
        field_to_group_by: Campo por el cual agrupar
        mean_field_name: Nombre de la columna de media resultante
    
    Returns:
        DataFrame con el campo de agrupación y la media calculada
    """
    if not columns_list:
        return pd.DataFrame(columns=[field_to_group_by, mean_field_name])
    
    # Convertir a numérico
    numeric_columns = df_to_check[columns_list].apply(pd.to_numeric, errors="coerce")
    
    # Calcular media por fila
    df_to_check[mean_field_name] = numeric_columns.mean(axis=1)
    
    # Agrupar si el campo existe
    if field_to_group_by in df_to_check.columns:
        df_output = df_to_check.groupby(field_to_group_by, as_index=False)[mean_field_name].mean()
    else:
        df_output = pd.DataFrame(columns=[field_to_group_by, mean_field_name])
    
    return df_output


def classify_profile(row, threshold):
    """
    Clasifica el perfil de un founder según sus puntuaciones z en las tres métricas.
    
    Args:
        row: Fila del DataFrame con las puntuaciones z
        threshold: Umbral para considerar valores altos/bajos
    
    Returns:
        String con la clasificación del perfil
    """
    zi = row[METRICS["individual"]["z_col"]]
    zt = row[METRICS["team"]["z_col"]]
    zb = row[METRICS["business"]["z_col"]]

    hi_i = zi >= threshold
    lo_i = zi <= -threshold
    hi_t = zt >= threshold
    lo_t = zt <= -threshold
    hi_b = zb >= threshold
    lo_b = zb <= -threshold

    # Clasificaciones ordenadas por prioridad
    if hi_i and hi_t and hi_b:
        return "Strategic profile (high in individual, team and business)"
    
    if hi_i and hi_t and not hi_b and not lo_b:
        return "Solid founder and team, weak business"
    
    if hi_i and (lo_t or lo_b):
        return "Individual talent wasted by team or business"
    
    if hi_t and lo_i and not lo_b:
        return "Strong team, weak business"
    
    if hi_b and (lo_i or lo_t):
        return "Weak founder in a strong project"
    
    if (lo_i and lo_t) or (lo_i and lo_b) or (lo_t and lo_b):
        return "High risk (person/team/business below average)"
    
    if hi_i or hi_t or hi_b:
        return "Promising profile (high in at least one metric)"
    
    return "Nothing to highlight"

def classify_profile_startup(row, threshold):
    """
    Clasifica el perfil de una startup según sus puntuaciones z en las tres métricas.
    
    Args:
        row: Fila del DataFrame con las puntuaciones z
        threshold: Umbral para considerar valores altos/bajos
    
    Returns:
        String con la clasificación del perfil
    """
    zi = "z_media_individual_agg"
    zt = row[METRICS["team"]["z_col"]]
    zb = row[METRICS["business"]["z_col"]]

    hi_i = zi >= threshold
    lo_i = zi <= -threshold
    hi_t = zt >= threshold
    lo_t = zt <= -threshold
    hi_b = zb >= threshold
    lo_b = zb <= -threshold

    # Clasificaciones ordenadas por prioridad
    if hi_i and hi_t and hi_b:
        return "Strategic company (high in individual, team and business)"
    
    if hi_i and hi_t and not hi_b and not lo_b:
        return "Solid founder and team, weak business"
    
    if hi_i and (lo_t or lo_b):
        return "Individual talents wasted by team or business"
    
    if hi_t and lo_i and not lo_b:
        return "Strong team, weak business"
    
    if hi_b and (lo_i or lo_t):
        return "Strong business, weak founders"
    
    if (lo_i and lo_t) or (lo_i and lo_b) or (lo_t and lo_b):
        return "High risk (person/team/business below average)"
    
    if hi_i or hi_t or hi_b:
        return "Promising company (high in at least one metric)"
    
    return "Nothing to highlight"

def scatter_two_dim(df, x_col, y_col, label_x, label_y, third_value, title, label, show_name=True):
    """
    Crea un gráfico de dispersión 2D con Plotly Express.
    """
    if df.empty:
        st.info("No hay datos suficientes para generar este mapa.")
        return

    # LIMPIEZA ADICIONAL: Asegurar que no hay duplicados
    if df.columns.duplicated().any():
        print(f"⚠️ Columnas duplicadas en scatter_two_dim: {df.columns[df.columns.duplicated()].tolist()}")
        df = df.loc[:, ~df.columns.duplicated(keep='first')]
    
    # Verificar que las columnas necesarias existen
    required_cols = [x_col, y_col, "Name", "Startup", "Perfil_exec", third_value]
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        st.error(f"Columnas faltantes en el DataFrame: {missing_cols}")
        return

    MARGIN = 0.15
    
    # Calcular rangos con margen
    x_min, x_max = df[x_col].min(), df[x_col].max()
    x_range = [x_min - x_min * MARGIN, x_max + x_max * MARGIN]
    
    y_min, y_max = df[y_col].min(), df[y_col].max()
    y_range = [y_min - y_min * MARGIN, y_max + y_max * MARGIN]
    
    # Definir tooltips
    tooltip_cols = ["Name", "Startup", "Perfil_exec", x_col, y_col, third_value]
    
    # Crear gráfico
    fig = px.scatter(
        df,
        x=x_col,
        y=y_col,
        color="Perfil_exec",
        text=label,
        custom_data=tooltip_cols,
        title=title,
        labels={
            x_col: f"score {label_x}",
            y_col: f"score {label_y}",
            "Perfil_exec": "Perfil"
        }
    )
    
    # Configurar hover
    if show_name:
        # Incluye Name (customdata[0]) y Startup (customdata[1])
        name_line = f"<b>{tooltip_cols[0]}</b>: %{{customdata[0]}}<br>"
        startup_line = f"<b>{tooltip_cols[1]}</b>: %{{customdata[1]}}<br>"
    else:
        # Si show_name es False, solo mostramos la Startup (y no Name)
        name_line = ""
        startup_line = f"<b>{tooltip_cols[1]}</b>: %{{customdata[1]}}<br>"

    # El resto de la plantilla (Perfil y 3 Medias)
    hover_template = f"""
    {name_line}
    {startup_line}
    <b>{tooltip_cols[2]}</b>: %{{customdata[2]}}<br>
    <br>
    <b>Individual Mean</b>: %{{customdata[3]:.2f}}<br>
    <b>Team Mean</b>: %{{customdata[4]:.2f}}<br>
    <b>Business Mean</b>: %{{customdata[5]:.2f}}<br>
    <extra></extra>
    """
    
    fig.update_traces(
        marker=dict(size=10, opacity=0.85),
        textposition='top center',
        mode='markers',
        hovertemplate=hover_template
    )
    
    # Configurar ejes
    fig.update_xaxes(
        range=x_range,
        title_font={"size": 14},
        zeroline=True,
        zerolinecolor='gray',
        zerolinewidth=1,
    )
    
    fig.update_yaxes(
        range=y_range,
        title_font={"size": 14},
        zeroline=True,
        zerolinecolor='gray',
        zerolinewidth=1,
    )
    
    # Añadir líneas de referencia
    fig.add_hline(y=0, line_dash="dash", line_color="grey")
    fig.add_vline(x=0, line_dash="dash", line_color="grey")
    
    # Layout
    fig.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=40, b=20),
        legend_title_text='Perfil'
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_founder_card(df_founder, show_name=True):
    """
    Renderiza una tarjeta con la información de un founder.
    
    Args:
        df_founder: DataFrame con los datos del founder (una fila)
        show_name: Si True, muestra el nombre; si False, muestra la startup
    """
    individual_mean = df_founder["media_individual"].mean()
    team_mean = df_founder["media_equipo"].mean()
    business_mean = df_founder["media_business"].mean()
    
    # Obtener logo
    row = df_founder.iloc[0]
    logo_data = row.get("original logo")
    if isinstance(logo_data, list) and len(logo_data) > 0 and 'url' in logo_data[0]:
        logo_url = logo_data[0]['url']
    else:
        logo_url = ""
    
    # Determinar qué mostrar
    startup = df_founder["Startup"].iloc[0]
    display_name = df_founder['Name'].iloc[0] if show_name else startup
    category = df_founder["Perfil_exec"].iloc[0] if show_name else df_founder["Perfil_startup"].iloc[0]
    
    with st.container(border=True):
        st.markdown(f"""
            <div style="display: flex; flex-direction: column;">
                <div style="display: flex; align-items: center; margin-bottom: 10px;">
                    <img class="logo-img-card" src="{logo_url}">
                    <h4 style="margin: 0 0 0 10px; font-weight: bold; font-size: 1.2em;">
                        <a href="https://decelera-dashboards.streamlit.app/Mexico_Feedback_Details_{st.session_state.selected_year}?startup={startup}">{display_name}</a>
                    </h4>
                </div>
                <div>
                    <p style='font-size: 0.5em;'>{category}</p>
                </div>
                <div style="display: flex; justify-content: space-around; width: 100%;">
                    <div style="text-align: center;">
                        <p style="font-size: 0.8em; margin-bottom: 0;">Individual Mean</p>
                        <p style="font-size: 1.4em; font-weight: bold; margin-top: 0; margin-bottom: 0;">
                            {round(individual_mean, 2)}
                        </p>
                    </div>
                    <div style="text-align: center;">
                        <p style="font-size: 0.8em; margin-bottom: 0;">Team Mean</p>
                        <p style="font-size: 1.4em; font-weight: bold; margin-top: 0; margin-bottom: 0;">
                            {round(team_mean, 2)}
                        </p>
                    </div>
                    <div style="text-align: center;">
                        <p style="font-size: 0.8em; margin-bottom: 0;">Business Mean</p>
                        <p style="font-size: 1.4em; font-weight: bold; margin-top: 0; margin-bottom: 0;">
                            {round(business_mean, 2)}
                        </p>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)


# =============================================================================
# CARGA DE DATOS
# =============================================================================

api = Api(API_KEY)

# Cargar datos de EM (Entrepreneur Metrics)
try:
    em_records = api.table(BASE_ID, TABLE_ID_EM).all(view=PROGRAM_NAME)
    em_data = [record["fields"] for record in em_records]
    em_df = pd.DataFrame(em_data)
except Exception as e:
    st.error(f"Error al cargar los datos de la tabla de EMs: {e}")
    em_df = pd.DataFrame()

# Cargar datos de DD (Due Diligence)
try:
    dd_records = api.table(BASE_ID, TABLE_ID_DD).all(view=PROGRAM_NAME)
    dd_data = [record["fields"] for record in dd_records]
    dd_df = pd.DataFrame(dd_data)
except Exception as e:
    st.error(f"Error al cargar los datos de la tabla de DDs: {e}")
    dd_df = pd.DataFrame()

# Aplicar corrección de NaN's
em_df = em_df.map(func=fix_cell)
dd_df = dd_df.map(func=fix_cell)

# =============================================================================
# PROCESAMIENTO DE DATOS
# =============================================================================

# Procesar columnas combinadas (Openness y Purpose)
cols_openness = [
    "Workstations | Openness (Individual)",
    "Paellas contest | Openness (Individual)"
]
cols_purpose = [
    "1:1's | Purpose (Individual)",
    "Workstations | Purpose (Individual)"
]

present_cols_openness = [c for c in cols_openness if c in dd_df.columns]
present_cols_purpose = [c for c in cols_purpose if c in dd_df.columns]

if present_cols_openness:
    dd_df["Openness"] = dd_df[present_cols_openness].apply(
        pd.to_numeric, errors="coerce"
    ).mean(axis=1)
else:
    dd_df["Openness"] = pd.Series(dtype=float)

if present_cols_purpose:
    dd_df["Purpose"] = dd_df[present_cols_purpose].apply(
        pd.to_numeric, errors="coerce"
    ).mean(axis=1)
else:
    dd_df["Purpose"] = pd.Series(dtype=float)

# Crear mapeo de personas a startups
person_to_company = {
    person: company
    for company, people in startup_founders.items()
    for person in people
}

df_people = pd.DataFrame(
    [(person, company) for person, company in person_to_company.items()],
    columns=["Name", "Startup"]
)
df_people["Name_norm"] = df_people["Name"].apply(normalize_name)
df_people = df_people.dropna(subset="Startup")

founder_list_norm = []
for founder in founder_list:
    founder_norm = normalize_name(founder)
    founder_list_norm.append(founder_norm)

# Renombrar columna Name si es necesario
if "Founder_str" in dd_df.columns and "Name" not in dd_df.columns:
    dd_df.rename(columns={"Founder_str": "Name"}, inplace=True)
elif "Name" not in dd_df.columns:
    dd_df["Name"] = None

# =============================================================================
# CÁLCULO DE MÉTRICAS
# =============================================================================

# 1. Métricas individuales
individual_cols = [c for c in fields["individual"] if c in dd_df.columns]
df_individual = metricas_agrupadas(dd_df, individual_cols, "Name", "media_individual")
df_individual["Name_norm"] = df_individual["Name"].apply(normalize_name)

# 2. Métricas de equipo
team_cols = [c for c in fields["team"] if c in dd_df.columns]
df_team = metricas_agrupadas(dd_df, team_cols, "Startup", "media_equipo")

# 3. Métricas de business
risk_reward_cols = [c for c in fields["risk_reward"] if c in em_df.columns]
df_business_rr = metricas_agrupadas(em_df, risk_reward_cols, "Startup", "media_risk_reward")

workstations_cols = [c for c in fields["workstations"] if c in dd_df.columns]
df_business_ws = metricas_agrupadas(dd_df, workstations_cols, "Startup", "media_workstations")

# Combinar métricas de business
df_business = pd.merge(df_business_rr, df_business_ws, on="Startup", how="outer")
business_cols = [col for col in ["media_risk_reward", "media_workstations"] if col in df_business.columns]
if business_cols:
    df_business["media_business"] = df_business[business_cols].mean(axis=1)
    df_business = df_business[["Startup", "media_business"]]

# =============================================================================
# CONSOLIDACIÓN DE DATOS
# =============================================================================

# Merge de todos los datos
df_final = df_individual.merge(df_people[["Name_norm", "Startup"]], on="Name_norm", how="left")

if not df_team.empty:
    df_final = df_final.merge(df_team, on="Startup", how="left", suffixes=('', '_DROP_TEAM'))

if not df_business.empty:
    df_final = df_final.merge(df_business, on="Startup", how="left", suffixes=('', '_DROP_BUS'))

# ELIMINACIÓN AGRESIVA DE COLUMNAS DUPLICADAS
# Eliminar todas las columnas que terminen en _DROP
drop_cols = [col for col in df_final.columns if '_DROP' in col]
if drop_cols:
    print(f"Eliminando columnas con sufijo _DROP: {drop_cols}")
    df_final.drop(columns=drop_cols, inplace=True)

# Verificar y eliminar duplicados por índice de columnas
if df_final.columns.duplicated().any():
    print(f"⚠️ ADVERTENCIA: Columnas duplicadas detectadas: {df_final.columns[df_final.columns.duplicated()].tolist()}")
    df_final = df_final.loc[:, ~df_final.columns.duplicated(keep='first')]
    print(f"Columnas después de eliminar duplicados: {df_final.columns.tolist()}")

# Añadir logos
if "original logo" in dd_df.columns and "Startup" in dd_df.columns:
    df_logo_mapping = dd_df[["Startup", "original logo"]].drop_duplicates(subset=["Startup"], keep="first")
    logo_series = df_logo_mapping.set_index("Startup")["original logo"]
    df_final["original logo"] = df_final["Startup"].map(logo_series)
else:
    df_final["original logo"] = None

# Añadir fotos
if "Headshot" in dd_df.columns and "Founder_str" in dd_df.columns:
    df_logo_mapping = dd_df[["Founder_str", "Headshot"]].drop_duplicates(subset=["Founder_str"], keep="first")
    logo_series = df_logo_mapping.set_index("Founder_str")["Headshot"]
    df_final["Headshot"] = df_final["Founder_str"].map(logo_series)
else:
    df_final["Headshot"] = None

# VERIFICACIÓN FINAL DE DUPLICADOS
if df_final.columns.duplicated().any():
    print("❌ ERROR: Aún hay columnas duplicadas después de la limpieza")
    print(f"Columnas duplicadas: {df_final.columns[df_final.columns.duplicated()].tolist()}")
    # Forzar eliminación
    df_final = df_final.T.drop_duplicates().T

# Calcular z-scores
for metric in ["media_individual", "media_equipo", "media_business"]:
    if metric in df_final.columns:
        mu = df_final[metric].mean()
        sigma = df_final[metric].std()
        if sigma > 0:
            df_final[f"z_{metric}"] = (df_final[metric] - mu) / sigma
        else:
            df_final[f"z_{metric}"] = 0
    else:
        df_final[f"z_{metric}"] = None

# Clasificar perfiles
df_final["Perfil_exec"] = df_final.apply(classify_profile, axis=1, args=(THRESHOLD,))

# VERIFICACIÓN FINAL ANTES DE USAR EN PLOTLY
print(f"✓ Columnas finales: {len(df_final.columns)}")
print(f"✓ ¿Hay duplicados?: {df_final.columns.duplicated().any()}")
if df_final.columns.duplicated().any():
    print(f"Columnas duplicadas restantes: {df_final.columns[df_final.columns.duplicated()].tolist()}")

df_final = df_final[df_final["Name_norm"].isin(founder_list_norm)]

# =============================================================================
# CÁLCULO DE PERFIL A NIVEL DE STARTUP (USANDO LA MEDIA INDIVIDUAL)
# =============================================================================

# 1. Calcular la media de Z-score Individual por Startup
df_z_individual_agg = df_final.groupby('Startup', as_index=False)[
    METRICS["individual"]["z_col"]
].mean().rename(columns={METRICS["individual"]["z_col"]: "z_media_individual_agg"})


# 2. Crear DataFrame de métricas de Startup
# Tomamos las métricas de equipo y negocio (que ya son por startup, aunque repetidas)
# y las combinamos con la media individual agregada.
df_startup_profiles = df_final[[
    "Startup",
    METRICS["team"]["z_col"],
    METRICS["business"]["z_col"]
]].drop_duplicates(subset=["Startup"]).copy()

# Fusionamos la media individual agregada
df_startup_profiles = df_startup_profiles.merge(
    df_z_individual_agg, 
    on="Startup", 
    how="left"
)

# 3. Preparar el DataFrame para usar classify_profile

# Renombramos temporalmente las columnas para que coincidan con la función classify_profile
df_startup_profiles.rename(columns={
    "z_media_individual_agg": METRICS["individual"]["z_col"] # Usamos el nombre original esperado
}, inplace=True)


# 4. Aplicar la clasificación de perfil de Startup
df_startup_profiles["Perfil_startup"] = df_startup_profiles.apply(
    classify_profile, 
    axis=1, 
    args=(THRESHOLD,)
)


# 5. Volver a renombrar la columna Z-score para evitar confusiones en el df_final
df_startup_profiles.rename(columns={
    METRICS["individual"]["z_col"]: "z_media_individual_agg" # Volvemos al nombre agregado
}, inplace=True)

# Seleccionamos solo las columnas necesarias para el merge
df_startup_profiles = df_startup_profiles[["Startup", "Perfil_startup"]]


# 6. Fusionar la nueva clasificación al df_final (a todas las filas de founders)
df_final = df_final.merge(
    df_startup_profiles, 
    on="Startup", 
    how="left"
)

# =============================================================================
# CALCULAR ESTADÍSTICAS GENERALES
# =============================================================================

num_startups = df_final["Startup"].nunique() if "Startup" in df_final.columns else 0
num_founders = df_final["Name_norm"].nunique() if "Name_norm" in df_final.columns else 0

# Calcular outliers
num_individual_outliers = 0
num_team_outliers = 0
num_business_outliers = 0

if "z_media_individual" in df_final.columns:
    num_individual_outliers = df_final[
        (df_final["z_media_individual"] < -THRESHOLD) | 
        (df_final["z_media_individual"] > THRESHOLD)
    ].shape[0]

if "z_media_equipo" in df_final.columns:
    num_team_outliers = df_final[
        (df_final["z_media_equipo"] < -THRESHOLD) | 
        (df_final["z_media_equipo"] > THRESHOLD)
    ]["Startup"].nunique()

if "z_media_business" in df_final.columns:
    num_business_outliers = df_final[
        (df_final["z_media_business"] < -THRESHOLD) | 
        (df_final["z_media_business"] > THRESHOLD)
    ]["Startup"].nunique()

# =============================================================================
# INTERFAZ DE USUARIO
# =============================================================================

st.markdown("")

# Métricas generales
cols = st.columns(5)
with cols[0]:
    st.metric(label="Number of startups", value=num_startups)
with cols[1]:
    st.metric(label="Number of founders", value=num_founders)
with cols[2]:
    pct_ind = round(num_individual_outliers / num_founders * 100, 2) if num_founders > 0 else 0
    st.metric(label="Individual Outliers (founders)", value=f"{num_individual_outliers} ({pct_ind}%)")
with cols[3]:
    pct_team = round(num_team_outliers / num_startups * 100, 2) if num_startups > 0 else 0
    st.metric(label="Team Outliers (startups)", value=f"{num_team_outliers} ({pct_team}%)")
with cols[4]:
    pct_bus = round(num_business_outliers / num_startups * 100, 2) if num_startups > 0 else 0
    st.metric(label="Business Outliers (startups)", value=f"{num_business_outliers} ({pct_bus}%)")

# ============================================================================
# SECCIÓN 0: OVERVIEW   -----   ESTA SECCIÓN DEBERÁ HACERSE MANUALMENTE
#=============================================================================

st.markdown("<h2>General Report</h2>", unsafe_allow_html=True)

columnas = st.columns(2)
with columnas[0]:
    st.markdown(
        """The first thing to highlight is Adrián Trucios, the founder of Airbag, who has an exceptional profile, being an outlier in all individual, team and business metrics.
        \nThis excellent profile is followed by Yerson Cacua, founder of CIFRATO. These two founders had the best performance in Mexico 2025"""
    )
    df_best = df_final[(df_final["Name_norm"] == "adrian trucios") | (df_final["Name_norm"] == "yerson cacua")]
    
    for _, row in df_best.iterrows():
        render_founder_card(pd.DataFrame([row]), show_name=True)

    st.markdown(
        """Also, it is worth highlighting Enrique Arredondo, founder of Ecosis, who has a very good profile in individal metrics, but he is apparently not sourrounded by a team to enhance his qualities."""
    )

    df_enrique = df_final[df_final["Name_norm"] == "enrique arredondo"]
    render_founder_card(df_enrique, show_name=True)

    st.markdown(
        """Also the founders of Handit.ai, that, despite the issues with the company, our metrics describe the situation, being outstanding founders (in individual and team terms) in a weak project"""
    )
    df_handit = df_final[(df_final["Name_norm"] == "cristhian camilo gomez") | (df_final["Name_norm"] == "jose manuel ramirez")]

    for _, row in df_handit.iterrows():
        render_founder_card(pd.DataFrame([row]), show_name=True)

with columnas[1]:
    st.markdown(
        """Regarding companies, we have to highlight the case of the three best businesses."""
    )

    df_best_business = df_final[(df_final["Startup"] == "Airbag") | (df_final["Startup"] == "Moabits SL") | (df_final["Startup"] == "CIFRATO")]

    for startup in set(df_best_business["Startup"].tolist()):
            df_all_founders = df_final[df_final["Startup"] == startup]
            avg_individual_mean = df_all_founders["media_individual"].mean()
            df_startup_row = df_all_founders.iloc[[0]].copy()
            df_startup_row["media_individual"].iloc[0] = avg_individual_mean

            render_founder_card(df_startup_row, show_name=False)
    
    st.markdown(
        """the team of admina is outstanding, despite the fact that Andrés Gómez is not  a top performer in indivual metrics."""
    )

    df_admina = df_final[df_final["Startup"] == "Admina"]

    for _, row in df_admina.iterrows():
        render_founder_card(pd.DataFrame([row]), show_name=True)

    
# =============================================================================
# SECCIÓN 1: ONE METRIC OUTLIERS
# =============================================================================

st.markdown("<h2>1. One Metric Outliers</h2>", unsafe_allow_html=True)

tab_good, tab_bad = st.tabs(["High Scores Outliers", "Low Scores Outliers"])

with tab_good:
    # Individual Outliers
    cols_good = st.columns(3)

    with cols_good[0]:
        st.markdown("<h3>Individual Outliers</h3>", unsafe_allow_html=True)
        df_individual_outliers = df_final[
            df_final["z_media_individual"] > 1
        ].sort_values(by="z_media_individual", ascending=False)
        
        for _, row in df_individual_outliers.iterrows():
            render_founder_card(pd.DataFrame([row]), show_name=True)

    # Team Outliers
    with cols_good[1]:
        st.markdown("<h3>Team Outliers</h3>", unsafe_allow_html=True)
        df_team_outliers = df_final[
            df_final["z_media_equipo"] > THRESHOLD
        ].sort_values(by="z_media_equipo", ascending=False).drop_duplicates(subset="Startup", keep="first")
        
        for startup in df_team_outliers["Startup"]:
            df_startup = df_final[df_final["Startup"] == startup].iloc[[0]]
            render_founder_card(df_startup, show_name=False)

    # Business Outliers
    with cols_good[2]:
        st.markdown("<h3>Business Outliers</h3>", unsafe_allow_html=True)
        df_business_outliers = df_final[
            df_final["z_media_business"] > THRESHOLD
        ].sort_values(by="z_media_business", ascending=False).drop_duplicates(subset="Startup", keep="first")
        
        for startup in df_business_outliers["Startup"]:
            df_startup = df_final[df_final["Startup"] == startup].iloc[[0]]
            render_founder_card(df_startup, show_name=False)

with tab_bad:
    # Individual Outliers
    cols_bad = st.columns(3)

    with cols_bad[0]:
        st.markdown("<h3>Individual Outliers</h3>", unsafe_allow_html=True)
        df_individual_outliers = df_final[
            df_final["z_media_individual"] < -THRESHOLD
        ].sort_values(by="z_media_individual", ascending=True)
        
        for _, row in df_individual_outliers.iterrows():
            render_founder_card(pd.DataFrame([row]), show_name=True)

    # Team Outliers
    with cols_bad[1]:
        st.markdown("<h3>Team Outliers</h3>", unsafe_allow_html=True)
        df_team_outliers = df_final[
            df_final["z_media_equipo"] < -THRESHOLD
        ].sort_values(by="z_media_equipo", ascending=True).drop_duplicates(subset="Startup", keep="first")
        
        for startup in df_team_outliers["Startup"]:
            df_startup = df_final[df_final["Startup"] == startup].iloc[[0]]
            render_founder_card(df_startup, show_name=False)

    # Business Outliers
    with cols_bad[2]:
        st.markdown("<h3>Business Outliers</h3>", unsafe_allow_html=True)
        df_business_outliers = df_final[
            df_final["z_media_business"] < -THRESHOLD
        ].sort_values(by="z_media_business", ascending=True).drop_duplicates(subset="Startup", keep="first")
        
        for startup in df_business_outliers["Startup"]:
            df_startup = df_final[df_final["Startup"] == startup].iloc[[0]]
            render_founder_card(df_startup, show_name=False)

# =============================================================================
# SECCIÓN 2: TWO METRICS OUTLIERS
# =============================================================================

st.markdown("")
st.markdown("<h2>2. Two Metrics Outliers</h2>", unsafe_allow_html=True)
st.markdown("")

tab_ivt, tab_ivb, tab_tvb = st.tabs([
    "Individual vs Team",
    "Individual vs Business",
    "Team vs Business"
])

# --- TAB 1: Individual vs Team ---
with tab_ivt:
    
    scatter_two_dim(
        df_final,
        METRICS["individual"]["mean_col"],
        METRICS["team"]["mean_col"],
        "Individual",
        "Equipo",
        "media_business",
        "Individual vs Equipo",
        "Name"
    )
    
    df_ivt_high = df_final[
        (df_final["z_media_individual"] > TWO_METRIC_THRESHOLD) & 
        (df_final["z_media_equipo"] < -TWO_METRIC_THRESHOLD)
    ].sort_values(by="z_media_individual", ascending=False)
    
    df_ivt_low = df_final[
        (df_final["z_media_individual"] < -TWO_METRIC_THRESHOLD) & 
        (df_final["z_media_equipo"] > TWO_METRIC_THRESHOLD)
    ].sort_values(by="z_media_individual", ascending=False)
    
    columns = st.columns(2)
    
    with columns[0]:
        st.markdown("<h3>High Individual, Low Team</h3>", unsafe_allow_html=True)
        st.markdown("<h5>High potential founders surrounded by a not enhancing team</h5>", unsafe_allow_html=True)
        for _, row in df_ivt_high.iterrows():
            render_founder_card(pd.DataFrame([row]), show_name=True)
    
    with columns[1]:
        st.markdown("<h3>Low Individual, High Team</h3>", unsafe_allow_html=True)
        st.markdown("<h5>Low potential founders enhanced by their team</h5>", unsafe_allow_html=True)
        for _, row in df_ivt_low.iterrows():
            render_founder_card(pd.DataFrame([row]), show_name=True)

# --- TAB 2: Individual vs Business ---
with tab_ivb:
    
    scatter_two_dim(
        df_final,
        METRICS["individual"]["mean_col"],
        METRICS["business"]["mean_col"],
        "Individual",
        "Business",
        "media_equipo",
        "Individual vs Business",
        "Name"
    )
    
    df_ivb_high = df_final[
        (df_final["z_media_individual"] > TWO_METRIC_THRESHOLD) & 
        (df_final["z_media_business"] < -TWO_METRIC_THRESHOLD)
    ].sort_values(by="z_media_individual", ascending=False)

    df_ivb_low = df_final[
        (df_final["z_media_individual"] < -TWO_METRIC_THRESHOLD) & 
        (df_final["z_media_business"] > TWO_METRIC_THRESHOLD)
    ].sort_values(by="z_media_individual", ascending=False)
    
    columns = st.columns(2)
    
    with columns[0]:
        st.markdown("<h3>High Individual, Low Business</h3>", unsafe_allow_html=True)
        st.markdown("<h5>High potential founders in a weak project</h5>", unsafe_allow_html=True)
        for _, row in df_ivb_high.iterrows():
            render_founder_card(pd.DataFrame([row]), show_name=True)
    
    with columns[1]:
        st.markdown("<h3>Low Individual, High Business</h3>", unsafe_allow_html=True)
        st.markdown("<h5>High potential project carried out by a low potential founder</h5>", unsafe_allow_html=True)
        for _, row in df_ivb_low.iterrows():
            render_founder_card(pd.DataFrame([row]), show_name=True)

# --- TAB 3: Team vs Business ---
with tab_tvb:
    df_plot = df_final.copy()
    if df_plot.columns.duplicated().any():
        df_plot = df_plot.loc[:, ~df_plot.columns.duplicated(keep='first')]
    
    scatter_two_dim(
        df_plot,
        METRICS["team"]["mean_col"],
        METRICS["business"]["mean_col"],
        "Equipo",
        "Business",
        "media_individual",
        "Team vs Business",
        "Name",
        show_name=False
    )
    
    df_tvb_high = df_final[
        (df_final["z_media_equipo"] > TWO_METRIC_THRESHOLD) & 
        (df_final["z_media_business"] < -TWO_METRIC_THRESHOLD)
    ].sort_values(by="z_media_equipo", ascending=False).drop_duplicates(subset="Startup", keep="first")
    
    df_tvb_low = df_final[
        (df_final["z_media_equipo"] < -TWO_METRIC_THRESHOLD) & 
        (df_final["z_media_business"] > TWO_METRIC_THRESHOLD)
    ].sort_values(by="z_media_equipo", ascending=False).drop_duplicates(subset="Startup", keep="first")
    
    columns = st.columns(2)
    
    with columns[0]:
        st.markdown("<h3>High Team, Low Business</h3>", unsafe_allow_html=True)
        st.markdown("<h5>Strong teams in weak projects</h5>", unsafe_allow_html=True)
        for startup in df_tvb_high["Startup"]:
            df_all_founders = df_final[df_final["Startup"] == startup]
            avg_individual_mean = df_all_founders["media_individual"].mean()
            df_startup_row = df_all_founders.iloc[[0]].copy()
            df_startup_row["media_individual"].iloc[0] = avg_individual_mean

            render_founder_card(df_startup_row, show_name=False)
    
    with columns[1]:
        st.markdown("<h3>Low Team, High Business</h3>", unsafe_allow_html=True)
        st.markdown("<h5>Weak teams in strong projects</h5>", unsafe_allow_html=True)
        for startup in df_tvb_low["Startup"]:
            df_all_founders = df_final[df_final["Startup"] == startup]
            avg_individual_mean = df_all_founders["media_individual"].mean()
            df_startup_row = df_all_founders.iloc[[0]].copy()
            df_startup_row["media_individual"].iloc[0] = avg_individual_mean

            render_founder_card(df_startup_row, show_name=False)