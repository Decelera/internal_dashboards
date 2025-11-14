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
            "Talk by Sven Huber",
            "Focus | Shadi Yazdan's talk (Day 7)"
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

    if not df_to_check.empty and field in df_to_check.columns.tolist():
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

with st.expander(label="**Resumen de las ideas principales**"):
    st.markdown("""
    #### Comentarios Generales
    ---

    #### Experiencia y propósito
    Los founders valoraron profundamente el enfoque **humano, introspectivo y transformador** de la fase. Mencionaron la facilidad con la que pudieron **abrirse, pedir ayuda y conectar genuinamente** con otros emprendedores.  
    Destacaron la **estructura del programa**, el **human pitch**, las **1:1s**, las **workstations**, y las **actividades de meditación y yoga**, que facilitaron el proceso de reconexión personal y claridad de propósito.  
    Muchos afirmaron que lograron **salir del modo operativo diario**, ganar perspectiva, y **reenfocarse en lo esencial** tanto a nivel personal como empresarial.  

    #### Aprendizaje y conexión
    El intercambio entre founders, EMs y equipo Decelera fue señalado como una de las mayores fortalezas. Los participantes mencionaron haber recibido **feedback valioso, nuevas ideas, y aprendizajes aplicables** a su startup.  
    Las conversaciones honestas y los espacios de reflexión permitieron **reconectar con el propósito, entender mejor sus desafíos y fortalecer la visión global de sus proyectos**.  

    #### Organización y dinámica
    La **transición de actividades**, el orden del contenido y el ambiente general fueron altamente valorados. El inicio en viernes ayudó a “desconectar” más fácilmente, generando el estado mental ideal para aprovechar las siguientes fases.

    ---

    #### Ideas de Mejora
    ---

    #### Ritmo y carga de actividades
    - Reducir ligeramente el **volumen de contenido en la primera fase** para permitir más desconexión.  
    - Dejar **espacios entre sesiones (10-15 min)** o una hora diaria libre para procesar aprendizajes, descansar o atender asuntos urgentes.  
    - Algunas actividades se sintieron **aceleradas o encadenadas**, dificultando mantener la concentración al final del día.  
    - Incluir momentos de **“no hacer nada”** a mitad del día, cuando aún hay energía para reflexionar.

    #### Estructura y contenido
    - Dedicar más tiempo a las **1:1s** y permitir llenar el feedback al momento.  
    - Ofrecer dinámicas específicas para **perfiles técnicos (CTOs)** y ejercicios por rol.  
    - Profundizar en **sesiones prácticas** y ejemplos reales que conecten los conceptos con la operación diaria.  
    - Ampliar ligeramente la duración de la fase o permitir más tiempo de interacción con los EMs.

    #### Logística y herramientas
    - Mejorar la **precisión de ubicaciones en la app** y añadir una forma sencilla de **conectar entre founders y EMs** durante los espacios de networking.  
    - Incluir opciones de **agenda compartida o recordatorios automáticos**.  
    - Aprovechar el entorno con **alguna actividad al aire libre o cultural**, para integrar mejor la experiencia con el lugar.

    #### Clima y confianza
    - Dejar las encuestas **sin nombres** para promover feedback más honesto.  
    - Mantener el espíritu actual, ya que la mayoría coincidió en que **la experiencia fue casi perfecta** y que la esencia de Decelera debe preservarse.

    ---s

    #### Síntesis
    > Esta fase logró un impacto profundo en los founders, permitiéndoles reconectar consigo mismos y con el propósito de sus startups.  
    > Las sugerencias se centran en **reducir la intensidad, ampliar el tiempo de reflexión y mantener el equilibrio entre acción, pausa y conexión humana.**
    """, unsafe_allow_html=True)


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

