from typing import Any
import streamlit as st
import pandas as pd
from pyairtable import Api
import plotly.graph_objects as go


#========================================PROGRAM CONFIGURATION=================================
#==============================================================================================

PROGRAM_YEAR = "2025"
PROGRAM_NAME = "Mexico 2025"
PAST_PROGRAM_NAME = "Menorca 2025"

#======================================PAGE CONFIGURATION=======================================
#===============================================================================================

if "selected_year" not in st.session_state:
    st.session_state.selected_year = PROGRAM_YEAR

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
    <h1 class="title-text">Decelera Program<br>Guests</h1>
</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
        [data-testid="stSidebarNav"] {
            display: none;
        }
    </style>
""", unsafe_allow_html=True)

#========================================SIDEBAR CONFIGURATION=====================================
#==================================================================================================

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


#====================================AIRTABLE CONFIGURATION=======================================
#=================================================================================================

def fix_cell(val):
    if isinstance(val, dict) and "specialValue" in val:
        return float("nan")
    return val

api_key = st.secrets["airtable_program"]["api_key"]
base_id = st.secrets["airtable_program"]["base_id"]
table_id = st.secrets["airtable_program"]["table_id"]

api = Api(api_key)

# Carga de datos actuales

try:
    records = api.table(base_id, table_id).all(view=PROGRAM_NAME)
    data = [record["fields"] for record in records]
    df = pd.DataFrame(data)
    df = df.map(func=fix_cell)
except Exception as e:
    st.warning(f"No se pudieron cargar los datos de este año. (Error: {e})")
    df = pd.DataFrame()

# Carga segura de datos pasados
try:
    records_past = api.table(base_id, table_id).all(view=PAST_PROGRAM_NAME) 
    data_past = [record["fields"] for record in records_past]
    df_past = pd.DataFrame(data_past)
    df_past = df_past.map(func=fix_cell)
except Exception as e:
    # Si falla (ej. la vista no existe), crea un df vacío y avisa en la app
    st.warning(f"No se pudieron cargar los datos comparativos del año pasado. Se mostrará solo el año actual. (Error: {e})")
    df_past = pd.DataFrame()


#============================================FIELDS CONFIGURATION==========================================
#==========================================================================================================


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

#=============================================FUNCTION CONFIGURATION========================================
#===========================================================================================================

color_scale=[
    [0.0, '#FFB950'],
    [0.5, '#FAF3DC'],
    [1.0, '#1FD0EF']
]

#funcion para ir representando las barras con comparacion con el año pasado
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

#funcion para calcular la media segura
def safe_mean(df_to_check, field):
    if not df_to_check.empty and field in df_to_check.columns.tolist():
        if not df_to_check[field].dropna().empty:
            return float(df_to_check[field].dropna().astype(float).mean())
    return float("nan")

#calculo seguro de los nps
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

#Para filtrar correctamente por la etiqueta de invitado
def safe_check_guest_type(x, type_name):
    if isinstance(x, list):
        return type_name in x
    if isinstance(x, str):
        return x == type_name
    return False

#Funcion segura para contar cuantos datos hay
def safe_count(df_to_check, field):
    if not df_to_check.empty and field in df_to_check.columns:
        return int(df_to_check[field].dropna().count())
    return float(0.0)


#=======================================NORMAILZACION (ESTO EN EL FUTURO NO HARA FALTA)====================
#==========================================================================================================

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

#para los de este año, que solo hay algunos
for field in fields_to_normalize:
    if field in df.columns:
        df[field] = df[field].apply(lambda x: safe_normalize(x) if pd.notna(x) else x)


for field in df_past.columns:
    try:
        df_past[field] = df_past[field].apply(lambda x: safe_normalize(x) if pd.notna(x) else x)
    except Exception as e:
        pass

#=============================================CALCULEMOS LAS COSILLAS=============================
#===========================================================================================================

#===================================Vamos con Founders===================================

#------------------------------Saquemos las medias-------------------------------------
#Filtro robusto
if not df.empty and "Guest_type" in df.columns.tolist():
    df_startup = df[df["Guest_type"].apply(safe_check_guest_type, type_name="Startup")]
else:
    df_startup = pd.DataFrame()

if not df_past.empty and "Guest_type" in df_past.columns.tolist():
    df_startup_past = df_past[df_past["Guest_type"].apply(safe_check_guest_type, type_name="Startup")]
else:
    df_startup_past = pd.DataFrame()

nps_startup_startup = calculate_nps(df=df_startup, field="Recommendation to Startups")

means_founder: list = []
means_founder_pasado: list = []
n_founder: list = []
n_founder_pasado: list = []

labels_startup = labels["Founders"]
for field in fields["Founders"]:
    means_founder.append(safe_mean(df_startup, field))
    n_founder.append(safe_count(df_startup, field))

    means_founder_pasado.append(safe_mean(df_startup_past, field))
    n_founder_pasado.append(safe_count(df_startup_past, field))

#==================================Vamos con EMs==================================

#------------------------------Saquemos las medias-------------------------------------
# --- Filtro robusto (acepta listas o strings) ---
if not df.empty and "Guest_type" in df.columns.tolist():
    df_em = df[df["Guest_type"].apply(safe_check_guest_type, type_name="EM")]
else:
    df_em = pd.DataFrame()

if not df_past.empty and "Guest_type" in df_past.columns:
    df_em_past = df_past[df_past["Guest_type"].apply(safe_check_guest_type, type_name="EM")]
else:
    df_em_past = pd.DataFrame()

nps_em_startup = calculate_nps(df=df_em, field="Recommendation to Startups")
nps_em_em = calculate_nps(df=df_em, field="EM's Fb | Recommendation to EM")

means_em: list = []
means_em_pasado: list = []
n_em: list = []
n_em_pasado: list = []

labels_em = labels["EMs"]
for field in fields["EMs"]:
    means_em.append(safe_mean(df_em, field))
    n_em.append(safe_count(df_em, field))

    means_em_pasado.append(safe_mean(df_em_past, field))
    n_em_pasado.append(safe_count(df_em_past, field))


#=================================Vamos con VCs==================================

#------------------------------Saquemos las medias-------------------------------------
# --- Filtro robusto (acepta listas o strings) ---
if not df.empty and "Guest_type" in df.columns.tolist():
    df_vc = df[df["Guest_type"].apply(safe_check_guest_type, type_name="VC")]
else:
    df_vc = pd.DataFrame()

if not df_past.empty and "Guest_type" in df_past.columns.tolist():
    df_vc_past = df_past[df_past["Guest_type"].apply(safe_check_guest_type, type_name="VC")]
else:
    df_vc_past = pd.DataFrame()

nps_vc_startup = calculate_nps(df=df_vc, field="Recommendation to Startups")
nps_vc_vc = calculate_nps(df=df_vc, field="VC's | Recommendation to vc")

means_vc: list = []
means_vc_pasado: list = []
labels_vc = labels["VCs"]
n_vc: list = []
n_vc_pasado: list = []

for field in fields["VCs"]:
    means_vc.append(safe_mean(df_vc, field))
    n_vc.append(safe_count(df_vc, field))

    means_vc_pasado.append(safe_mean(df_vc_past, field))
    n_vc_pasado.append(safe_count(df_vc_past, field))
        

#===============================================REPRESENTAMOS TO=============================
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

with st.expander("**Resumen de las ideas principales**"):
    st.markdown("""
    #### Experiencia transformadora y humana
    Decelera es percibido como una experiencia única por su enfoque en el bienestar, la introspección y el crecimiento personal, combinando aceleración empresarial con humanidad y propósito.

    #### Comunidad y conexiones
    Se valoró la calidad humana de founders, mentores e inversionistas, así como la autenticidad y profundidad de las conversaciones. La comunidad y el apoyo mutuo fueron grandes diferenciadores.

    #### Espacios de reflexión
    Se sugiere crear pequeños bloques diarios (~30 min) para procesar aprendizajes, descansar y asimilar ideas, además de incluir momentos de journaling o pausas durante el día.

    #### Áreas de mejora
    - Mejorar la selección de inversionistas, priorizando a quienes estén activos y listos para invertir.  
    - Ampliar networking y 1:1s, dejando más espacio libre para conectar de forma orgánica.  
    - Añadir sesiones tácticas sobre temas legales, fundraising y estructura internacional.  
    - Mejorar app, tiempos y materiales (por ejemplo, el cuaderno).

    #### Enfoque regional y diversidad
    Incluir contenidos adaptados a ecosistemas como LATAM y fomentar mayor diversidad (más fundadoras mujeres y startups en distintas etapas).

    #### Síntesis
    > Decelera es un programa profundamente humano y transformador.  
    > Las sugerencias apuntan a refinar la logística, fortalecer la comunidad y ampliar el impacto práctico más allá del retiro.
    """, unsafe_allow_html=True)



with st.expander(label="Improvement ideas from founders"):
    if not df_startup.empty and "Improvement ideas" in df_startup.columns.tolist():

        comments_founders = df_startup[["Name", "Improvement ideas"]].dropna(subset=["Improvement ideas"])
        for index, row in comments_founders.iterrows():
            name = row["Name"]
            comment = row["Improvement ideas"]
            
            with st.expander(label=f"Improvement ideas from {name}"):
                st.markdown(body=comment)

with st.expander(label="Most positive aspect from founders"):
    if not df_startup.empty and "Most positive aspect" in df_startup.columns.tolist():

        comments_founders = df_startup[["Name", "Most positive aspect"]].dropna(subset=["Most positive aspect"])
        for index, row in comments_founders.iterrows():
            name = row["Name"]
            comment = row["Most positive aspect"]
            
            with st.expander(label=f"Most positive aspect from {name}"):
                st.markdown(body=comment)

with st.expander(label="Top 3 outcomes from founders"):
    if not df_startup.empty and "Top 3 outcomes" in df_startup.columns.tolist():

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

with st.expander(label="**Resumen de las ideas principales**"):
    st.markdown("""
    #### Comentarios Positivos
    ---

    #### Calidad del programa y participantes
    Alta calidad de founders y startups, con gran disposición para aprender, conectar y compartir. Los mentores destacaron el **mejor nivel respecto al año anterior** y la **diversidad de perfiles**. La combinación de founders, EMs, VCs y el equipo generó un ambiente inspirador y colaborativo.

    #### Experiencia y equipo
    El **equipo de Decelera** fue ampliamente reconocido por su energía, propósito y profesionalismo. Se destacó la **organización impecable, la logística, y la atención al detalle**, además del ambiente humano y cercano que se mantuvo durante todo el evento.

    #### Conexión y momentos informales
    Los momentos fuera de las sesiones formales —comidas, cenas y actividades sociales— fueron percibidos como los más valiosos para **crear vínculos auténticos y conversaciones profundas** entre startups, mentores e inversionistas.

    #### Actividades destacadas
    El **Founder’s Arena**, las **sesiones 1:1**, el **yoga y la meditación matinal**, y la **claridad del programa** fueron considerados puntos fuertes. También se valoró el **balance entre actividades** y la **mejora en la calidad del contenido y del hotel** respecto a años previos.

    #### Reflexiones sobre el acompañamiento a startups
    Varios mentores resaltaron la necesidad de que los founders cuenten con **guías estructuradas y marcos operativos** para aterrizar estrategias de expansión, internacionalización y alineación interna. Decelera fue vista como una plataforma ideal para catalizar ese tipo de crecimiento sostenible.

    ---

    #### Ideas de Mejora
    ---

    #### Estructura y tiempos
    - **Agenda demasiado cargada**, con poco tiempo para descansos o interacción orgánica.  
    - **1:1s muy intensos**; sugerencia de dividirlos en más jornadas o dejar espacio para completar feedback.  
    - Solicitud de **bloques abiertos o menos estructurados** para conversaciones más naturales.  
    - **Evitar solapamiento de charlas** o sesiones demasiado teóricas.

    #### Preparación y logística
    - Entregar con anticipación la **agenda de 1:1s y materiales (pitch deck, one-pager)**.  
    - Mejorar el **uso de la app**, añadiendo opción de sincronizar con calendarios personales.  
    - Revisar temas logísticos como **traslados y tiempos de espera**.

    #### Networking y comunidad
    - Más **espacios para conectar entre EMs e inversionistas**, no solo con startups.  
    - Incluir dinámicas para que **mentores inversores puedan conocer a todos los founders**, aunque sea brevemente.  
    - **Fortalecer el seguimiento post-retreat** con grupos o check-ins de progreso.

    #### Contenido y enfoque
    - Separar founders **primerizos de repetidores** para adaptar mejor las sesiones.  
    - Promover **workshops prácticos** sobre estrategia de mercado y crecimiento.  
    - En las charlas, fomentar **contenido más accionable** y menos centrado en la historia del ponente.

    ---

    #### Síntesis
    > Decelera sigue consolidándose como una experiencia de alto valor humano y profesional.  
    > Las mejoras se centran en **ajustar tiempos, fortalecer la preparación y logística, y ofrecer más espacios orgánicos y prácticos de conexión y aprendizaje.**
    """, unsafe_allow_html=True)


with st.expander(label="Comments from EMs"):
    if not df_em.empty and "Comments" in df_em.columns.tolist():

        comments_founders = df_em[["Name", "Comments"]].dropna(subset=["Comments"])
        for index, row in comments_founders.iterrows():
            name = row["Name"]
            comment = row["Comments"]
            
            with st.expander(label=f"Comments from {name}"):
                st.markdown(body=comment)

with st.expander(label="Improvement ideas from EMs"):
    if not df_em.empty and "Improvement ideas" in df_em.columns.tolist():

        comments_founders = df_em[["Name", "Improvement ideas"]].dropna(subset=["Improvement ideas"])
        for index, row in comments_founders.iterrows():
            name = row["Name"]
            comment = row["Improvement ideas"]
            
            with st.expander(label=f"Improvement ideas from {name}"):
                st.markdown(body=comment)

with st.expander(label="Top3 1:1's from EMs"):
    if not df_em.empty and "EM's Fb | Top3 1:1's" in df_em.columns.tolist():

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

with st.expander(label="**Resumen de las ideas principales**"):
    st.markdown("""
    #### Comentarios Generales
    ---

    #### Experiencia y ambiente
    El evento fue percibido como **auténtico, bien diseñado y de alto valor humano**. Los inversionistas destacaron la **energía positiva, la calidad de los founders y startups**, y el formato más **personal y cercano**, que facilita la conexión real y el entendimiento del propósito detrás de cada proyecto.  
    Varios comentaron que el programa **inspira confianza y transparencia**, lo que permite conversaciones más profundas y colaboraciones potenciales. Algunos incluso ya están **en conversaciones con startups** que conocieron durante el evento.

    ---

    #### Ideas de Mejora
    ---

    #### Agenda y planificación
    - Compartir la **agenda y horarios con mayor anticipación** para que los inversionistas puedan organizar su tiempo y participar más activamente.  
    - Incluir un **día opcional previo o posterior** para que los inversores puedan conectar con los founders antes o después del programa principal.  
    - Después del **Demo Day**, crear un **espacio de 1:1s** para profundizar conversaciones sobre oportunidades específicas.

    #### Networking y relación con startups
    - Aumentar la **profundidad de las sesiones de networking** entre inversionistas y startups, ya que algunos percibieron menos interacción que en ediciones previas.  
    - Fortalecer también las conexiones **entre los mismos inversionistas**, generando dinámicas colaborativas o de intercambio de criterios.

    #### Herramientas y logística
    - Hacer más completa la **información de las startups en la app**, incluyendo detalles de contacto y tracción.  
    - Agregar **links directos a perfiles** desde la aplicación para facilitar el seguimiento.  
    - Mejorar la **organización del transporte para inversionistas**, buscando opciones más cómodas o coordinadas.

    ---

    #### Síntesis
    > Los inversionistas valoran el enfoque humano, la calidad del ecosistema y el formato íntimo del programa.  
    > Las sugerencias se centran en **anticipar información clave, mejorar las herramientas de conexión y ampliar el tiempo de interacción con los founders.**
    """, unsafe_allow_html=True)


with st.expander(label="Comments from VCs"):
    if not df_vc.empty and "Comments" in df_vc.columns.tolist():

        comments_founders = df_vc[["Name", "Comments"]].dropna(subset=["Comments"])
        for index, row in comments_founders.iterrows():
            name = row["Name"]
            comment = row["Comments"]
            
            with st.expander(label=f"Comments from {name}"):
                st.markdown(body=comment)

with st.expander(label="Improvement ideas from VCs"):
    if not df_vc.empty and "Improvement ideas" in df_vc.columns.tolist():

        comments_founders = df_vc[["Name", "Improvement ideas"]].dropna(subset=["Improvement ideas"])
        for index, row in comments_founders.iterrows():
            name = row["Name"]
            comment = row["Improvement ideas"]
            
            with st.expander(label=f"Improvement ideas from {name}"):
                st.markdown(body=comment)

with st.expander(label="Investment interest from VCs"):
    if not df_vc.empty and "Investment Interest" in df_vc.columns.tolist():

        comments_founders = df_vc[["Name", "Investment Interest"]].dropna(subset=["Investment Interest"])
        for index, row in comments_founders.iterrows():
            name = row["Name"]
            comment = row["Investment Interest"]
            
            with st.expander(label=f"Investment interest from {name}"):
                st.markdown(body=comment)

st.markdown(body="---")