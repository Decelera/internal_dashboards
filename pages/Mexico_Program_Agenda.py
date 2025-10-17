import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Mexico - Program - Agenda",
    page_icon="../.streamlit/static/favicon.png",
    layout="wide"
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
    
    # 2025 (Title 2)
    st.markdown("&nbsp;&nbsp;&nbsp;&nbsp;**2025**")
    
    # Investment section (Title 4)
    st.markdown("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Investment**")
    
    # Investment pages (Title 5)
    if st.button("General", key="mx_inv_general", use_container_width=True):
        st.switch_page("pages/Mexico_Investment_General.py")
    
    if st.button("Per Startup", key="mx_inv_startup", use_container_width=True):
        st.switch_page("pages/Mexico_Investment_Per_Startup.py")
    
    # Program section (Title 4)
    st.markdown("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Program**")
    
    # Program pages (Title 5)
    if st.button("General", key="mx_prog_general", use_container_width=True):
        st.switch_page("pages/Mexico_Program_General.py")
    
    if st.button("Agenda", key="mx_prog_agenda", use_container_width=True):
        st.switch_page("pages/Mexico_Program_Agenda.py")
    
    st.markdown("---")
    
    # Menorca (Title 1)
    st.markdown("#### Menorca")
    
    # 2025 (Title 2)
    st.markdown("&nbsp;&nbsp;&nbsp;&nbsp;**2025**")
    
    # Investment section (Title 4)
    st.markdown("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Investment**")
    
    # Investment pages (Title 5)
    if st.button("General", key="mn_inv_general", use_container_width=True):
        st.switch_page("pages/Menorca_Investment_General.py")
    
    if st.button("Per Startup", key="mn_inv_startup", use_container_width=True):
        st.switch_page("pages/Menorca_Investment_Per_Startup.py")
    
    # Program section (Title 4)
    st.markdown("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Program**")
    
    # Program pages (Title 5)
    if st.button("General", key="mn_prog_general", use_container_width=True):
        st.switch_page("pages/Menorca_Program_General.py")
    
    if st.button("Agenda", key="mn_prog_agenda", use_container_width=True):
        st.switch_page("pages/Menorca_Program_Agenda.py")
# Breadcrumb navigation
st.caption("Mexico → 2025 → Investment → Program → Agenda")

# Page header
st.title("Mexico - Program - Agenda")

st.markdown("---")

import streamlit as st
import pandas as pd
from pyairtable import Api
import plotly.graph_objects as go

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

df = df.map(fix_cell)
df = df[df["Event"].apply(lambda x: "Mexico 2025" in x) & df["Guest_type"].apply(lambda x: "Startup" in x)]
#=========================CONFIG===============================

fields = {
    "Breathe": [
        "Breathe | Human pitch (Day 1)",
        "Breathe | Mindfulness (Day 2)",
        "Breathe | Yoga (Day 2)",
        "Breathe | Pitching dynamic (Day 2)",
        "Breathe | Journaling (Day 2)",
        "Breathe | Workstations",
        "Breathe | Founder Arena (1)",
        "Breathe | Founder Arena (2)",
        "Breathe | Founder Arena (3)",
        "Talk by Jose de la Luz",
        "Talk by Juanma Lopera",
        "Talk by Diego Meller",
        "Talk by Alex Wieland",
        "Breathe | Marcos' talk (Day 1)",
        "Breathe | Beth Susanne's talk (Day 2)",
        "Breathe | Cocktail at Binibeca (Day 1)",
        "Breathe | New connections",
        "Breathe | Satisfaction",
        "Breathe | Wellbeing",
        "Breathe | Organization"
    ],
    "Focus": [
        "Focus | Mindfulness (Day 3)",
        "Focus | Body movement (Day 3)",
        "Focus | Power yoga (Day 5)",
        "Focus | Journaling (Day 3)",
        "Talk by Alejandro Lopez",
        "Talk by Javier Cardona",
        "Talk by Eyal Shatz",
        "Talk by Sofia Storberg",
        "Breathe | Sean Cook's talk (Day 2)",
        "Talk by Vincent Speranza",
        "Talk by Victor Noguera",
        "Talk by Jose V. Fernandez",
        "Talk by Sven Huber",
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
        "Kiin Beh",
        "Focus | Satisfaction",
        "Focus | Wellbeing",
        "Focus | Organization"
    ],
    "Grow": [
        "Grow | Mindfulness (Day 8)",
        "Grow | HIT",
        "Grow | Journaling",
        "Grow | Human Pitch",
        "Talk by Evaristo Babe",
        "Talk by Evaristo and Carolina",
        "Grow | Demo day",
        "Grow | Satisfaction",
        "Grow | Wellbeing",
        "Grow | Organization"
    ]
}