with st.expander(label="**Resumen ideas principales**"):
    st.markdown("""
    #### Comentarios Generales
    ---

    #### Conexión y propósito
    Los founders destacaron esta fase como **profundamente transformadora**. Las conversaciones, 1:1s y actividades generaron **reflexión, claridad y alineación entre propósito personal y visión de empresa**.  
    Se valoró el ambiente de apertura, vulnerabilidad y confianza, que permitió cuestionarse, replantear estrategias y conectar emocionalmente con otros founders.  
    El **enfoque humano y consciente** de Decelera ayudó a frenar el ritmo, reconectarse con uno mismo y **redescubrir la motivación y dirección** del negocio.

    #### Aprendizaje y dinámicas
    Las **1:1s** fueron consideradas el elemento más valioso: aportaron feedback real, perspectivas distintas y herramientas aplicables.  
    Los participantes mencionaron también el **valor de los talks**, las **Founder Arenas**, las **visitas como Kiin Beh**, el **Demo Day** y las **actividades de mindfulness y yoga**.  
    Se resaltó la calidad de los EMs (especialmente Sean, Sofia, Shadi y Rui), las conversaciones tácticas y la combinación entre inspiración y acción práctica.  
    Muchos coincidieron en que esta fase fue el momento donde “**ocurrió la verdadera transformación**”.

    #### Impacto y resultados
    Los founders salieron con **más foco, energía renovada y claridad estratégica**. Algunos mencionaron haber replanteado su modelo de negocio o redirigido esfuerzos de equipo tras los aprendizajes.  
    Las actividades fuera del hotel y los espacios con la comunidad (como la visita a la escuela) fueron percibidos como experiencias significativas que reforzaron el sentido de propósito y compromiso con el impacto.

    ---

    #### Ideas de Mejora
    ---

    #### Ritmo y tiempo
    - Añadir **pequeños espacios libres (30-45 min)** durante el día para procesar aprendizajes, descansar o atender pendientes.  
    - Incluir **más tiempo para las 1:1s** (20 min fueron insuficientes para abordar temas complejos).  
    - Reducir la carga informativa o intercalar pausas para asimilar el contenido.  
    - Ampliar el **tiempo de journaling o reflexión estructurada** después de actividades intensas.  
    - Mantener una jornada más equilibrada, evitando sensación de cansancio acumulado.

    #### Preparación y contexto
    - Dar a los **EMs más contexto previo sobre cada startup** para aprovechar mejor las 1:1s.  
    - Enviar **información preparatoria antes del evento** para que founders lleguen con objetivos claros.  
    - Mejorar la **coordinación y claridad en actividades prácticas** (por ejemplo, el cooking contest o dinámicas de equipo).

    #### Contenido y enfoque
    - Introducir charlas o espacios sobre temas personales como **impacto del emprendimiento en la familia o equilibrio personal**.  
    - Repetir actividades comparativas como el **Workstation inicial y final** para medir evolución.  
    - Incluir más **actividades fuera del hotel** y experiencias culturales que fortalezcan la conexión con el entorno.  
    - Facilitar **networking guiado o por categorías** para founders menos extrovertidos.

    #### Logística y comunicación
    - Mejorar **audio, micrófonos y transporte**, y avisar con antelación que el programa requiere dedicación completa.  
    - Permitir grabar las **1:1s** para revisar aprendizajes.  
    - Aumentar la claridad sobre ubicaciones y tiempos en la app.

    ---

    #### Síntesis
    > Esta fase consolidó el impacto de Decelera como un programa que une profundidad humana con enfoque estratégico.  
    > Las mejoras propuestas apuntan a **optimizar el ritmo, ampliar el tiempo de reflexión y fortalecer la preparación de los EMs y logística**, sin perder la esencia de conexión, propósito y aprendizaje colectivo.
    """, unsafe_allow_html=True)


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

