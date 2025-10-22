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

st.markdown("---")

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

# Apply normalization manually to avoid type issues
fields_to_normalize: list[str] = [
    "Confidence of growth",
    "Connections with EM's",
    "Connections with VC's",
    "Connections with other Startups",
    "Investment ready",
    "Satisfaction"
]

df[fields_to_normalize] = df[fields_to_normalize].apply(lambda x: (x.astype(float) / 10 * 3) + 1)


#===================================Vamos con Founders===================================

#------------------------------Saquemos las medias-------------------------------------
means_founder: list = []
labels_startup = labels["Founders"]
for field in fields["Founders"]:
    mean_founder: float = float(df[field].dropna().astype(float).mean())
    means_founder.append(mean_founder)

#==================================Vamos con EMs==================================

#------------------------------Saquemos las medias-------------------------------------
means_em: list = []
labels_em = labels["EMs"]
for field in fields["EMs"]:
    mean_em: float = float(df[field].dropna().astype(float).mean())
    means_em.append(mean_em)

#=================================Vamos con VCs==================================

#------------------------------Saquemos las medias-------------------------------------
means_vc: list = []
labels_vc = labels["VCs"]
for field in fields["VCs"]:
    mean_vc: float = float(df[field].dropna().astype(float).mean())
    means_vc.append(mean_vc)
#--------------------------------------------------------------------------------------------
st.markdown(body="Here you will find the feedback submitted by founders, experience makers and VC's about the program")

st.markdown(body="<h1 style='text-align: center;'>Founders</h1>", unsafe_allow_html=True)

ordered_pairs_founder = sorted(zip(means_founder, labels["Founders"]), reverse=True)
values_graph_founder = [value for value, label in ordered_pairs_founder]
labels_graph_founder = [label for value, label in ordered_pairs_founder]
barras(values=values_graph_founder, labels=labels_graph_founder, title=f"Founders feedback")

st.markdown(body="---")

st.markdown(body="<h1 style='text-align: center;'>EM's</h1>", unsafe_allow_html=True)

ordered_pairs_em = sorted(zip(means_em, labels["EMs"]), reverse=True)
values_graph_em = [value for value, label in ordered_pairs_em]
labels_graph_em = [label for value, label in ordered_pairs_em]
barras(values=values_graph_em, labels=labels_graph_em, title=f"EM's feedback")

st.markdown(body="---")

st.markdown(body="<h1 style='text-align: center;'>VC's</h1>", unsafe_allow_html=True)

ordered_pairs_vc = sorted(zip(means_vc, labels["VCs"]), reverse=True)
values_graph_vc = [value for value, label in ordered_pairs_vc]
labels_graph_vc = [label for value, label in ordered_pairs_vc]
barras(values=values_graph_vc, labels=labels_graph_vc, title=f"VC's feedback")

st.markdown(body="---")