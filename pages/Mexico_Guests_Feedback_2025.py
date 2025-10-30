from typing import Any
import streamlit as st
import pandas as pd
from pyairtable import Api
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="Mexico - Program - Agenda",
    page_icon="https://images.squarespace-cdn.com/content/v1/67811e8fe702fd5553c65249/c5500619-9712-4b9b-83ee-a697212735ae/Disen%CC%83o+sin+ti%CC%81tulo+%2840%29.png",
    layout="wide"
)

if "selected_year" not in st.session_state:
    st.session_state.selected_year = "2025"

st.markdown(body="""
<style>
.outer-container {
    display: flex;
    justify-content: center; /* Centra horizontalmente */
    width: 100%; /* Ocupa todo el ancho disponible */
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
    font-size: 2.5em; /* Tamaño del título */
    font-weight: bold;
}
</style>
<div class="outer-container">
<div class="container">
    <img class="logo-img" src="https://images.squarespace-cdn.com/content/v1/67811e8fe702fd5553c65249/c5500619-9712-4b9b-83ee-a697212735ae/Disen%CC%83o+sin+ti%CC%81tulo+%2840%29.png">
    <h1 class="title-text">Decelera Program<br>Guests</h1>
</div>
</div>
""", unsafe_allow_html=True)

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
    
    # Investment section (Title 4)
    st.markdown("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Investment**")
    
    # Investment pages (Title 5)
    if st.button("Risk-Reward", key="mx_inv_general", use_container_width=True):
        st.switch_page(f"pages/Mexico_Risk_Reward_{st.session_state.selected_year}.py")
    
    if st.button("Feedback details", key="mx_inv_startup", use_container_width=True):
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
    if st.button("Risk-Reward", key="mn_inv_general", use_container_width=True):
        st.switch_page(f"pages/Menorca_Risk_Reward_{st.session_state.selected_year}.py")
    
    if st.button("Feedback details", key="mn_inv_startup", use_container_width=True):
        st.switch_page(f"pages/Menorca_Feedback_Details_{st.session_state.selected_year}.py")
    
    # Program section (Title 4)
    st.markdown("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Program**")
    
    # Program pages (Title 5)
    if st.button("Guests feedback", key="mn_prog_general", use_container_width=True):
        st.switch_page(f"pages/Menorca_Guests_Feedback_{st.session_state.selected_year}.py")
    
    if st.button("Breathe-Focus-Grow", key="mn_prog_agenda", use_container_width=True):
        st.switch_page(f"pages/Menorca_Breathe-Focus-Grow_{st.session_state.selected_year}.py")

api_key = st.secrets["airtable_program"]["api_key"]
base_id = st.secrets["airtable_program"]["base_id"]
table_id = st.secrets["airtable_program"]["table_id"]

api = Api(api_key)

# Carga de datos actuales
records = api.table(base_id, table_id).all(view="Guests Feedback")
data = [record["fields"] for record in records]
df = pd.DataFrame(data)

def fix_cell(val):
    if isinstance(val, dict) and "specialValue" in val:
        return float("nan")
    return val

# Carga segura de datos pasados
try:
    records_past = api.table(base_id, table_id).all(view="Menorca 2025") 
    data_past = [record["fields"] for record in records_past]
    df_past = pd.DataFrame(data_past)
    df_past = df_past.map(func=fix_cell)
except Exception as e:
    # Si falla (ej. la vista no existe), crea un df vacío y avisa en la app
    st.warning(f"No se pudieron cargar los datos comparativos del año pasado. Se mostrará solo el año actual. (Error: {e})")
    df_past = pd.DataFrame()

df = df.map(func=fix_cell)

#=========================CONFIG========================================

fields = {
    "Founders": [
        "Guest logistics",
        "Communication from team",
        "Program website",
        "Connections with EM's",
        "Connections with VC's",
        "Connections with other Startups",
        "Investment ready",
        "Confidence of growth"
    ],
    "EMs": [
        "Satisfaction",
        "Guest logistics",
        "Communication from team",
        "Program website",
        "Content relevance",
        "Wellbeing",
        "Networking",
        "EM's Fb | Info talks",
        "EM's Fb | 1:1's",
        "EM's Fb | 1:1's Fb",
        "EM's Fb | Info 1:1's"
    ],
    "VCs": [
        "Satisfaction",
        "Communication from team",
        "Program website",
        "EM's Fb | Demo day",
        "Networking",
    ]
}