with st.expander(label="**Resumen ideas principales**"):
    st.markdown("""
    #### Comentarios Generales
    ---

    #### Experiencia general
    La **fase Grow** fue percibida como el cierre perfecto del proceso. Los founders destacaron el equilibrio entre **inspiración y ejecución**, la claridad estratégica alcanzada y la energía positiva del **Demo Day**.  
    Muchos mencionaron haber consolidado su propósito, estructurado sus próximos pasos y definido estrategias de crecimiento claras.  
    La **metodología** y el flujo entre fases fueron considerados coherentes, ayudando a mantener foco y aprovechar aprendizajes previos.

    #### Aprendizaje y conexión
    Los participantes resaltaron la **profundidad de las conversaciones** y el impacto de los **mentores** —especialmente Evaristo, Carolina, Varis y Sean— por su capacidad de guiar desde la experiencia y la reflexión.  
    Las **1:1s, Founder Arenas, talks y dinámicas de mindfulness** fueron muy valoradas por su aporte tanto personal como profesional.  
    Actividades como la visita a **Kiin Beh**, el **Castle Contest** y el **Demo Day** reforzaron la conexión emocional y el sentido de propósito.  
    Se destacó también el ambiente de colaboración y vulnerabilidad, que facilitó un aprendizaje compartido genuino.

    #### Impacto personal y profesional
    Esta fase ayudó a los founders a **convertir introspección en acción**, clarificando estrategias de expansión, posicionamiento y alianzas.  
    Varios mencionaron que salieron **más centrados, conscientes y alineados** con su visión de empresa. Algunos incluso tomaron decisiones clave, como cerrar o reestructurar sus startups, con serenidad y propósito.  
    La experiencia con los VCs fue relevante, y el programa logró **conectar crecimiento humano con crecimiento empresarial**.

    ---

    #### Ideas de Mejora
    ---

    #### Ritmo y estructura
    - Ajustar el calendario para dejar **más tiempo de preparación y descanso** entre actividades.  
    - Ampliar **espacios de reflexión o feedback posterior** a cada sesión para aterrizar aprendizajes.  
    - Mantener la energía del final equilibrando inspiración y ejecución; algunos sintieron el viernes un poco lento o con mucho contenido acumulado.  
    - Incluir **momentos de journaling estructurados** o espacios para escribir el plan de acción final.

    #### Contenido y enfoque
    - Añadir **más sesiones tácticas** sobre escalabilidad, legalidad internacional, compensaciones y alineación con inversionistas.  
    - Repetir o ampliar talleres con **Carolina, Varis o Beth**, especialmente sobre pitching y storytelling.  
    - Crear un bloque final para **descubrir oportunidades de colaboración entre startups** del mismo batch.  
    - Incluir una charla sobre **cuándo y cómo escalar** responsablemente, no solo cómo crecer.

    #### Inversionistas y networking
    - Mejorar la **interacción con VCs y ángeles**, ofreciendo más espacios 1:1 o dinámicas guiadas.  
    - Incorporar **mentorías específicas con inversionistas**, y dar visibilidad en la app de su disponibilidad y permanencia.  
    - Permitir que los pitches sean en el **idioma nativo (español)** cuando todos los asistentes lo compartan, para maximizar la claridad y confianza.  
    - Incluir más **early-stage investors** para generar tracción e interés temprano.

    #### Logística y comunicación
    - Avisar con claridad que el programa es **full time**, para que los founders puedan planificar y desconectarse totalmente.  
    - Mejorar la **coordinación en dinámicas prácticas** (como el cooking contest) y el seguimiento en app.  
    - Añadir una **actividad final de meditación o ejercicio** el último día para cerrar con calma y energía.

    ---

    #### Síntesis
    > La fase Grow consolidó todo el proceso de Decelera, transformando la reflexión en acción y la claridad en estrategia.  
    > Las mejoras sugeridas se enfocan en **refinar el ritmo, fortalecer la interacción con inversionistas y ampliar el enfoque táctico y colaborativo**, manteniendo la esencia humana y estratégica del programa.
    """, unsafe_allow_html=True)


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