labels = {
    "Breathe": [
        "Human pitch",
        "Mindfulness",
        "Yoga",
        "Pitching dynamic",
        "Journaling",
        "Workstations",
        "Founder Arena: Rui y Juanma",
        "Founder Arena: Jose de la Luz",
        "Founder Arena: Alex Wieland",
        "Talk by Jose de la Luz",
        "Talk by Juanma Lopera",
        "Talk by Diego Meller",
        "Talk by Alex Wieland",
        "Talk by Marcos",
        "Talk by Beth Susanne",
        "Welcome coktail",
        "New connections value",
        "Overall experience",
        "Wellbeing",
        "Clear Information"
    ],
    "Focus": [
        "Mindfulness",
        "Body movement",
        "Power yoga",
        "Journaling",
        "Talk by Alejandro Lopez",
        "Talk by Javier Cardona",
        "Talk by Eyal Shatz",
        "Talk by Sofia Storberg",
        "Talk by Sean Cook",
        "Talk by Vincent Speranza",
        "Talk by Victor Noguera",
        "Talk by Jose V. Fernandez",
        "Talk by Sven Huber",
        "Founder Arena: Sean Cook",
        "Founder Arena: Sofia Storberg",
        "Founder Arena: Shadi Yazdan",
        "Founder Arena: Varis y Carolina",
        "Founder Arena: Javier y Eyal",
        "Founder Arena: Rui Fernandez",
        "Founder arena: Mesa de VC's",
        "Founder Arena: Jose V. Fernandez",
        "1:1's matching",
        "Cenote Yax Kiin",
        "Cooking contest",
        "Kiin Beh",
        "Satisfaction overall",
        "Wellbeing",
        "Clear Information"
    ],
    "Grow": [
        "Mindfulness",
        "HIT",
        "Journaling",
        "Human pitch",
        "Talk by Evaristo Babe",
        "Talk by Evaristo and Carolina",
        "Demo day",
        "Satisfaction overall",
        "Wellbeing",
        "Clear Information"
    ]
}

deceleration_map = {
    "1": "Very accelerated",
    "2": "A little acelerated",
    "3": "Decelerated",
    "4": "Fully decelerated"
}

decelera_colors = ["1FD0EF", "#FFB950", "#FAF3DC", "#1158E5"]

st.set_page_config(
    page_title="Opencall Dashboard Decelera Mexico 2025",
    layout="centered"
)

num_columns = 3
#====================================================================
st.markdown("<p>All these scores are out of 4</p>", unsafe_allow_html=True)
#-----------------------------Breathe---------------------------------
st.markdown("<h1 style='text-align: center;'>Breathe</h1>", unsafe_allow_html=True)

num_rows = (len(fields["Breathe"]) + num_columns -1) // num_columns

for i in range(num_rows):
    cols = st.columns(num_columns)

    row_fields = fields["Breathe"][i * num_columns : (i + 1) * num_columns]

    for j, field in enumerate(row_fields):
        mean = df[field].dropna().astype(float).mean()

        with cols[j]:

            st.markdown(
                f"""
                <div style="
                    border: 2px solid #909090;
                    border-radius: 15px; /* Bordes redondeados */
                    padding: 20px;
                    text-align: center;
                    background-color: #f9f9f9;
                    box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
                    height: 150px; /* Altura fija para alinear tarjetas */
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                ">
                    <h4 style="margin-bottom: 10px;">{labels["Breathe"][fields["Breathe"].index(field)]}</h4>
                    <p style="font-size: 28px; font-weight: bold; margin: 0;">{mean:.2f}</p>
                </div>
                """,
                unsafe_allow_html=True)
            st.write("")

comments = df[["Name", "Breathe | Comments"]].dropna()
improvement_ideas = df[["Name", "Breathe | Improvement ideas"]].dropna()
with st.expander("Ver comentarios de Breathe"):
    for i, comment in enumerate(comments["Breathe | Comments"].tolist()):
        with st.expander(f"Ver comentario de {comments['Name'].iloc[i]}"):
            st.info(comment)

with st.expander("Ver ideas de mejora de Breathe"):
    for i, comment in enumerate(improvement_ideas["Breathe | Improvement ideas"].tolist()):
        with st.expander(f"Ver idea de {improvement_ideas['Name'].iloc[i]}"):
            st.info(comment)

deceleration_count = df["Breathe | Deceleration"].dropna().value_counts()
deceleration_mapped = deceleration_count.rename(index=deceleration_map)

fig = go.Figure(data=[go.Pie(
    labels=deceleration_mapped.index,
    values=deceleration_mapped.values,
    marker=dict(colors=decelera_colors)
)])