labels = {
    "Founders": [
        "Guest logistics",
        "Communication from team",
        "Program app",
        "Connections with EM's",
        "Connections with VC's",
        "Connections with other Startups",
        "Investment ready",
        "Confidence of growth"
    ],
    "EMs": [
        "Overall experience",
        "Guest logistics",
        "Communication from team",
        "Program app",
        "Content relevance",
        "Wellbeing",
        "Networking",
        "Info provided for talk",
        "1:1's satisfaction",
        "1:1's provided feedback",
        "Info provided for 1:1's"
    ],
    "VCs": [
        "Overall experience",
        "Communication from team",
        "Program app",
        "Demo day",
        "Networking"
    ]
}

color_scale=[
    [0.0, '#FFB950'],
    [0.5, '#FAF3DC'],
    [1.0, '#1FD0EF']
]

# --- Función 'barras' comparativa y robusta ---
def barras(values_actual, labels, values_pasado, title, n_actual, n_pasado) -> None:
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Mexico 2025',
        x=labels,
        y=values_actual,
        customdata=n_actual,
        hovertemplate='Muestra: %{customdata}<extra></extra>',
        texttemplate=[f'{y:.2f}' if pd.notna(y) else '' for y in values_actual],
        textposition='outside',
        marker=dict(
            color=values_actual,
            colorscale=color_scale,
            line=dict(color='black', width=1.5)
        ),
        textfont=dict(color='black')
    ))

    hay_datos_pasados = pd.Series(values_pasado).notna().any()

    if hay_datos_pasados:
        fig.add_trace(go.Bar(
            name='Menorca 2025',
            x=labels,
            y=values_pasado, #plotly ignora los nan, asi que palante
            customdata=n_pasado,
            hovertemplate='Muestra: %{customdata}<extra></extra>',
            texttemplate=[f'{y:.2f}' if pd.notna(y) else '' for y in values_pasado],
            textposition='outside',
            marker=dict(
                color='rgba(0,0,0,0)',
                line=dict(color='darkgrey', width=1.5)
            ),
            textfont=dict(color='darkgrey')
        ))
    
    all_values = [v for v in values_actual if pd.notna(v)] + \
                 [v for v in values_pasado if pd.notna(v)]
    
    range_min = 0 
    range_max = max(all_values) * 1.15 if all_values else 5

    fig.update_layout(
        title=title,
        yaxis_title='Mean Score',
        template="plotly_white",
        barmode='group',
        yaxis=dict(
            range=[range_min, range_max]
        ),
        xaxis=dict(
            tickfont=dict(color='black'),
            tickangle=-45
        ),
        legend_title_text='Periodo',
    )
    
    st.plotly_chart(fig, use_container_width=True)

def metric(value, label) -> None:
    st.metric(value=value, label=label)

# --- Función 'safe_mean' ---
def safe_mean(df_to_check, field):
    if not df_to_check.empty and field in df_to_check.columns:
        if not df_to_check[field].dropna().empty:
            return float(df_to_check[field].dropna().astype(float).mean())
    return float("nan")

def calculate_nps(df, field):
    if df.empty or field not in df.columns:
        return float("nan") 
        
    scores = df[field].dropna().astype(float).tolist()
    
    if not scores:
        return float("nan") 
        
    n_prom = 0
    n_detr = 0
    for score in scores:
        if score == 9 or score == 10:
            n_prom += 1
        elif 0 <= score <= 6:
            n_detr += 1
        else:
            pass
    return (n_prom - n_detr) / len(scores) * 100

# Apply normalization manually to avoid type issues
fields_to_normalize: list[str] = [
    "Confidence of growth",
    "Connections with EM's",
    "Connections with VC's",
    "Connections with other Startups",
    "Investment ready"
]

# --- Normalización segura ---
def safe_normalize(x):
    if pd.notna(x):
        return (float(x) / 10 * 3) + 1
    return x

