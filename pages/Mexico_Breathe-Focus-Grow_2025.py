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
    <h1 class="title-text">Decelera Program<br>Breathe - Focus - Grow</h1>
</div>
</div>
""", unsafe_allow_html=True)

#center metrics
st.markdown(
    """
    <style>
    /* 1. Centra el BLOQUE entero de la métrica en su columna */
    div[data-testid="stMetric"] {
        align-self: center;
    }

    /* 2. Centra el TEXTO de la etiqueta */
    div[data-testid="stMetricLabel"] {
        text-align: center;
    }
    
    /* 3. Centra el VALOR (que es un contenedor flex) */
    div[data-testid="stMetricValue"] {
        justify-content: center;
    }
    
    /* 4. (Opcional) Centra el DELTA (también es flex) */
    div[data-testid="stMetricDelta"] {
        justify-content: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

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
records = api.table(base_id, table_id).all(view="Breathe-Focus-Grow")
data = [record["fields"] for record in records]
df = pd.DataFrame(data)

records_past = api.table(base_id, table_id).all(view='Menorca 2025')
data_past = [record["fields"] for record in records_past]
df_past = pd.DataFrame(data_past)

def fix_cell(val):
    if isinstance(val, dict) and "specialValue" in val:
        return float("nan")
    return val

df = df.map(func=fix_cell)
df_past = df_past.map(func=fix_cell)
#=========================CONFIG========================================

fields: dict = {
    "Breathe": {
        "Talks": [
            "Talk by Jose de la Luz",
            "Talk by Juanma Lopera",
            "Talk by Diego Meller",
            "Talk by Alex Wieland",
            "Breathe | Marcos' talk (Day 1)",
            "Breathe | Beth Susanne's talk (Day 2)"
        ],
        "Well-being": [
            "Breathe | Human pitch (Day 1)",
            "Breathe | Mindfulness (Day 2)",
            "Breathe | Yoga (Day 2)",
            "Breathe | Journaling (Day 2)",
        ],
        "Networking": [
            "Breathe | Founder Arena (1)",
            "Breathe | Founder Arena (2)",
            "Breathe | Founder Arena (3)",
            "Breathe | Cocktail at Binibeca (Day 1)",
            "Breathe | New connections"
        ],
        "Investment": [
            "Breathe | Pitching dynamic (Day 2)",
            "Breathe | Workstations",
        ]
    },
    "Focus": {
        "Talks": [
            "Talk by Javier Cardona",
            "Talk by Eyal Shatz",
            "Talk by Sofia Storberg",
            "Breathe | Sean Cook's talk (Day 2)",
            "Talk by Vincent Speranza",
            "Talk by Victor Noguera",
            "Talk by Jose V. Fernandez",
            "Talk by Sven Huber"
        ],
        "Well-being": [
            "Focus | Mindfulness (Day 3)",
            "Focus | Body movement (Day 3)",
            "Focus | Power yoga (Day 5)",
            "Focus | Journaling (Day 3)",
        ],
        "Networking": [
            "Focus | The founder arena (1)",
            "Focus | Founder arena (2)",
            "Focus | Founder Arena (3)",
            "Focus | Founder Arena (4)",
            "Founder Arena - Javier y Eyal",
            "Founder Arena - Rui Fernandez",
            "Founder arena - Mesa de VC's",
            "Founder Arena - Jose V. Fernandez",
            "Cenote",
            "Focus | Paellas contest",
            "Kiin Beh"
        ],
        "Investment": [
            "Focus | 1:1's matching (Day 3)"
        ]
    },
    "Grow": {
        "Talks":[
            "Talk by Evaristo Babe",
            "Talk by Evaristo and Carolina"
        ],
        "Well-being": [
            "Grow | Mindfulness (Day 8)",
            "Grow | HIT",
            "Grow | Journaling",
            "Grow | Human Pitch",
        ],
        "Investment": [
            "Grow | Demo day"
        ]
    }
}

general_fields: dict = {
    "Breathe": [
        "Breathe | Satisfaction",
        "Breathe | Wellbeing",
        "Breathe | Organization"
    ],
    "Focus": [
        "Focus | Satisfaction",
        "Focus | Wellbeing",
        "Focus | Organization"
    ],
    "Grow": [
        "Grow | Satisfaction",
        "Grow | Wellbeing",
        "Grow | Organization"
    ]
}

labels: dict = {
    "Breathe": {
        "Talks": [
            "Talk by Jose de la Luz",
            "Talk by Juanma Lopera",
            "Talk by Diego Meller",
            "Talk by Alex Wieland",
            "Talk by Marcos",
            "Talk by Beth Susanne"
        ],
        "Well-being": [
            "Human pitch",
            "Mindfulness (breathe)",
            "Yoga (breathe)",
            "Journaling (breathe)",
        ],
        "Networking": [
            "Founder Arena Rui and Juanma",
            "Founder Arena Jose de la Luz",
            "Founder Arena Alex Wieland",
            "Welcome Cocktail",
            "New connections value"
        ],
        "Investment": [
            "Pitching dynamic",
            "Workstations"
        ]
    },
    "Focus": {
        "Talks": [
            "Talk by Javier Cardona",
            "Talk by Eyal Shatz",
            "Talk by Sofia Storberg",
            "Talk by Sean Cook",
            "Talk by Vincent Speranza",
            "Talk by Victor Noguera",
            "Talk by Jose V. Fernandez",
            "Talk by Sven Huber"
        ],
        "Well-being": [
            "Mindfulness (focus)",
            "Body movement",
            "Yoga (focus)",
            "Journaling (focus)"
        ],
        "Networking": [
            "The founder arena Sean Cook",
            "Founder arena Sofia Storberg",
            "Founder Arena Shadi Yazdan",
            "Founder Arena Varis and Carolina",
            "Founder Arena Javier y Eyal",
            "Founder Arena Rui Fernandez",
            "Founder arena Mesa de VC's",
            "Founder Arena Jose V. Fernandez",
            "Cenote",
            "Cooking Contest",
            "Kiin Beh"
        ],
        "Investment": [
            "1:1's matching"
        ]
    },
    "Grow": {
        "Talks":[
            "Talk by Evaristo Babe",
            "Talk by Evaristo and Carolina"
        ],
        "Well-being": [
            "Mindfulness (grow)",
            "HIT",
            "Journaling (grow)",
            "Human pitch wrap up",
        ],
        "Investment": [
            "Demo day"
        ]
    }
}

# Voy a intentar quedarme con los campos de menorca 2025 que coinciden con los de este año


general_labels: list = [
    "Overall experience",
    "Wellbeing dynamics",
    "Information and coordination"
]

phases = ["Breathe", "Focus", "Grow"]
categories_to_merge = ["Talks", "Well-being", "Networking", "Investment"]

if "General" not in fields:
    fields["General"] = {}
for category in categories_to_merge:
    all_items = []
    for phase in phases:
        all_items.extend(fields[phase].get(category, []))
    fields["General"][category] = all_items

if "General" not in labels:
    labels["General"] = {}
for category in categories_to_merge:
    all_items = []
    for phase in phases:
        all_items.extend(labels[phase].get(category, []))
    labels["General"][category] = all_items

color_scale=[
    [0.0, '#FFB950'],
    [0.5, '#FAF3DC'],
    [1.0, '#1FD0EF']
]

# <--- MODIFICADO --- He actualizado la función 'barras' para la comparativa con los colores solicitados
def barras(values_actual, labels, values_pasado, title) -> None:
    """
    Genera un gráfico de barras comparativo (actual vs. pasado).
    'values_pasado' debe tener la misma longitud que 'labels' y 'values_actual',
    usando float("nan") para los campos que no coinciden.
    """
    fig = go.Figure()
    
    # --- Trace 1: Año Actual --- (Aplica la escala de colores original)
    fig.add_trace(go.Bar(
        name='Mexico 2025', # Etiqueta para la leyenda
        x=labels,
        y=values_actual,
        texttemplate=[f'{y:.2f}' if pd.notna(y) else '' for y in values_actual], # Oculta texto si es NaN
        textposition='outside',
        marker=dict(
            color=values_actual, # <--- Se usa values_actual para aplicar la escala
            colorscale=color_scale, # <--- Aplica tu escala de colores
            line=dict(color='black', width=1.5)
        ),
        textfont=dict(color='black')
    ))

    # --- Trace 2: Año Pasado --- (Transparente con borde gris)
    hay_valores_pasado = pd.Series(values_pasado).notna().any()

    if hay_valores_pasado:
        fig.add_trace(go.Bar(
            name='Menorca 2025', # Etiqueta para la leyenda
            x=labels,
            y=values_pasado, # Plotly ignora los valores 'nan'
            texttemplate=[f'{y:.2f}' if pd.notna(y) else '' for y in values_pasado], # Oculta texto si es NaN
            textposition='outside',
            marker=dict(
                color='rgba(0,0,0,0)',  # <--- Transparente
                line=dict(color='darkgrey', width=1.5) # <--- Borde gris
            ),
            textfont=dict(color='darkgrey') # <--- El texto también en gris para que se vea
        ))
    
    # Calcular el rango máximo de forma segura, ignorando NaNs
    all_values = [v for v in values_actual if pd.notna(v)] + \
                 [v for v in values_pasado if pd.notna(v)]
    
    # Asegurarse de que el rango no esté vacío y tenga un default
    range_max = max(all_values) * 1.15 if all_values else 5 # Default a 5 si no hay datos

    fig.update_layout(
        title=title,
        yaxis_title='Mean Score',
        template="plotly_white",
        barmode='group', # <-- Clave para agrupar las barras
        yaxis=dict(
            range=[0, range_max] # Rango desde 0 hasta el máximo + 15%
        ),
        xaxis=dict(
            tickfont=dict(color='black'),
            tickangle=-45
        ),
        legend_title_text='Periodo'
    )
    
    st.plotly_chart(fig, use_container_width=True)
# <--- FIN DE LA MODIFICACIÓN ---

def metric(value, label) -> None:
    st.metric(value=value, label=label)

#medias de satisfaction, wellbeing y organization

general_means_per_phase: dict[str, list[float]] = {}
for phase in general_fields.keys():
    general_means_per_phase[phase] = []
    for field in general_fields[phase]:
        mean: float = round(float(df[field].dropna().astype(float).mean()), 2)
        general_means_per_phase[phase].append(mean)

general_means: list[float] = [0.0, 0.0, 0.0]
for i in range(3):
    for phase in general_means_per_phase.keys():
        general_means[i] += round(general_means_per_phase[phase][i], 2)

general_means: list[float] = [round(x / 3, 2) for x in general_means]


# <--- AÑADIDO --- Helper para calcular medias de forma segura ---
# Obtener los sets de columnas UNA SOLA VEZ para eficiencia
cols_pasado = set(df_past.columns)

def safe_mean(df_to_check, field):
    """Calcula la media si el campo existe, si no, devuelve nan."""
    # Usamos .columns.values porque 'in' es más rápido en un set/list que en un Index
    if field in df_to_check.columns.values:
        return float(df_to_check[field].dropna().astype(float).mean())
    return float("nan") # Devuelve NaN si el campo no existe

#===================================Vamos con Breathe===================================

#------------------------------Saquemos las medias-------------------------------------
means_breathe: dict = {}
means_breathe_pasado: dict = {} # <--- AÑADIDO
labels_breathe = labels["Breathe"]
for category in fields["Breathe"].keys():

    means_breathe[category] = []
    means_breathe_pasado[category] = [] # <--- AÑADIDO
    for field in fields["Breathe"][category]:
        # Calcula la media del año actual (siempre debe existir según 'fields')
        means_breathe[category].append(safe_mean(df, field))
        
        # Calcula la media del año pasado (dará NaN si el campo no existe)
        means_breathe_pasado[category].append(safe_mean(df_past, field)) # <--- AÑADIDO

#==================================Vamos con Focus==================================

#------------------------------Saquemos las medias-------------------------------------
means_focus: dict = {}
means_focus_pasado: dict = {} # <--- AÑADIDO
labels_focus = labels["Focus"]
for category in fields["Focus"].keys():

    means_focus[category] = []
    means_focus_pasado[category] = [] # <--- AÑADIDO
    for field in fields["Focus"][category]:
        means_focus[category].append(safe_mean(df, field))
        means_focus_pasado[category].append(safe_mean(df_past, field)) # <--- AÑADIDO

#=================================Vamos con Grow==================================

#------------------------------Saquemos las medias-------------------------------------
means_grow: dict = {}
means_grow_pasado: dict = {} # <--- AÑADIDO
labels_grow = labels["Grow"]
for category in fields["Grow"].keys():

    means_grow[category] = []
    means_grow_pasado[category] = [] # <--- AÑADIDO
    for field in fields["Grow"][category]:
        means_grow[category].append(safe_mean(df, field))
        means_grow_pasado[category].append(safe_mean(df_past, field)) # <--- AÑADIDO

#===========================General================================================

#--------------------------------las mediaas-----------------------------------------
means_general: dict = {}
means_general_pasado: dict = {} # <--- AÑADIDO
labels_general = labels["General"]
for category in fields["General"].keys():

    means_general[category] = []
    means_general_pasado[category] = [] # <--- AÑADIDO
    for field in fields["General"][category]:
        means_general[category].append(safe_mean(df, field))
        means_general_pasado[category].append(safe_mean(df_past, field)) # <--- AÑADIDO

#--------------------------------------------------------------------------------------------

st.markdown(body="Here you will find the average score for each event in the program, divided by Talks, Well-being and Networking:\n1. General: all events per category\n2. Breathe - Focus - Grow: all events too, but also divided by the phases")

st.markdown(body="<h1 style='text-align: center;'>General</h1>", unsafe_allow_html=True)

cols = st.columns(3)
for i in range(3):
    with cols[i]:
        st.metric(value=general_means[i], label=general_labels[i])

# <--- MODIFICADO --- Bucle de gráficos "General"
for category in fields["General"].keys():
    # Zip de las TRES listas para ordenar todo junto
    ordered_tuples_general = sorted(
        zip(
            means_general[category],
            means_general_pasado[category], # <--- AÑADIDO
            labels_general[category]
        ),
        key=lambda x: -1 if pd.isna(x[0]) else x[0], # Ordena por media actual (manejando NaNs)
        reverse=True
    )
    
    # Descomprimir las listas ya ordenadas
    values_graph_general = [v_act for v_act, v_pas, lab in ordered_tuples_general]
    values_graph_general_pasado = [v_pas for v_act, v_pas, lab in ordered_tuples_general] # <--- AÑADIDO
    labels_graph_general = [lab for v_act, v_pas, lab in ordered_tuples_general]

    # Llamar a la nueva función barras
    barras(
        values_actual=values_graph_general,
        labels=labels_graph_general,
        values_pasado=values_graph_general_pasado, # <--- AÑADIDO
        title=f"All: {category}"
    )

st.markdown(body="---")

st.markdown(body="<h1 style='text-align: center;'>Breathe</h1>", unsafe_allow_html=True)

#satisfaction, wellbeing y organization
cols = st.columns(3)
for i in range(3):
    with cols[i]:
        st.metric(value=general_means_per_phase["Breathe"][i], label=general_labels[i], delta=round(general_means_per_phase["Breathe"][i] - general_means[i], 2))

# <--- MODIFICADO --- Bucle de gráficos "Breathe"
for category in fields["Breathe"].keys():
    ordered_tuples_breathe = sorted(
        zip(
            means_breathe[category],
            means_breathe_pasado[category], # <--- AÑADIDO
            labels_breathe[category]
        ), 
        key=lambda x: -1 if pd.isna(x[0]) else x[0],
        reverse=True
    )
    
    values_graph_breathe = [v_act for v_act, v_pas, lab in ordered_tuples_breathe]
    values_graph_breathe_pasado = [v_pas for v_act, v_pas, lab in ordered_tuples_breathe] # <--- AÑADIDO
    labels_graph_breathe = [lab for v_act, v_pas, lab in ordered_tuples_breathe]
    
    barras(
        values_actual=values_graph_breathe,
        labels=labels_graph_breathe,
        values_pasado=values_graph_breathe_pasado, # <--- AÑADIDO
        title=f"Breathe: {category}"
    )

st.markdown(body="---")

st.markdown(body="<h1 style='text-align: center;'>Focus</h1>", unsafe_allow_html=True)

cols = st.columns(3)
for i in range(3):
    with cols[i]:
        st.metric(value=general_means_per_phase["Focus"][i], label=general_labels[i], delta=round(general_means_per_phase["Focus"][i] - general_means[i], 2))

# <--- MODIFICADO --- Bucle de gráficos "Focus"
for category in fields["Focus"].keys():
    ordered_tuples_focus = sorted(
        zip(
            means_focus[category],
            means_focus_pasado[category], # <--- AÑADIDO
            labels_focus[category]
        ), 
        key=lambda x: -1 if pd.isna(x[0]) else x[0],
        reverse=True
    )

    values_graph_focus = [v_act for v_act, v_pas, lab in ordered_tuples_focus]
    values_graph_focus_pasado = [v_pas for v_act, v_pas, lab in ordered_tuples_focus] # <--- AÑADIDO
    labels_graph_focus = [lab for v_act, v_pas, lab in ordered_tuples_focus]
    
    barras(
        values_actual=values_graph_focus,
        labels=labels_graph_focus,
        values_pasado=values_graph_focus_pasado, # <--- AÑADIDO
        title=f"Focus: {category}"
    )

st.markdown(body="---")

st.markdown(body="<h1 style='text-align: center;'>Grow</h1>", unsafe_allow_html=True)

cols = st.columns(3)
for i in range(3):
    with cols[i]:
        st.metric(value=general_means_per_phase["Grow"][i], label=general_labels[i], delta=round(general_means_per_phase["Grow"][i] - general_means[i], 2))

# <--- MODIFICADO --- Bucle de gráficos "Grow"
for category in fields["Grow"].keys():
    ordered_tuples_grow = sorted(
        zip(
            means_grow[category],
            means_grow_pasado[category], # <--- AÑADIDO
            labels_grow[category]
        ), 
        key=lambda x: -1 if pd.isna(x[0]) else x[0],
        reverse=True
    )
    
    values_graph_grow = [v_act for v_act, v_pas, lab in ordered_tuples_grow]
    values_graph_grow_pasado = [v_pas for v_act, v_pas, lab in ordered_tuples_grow] # <--- AÑADIDO
    labels_graph_grow = [lab for v_act, v_pas, lab in ordered_tuples_grow]

    barras(
        values_actual=values_graph_grow,
        labels=labels_graph_grow,
        values_pasado=values_graph_grow_pasado, # <--- AÑADIDO
        title=f"Grow: {category}"
    )