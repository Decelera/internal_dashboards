from typing import Any
import streamlit as st
import streamlit as st
import pandas as pd
from pyairtable import Api
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="Mexico - Program - Agenda",
    page_icon="../.streamlit/static/favicon.png",
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
records = api.table(base_id, table_id).all(view="Guests Feedback")
data = [record["fields"] for record in records]
df = pd.DataFrame(data)

def fix_cell(val):
    if isinstance(val, dict) and "specialValue" in val:
        return float("nan")
    return val

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

def barras(values, labels, title) -> None:
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=labels,
        y=values,
        texttemplate='%{y:.2f}',
        textposition='outside',
        marker=dict(
            color=values,
            colorscale='RdYlGn',
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

def calculate_nps(df, field):
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

# Apply normalization manually to avoid type issues
fields_to_normalize: list[str] = [
    "Confidence of growth",
    "Connections with EM's",
    "Connections with VC's",
    "Connections with other Startups",
    "Investment ready"
]

df[fields_to_normalize] = df[fields_to_normalize].apply(lambda x: (x.astype(float) / 10 * 3) + 1)


#===================================Vamos con Founders===================================

#------------------------------Saquemos las medias-------------------------------------
df_startup = df[df["Guest_type"].apply(lambda x: "Startup" in x)]

nps_startup_startup = calculate_nps(df=df_startup, field="Recommendation to Startups")

means_founder: list = []
labels_startup = labels["Founders"]
for field in fields["Founders"]:
    mean_founder: float = float(df_startup[field].dropna().astype(float).mean())
    means_founder.append(mean_founder)

#==================================Vamos con EMs==================================

#------------------------------Saquemos las medias-------------------------------------
df_em = df[df["Guest_type"].apply(lambda x: "EM" in x)]

nps_em_startup = calculate_nps(df=df_em, field="Recommendation to Startups")
nps_em_em = calculate_nps(df=df_em, field="EM's Fb | Recommendation to EM")

means_em: list = []
labels_em = labels["EMs"]
for field in fields["EMs"]:
    mean_em: float = float(df_em[field].dropna().astype(float).mean())
    means_em.append(mean_em)

#=================================Vamos con VCs==================================

#------------------------------Saquemos las medias-------------------------------------
df_vc = df[df["Guest_type"].apply(lambda x: "VC" in x)]

nps_vc_startup = calculate_nps(df=df_vc, field="Recommendation to Startups")
nps_vc_vc = calculate_nps(df=df_vc, field="VC's | Recommendation to vc")

means_vc: list = []
labels_vc = labels["VCs"]
for field in fields["VCs"]:
    mean_vc: float = float(df_vc[field].dropna().astype(float).mean())
    means_vc.append(mean_vc)
#--------------------------------------------------------------------------------------------
st.markdown(body="Here you will find the feedback submitted by founders, experience makers and VC's about the program")

st.markdown(body="<h1 style='text-align: center;'>Founders</h1>", unsafe_allow_html=True)

st.metric(value=round(nps_startup_startup, 2), label="NPS Startups to Startups")

ordered_pairs_founder = sorted(zip(means_founder, labels["Founders"]), reverse=True)
values_graph_founder = [value for value, label in ordered_pairs_founder]
labels_graph_founder = [label for value, label in ordered_pairs_founder]
barras(values=values_graph_founder, labels=labels_graph_founder, title=f"Founders feedback")

st.markdown(body="---") #==============================================================================

st.markdown(body="<h1 style='text-align: center;'>EM's</h1>", unsafe_allow_html=True)

cols = st.columns(2)
with cols[0]:
    st.metric(value=round(nps_em_em, 2), label="NPS EM's to EM's")
with cols[1]:
    st.metric(value=round(nps_em_startup, 2), label="NPS EM's to Startup")

ordered_pairs_em = sorted(zip(means_em, labels["EMs"]), reverse=True)
values_graph_em = [value for value, label in ordered_pairs_em]
labels_graph_em = [label for value, label in ordered_pairs_em]
barras(values=values_graph_em, labels=labels_graph_em, title=f"EM's feedback")

st.markdown(body="---") #======================================================================================0

st.markdown(body="<h1 style='text-align: center;'>VC's</h1>", unsafe_allow_html=True)

cols = st.columns(2)
with cols[0]:
    st.metric(value=round(nps_vc_vc, 2), label="NPS VC's to VC's")
with cols[1]:
    st.metric(value=round(nps_vc_startup, 2), label="NPS VC's to Startups")

ordered_pairs_vc = sorted(zip(means_vc, labels["VCs"]), reverse=True)
values_graph_vc = [value for value, label in ordered_pairs_vc]
labels_graph_vc = [label for value, label in ordered_pairs_vc]
barras(values=values_graph_vc, labels=labels_graph_vc, title=f"VC's feedback")

st.markdown(body="---")