for field in df_past.columns:
    try:
        df_past[field] = df_past[field].apply(lambda x: safe_normalize(x) if pd.notna(x) else x)
    except Exception as e:
        pass

for field in fields_to_normalize:
    if field in df.columns:
        df[field] = df[field].apply(safe_normalize)
    if not df_past.empty and field in df_past.columns:
        df_past[field] = df_past[field].apply(safe_normalize)

# --- Helper seguro para filtrar 'Guest_type' ---
def safe_check_guest_type(x, type_name):
    if isinstance(x, list):
        return type_name in x
    if isinstance(x, str):
        return x == type_name
    return False

# FUncion segura para contar el numero de datos de cada metrica
def safe_count(df_to_check, field):
    if not df_to_check.empty and field in df_to_check.columns:
        return int(df_to_check[field].dropna().count())
    return float("nan")

#===================================Vamos con Founders===================================

#------------------------------Saquemos las medias-------------------------------------
# --- Filtro robusto (acepta listas o strings) ---
df_startup = df[df["Guest_type"].apply(safe_check_guest_type, type_name="Startup")]

df_startup_past = pd.DataFrame()
if not df_past.empty and "Guest_type" in df_past.columns:
    df_startup_past = df_past[df_past["Guest_type"].apply(safe_check_guest_type, type_name="Startup")]

nps_startup_startup = calculate_nps(df=df_startup, field="Recommendation to Startups")

means_founder: list = []
means_founder_pasado: list = []
n_founder: list = []
n_founder_pasado: list = []

labels_startup = labels["Founders"]
for field in fields["Founders"]:
    means_founder.append(safe_mean(df_startup, field))
    means_founder_pasado.append(safe_mean(df_startup_past, field))

    n_founder.append(safe_count(df_startup, field))
    n_founder_pasado.append(safe_count(df_startup_past, field))

#==================================Vamos con EMs==================================

#------------------------------Saquemos las medias-------------------------------------
# --- Filtro robusto (acepta listas o strings) ---
df_em = df[df["Guest_type"].apply(safe_check_guest_type, type_name="EM")]

df_em_past = pd.DataFrame()
if not df_past.empty and "Guest_type" in df_past.columns:
    df_em_past = df_past[df_past["Guest_type"].apply(safe_check_guest_type, type_name="EM")]

nps_em_startup = calculate_nps(df=df_em, field="Recommendation to Startups")
nps_em_em = calculate_nps(df=df_em, field="EM's Fb | Recommendation to EM")

means_em: list = []
means_em_pasado: list = []
n_em: list = []
n_em_pasado: list = []

labels_em = labels["EMs"]
for field in fields["EMs"]:
    means_em.append(safe_mean(df_em, field))
    means_em_pasado.append(safe_mean(df_em_past, field))

    n_em.append(safe_count(df_em, field))
    n_em_pasado.append(safe_count(df_em_past, field))

#=================================Vamos con VCs==================================

#------------------------------Saquemos las medias-------------------------------------
# --- Filtro robusto (acepta listas o strings) ---
df_vc = df[df["Guest_type"].apply(safe_check_guest_type, type_name="VC")]

df_vc_past = pd.DataFrame()
if not df_past.empty and "Guest_type" in df_past.columns:
    df_vc_past = df_past[df_past["Guest_type"].apply(safe_check_guest_type, type_name="VC")]

nps_vc_startup = calculate_nps(df=df_vc, field="Recommendation to Startups")
nps_vc_vc = calculate_nps(df=df_vc, field="VC's | Recommendation to vc")

means_vc: list = []
means_vc_pasado: list = []
labels_vc = labels["VCs"]
n_vc: list = []
n_vc_pasado: list = []

for field in fields["VCs"]:
    means_vc.append(safe_mean(df_vc, field))
    means_vc_pasado.append(safe_mean(df_vc_past, field))

    n_vc.append(safe_count(df_vc, field))
    n_vc_pasado.append(safe_count(df_vc_past, field))
#--------------------------------------------------------------------------------------------
st.markdown(body="Here you will find the feedback submitted by founders, experience makers and VC's about the program")

st.markdown(body="<h1 style='text-align: center;'>Founders</h1>", unsafe_allow_html=True)

