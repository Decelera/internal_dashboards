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
    <h1 class="title-text">Program Feedback<br>Breathe - Focus - Grow</h1>
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

api_key = st.secrets["airtable_program"]["api_key"]
base_id = st.secrets["airtable_program"]["base_id"]
table_id = st.secrets["airtable_program"]["table_id"]

api = Api(api_key)
records = api.table(base_id, table_id).all(view="Menorca 2025")
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
            "Breathe | Marcos' talk (Day 1)",
            "Breathe | Grace Gu's talk (Day1)",
            "Breathe | Alex Rojas' talk (Day 1)",
            "Breathe | Ranny Nachmis' talk (Day 1)",
            "Breathe | Andrea Klimowitz's talk (Day 2)",
            "Breathe | Sean Cook's talk (Day 2)",
            "Breathe | David Baratech's talk (Day 2)",
            "Breathe | Beth Susanne's talk (Day 2)",
        ],
        "Well-being": [
            "Breathe | Lavanda ritual (Day 1)",
            "Breathe | Human pitch (Day 1)",
            "Breathe | Mindfulness (Day 2)",
            "Breathe | Yoga (Day 2)",
            "Breathe | Journaling (Day 2)"
        ],
        "Networking": [
            "Breathe | Cocktail at Binibeca (Day 1)",
            "Breathe | Pitching dynamic (Day 2)",
        ]
    },
    "Focus": {
        "Talks": [
            "Focus | Shari Swan's talk (Day 3)",
            "Focus | Jorge Gonzalez-Iglesias' talk (Day 3)",
            "Focus | Ivan Peña's talk (Day 3)",
            "Focus | Paul Ford's talk (Day 3)",
            "Focus | Fernando Cabello's talk (Day 3)",
            "Focus | Elise Mitchel's talk (Day 3)",
            "Focus | Gennaro Bifulco's talk (Day 4)",
            "Focus | Rui Fernandes' talk (Day 4)",
            "Focus | Oscar Macia's talk (Day 5)",
            "Focus | Jair Halevi's talk (Day 5)",
            "Focus | Torsten Kolind's talk (Day 5)",
            "Focus | Philippe Gelis' talk (Day 5)",
            "Focus | Juan de Antonio's talk (Day 5)",
            "Focus | Pedro Claveria's talk (Day 6)",
            "Focus | Juan Pablo Tejela & Laura Montells' talk (Day 6)",
            "Focus | Oscar Macia´s talk (Day 6)",
            "Focus | Juanjo, Arnau & Meri's talk (Day 7)",
            "Focus | Bastian's talk (Day 8)",
            "Focus | Shadi Yazdan's talk (Day 7)",
        ],
        "Well-being": [
            "Focus | Mindfulness (Day 3)",
            "Focus | Body movement (Day 3)",
            "Focus | Journaling (Day 3)",
            "Focus | Minfulness (Day 4)",
            "Focus | Breathwork (Day 4)",
            "Focus | Mindfulness (Day 5)",
            "Focus | Power yoga (Day 5)",
            "Focus | Startup mirror (Day 5)",
            "Focus | Mindfulness (Day 7)",
            "Focus | Soft yoga (Day 7)",
        ],
        "Networking": [
            "Focus | The founder arena (1)",
            "Focus | Castle contest (Day 4)",
            "Focus | 10th anniversary (Day 5)",
            "Focus | Founder arena (2)",
            "Focus | Paellas contest"
        ],
        "Investment": [
            "Focus | 1:1's matching (Day 3)",
            "Focus | 1:1's matching (Day 4)",
            "Focus | 1:1's matching (Day 5)",
            "Focus | Workstations (Day 6)",
            "Focus | 1:1's matching (Day 7)"
        ]
    },
    "Grow": {
        "Talks":[
            "Grow | Tom Dyer (Day 9)",
        ],
        "Well-being": [
            "Grow | Mindfulness (Day 8)",
            "Grow | Milu (Day 8)",
            "Grow | Mindfulness (Day 9)"
        ],
        "Networking": [
            "Grow | Open arena (Day 8)",
            "Grow | Human Pitch",
            "Grow | Farewell party (Day 9)"
        ],
        "Investment": [
            "Grow | Demo day",
            "Grow | 1:1's (Day 9)"
        ]
    }
}

