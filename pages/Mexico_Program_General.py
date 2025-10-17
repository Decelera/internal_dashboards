import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Mexico - Program - General",
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
st.caption("Mexico → 2025 → Investment → Program → General")

# Page header
st.title("Mexico - Program - General")

st.markdown("---")

import streamlit as st
import pandas as pd
from pyairtable import Api

api_key = st.secrets["airtable_mexico_program"]["api_key"]
base_id = st.secrets["airtable_mexico_program"]["base_id"]
table_id = st.secrets["airtable_mexico_program"]["table_id"]

api = Api(api_key)
records = api.table(base_id, table_id).all(view="Guests Feedback")
data = [record["fields"] for record in records]
df = pd.DataFrame(data)

def fix_cell(val):
    if isinstance(val, dict) and "specialValue" in val:
        return float("nan")
    return val

df = df.map(fix_cell)

#=========================CONFIG==============================

fields = {
    "Founders": [
        "Guest logistics",
        "Communication from team",
        "Program website",
        "Satisfaction",
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
        "Overall experience",
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

def calculate_nps(field):
    scores = df[field].dropna().astype(float).tolist()
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

num_columns = 3
df = df[df["Event"].apply(lambda x: "Mexico 2025" in x)]
#=================================FOUNDERS===============================================

st.markdown("<h1 style='text-align: center;'>Founders feedback</h1>", unsafe_allow_html=True)
CATEGORY = "Founders"
RECOMENDATION = "Recommendation to Startups"
df_startups = df[df["Guest_type"].apply(lambda x: "Startup" in x)]
for field in ["Satisfaction", "Connections with EM's", "Connections with VC's", "Connections with other Startups", "Investment ready", "Confidence of growth"]:
    df_startups[field] = df_startups[field].astype(float) / 10 * 3 + 1

num_rows = (len(fields[CATEGORY]) + num_columns -1) // num_columns
nps = calculate_nps(RECOMENDATION)

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
            <h4 style="margin-bottom: 10px;">NPS to other startups</h4>
            <p style="font-size: 28px; font-weight: bold; margin: 0;">{nps:.2f}</p>
        </div>
        """,
        unsafe_allow_html=True)
st.write("")

for i in range(num_rows):
    cols = st.columns(num_columns)

    row_fields = fields[CATEGORY][i * num_columns : (i + 1) * num_columns]

    for j, field in enumerate(row_fields):
        mean = df_startups[field].dropna().astype(float).mean()

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
                    <h4 style="margin-bottom: 10px;">{labels[CATEGORY][fields[CATEGORY].index(field)]}</h4>
                    <p style="font-size: 28px; font-weight: bold; margin: 0;">{mean:.2f}</p>
                </div>
                """,
                unsafe_allow_html=True)
            st.write("")

top3 = df_startups[["Name", "Top 3 outcomes"]].dropna()
most_positive = df_startups[["Name", "Most positive aspect"]].dropna()
improvement = df_startups[["Name", "Improvement ideas"]].dropna()

with st.expander("Ver top 3 outcomes del programa"):
    for i, comment in enumerate(top3["Top 3 outcomes"].tolist()):
        with st.expander(f"Ver comentario de {top3['Name'].iloc[i]}"):
            st.info(comment)

with st.expander("Ver aspectos más positivos del programa"):
    for i, comment in enumerate(most_positive["Most positive aspect"].tolist()):
        with st.expander(f"Ver aspectos más positivos de {most_positive['Name'].iloc[i]}"):
            st.info(comment)

with st.expander("Ver ideas de mejora del programa"):
    for i, comment in enumerate(improvement["Improvement ideas"].tolist()):
        with st.expander(f"Ver ideas de mejora de {improvement['Name'].iloc[i]}"):
            st.info(comment)

st.markdown("---")
#===================================EM's===================================================

st.markdown("<h1 style='text-align: center;'>EM's feedback</h1>", unsafe_allow_html=True)
CATEGORY = "EMs"
RECOMENDATION_1 = "EM's Fb | Recommendation to EM"
RECOMENDATION_2 = "Recommendation to Startups"
df_em = df[df["Guest_type"].apply(lambda x: "EM" in x)]

num_rows = (len(fields[CATEGORY]) + num_columns -1) // num_columns
nps_startups = calculate_nps(RECOMENDATION_1)
nps_em = calculate_nps(RECOMENDATION_2)

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
            <h4 style="margin-bottom: 10px;">NPS to other startups</h4>
            <p style="font-size: 28px; font-weight: bold; margin: 0;">{nps_startups:.2f}</p>
        </div>
        """,
        unsafe_allow_html=True)
st.write("")

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
            <h4 style="margin-bottom: 10px;">NPS to other EM's</h4>
            <p style="font-size: 28px; font-weight: bold; margin: 0;">{nps_em:.2f}</p>
        </div>
        """,
        unsafe_allow_html=True)