st.metric(value=round(nps_startup_startup, 2) if pd.notna(nps_startup_startup) else "N/A", label="NPS Startups to Startups")

ordered_pairs_founder = sorted(
    zip(means_founder, means_founder_pasado, n_founder, n_founder_pasado, labels["Founders"]),
    key=lambda x: -1 if pd.isna(x[0]) else x[0],
    reverse=True
)
values_graph_founder = [v_act for v_act, v_pas, n_act, n_pas, lab in ordered_pairs_founder]
values_graph_founder_pasado = [v_pas for v_act, v_pas, n_act, n_pas, lab in ordered_pairs_founder]
n_graph_founder = [n_act for v_act, v_pas, n_act, n_pas, lab in ordered_pairs_founder]
n_graph_founder_pasado = [n_pas for v_act, v_pas, n_act, n_pas, lab in ordered_pairs_founder]
labels_graph_founder = [lab for v_act, v_pas, n_act, n_pas, lab in ordered_pairs_founder]

barras(
    values_actual=values_graph_founder,
    labels=labels_graph_founder,
    values_pasado=values_graph_founder_pasado,
    title=f"Founders feedback",
    n_actual=n_graph_founder,
    n_pasado=n_graph_founder_pasado
)

with st.expander(label="Improvement ideas from founders"):
    if not df_startup["Improvement ideas"].empty:

        comments_founders = df_startup[["Name", "Improvement ideas"]].dropna(subset=["Improvement ideas"])
        for index, row in comments_founders.iterrows():
            name = row["Name"]
            comment = row["Improvement ideas"]
            
            with st.expander(label=f"Improvement ideas from {name}"):
                st.markdown(body=comment)

with st.expander(label="Most positive aspect from founders"):
    if not df_startup["Most positive aspect"].empty:

        comments_founders = df_startup[["Name", "Most positive aspect"]].dropna(subset=["Most positive aspect"])
        for index, row in comments_founders.iterrows():
            name = row["Name"]
            comment = row["Most positive aspect"]
            
            with st.expander(label=f"Most positive aspect from {name}"):
                st.markdown(body=comment)

with st.expander(label="Top 3 outcomes from founders"):
    if not df_startup["Top 3 outcomes"].empty:

        comments_founders = df_startup[["Name", "Top 3 outcomes"]].dropna(subset=["Top 3 outcomes"])
        for index, row in comments_founders.iterrows():
            name = row["Name"]
            comment = row["Top 3 outcomes"]
            
            with st.expander(label=f"Top 3 outcomes from {name}"):
                st.markdown(body=comment)

st.markdown(body="---") #==============================================================================

st.markdown(body="<h1 style='text-align: center;'>EM's</h1>", unsafe_allow_html=True)

cols = st.columns(2)
with cols[0]:
    st.metric(value=round(nps_em_em, 2) if pd.notna(nps_em_em) else "N/A", label="NPS EM's to EM's")
with cols[1]:
    st.metric(value=round(nps_em_startup, 2) if pd.notna(nps_em_startup) else "N/A", label="NPS EM's to Startup")

ordered_pairs_em = sorted(
    zip(means_em, means_em_pasado, n_em, n_em_pasado, labels["EMs"]),
    key=lambda x: -1 if pd.isna(x[0]) else x[0],
    reverse=True
)
values_graph_em = [v_act for v_act, v_pas, n_act, n_pas, lab in ordered_pairs_em]
values_graph_em_pasado = [v_pas for v_act, v_pas, n_act, n_pas, lab in ordered_pairs_em]
labels_graph_em = [lab for v_act, v_pas, n_act, n_pas, lab in ordered_pairs_em]
n_graph_em = [n_act for v_act, v_pas, n_act, n_pas, lab in ordered_pairs_em]
n_graph_em_pasado = [n_pas for v_act, v_pas, n_act, n_pas, lab in ordered_pairs_em]

barras(
    values_actual=values_graph_em,
    labels=labels_graph_em,
    values_pasado=values_graph_em_pasado,
    title=f"EM's feedback",
    n_actual=n_graph_em,
    n_pasado=n_graph_em_pasado
)