labels: dict = {
    "Breathe": {
        "Talks": [
            "Talk by Marcos",
            "Talk byb Grace Gu",
            "Talk by Alex Rojas",
            "Talk by Rannth Nachmis",
            "Talk by Andrea Klimowitz",
            "Talk by Sean Cook",
            "Talk by David Baratech",
            "Talk by Beth Susanne",
        ],
        "Well-being": [
            "Lavanda ritual (Day 1)",
            "Human pitch (Day 1)",
            "Mindfulness (Day 2)",
            "Yoga (Day 2)",
            "Journaling (Day 2)",
        ],
        "Networking": [
            "Cocktail at Binibeca (Day 1)",
            "Pitching dynamic (Day 2)",
        ]
    },
    "Focus": {
        "Talks": [
            "Talk by Shari Swan",
            "Talk by Jorge Gonzalez-Iglesias",
            "Talk by Ivan Peña",
            "Talk by Paul Ford",
            "Talk by Fernando Cabello",
            "Talk by Elise Mitchel",
            "Talk by Gennaro Bifulco",
            "Talk by Rui Fernandes",
            "Talk by Oscar Macia (day 5)",
            "Talk by Jair Halevi",
            "Talk by Torsten Kolind",
            "Talk by Philippe Gelis",
            "Talk by Juan de Antonio",
            "Talk by Pedro Claveria",
            "Talk by Juan Pablo Tejela & Laura Montells",
            "Talk by Oscar Macia (day 6)",
            "Talk by Juanjo, Arnau & Meri",
            "Talk by Bastian",
            "Talk by Shadi Yazdan",
        ],
        "Well-being": [
            "Mindfulness (Day 3)",
            "Body movement (Day 3)",
            "Journaling (Day 3)",
            "Minfulness (Day 4)",
            "Breathwork (Day 4)",
            "Mindfulness (Day 5)",
            "Power yoga (Day 5)",
            "Startup mirror (Day 5)",
            "Mindfulness (Day 7)",
            "Soft yoga (Day 7)",
        ],
        "Networking": [
            "The founder arena (1)",
            "Castle contest (Day 4)",
            "10th anniversary (Day 5)",
            "Founder arena (2)",
            "Paellas contest"
        ],
        "Investment": [
            "1:1's matching (Day 3)",
            "1:1's matching (Day 4)",
            "1:1's matching (Day 5)",
            "Workstations (Day 6)",
            "1:1's matching (Day 7)"
        ]
    },
    "Grow": {
        "Talks":[
            "Talk by Tom Dyer",
        ],
        "Well-being": [
            "Mindfulness (Day 8)",
            "Milu (Day 8)",
            "Mindfulness (Day 9)"
        ],
        "Networking": [
            "Open arena (Day 8)",
            "Human pitch wrap up",
            "Farewell party (Day 9)"
        ],
        "Investment": [
            "Demo day",
            "1:1's (Day 9)"
        ]
    }
}

comment_fields = {
    "Breathe": [
        "Breathe | Comments",
        "Breathe | Improvement ideas"
    ],
    "Focus": [
        "Focus | Comments",
        "Focus | Improvement ideas",
        "Focus | Top 3 1:1's"
    ],
    "Grow": [
        "Grow | Comments",
        "Grow | Improvement Ideas"
    ]
}

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

for category in fields["General"].keys():
    ordered_pairs_general = sorted(zip(means_general[category], labels_general[category]), reverse=True)
    values_graph_general = [value for value, label in ordered_pairs_general]
    labels_graph_general = [label for value, label in ordered_pairs_general]
    barras(values=values_graph_general, labels=labels_graph_general, title=f"All: {category}")

st.markdown(body="---")

st.markdown(body="<h1 style='text-align: center;'>Breathe</h1>", unsafe_allow_html=True)

for category in fields["Breathe"].keys():
    ordered_pairs_breathe = sorted(zip(means_breathe[category], labels_breathe[category]), reverse=True)
    values_graph_breathe = [value for value, label in ordered_pairs_breathe]
    labels_graph_breathe = [label for value, label in ordered_pairs_breathe]
    barras(values=values_graph_breathe, labels=labels_graph_breathe, title=f"Breathe: {category}")

with st.expander(label="Comentarios de Breathe"):
    if not df[comment_fields["Breathe"][0]].empty:

        comments_breathe = df[["Name", comment_fields["Breathe"][0]]].dropna(subset=[comment_fields["Breathe"][0]])
        for index, row in comments_breathe.iterrows():
            name = row["Name"]
            comment = row[comment_fields["Breathe"][0]]
            
            with st.expander(label=f"Comment from {name}"):
                st.markdown(body=comment)

st.markdown(body="---")

st.markdown(body="<h1 style='text-align: center;'>Focus</h1>", unsafe_allow_html=True)

for category in fields["Focus"].keys():
    ordered_pairs_focus = sorted(zip(means_focus[category], labels_focus[category]), reverse=True)
    values_graph_focus = [value for value, label in ordered_pairs_focus]
    labels_graph_focus = [label for value, label in ordered_pairs_focus]
    barras(values=values_graph_focus, labels=labels_graph_focus, title=f"Focus: {category}")

with st.expander(label="Comentarios de Focus"):
    if not df[comment_fields["Focus"][0]].empty:

        comments_focus = df[["Name", comment_fields["Focus"][0]]].dropna(subset=[comment_fields["Focus"][0]])
        for index, row in comments_focus.iterrows():
            name = row["Name"]
            comment = row[comment_fields["Focus"][0]]
            
            with st.expander(label=f"Comment from {name}"):
                st.markdown(body=comment)

st.markdown(body="---")

st.markdown(body="<h1 style='text-align: center;'>Grow</h1>", unsafe_allow_html=True)

for category in fields["Grow"].keys():
    ordered_pairs_grow = sorted(zip(means_grow[category], labels_grow[category]), reverse=True)
    values_graph_grow = [value for value, label in ordered_pairs_grow]
    labels_graph_grow = [label for value, label in ordered_pairs_grow]
    barras(values=values_graph_grow, labels=labels_graph_grow, title=f"Grow: {category}")

with st.expander(label="Comentarios de Grow"):
    if not df[comment_fields["Grow"][0]].empty:

        comments_grow = df[["Name", comment_fields["Grow"][0]]].dropna(subset=[comment_fields["Grow"][0]])
        for index, row in comments_grow.iterrows():
            name = row["Name"]
            comment = row[comment_fields["Grow"][0]]
            
            with st.expander(label=f"Comment from {name}"):
                st.markdown(body=comment)


st.markdown(body="---")