st.write("")

for i in range(num_rows):
    cols = st.columns(num_columns)

    row_fields = fields[CATEGORY][i * num_columns : (i + 1) * num_columns]

    for j, field in enumerate(row_fields):
        mean = df_em[field].dropna().astype(float).mean()

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
                    <h4 style="margin-bottom: 10px;">{labels[CATEGORY][fields[CATEGORY].index(field)]}</h4>
                    <p style="font-size: 28px; font-weight: bold; margin: 0;">{mean:.2f}</p>
                </div>
                """,
                unsafe_allow_html=True)
            st.write("")

comments = df_em[["Name", "Comments"]].dropna()
improvement_ideas = df_em[["Name", "Improvement ideas"]].dropna()
top3 = df_em[["Name", "EM's Fb | Top3 1:1's"]].dropna()
with st.expander("Ver comentarios de EM's"):
    for i, comment in enumerate(comments["Comments"].tolist()):
        with st.expander(f"Ver comentario de {comments['Name'].iloc[i]}"):
            st.info(comment)

with st.expander("Ver ideas de mejora de EM's"):
    for i, comment in enumerate(improvement_ideas["Improvement ideas"].tolist()):
        with st.expander(f"Ver idea de {improvement_ideas['Name'].iloc[i]}"):
            st.info(comment)

with st.expander("Ver top 3 1:1's de EM's"):
    for i, comment in enumerate(top3["EM's Fb | Top3 1:1's"].tolist()):
        with st.expander(f"Ver top 3 1:1's de {top3['Name'].iloc[i]}"):
            st.info(comment)

st.markdown("---")

#=======================================VCs==================================================

st.markdown("<h1 style='text-align: center;'>VC's feedback</h1>", unsafe_allow_html=True)
CATEGORY = "VCs"
RECOMENDATION_1 = "VC's | Recommendation to vc"
RECOMENDATION_2 = "Recommendation to Startups"
df_vc = df[df["Guest_type"].apply(lambda x: "VC" in x)]

num_rows = (len(fields[CATEGORY]) + num_columns -1) // num_columns
nps_startups = calculate_nps(RECOMENDATION_1)
nps_vc = calculate_nps(RECOMENDATION_2)

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
            <h4 style="margin-bottom: 10px;">NPS to other startups</h4>
            <p style="font-size: 28px; font-weight: bold; margin: 0;">{nps_startups:.2f}</p>
        </div>
        """,
        unsafe_allow_html=True)
st.write("")

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
            <h4 style="margin-bottom: 10px;">NPS to other VCs</h4>
            <p style="font-size: 28px; font-weight: bold; margin: 0;">{nps_vc:.2f}</p>
        </div>
        """,
        unsafe_allow_html=True)
st.write("")

for i in range(num_rows):
    cols = st.columns(num_columns)

    row_fields = fields[CATEGORY][i * num_columns : (i + 1) * num_columns]

    for j, field in enumerate(row_fields):
        mean = df_vc[field].dropna().astype(float).mean()

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
                    <h4 style="margin-bottom: 10px;">{labels[CATEGORY][fields[CATEGORY].index(field)]}</h4>
                    <p style="font-size: 28px; font-weight: bold; margin: 0;">{mean:.2f}</p>
                </div>
                """,
                unsafe_allow_html=True)
            st.write("")

comments = df_vc[["Name", "Comments"]].dropna()
improvement_ideas = df_vc[["Name", "Improvement ideas"]].dropna()
top_companies = df_vc[["Name", "Investment Interest"]].dropna()
with st.expander("Ver qué influyó en el interés de inversión de VC's"):
    for i, comment in enumerate(comments["Comments"].tolist()):
        with st.expander(f"Ver comentario de {comments['Name'].iloc[i]}"):
            st.info(comment)

with st.expander("Ver ideas de mejora de VC's"):
    for i, comment in enumerate(improvement_ideas["Improvement ideas"].tolist()):
        with st.expander(f"Ver idea de {improvement_ideas['Name'].iloc[i]}"):
            st.info(comment)

with st.expander("Ver top compañías para invertir según VC's"):
    for i, comment in enumerate(top_companies["Investment Interest"].tolist()):
        with st.expander(f"Ver top companies de {top_companies['Name'].iloc[i]}"):
            st.info(comment)

st.markdown("---")