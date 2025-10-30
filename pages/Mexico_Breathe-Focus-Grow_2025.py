from typing import Any
import streamlit as st
import pandas as pd
from pyairtable import Api
import plotly.graph_objects as go

#===============================================================CONFIGURACION DEL PROGRAMA===============================================
#=========================================================================================================================================

PROGRAM_YEAR = "2025"
PROGRAM_NAME = "Mexico 2025" #Este campo tiene que estar en formato "Localizacion Año", por ejemplo "Mexico 2025", sin tildes y con la primera en mayúscula
PAST_PROGRAM_NAME = "Menorca 2025"

#EN PRINCIPIO, SOLO MODIFICANDO ESTAS VARIABLES EL DASHBOARD DEBERIA FUNCIONAR CORRECTAMENTE MIENTRAS SE MANTENGAN LOS CAMPOS


#===============================================================CONFIGURACION DE LA PAGINA================================================
#=========================================================================================================================================
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
    <h1 class="title-text">Mexico 2025<br>Breathe - Focus - Grow</h1>
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

#==========================================================CONFIGURACION DEL SIDEBAR=====================================================
#========================================================================================================================================

if "selected_year" not in st.session_state:
    st.session_state.selected_year = PROGRAM_YEAR

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


#===========================================================CONFIGURACION DE LOS DATOS DE AIRTABLE======================================
#=======================================================================================================================================


api_key = st.secrets["airtable_program"]["api_key"]
base_id = st.secrets["airtable_program"]["base_id"]
table_id = st.secrets["airtable_program"]["table_id"]

api = Api(api_key)

#DataFrame del programa actual
try:
    records = api.table(base_id, table_id).all(view=PROGRAM_NAME)
    data = [record["fields"] for record in records]
    df = pd.DataFrame(data)
except Exception as e:
    st.warning(f"No se pudieron cargar los datos del programa actual (Error: {e})")
    df = pd.DataFrame()

#DataFrame del programa pasado
try:
    records_past = api.table(base_id, table_id).all(view=PAST_PROGRAM_NAME)
    data_past = [record["fields"] for record in records_past]
    df_past = pd.DataFrame(data_past)
except Exception as e:
    st.warning(f"No se pudieron cargar los datos del programa pasado (Error: {e})")
    df_past = pd.DataFrame()

#Arreglamos valores nulos
def fix_cell(val):
    if isinstance(val, dict) and "specialValue" in val:
        return float("nan")
    return val

df = df.map(func=fix_cell)
df_past = df_past.map(func=fix_cell)


#===========================================================CONFIGURACION DE LOS CAMPOS===============================================
#======================================================================================================================================


#Campos de Breathe Focus Grow
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

#Campos generales
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

#Etiquetas de Breathe Focus Grow
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

#Etiquetas de los campos generales
general_labels: list = [
    "Overall experience",
    "Wellbeing dynamics",
    "Information and coordination"
]

#Campos de comentarios
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


#Construimos los campos y las etiquetas para una review de las tres fases juntas (a lo que llamamos General)
categories_to_merge = ["Talks", "Well-being", "Networking", "Investment"]

if "General" not in fields:
    fields["General"] = {}
for category in categories_to_merge:
    all_items = []
    for phase in fields.keys():
        all_items.extend(fields[phase].get(category, []))
    fields["General"][category] = all_items

if "General" not in labels:
    labels["General"] = {}
for category in categories_to_merge:
    all_items = []
    for phase in fields.keys():
        all_items.extend(labels[phase].get(category, []))
    labels["General"][category] = all_items


#=================================================================CONFIGURACION DE LAS FUNCIONES====================================================================
#===================================================================================================================================================================


#Escala de color Decelera
color_scale=[
    [0.0, '#FFB950'],
    [0.5, '#FAF3DC'],
    [1.0, '#1FD0EF']
]

