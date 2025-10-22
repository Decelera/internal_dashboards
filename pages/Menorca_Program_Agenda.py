import streamlit as st
import pandas as pd
from pyairtable import Api
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="Menorca - Program - Agenda",
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
    if st.button("Risk-Reward", key="mx_inv_general", use_container_width=True):
        st.switch_page("pages/Mexico_Investment_General.py")
    
    if st.button("Feedback details", key="mx_inv_startup", use_container_width=True):
        st.switch_page("pages/Mexico_Investment_Per_Startup.py")
    
    # Program section (Title 4)
    st.markdown("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Program**")
    
    # Program pages (Title 5)
    if st.button("Guests feedback", key="mx_prog_general", use_container_width=True):
        st.switch_page("pages/Mexico_Program_General.py")
    
    if st.button("Breathe-Focus-Grow", key="mx_prog_agenda", use_container_width=True):
        st.switch_page("pages/Mexico_Program_Agenda.py")
    
    st.markdown("---")
    
    # Menorca (Title 1)
    st.markdown("#### Menorca")
    
    # 2025 (Title 2)
    st.markdown("&nbsp;&nbsp;&nbsp;&nbsp;**2025**")
    
    # Investment section (Title 4)
    st.markdown("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Investment**")
    
    # Investment pages (Title 5)
    if st.button("Risk-Reward", key="mn_inv_general", use_container_width=True):
        st.switch_page("pages/Menorca_Investment_General.py")
    
    if st.button("Feedback details", key="mn_inv_startup", use_container_width=True):
        st.switch_page("pages/Menorca_Investment_Per_Startup.py")
    
    # Program section (Title 4)
    st.markdown("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Program**")
    
    # Program pages (Title 5)
    if st.button("Guests feedback", key="mn_prog_general", use_container_width=True):
        st.switch_page("pages/Menorca_Program_General.py")
    
    if st.button("Breathe-Focus-Grow", key="mn_prog_agenda", use_container_width=True):
        st.switch_page("pages/Menorca_Program_Agenda.py")

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

df = df.map(fix_cell)
df = df[df["Event"].apply(lambda x: "Menorca 2025" in x) & df["Guest_type"].apply(lambda x: "Startup" in x)]
#=========================CONFIG===============================

fields = {
    "Breathe": [
        "Breathe | Marcos' talk (Day 1)",
        "Breathe | Grace Gu's talk (Day1)",
        "Breathe | Alex Rojas' talk (Day 1)",
        "Breathe | Ranny Nachmis' talk (Day 1)",
        "Breathe | Lavanda ritual (Day 1)",
        "Breathe | Human pitch (Day 1)",
        "Breathe | Cocktail at Binibeca (Day 1)",
        "Breathe | Mindfulness (Day 2)",
        "Breathe | Yoga (Day 2)",
        "Breathe | Andrea Klimowitz's talk (Day 2)",
        "Breathe | Sean Cook's talk (Day 2)",
        "Breathe | David Baratech's talk (Day 2)",
        "Breathe | Beth Susanne's talk (Day 2)",
        "Breathe | Pitching dynamic (Day 2)",
        "Breathe | Journaling (Day 2)"
        ],
    "Focus": [
        "Focus | Mindfulness (Day 3)",
        "Focus | Body movement (Day 3)",
        "Focus | Shari Swan's talk (Day 3)",
        "Focus | Jorge Gonzalez-Iglesias' talk (Day 3)",
        "Focus | Ivan Peña's talk (Day 3)",
        "Focus | 1:1's matching (Day 3)",
        "Focus | Paul Ford's talk (Day 3)",
        "Focus | Fernando Cabello's talk (Day 3)",
        "Focus | Elise Mitchel's talk (Day 3)",
        "Focus | Journaling (Day 3)",
        "Focus | The founder arena (1)",
        "Focus | Minfulness (Day 4)",
        "Focus | Breathwork (Day 4)",
        "Focus | Gennaro Bifulco's talk (Day 4)",
        "Focus | Rui Fernandes' talk (Day 4)",
        "Focus | 1:1's matching (Day 4)",
        "Focus | Castle contest (Day 4)",
        "Focus | Mindfulness (Day 5)",
        "Focus | Power yoga (Day 5)",
        "Focus | Oscar Macia's talk (Day 5)",
        "Focus | Jair Halevi's talk (Day 5)",
        "Focus | Torsten Kolind's talk (Day 5)",
        "Focus | Philippe Gelis' talk (Day 5)",
        "Focus | 1:1's matching (Day 5)",
        "Focus | Startup mirror (Day 5)",
        "Focus | Juan de Antonio's talk (Day 5)",
        "Focus | 10th anniversary (Day 5)",
        "Focus | Workstations (Day 6)",
        "Focus | Pedro Claveria's talk (Day 6)",
        "Focus | Juan Pablo Tejela & Laura Montells' talk (Day 6)",
        "Focus | Oscar Macia´s talk (Day 6)",
        "Focus | Founder arena (2)",
        "Focus | Mindfulness (Day 7)",
        "Focus | Soft yoga (Day 7)",
        "Focus | Juanjo, Arnau & Meri's talk (Day 7)",
        "Focus | Bastian's talk (Day 8)",
        "Focus | 1:1's matching (Day 7)",
        "Focus | Shadi Yazdan's talk (Day 7)",
        "Focus | Paellas contest"
        ],
    "Grow": [
        "Grow | Mindfulness (Day 8)",
        "Grow | Milu (Day 8)",
        "Grow | Pitching (Day 8)",
        "Grow | Open arena (Day 8)",
        "Grow | Mindfulness (Day 9)",
        "Grow | Tom Dyer (Day 9)",
        "Grow | 1:1's (Day 9)",
        "Grow | Warp up (Day 9)",
        "Grow | Farewell party (Day 9)"
        ]
}

labels = {
    "Breathe": [
        field.replace("Breathe | ", "") for field in fields["Breathe"]
    ],
    "Focus": [
        field.replace("Focus | ", "") for field in fields["Focus"]
    ],
    "Grow": [
        field.replace("Grow | ", "") for field in fields["Grow"]
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
with st.expander("Ver comentarios de Breathe"):
    for i, comment in enumerate(comments["Breathe | Comments"].tolist()):
        with st.expander(f"Ver comentario de {comments['Name'].iloc[i]}"):
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

with st.expander("Ver comentarios de Focus"):
    for i, comment in enumerate(comments["Focus | Comments"].tolist()):
        with st.expander(f"Ver comentario de {comments['Name'].iloc[i]}"):
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
with st.expander("Ver comentarios de Grow"):
    for i, comment in enumerate(comments["Grow | Comments"].tolist()):
        with st.expander(f"Ver comentario de {comments['Name'].iloc[i]}"):
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