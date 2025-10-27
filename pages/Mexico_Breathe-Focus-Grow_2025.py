from typing import Any
from narwhals.functions import all_
import streamlit as st
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

def fix_cell(val):
    if isinstance(val, dict) and "specialValue" in val:
        return float("nan")
    return val

df = df.map(func=fix_cell)
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
            "Breathe | Pitching dynamic (Day 2)",
            "Breathe | Workstations",
            "Breathe | Founder Arena (1)",
            "Breathe | Founder Arena (2)",
            "Breathe | Founder Arena (3)",
            "Breathe | Cocktail at Binibeca (Day 1)",
            "Breathe | New connections"
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
            "Focus | 1:1's matching (Day 3)",
            "Cenote",
            "Focus | Paellas contest",
            "Kiin Beh"
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
        "Networking": [
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
            "Pitching dynamic",
            "Workstations",
            "Founder Arena Rui and Juanma",
            "Founder Arena Jose de la Luz",
            "Founder Arena Alex Wieland",
            "Welcome Cocktail",
            "New connections value"
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
            "1:1's matching",
            "Cenote",
            "Cooking Contest",
            "Kiin Beh"
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
        "Networking": [
            "Demo day"
        ]
    }
}

general_labels: list = [
    "Overall experience",
    "Wellbeing dynamics",
    "Information and coordination"
]

phases = ["Breathe", "Focus", "Grow"]
categories_to_merge = ["Talks", "Well-being", "Networking"]

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

def barras(values, labels, title) -> None:
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=labels,
        y=values,
        texttemplate='%{y:.2f}',
        textposition='outside',
        marker=dict(
            color=values,
            colorscale=color_scale,
            line=dict(
                color='black',
                width=1.5
            )
        ),
        textfont=dict(color='black')
    ))
    
    range_max = max(values) * 1.15 if values else 1

    fig.update_layout(
        title=title,
        yaxis_title='Mean Score',
        template="plotly_white",
        yaxis=dict(
            range=[1, range_max]
        ),
        xaxis=dict(
            tickfont=dict(color='black'),
            tickangle=-45
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)

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

#===================================Vamos con Breathe===================================

#------------------------------Saquemos las medias-------------------------------------
means_breathe: dict = {}
labels_breathe = labels["Breathe"]
for category in fields["Breathe"].keys():

    means_breathe[category] = []
    for field in fields["Breathe"][category]:
        mean_breathe: float = float(df[field].dropna().astype(float).mean())
        means_breathe[category].append(mean_breathe)

#==================================Vamos con Focus==================================

#------------------------------Saquemos las medias-------------------------------------
means_focus: dict = {}
labels_focus = labels["Focus"]
for category in fields["Focus"].keys():

    means_focus[category] = []
    for field in fields["Focus"][category]:
        mean_focus: float = float(df[field].dropna().astype(float).mean())
        means_focus[category].append(mean_focus)

#=================================Vamos con Grow==================================

#------------------------------Saquemos las medias-------------------------------------
means_grow: dict = {}
labels_grow = labels["Grow"]
for category in fields["Grow"].keys():

    means_grow[category] = []
    for field in fields["Grow"][category]:
        mean_grow: float = float(df[field].dropna().astype(float).mean())
        means_grow[category].append(mean_grow)

#===========================General================================================

#--------------------------------las mediaas-----------------------------------------
means_general: dict = {}
labels_general = labels["General"]
for category in fields["General"].keys():

    means_general[category] = []
    for field in fields["General"][category]:
        mean_general: float = float(df[field].dropna().astype(float).mean())
        means_general[category].append(mean_general)

#--------------------------------------------------------------------------------------------

st.markdown(body="Here you will find the average score for each event in the program, divided by Talks, Well-being and Networking:\n1. General: all events per category\n2. Breathe - Focus - Grow: all events too, but also divided by the phases")

st.markdown(body="<h1 style='text-align: center;'>General</h1>", unsafe_allow_html=True)

cols = st.columns(3)
for i in range(3):
    with cols[i]:
        st.metric(value=general_means[i], label=general_labels[i])

for category in fields["General"].keys():
    ordered_pairs_general = sorted(zip(means_general[category], labels_general[category]), reverse=True)
    values_graph_general = [value for value, label in ordered_pairs_general]
    labels_graph_general = [label for value, label in ordered_pairs_general]
    barras(values=values_graph_general, labels=labels_graph_general, title=f"All: {category}")

st.markdown(body="---")

st.markdown(body="<h1 style='text-align: center;'>Breathe</h1>", unsafe_allow_html=True)

#satisfaction, wellbeing y organization
cols = st.columns(3)
for i in range(3):
    with cols[i]:
        st.metric(value=general_means_per_phase["Breathe"][i], label=general_labels[i], delta=round(general_means_per_phase["Breathe"][i] - general_means[i], 2))

for category in fields["Breathe"].keys():
    ordered_pairs_breathe = sorted(zip(means_breathe[category], labels_breathe[category]), reverse=True)
    values_graph_breathe = [value for value, label in ordered_pairs_breathe]
    labels_graph_breathe = [label for value, label in ordered_pairs_breathe]
    barras(values=values_graph_breathe, labels=labels_graph_breathe, title=f"Breathe: {category}")

st.markdown(body="---")

st.markdown(body="<h1 style='text-align: center;'>Focus</h1>", unsafe_allow_html=True)

cols = st.columns(3)
for i in range(3):
    with cols[i]:
        st.metric(value=general_means_per_phase["Focus"][i], label=general_labels[i], delta=round(general_means_per_phase["Focus"][i] - general_means[i], 2))

for category in fields["Focus"].keys():
    ordered_pairs_focus = sorted(zip(means_focus[category], labels_focus[category]), reverse=True)
    values_graph_focus = [value for value, label in ordered_pairs_focus]
    labels_graph_focus = [label for value, label in ordered_pairs_focus]
    barras(values=values_graph_focus, labels=labels_graph_focus, title=f"Focus: {category}")

st.markdown(body="---")

st.markdown(body="<h1 style='text-align: center;'>Grow</h1>", unsafe_allow_html=True)

cols = st.columns(3)
for i in range(3):
    with cols[i]:
        st.metric(value=general_means_per_phase["Grow"][i], label=general_labels[i], delta=round(general_means_per_phase["Grow"][i] - general_means[i], 2))

for category in fields["Grow"].keys():
    ordered_pairs_grow = sorted(zip(means_grow[category], labels_grow[category]), reverse=True)
    values_graph_grow = [value for value, label in ordered_pairs_grow]
    labels_graph_grow = [label for value, label in ordered_pairs_grow]
    barras(values=values_graph_grow, labels=labels_graph_grow, title=f"Grow: {category}")

st.markdown(body="---")