fig.update_layout(title_text="Deceleration thermometer")

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
#-----------------------------Focus---------------------------------
st.markdown("<h1 style='text-align: center;'>Focus</h1>", unsafe_allow_html=True)

num_rows = (len(fields["Focus"]) + num_columns -1) // num_columns

for i in range(num_rows):
    cols = st.columns(num_columns)

    row_fields = fields["Focus"][i * num_columns : (i + 1) * num_columns]

    for j, field in enumerate(row_fields):

        with cols[j]:
            mean = df[field].dropna().astype(float).mean()

            st.markdown(
                f"""
                <div style="
                    border: 2px solid #909090;
                    border-radius: 15px; /* Bordes redondeados */
                    padding: 20px;
                    text-align: center;
                    background-color: #f9f9f9;
                    box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
                    height: 150px; /* Altura fija para alinear tarjetas */
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                ">
                    <h4 style="margin-bottom: 10px;">{labels["Focus"][fields["Focus"].index(field)]}</h4>
                    <p style="font-size: 28px; font-weight: bold; margin: 0;">{mean:.2f}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            st.write("")

comments = df[["Name", "Focus | Comments"]].dropna()
improvement_ideas = df[["Name", "Focus | Improvement ideas"]].dropna()
top3 = df[["Name", "Focus | Top 3 1:1's"]].dropna()
with st.expander("Ver comentarios de Focus"):
    for i, comment in enumerate(comments["Focus | Comments"].tolist()):
        with st.expander(f"Ver comentario de {comments['Name'].iloc[i]}"):
            st.info(comment)

with st.expander("Ver ideas de mejora de Focus"):
    for i, comment in enumerate(improvement_ideas["Focus | Improvement ideas"].tolist()):
        with st.expander(f"Ver idea de {improvement_ideas['Name'].iloc[i]}"):
            st.info(comment)

with st.expander("Ver top 3 1:1's de Focus"):
    for i, comment in enumerate(top3["Focus | Top 3 1:1's"].tolist()):
        with st.expander(f"Ver top 3 1:1's de {top3['Name'].iloc[i]}"):
            st.info(comment)

deceleration_count = df["Focus | Decelerator"].dropna().value_counts()
deceleration_mapped = deceleration_count.rename(index=deceleration_map)

fig = go.Figure(data=[go.Pie(
    labels=deceleration_mapped.index,
    values=deceleration_mapped.values,
    marker=dict(colors=decelera_colors)
)])

fig.update_layout(title_text="Deceleration thermometer")

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
#-----------------------------Grow---------------------------------
st.markdown("<h1 style='text-align: center;'>Grow</h1>", unsafe_allow_html=True)

num_rows = (len(fields["Grow"]) + num_columns -1) // num_columns

for i in range(num_rows):
    cols = st.columns(num_columns)

    row_fields = fields["Grow"][i * num_columns : (i + 1) * num_columns]

    for j, field in enumerate(row_fields):

        with cols[j]:
            mean = df[field].dropna().astype(float).mean()

            st.markdown(
                f"""
                <div style="
                    border: 2px solid #909090;
                    border-radius: 15px; /* Bordes redondeados */
                    padding: 20px;
                    text-align: center;
                    background-color: #f9f9f9;
                    box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
                    height: 150px; /* Altura fija para alinear tarjetas */
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                ">
                    <h4 style="margin-bottom: 10px;">{labels["Grow"][fields["Grow"].index(field)]}</h4>
                    <p style="font-size: 28px; font-weight: bold; margin: 0;">{mean:.2f}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            st.write("")

comments = df[["Name", "Grow | Comments"]].dropna()
improvement_ideas = df[["Name", "Grow | Improvement Ideas"]].dropna()
with st.expander("Ver comentarios de Grow"):
    for i, comment in enumerate(comments["Grow | Comments"].tolist()):
        with st.expander(f"Ver comentario de {comments['Name'].iloc[i]}"):
            st.info(comment)

with st.expander("Ver ideas de mejora de Grow"):
    for i, comment in enumerate(improvement_ideas["Grow | Improvement Ideas"].tolist()):
        with st.expander(f"Ver idea de {improvement_ideas['Name'].iloc[i]}"):
            st.info(comment)
        
deceleration_count = df["Grow | Acceleration"].dropna().value_counts()
deceleration_mapped = deceleration_count.rename(index=deceleration_map)

fig = go.Figure(data=[go.Pie(
    labels=deceleration_mapped.index,
    values=deceleration_mapped.values,
    marker=dict(colors=decelera_colors)
)])

fig.update_layout(title_text="Deceleration thermometer")

st.plotly_chart(fig, use_container_width=True)