def barras(values_actual, labels, values_pasado, title, n_actual, n_pasado) -> None:
    """
    Genera un gráfico de barras comparativo (actual vs. pasado).
    'values_pasado' debe tener la misma longitud que 'labels' y 'values_actual',
    usando float("nan") para los campos que no coinciden.
    """

    fig = go.Figure()
    
    #Programa actual (con escala de colores)
    fig.add_trace(go.Bar(
        name=PROGRAM_NAME,
        x=labels,
        y=values_actual,
        customdata=n_actual,
        hovertemplate='Muestra: %{customdata}',
        texttemplate=[f'{y:.2f}' if pd.notna(y) else '' for y in values_actual],
        textposition='outside',
        marker=dict(
            color=values_actual,
            colorscale=color_scale,
            line=dict(color='black', width=1.5)
        ),
        textfont=dict(color='black')
    ))

    #Programa anterior (transparente, que llame menos la atención)
    hay_valores_pasado = pd.Series(values_pasado).notna().any()

    if hay_valores_pasado:
        fig.add_trace(go.Bar(
            name=PAST_PROGRAM_NAME,
            x=labels,
            y=values_pasado,
            customdata=n_pasado,
            hovertemplate='Muestra: %{customdata}',
            texttemplate=[f'{y:.2f}' if pd.notna(y) else '' for y in values_pasado],
            textposition='outside',
            marker=dict(
                color='rgba(0,0,0,0)',
                line=dict(color='darkgrey', width=1.5)
            ),
            textfont=dict(color='darkgrey')
        ))
    
    # Calcular el rango máximo de forma segura, ignorando NaNs
    all_values = [v for v in values_actual if pd.notna(v)] + \
                 [v for v in values_pasado if pd.notna(v)]
    
    # Asegurarse de que el rango no esté vacío y tenga un default
    range_max = max(all_values) * 1.15 if all_values else 5

    fig.update_layout(
        title=title,
        yaxis_title='Mean Score',
        template="plotly_white",
        barmode='group',
        yaxis=dict(
            range=[1, range_max]
        ),
        xaxis=dict(
            tickfont=dict(color='black'),
            tickangle=-45
        ),
        legend_title_text='Programa'
    )
    
    st.plotly_chart(fig, use_container_width=True)

#Funcion para calcular una media de forma segura
def safe_mean(df_to_check, field):
    """Calcula la media si el campo existe, si no, devuelve nan."""

    if field in df_to_check.columns.tolist():
        return float(df_to_check[field].dropna().astype(float).mean())

    return float("nan") # Devuelve NaN si el campo no existe

#Funcion para calcular un conteo de forma segura
def safe_count(df_to_check, field) -> int:
    """Calcula el conteo si el campo existe, si no, devuelve 0."""

    if not df_to_check.empty and field in df_to_check.columns.tolist():
        return int(df_to_check[field].dropna().count())

    return 0


#===========================================================CALCULOS DE LAS METRICAS==============================================================================
#=================================================================================================================================================================


#medias de satisfaction, wellbeing y organization
general_means_per_phase: dict[str, list[float]] = {}
for phase in general_fields.keys():
    general_means_per_phase[phase] = []
    for field in general_fields[phase]:
        mean: float = round(safe_mean(df, field), 2)
        general_means_per_phase[phase].append(mean)

general_means: list = [0.0, 0.0, 0.0]
for i in range(3):
    for phase in general_means_per_phase.keys():
        if general_means_per_phase[phase][i]:
            general_means[i] += round(general_means_per_phase[phase][i], 2)

general_means: list[float] = [round(x / 3, 2) for x in general_means]

#===================================Vamos con Breathe===================================

#------------------------------Saquemos las medias-------------------------------------

#En estos diccionarios guardaremos las medias (en listas normales) y las organizamos por categoria
means_breathe: dict = {}
means_breathe_pasado: dict = {}
n_breathe: dict = {}
n_breathe_pasado: dict = {}

for category in fields["Breathe"].keys():

    #definimos las listas que vamos a ir rellenando
    means_breathe[category] = []
    means_breathe_pasado[category] = []
    n_breathe[category] = []
    n_breathe_pasado[category] = []

    for field in fields["Breathe"][category]:
        # Calcula la media del año actual y del año pasado (la del pasado dara nan si no existe, pero la funcion de barras lo ignora)
        means_breathe[category].append(safe_mean(df, field))
        means_breathe_pasado[category].append(safe_mean(df_past, field))

        n_breathe[category].append(safe_count(df, field))
        n_breathe_pasado[category].append(safe_count(df_past, field))

#==================================Vamos con Focus==================================

#------------------------------Saquemos las medias-------------------------------------

#En estos diccionarios guardaremos las medias (en listas normales) y las organizamos por categoria
means_focus: dict = {}
means_focus_pasado: dict = {}
n_focus: dict = {}
n_focus_pasado: dict = {}

for category in fields["Focus"].keys():

    #definimos las listas que vamos a ir rellenando
    means_focus[category] = []
    means_focus_pasado[category] = []
    n_focus[category] = []
    n_focus_pasado[category] = []

    for field in fields["Focus"][category]:

        # Calcula la media del año actual y del año pasado (la del pasado dara nan si no existe, pero la funcion de barras lo ignora)
        means_focus[category].append(safe_mean(df, field))
        means_focus_pasado[category].append(safe_mean(df_past, field))

        n_focus[category].append(safe_count(df, field))
        n_focus_pasado[category].append(safe_count(df_past, field))