with st.expander(label="Comments from EMs"):
    if not df_em["Comments"].empty:

        comments_founders = df_em[["Name", "Comments"]].dropna(subset=["Comments"])
        for index, row in comments_founders.iterrows():
            name = row["Name"]
            comment = row["Comments"]
            
            with st.expander(label=f"Comments from {name}"):
                st.markdown(body=comment)

with st.expander(label="Improvement ideas from EMs"):
    if not df_em["Improvement ideas"].empty:

        comments_founders = df_em[["Name", "Improvement ideas"]].dropna(subset=["Improvement ideas"])
        for index, row in comments_founders.iterrows():
            name = row["Name"]
            comment = row["Improvement ideas"]
            
            with st.expander(label=f"Improvement ideas from {name}"):
                st.markdown(body=comment)

with st.expander(label="Top3 1:1's from EMs"):
    if not df_em["EM's Fb | Top3 1:1's"].empty:

        comments_founders = df_em[["Name", "EM's Fb | Top3 1:1's"]].dropna(subset=["EM's Fb | Top3 1:1's"])
        for index, row in comments_founders.iterrows():
            name = row["Name"]
            comment = row["EM's Fb | Top3 1:1's"]
            
            with st.expander(label=f"Top3 1:1's from {name}"):
                st.markdown(body=comment)

st.markdown(body="---") #======================================================================================0

st.markdown(body="<h1 style='text-align: center;'>VC's</h1>", unsafe_allow_html=True)

cols = st.columns(2)
with cols[0]:
    st.metric(value=round(nps_vc_vc, 2) if pd.notna(nps_vc_vc) else "N/A", label="NPS VC's to VC's")
with cols[1]:
    st.metric(value=round(nps_vc_startup, 2) if pd.notna(nps_vc_startup) else "N/A", label="NPS VC's to Startups")

ordered_pairs_vc = sorted(
    zip(means_vc, means_vc_pasado, n_vc, n_vc_pasado, labels["VCs"]),
    key=lambda x: -1 if pd.isna(x[0]) else x[0],
    reverse=True
)
values_graph_vc = [v_act for v_act, v_pas, n_act, n_pas, lab in ordered_pairs_vc]
values_graph_vc_pasado = [v_pas for v_act, v_pas, n_act, n_pas, lab in ordered_pairs_vc]
n_graph_vc = [n_act for v_act, v_pas, n_act, n_pas, lab in ordered_pairs_vc]
n_graph_vc_pasado = [n_pas for v_act, v_pas, n_act, n_pas, lab in ordered_pairs_vc]
labels_graph_vc = [lab for v_act, v_pas, n_act, n_pas, lab in ordered_pairs_vc]

barras(
    values_actual=values_graph_vc,
    labels=labels_graph_vc,
    values_pasado=values_graph_vc_pasado,
    title=f"VC's feedback",
    n_actual=n_graph_vc,
    n_pasado=n_graph_vc_pasado
)

with st.expander(label="Comments from VCs"):
    if not df_vc["Comments"].empty:

        comments_founders = df_vc[["Name", "Comments"]].dropna(subset=["Comments"])
        for index, row in comments_founders.iterrows():
            name = row["Name"]
            comment = row["Comments"]
            
            with st.expander(label=f"Comments from {name}"):
                st.markdown(body=comment)

with st.expander(label="Improvement ideas from VCs"):
    if not df_vc["Improvement ideas"].empty:

        comments_founders = df_vc[["Name", "Improvement ideas"]].dropna(subset=["Improvement ideas"])
        for index, row in comments_founders.iterrows():
            name = row["Name"]
            comment = row["Improvement ideas"]
            
            with st.expander(label=f"Improvement ideas from {name}"):
                st.markdown(body=comment)

with st.expander(label="Investment interest from VCs"):
    if not df_vc["Investment Interest"].empty:

        comments_founders = df_vc[["Name", "Investment Interest"]].dropna(subset=["Investment Interest"])
        for index, row in comments_founders.iterrows():
            name = row["Name"]
            comment = row["Investment Interest"]
            
            with st.expander(label=f"Investment interest from {name}"):
                st.markdown(body=comment)

st.markdown(body="---")