#=================================Vamos con Grow==================================

#------------------------------Saquemos las medias-------------------------------------

#En estos diccionarios guardaremos las medias (en listas normales) y las organizamos por categoria
means_grow: dict = {}
means_grow_pasado: dict = {}
n_grow: dict = {}
n_grow_pasado: dict = {}

for category in fields["Grow"].keys():
    
    #definimos las listas que vamos a ir rellenando
    means_grow[category] = []
    means_grow_pasado[category] = []
    n_grow[category] = []
    n_grow_pasado[category] = []

    for field in fields["Grow"][category]:

        # Calcula la media del año actual y del año pasado (la del pasado dara nan si no existe, pero la funcion de barras lo ignora)
        means_grow[category].append(safe_mean(df, field))
        means_grow_pasado[category].append(safe_mean(df_past, field))

        n_grow[category].append(safe_count(df, field))
        n_grow_pasado[category].append(safe_count(df_past, field))

#===========================General================================================

#--------------------------------las mediaas-----------------------------------------

#En estos diccionarios guardaremos las medias (en listas normales) y las organizamos por categoria
means_general: dict = {}
means_general_pasado: dict = {}
n_general: dict = {}
n_general_pasado: dict = {}

for category in fields["General"].keys():

    #En estos diccionarios guardaremos las medias (en listas normales) y las organizamos por categoria
    means_general[category] = []
    means_general_pasado[category] = [] 
    n_general[category] = []
    n_general_pasado[category] = []

    for field in fields["General"][category]:

        # Calcula la media del año actual y del año pasado (la del pasado dara nan si no existe, pero la funcion de barras lo ignora)
        means_general[category].append(safe_mean(df, field))
        means_general_pasado[category].append(safe_mean(df_past, field))

        n_general[category].append(safe_count(df, field))
        n_general_pasado[category].append(safe_count(df_past, field))

#==========================================================================VAMOS A REPRESENTAR LOS DATOS QUE HEMOS CALCULADO=========================================
#====================================================================================================================================================================

#=======================Vamos con General========================

st.markdown(body="Here you will find the average score for each event in the program, divided by Talks, Well-being and Networking:\n1. General: all events per category\n2. Breathe - Focus - Grow: all events too, but also divided by the phases")

st.markdown(body="<h1 style='text-align: center;'>General</h1>", unsafe_allow_html=True)

cols = st.columns(3)
for i in range(3):
    with cols[i]:
        st.metric(value=general_means[i], label=general_labels[i])

#Comprimimos los datos para que al ordenar por la media actual, no se pierda el orden de las categorías
for category in fields["General"].keys():
    # Zip de las TRES listas para ordenar todo junto
    ordered_tuples_general = sorted(
        zip(
            means_general[category],
            means_general_pasado[category],
            labels["General"][category],
            n_general[category],
            n_general_pasado[category]
        ),
        key=lambda x: -1 if pd.isna(x[0]) else x[0], # Ordena por media actual (manejando nan's)
        reverse=True
    )
    
    # Descomprimir las listas ya ordenadas
    values_graph_general = [v_act for v_act, v_pas, lab, n_act, n_pas in ordered_tuples_general]
    values_graph_general_pasado = [v_pas for v_act, v_pas, lab, n_act, n_pas in ordered_tuples_general]
    labels_graph_general = [lab for v_act, v_pas, lab, n_act, n_pas in ordered_tuples_general]
    n_graph_general = [n_act for v_act, v_pas, lab, n_act, n_pas in ordered_tuples_general]
    n_graph_general_pasado = [n_pas for v_act, v_pas, lab, n_act, n_pas in ordered_tuples_general]

    # Llamamos a la función barras, que ya lo tenemos todo
    barras(
        values_actual=values_graph_general,
        labels=labels_graph_general,
        values_pasado=values_graph_general_pasado,
        title=f"All: {category}",
        n_actual=n_graph_general,
        n_pasado=n_graph_general_pasado
    )

st.markdown(body="---")

#======================Vamos con Breathe========================

st.markdown(body="<h1 style='text-align: center;'>Breathe</h1>", unsafe_allow_html=True)

#satisfaction, wellbeing y organization
cols = st.columns(3)
for i in range(3):
    with cols[i]:
        st.metric(value=general_means_per_phase["Breathe"][i], label=general_labels[i], delta=round(general_means_per_phase["Breathe"][i] - general_means[i], 2))

#Comprimimos los datos para que al ordenar por la media actual, no se pierda el orden de las categorías
for category in fields["Breathe"].keys():
    ordered_tuples_breathe = sorted(
        zip(
            means_breathe[category],
            means_breathe_pasado[category],
            labels["Breathe"][category],
            n_breathe[category],
            n_breathe_pasado[category]
        ), 
        key=lambda x: -1 if pd.isna(x[0]) else x[0],
        reverse=True
    )
    
    # Descomprimir las listas ya ordenadas
    values_graph_breathe = [v_act for v_act, v_pas, lab, n_act, n_pas in ordered_tuples_breathe]
    values_graph_breathe_pasado = [v_pas for v_act, v_pas, lab, n_act, n_pas in ordered_tuples_breathe]
    n_graph_breathe = [n_act for v_act, v_pas, lab, n_act, n_pas in ordered_tuples_breathe]
    n_graph_breathe_pasado = [n_pas for v_act, v_pas, lab, n_act, n_pas in ordered_tuples_breathe]
    labels_graph_breathe = [lab for v_act, v_pas, lab, n_act, n_pas in ordered_tuples_breathe]
    
    # Llamamos a la función barras, que ya lo tenemos todo
    barras(
        values_actual=values_graph_breathe,
        labels=labels_graph_breathe,
        values_pasado=values_graph_breathe_pasado,
        title=f"Breathe: {category}",
        n_actual=n_graph_breathe,
        n_pasado=n_graph_breathe_pasado
    )

#Ahora hay que poner los campos de los comentarios
with st.expander(label="Comentarios de Breathe"):

    if comment_fields["Breathe"][0] in df.columns.tolist() and "Name" in df.columns.tolist() and not df[comment_fields["Breathe"][0]].empty:

        comments_breathe = df[["Name", comment_fields["Breathe"][0]]].dropna(subset=[comment_fields["Breathe"][0]])
        for index, row in comments_breathe.iterrows():
            name = row["Name"]
            comment = row[comment_fields["Breathe"][0]]
            
            with st.expander(label=f"Comment from {name}"):
                st.markdown(body=comment)

with st.expander(label="Improvement ideas de Breathe"):
    if comment_fields["Breathe"][1] in df.columns.tolist() and "Name" in df.columns.tolist() and not df[comment_fields["Breathe"][1]].empty:

        comments_breathe = df[["Name", comment_fields["Breathe"][1]]].dropna(subset=[comment_fields["Breathe"][1]])
        for index, row in comments_breathe.iterrows():
            name = row["Name"]
            comment = row[comment_fields["Breathe"][1]]
            
            with st.expander(label=f"Improvement idea from {name}"):
                st.markdown(body=comment)

st.markdown(body="---")

#======================Vamos con Focus=========================

st.markdown(body="<h1 style='text-align: center;'>Focus</h1>", unsafe_allow_html=True)

cols = st.columns(3)
for i in range(3):
    with cols[i]:
        st.metric(value=general_means_per_phase["Focus"][i], label=general_labels[i], delta=round(general_means_per_phase["Focus"][i] - general_means[i], 2))

#Comprimimos los datos para que al ordenar por la media actual, no se pierda el orden de las categorías
for category in fields["Focus"].keys():
    ordered_tuples_focus = sorted(
        zip(
            means_focus[category],
            means_focus_pasado[category],
            labels["Focus"][category],
            n_focus[category],
            n_focus_pasado[category]
        ), 
        key=lambda x: -1 if pd.isna(x[0]) else x[0],
        reverse=True
    )

    # Descomprimir las listas ya ordenadas
    values_graph_focus = [v_act for v_act, v_pas, lab, n_act, n_pas in ordered_tuples_focus]
    values_graph_focus_pasado = [v_pas for v_act, v_pas, lab, n_act, n_pas in ordered_tuples_focus]
    labels_graph_focus = [lab for v_act, v_pas, lab, n_act, n_pas in ordered_tuples_focus]
    n_graph_focus = [n_act for v_act, v_pas, lab, n_act, n_pas in ordered_tuples_focus]
    n_graph_focus_pasado = [n_pas for v_act, v_pas, lab, n_act, n_pas in ordered_tuples_focus]
    
    barras(
        values_actual=values_graph_focus,
        labels=labels_graph_focus,
        values_pasado=values_graph_focus_pasado,
        title=f"Focus: {category}",
        n_actual=n_graph_focus,
        n_pasado=n_graph_focus_pasado
    )

with st.expander(label="Comentarios de Focus"):
    if comment_fields["Focus"][0] in df.columns.tolist() and "Name" in df.columns.tolist() and not df[comment_fields["Focus"][0]].empty:

        comments_focus = df[["Name", comment_fields["Focus"][0]]].dropna(subset=[comment_fields["Focus"][0]])
        for index, row in comments_focus.iterrows():
            name = row["Name"]
            comment = row[comment_fields["Focus"][0]]
            
            with st.expander(label=f"Comment from {name}"):
                st.markdown(body=comment)

with st.expander(label="Improvement ideas de Focus"):
    if comment_fields["Focus"][1] in df.columns.tolist() and "Name" in df.columns.tolist() and not df[comment_fields["Focus"][1]].empty:

        comments_focus = df[["Name", comment_fields["Focus"][1]]].dropna(subset=[comment_fields["Focus"][1]])
        for index, row in comments_focus.iterrows():
            name = row["Name"]
            comment = row[comment_fields["Focus"][1]]
            
            with st.expander(label=f"Improvement idea from {name}"):
                st.markdown(body=comment)
            
with st.expander(label="Top 3 1:1's de Focus"):
    if comment_fields["Focus"][2] in df.columns.tolist() and "Name" in df.columns.tolist() and not df[comment_fields["Focus"][2]].empty:

        comments_focus = df[["Name", comment_fields["Focus"][2]]].dropna(subset=[comment_fields["Focus"][2]])
        for index, row in comments_focus.iterrows():
            name = row["Name"]
            comment = row[comment_fields["Focus"][2]]
            
            with st.expander(label=f"Top 3 1:1's from {name}"):
                st.markdown(body=comment)

st.markdown(body="---")

#======================Vamos con Grow=========================

st.markdown(body="<h1 style='text-align: center;'>Grow</h1>", unsafe_allow_html=True)

cols = st.columns(3)
for i in range(3):
    with cols[i]:
        st.metric(value=general_means_per_phase["Grow"][i], label=general_labels[i], delta=round(general_means_per_phase["Grow"][i] - general_means[i], 2))

#Comprimimos los datos para que al ordenar por la media actual, no se pierda el orden de las categorías
for category in fields["Grow"].keys():
    ordered_tuples_grow = sorted(
        zip(
            means_grow[category],
            means_grow_pasado[category],
            labels["Grow"][category],
            n_grow[category],
            n_grow_pasado[category]
        ), 
        key=lambda x: -1 if pd.isna(x[0]) else x[0],
        reverse=True
    )
    
    values_graph_grow = [v_act for v_act, v_pas, lab, n_act, n_pas in ordered_tuples_grow]
    values_graph_grow_pasado = [v_pas for v_act, v_pas, lab, n_act, n_pas in ordered_tuples_grow]
    labels_graph_grow = [lab for v_act, v_pas, lab, n_act, n_pas in ordered_tuples_grow]
    n_graph_grow = [n_act for v_act, v_pas, lab, n_act, n_pas in ordered_tuples_grow]
    n_graph_grow_pasado = [n_pas for v_act, v_pas, lab, n_act, n_pas in ordered_tuples_grow]

    barras(
        values_actual=values_graph_grow,
        labels=labels_graph_grow,
        values_pasado=values_graph_grow_pasado,
        title=f"Grow: {category}",
        n_actual=n_graph_grow,
        n_pasado=n_graph_grow_pasado
    )

with st.expander(label="Comentarios de Grow"):
    if comment_fields["Grow"][0] in df.columns.tolist() and "Name" in df.columns.tolist() and not df[comment_fields["Grow"][0]].empty:

        comments_grow = df[["Name", comment_fields["Grow"][0]]].dropna(subset=[comment_fields["Grow"][0]])
        for index, row in comments_grow.iterrows():
            name = row["Name"]
            comment = row[comment_fields["Grow"][0]]
            
            with st.expander(label=f"Comment from {name}"):
                st.markdown(body=comment)

with st.expander(label="Improvement ideas de Grow"):
    if comment_fields["Grow"][1] in df.columns.tolist() and "Name" in df.columns.tolist() and not df[comment_fields["Grow"][1]].empty:

        comments_grow = df[["Name", comment_fields["Grow"][1]]].dropna(subset=[comment_fields["Grow"][1]])
        for index, row in comments_grow.iterrows():
            name = row["Name"]
            comment = row[comment_fields["Grow"][1]]
            
            with st.expander(label=f"Improvement ideas from {name}"):
                st.markdown(body=comment)