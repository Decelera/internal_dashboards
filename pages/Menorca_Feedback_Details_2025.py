import numpy as np
from pyairtable import Api
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import statistics
import math

# Page configuration
st.set_page_config(
    page_title="Mexico - Investment - Per Startup",
    page_icon="https://images.squarespace-cdn.com/content/v1/67811e8fe702fd5553c65249/c5500619-9712-4b9b-83ee-a697212735ae/Disen%CC%83o+sin+ti%CC%81tulo+%2840%29.png",
    layout="wide"
)

if "selected_year" not in st.session_state:
    st.session_state.selected_year = "2025"

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
        
api_key = st.secrets["airtable_mexico_investment"]["api_key"]
base_id = st.secrets["airtable_mexico_investment"]["base_id"]

table_id_team = st.secrets["airtable_mexico_investment"]["table_id_team"]
table_id_em = st.secrets["airtable_mexico_investment"]["table_id_em"]
table_id_olbi = st.secrets["airtable_mexico_investment"]["table_id_olbi"]

api = Api(api_key)
table_em = api.table(base_id, table_id_em)
table_team = api.table(base_id, table_id_team)
table_olbi = api.table(base_id, table_id_olbi)

records_team = table_team.all(view="Menorca 2025")
records_em = table_em.all(view="Menorca 2025")
records_olbi = table_olbi.all(view="Menorca 2025")

data_team = [record['fields'] for record in records_team]
data_em = [record['fields'] for record in records_em]
data_olbi = [record['fields'] for record in records_olbi]

df_team = pd.DataFrame(data_team)
df_em = pd.DataFrame(data_em)
df_olbi = pd.DataFrame(data_olbi)

def fix_cell(val):
    if isinstance(val, dict) and "specialValue" in val:
        return float("nan")
    return val

df_team = df_team.map(fix_cell)
df_em = df_em.map(fix_cell)
df_olbi = df_olbi.map(fix_cell)

#Vamos con ellooooo

#==================CONFIG==============================
startup_founders = {
    "Heuristik": ["Antxon Caballero", "Thomas Carson"],
    "Metly": ["Anna Torrents", "Graeme Harris", "Lydia Taranilla"],
    "Skor": ["Aditya Malhotra", "Carlos Moreno Martín"],
    "Robopedics": ["Dionís Guzmán", "Iván Martínez", "Marc Serra"],
    "Quix": ["Ignacio Barrea", "Santiago Gomez"],
    "Calliope": ["Joaquin Diez", "Rafael Casuso"],
    "Nidus Lab": ["Ana Lozano Portillo"],
    "Vivra": ["Carlos Arboleya", "Carlos Saro"],
    "Lowerton": ["Artem Loginov", "Dimitry Zaets", "Gorka Muñecas"],
    "Chemometric Brain": ["Henrik Stamm Kristensen", "Jacob Kristensen Illán"],
    "Stamp": ["Javier Castrillo"],
    "SheerMe": ["Shakil Satar"],
    "Zell": ["Alberto Garagnani", "Moritz Beck"],
    "Anyformat": ["Alejandro Fernández Rodríguez", "Juan Huguet"],
    "Valerdat": ["Eduard Aran Calonja"],
    "Kestrix Ltd.": ["Lucy Lyons"],
    "Gaddex": ["Alejandro Paloma", "Victor Vicente Sánchez"],
    "Sheldonn": ["Francisco Alejandro Jurado Pérez", "Giorgio Fidei"],
    "Vixiees": ["Alex Sanchez", "Nil Rodas"],
    "IKI Health Group sL": ["Patricia Puiggros", "Silvia Fernandez Mulero"],
    "ByteHide": ["Juan Alberto España Garcia"]
}

startups = list(startup_founders.keys())

fields = {
    "team": [
        "Castle Contest | Conflict resolution (Team)", "Castle Contest | Clear vision and alignment (Team)",
        "Castle Contest | Confidence and respect between founders (Team)",
        "Castle Contest | Clear roles",
        "Castle Contest | Complementary hard skills between founders",
        "Castle Contest | Execution and speed (Team)",
        "1:1's | Team ambition (Team)",
        "1:1's | Product and customer focus (Team)"
    ],
    "individual": [
        "Workstations | Integrity and honesty (Individual)",
        "Workstations | Relevant experience and network (Individual)",
        "Paellas contest | Visionary leadership (Individual)",
        "Paellas contest | Active listening (Individual)",
        "Paellas contest | Flexibility (Individual)",
        "Paellas contest | Self awareness and management of emotions (Individual)",
        "Openness",
        "Purpose"
    ]
}

risk_reward_fields = {
    "risk_scores": [
        "RISK | State of development_Score",
        "RISK | Momentum_Score",
        "RISK | Management_Score"
    ],
    "risk_flags": [
        "RISK | State of development_Flag",
        "RISK | Momentum_Flag",
        "RISK | Management_Flag"
    ],
    "risk_exp": [
        "RISK | State of development_exp",
        "RISK | Momentum_exp",
        "RISK | Management_exp",
    ],
    "reward_scores": [
        "Reward | Market_Score",
        "Reward | Team_Score",
        "Reward | Pain_Score",
        "Reward | Scalability_Score"
    ],
    "reward_flags": [
        "Reward | Market_Flag",
        "Reward | Team_Flag",
        "Reward | Pain_Flag",
        "Reward | Scalability_Flag"
    ],
    "reward_exp": [
        "Reward | Market_exp",
        "Reward | Team_exp",
        "Reward | Pain_exp",
        "Reward | Scalability_exp"
    ]
}

expected_fields = [
    "Startup",
    "Talks | Unconventional thinking (Individual)",
    "Workstations | Unconventional thinking (Individual)",
    "Founder arena | Unconventional thinking (Individual)",
    "Workstations | Openness (Individual)",
    "Paellas contest | Openness (Individual)",
    "Workstations | Purpose (Individual)",
    "1:1's | Purpose (Individual)",
    "Workstations | Challenge clearness (Bussiness)",
    "Workstations | Challenge importance (Bussiness)"
    ]

for col in expected_fields:
    if col not in df_team.columns:
        df_team[col] = np.nan

for col in fields['team']:
    if col not in df_team.columns:
        df_team[col] = np.nan
    
for col in fields['individual']:
    if col not in df_team.columns:
        df_team[col] = np.nan

for keys in risk_reward_fields.keys():
    for col in risk_reward_fields[keys]:
        if col not in df_em.columns:
            df_em[col] = np.nan

if "Startup" not in df_em.columns:
    df_em["Startup"] = np.nan

if "EM_Name" not in df_em.columns:
    df_em["EM_Name"] = np.nan

labels = {
    "team": [
        "Conflict resolution",
        "Clear vision and alignment",
        "Confidence and respect",
        "Clear roles",
        "Complementary hard skills",
        "Execution and speed",
        "Team ambition",
        "Product and customer focus"
    ],
    "individual": [
        "Integrity and honesty",
        "Relevant experience and network",
        "Visionary leadership",
        "Active listening",
        "Flexibility",
        "Management of emotions",
        "Openness",
        "Purpose",
        "Confidence",
        "Ambition"
    ],
    "risk": [
        "State of development",
        "Momentum",
        "Management"
    ],
    "reward": [
        "Market",
        "Team",
        "Pain",
        "Scalability"
    ]
}
#==========================================================

st.markdown("""
<style>
    div[data-testid="stVerticalBlock"] div[data-testid="stVerticalBlock"] div.st-emotion-cache-1jicfl2 {
        background-color: #d8dbdb;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border: 2px solid black;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
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
    <h1 class="title-text">Program Feedback<br>Menorca 2025</h1>
</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<h4>Here you will find an overview of the program feedback</h4>
""",
unsafe_allow_html=True)

WIDGET_KEY = "startup_selector_state"

if WIDGET_KEY not in st.session_state:
    param_from_url = st.query_params.get("startup")
    
    if param_from_url and param_from_url in startups:
        st.session_state[WIDGET_KEY] = param_from_url
    else:
        st.session_state[WIDGET_KEY] = startups[0]

def update_state_and_url():
    st.query_params["startup"] = st.session_state[WIDGET_KEY]

#----------------------------A partir de aqui dropdown de startup--------------------------

startup = st.selectbox(
    "Select a startup",
    options=startups,
    key=WIDGET_KEY,
    index=startups.index(st.session_state[WIDGET_KEY]),
    on_change=update_state_and_url
)

df_team_startup = df_team[df_team["Startup"] == startup]
df_em_startup = df_em[df_em["Startup"] == startup]

row = df_team_startup.iloc[0]
logo_data = row.get("original logo")
if isinstance(logo_data, list) and len(logo_data) > 0 and 'url' in logo_data[0]:
    logo_url = logo_data[0]['url']
    st.image(logo_url, width=250)
#--------------------------Parte de business metrics---------------------------------
fields_risk = risk_reward_fields["risk_scores"]
fields_reward = risk_reward_fields["reward_scores"]
fields_workstations = ["Workstations | Challenge clearness (Bussiness)", "Workstations | Challenge importance (Bussiness)"]
means_risk = []
means_risk_total = []
means_reward = []
means_reward_total = []
means_workstations = []
means_workstations_total = []

for field in fields_risk:
    mean_risk = df_em_startup[field].dropna().astype(float).mean()
    means_risk.append(mean_risk)
    mean_risk_total = df_em[field].dropna().astype(float).mean()
    means_risk_total.append(mean_risk_total)

fields_mean_risk = statistics.mean(means_risk)
fields_mean_risk_total = statistics.mean(means_risk_total)

for field in fields_reward:
    mean_reward = df_em_startup[field].dropna().astype(float).mean()
    means_reward.append(mean_reward)
    mean_reward_total = df_em[field].dropna().astype(float).mean()
    means_reward_total.append(mean_reward_total)

fields_mean_reward = statistics.mean(means_reward)
fields_mean_reward_total = statistics.mean(means_reward_total)

for field in fields_workstations:
    mean_workstations = df_team_startup[field].dropna().astype(float).mean()
    means_workstations.append(mean_workstations)
    mean_workstations_total = df_team[field].dropna().astype(float).mean()
    means_workstations_total.append(mean_workstations_total)

fields_mean_workstations = statistics.mean(means_workstations)
fields_mean_workstations_total = statistics.mean(means_workstations_total)

means_risk.append(means_risk[0])
means_risk_total.append(means_risk_total[0])
means_reward.append(means_reward[0])
means_reward_total.append(means_reward_total[0])

labels_risk = labels["risk"]
labels_risk.append(labels_risk[0])
labels_reward = labels["reward"]
labels_reward.append(labels_reward[0])
labels_workstations = ["Challenge clearness", "Challenge importance"]

with st.container(border=True):
    st.markdown("""
    <h5>Business Metrics</h5>
    """,
    unsafe_allow_html=True)

    cols = st.columns(3)
    with cols[0]:
        fig = go.Figure()

        fig.add_trace(go.Scatterpolar(
            name="All",
            r=means_risk_total,
            theta=labels_risk,
            line=dict(color='rgb(255, 185, 80)')
        ))

        fig.add_trace(go.Scatterpolar(
            name="Startup",
            r=means_risk,
            theta=labels_risk,
            fill='toself',
            fillcolor='rgba(47, 208, 239, 0.4)',
            line=dict(color='rgb(47, 208, 239)')
        ))

        fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                    visible=True,
                    range=[0, 4]
                    )),
                height=375,
                width=375,
                title='Risk metrics'
            )

        st.plotly_chart(fig)

        cols_2 = st.columns(spec=3)
        with cols_2[1]:
            st.metric(label="mean", value=round(fields_mean_risk, 2), delta=round(fields_mean_risk - fields_mean_risk_total, 2))

    with cols[1]:
        fig = go.Figure()

        fig.add_trace(go.Scatterpolar(
            name="All",
            r=means_reward_total,
            theta=labels_reward,
            line=dict(color='rgb(255, 185, 80)')
        ))

        fig.add_trace(go.Scatterpolar(
            name="Startup",
            r=means_reward,
            theta=labels_reward,
            fill='toself',
            fillcolor='rgba(47, 208, 239, 0.4)',
            line=dict(color='rgb(47, 208, 239)')
        ))

        fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                    visible=True,
                    range=[0, 4]
                    )),
                height=375,
                width=375,
                title='Reward metrics'
            )

        st.plotly_chart(fig)

        cols_2 = st.columns(3)
        with cols_2[1]:
            st.metric(label="mean", value=round(fields_mean_reward, 2), delta=round(fields_mean_reward - fields_mean_reward_total, 2))

    with cols[2]:
        fig = go.Figure()

        fig.add_trace(trace=go.Bar(
            x=labels_workstations,
            y=means_workstations,
            name='Startup',
            marker=dict(
                color='rgba(47, 208, 239, 0.6)',
                line=dict(
                    color='rgb(47, 208, 239)',
                    width=2
                )
            )
        ))

        fig.add_trace(trace=go.Bar(
            x=labels_workstations,
            y=means_workstations_total,
            name='All',
            marker=dict(
                color='rgba(255, 185, 80, 0.6)',
                line=dict(
                    color='rgb(255, 185, 80)',
                    width=2
                )
            )
        ))

        fig.update_layout(
            title='Workstations',
            width=375,
            height=375
        )
        st.plotly_chart(fig)

        cols_2 = st.columns(3)
        with cols_2[1]:
            st.metric(label="mean", value=round(fields_mean_workstations, 2), delta=round(fields_mean_workstations - fields_mean_workstations_total, 2))
    
    if not df_em_startup["EM_Name"].empty:
        em_list = ["---"] + df_em_startup["EM_Name"].tolist()
    else:
        em_list = ["---"]
    experience_maker = st.selectbox("Experience Maker Feedback", em_list, index=0)
    df_em_startup_em = df_em_startup[df_em_startup["EM_Name"] == experience_maker]
    
    if experience_maker != "---":
        st.markdown(body="----Risk----")
    for i, field in enumerate(fields_risk):
        if not df_em_startup_em[risk_reward_fields["risk_flags"][i]].empty:
            flag = df_em_startup_em[risk_reward_fields["risk_flags"][i]].item()
        else:
            flag = np.nan

        if flag == "🟢 Green flag":
            color = "green"
        elif flag == "🔴 Red flag":
            color = "red"
        else:
            color = "orange"
        
        if not df_em_startup_em[risk_reward_fields["risk_exp"][i]].empty:
            explanation = df_em_startup_em[risk_reward_fields["risk_exp"][i]].item()
        else:
            explanation = np.nan
        
        if experience_maker == "---":
            continue
        else:
            st.markdown(f"""
            <p style="color: {color};">{labels_risk[i]}<span style="color: black;">{[df_em_startup_em[field].item() if not df_em_startup_em[field].empty else ""]}</span>: 
            <span style="color: black;">{explanation}</span></p>
            """, unsafe_allow_html=True)

    if experience_maker != "---":
        st.markdown(body="----Reward----")
    for i, field in enumerate(fields_reward):
        if not df_em_startup_em[risk_reward_fields["reward_flags"][i]].empty:
            flag = df_em_startup_em[risk_reward_fields["reward_flags"][i]].item()
        else:
            flag = np.nan

        if flag == "🟢 Green flag":
            color = "green"
        elif flag == "🔴 Red flag":
            color = "red"
        else:
            color = "orange"
        
        if not df_em_startup_em[risk_reward_fields["reward_exp"][i]].empty:
            explanation = df_em_startup_em[risk_reward_fields["reward_exp"][i]].item()
        else:
            explanation = np.nan
        
        if experience_maker == "---":
            continue
        else:
            st.markdown(f"""
            <p style="color: {color};">{labels_reward[i]}<span style="color: black;">{[df_em_startup_em[field].item() if not df_em_startup_em[field].empty else ""]}</span>: 
            <span style="color: black;">{explanation}</span></p>
            """, unsafe_allow_html=True)

#=========================Grafico de Arañaaa===========================
fields_team = fields['team']
means_team = []
means_team_total = []

for field in fields_team:
    mean = df_team_startup[field].dropna().astype(float).mean()
    means_team.append(mean)
    mean_total = df_team[field].dropna().astype(float).mean()
    means_team_total.append(mean_total)

fields_mean_team = np.mean(means_team)
fields_mean_team_total = np.mean(means_team_total)

means_team_total.append(means_team_total[0])
means_team.append(means_team[0])
labels_team = labels["team"]
labels_team.append(labels_team[0])
#grafico de araña de team

fig = go.Figure()

fig.add_trace(go.Scatterpolar(
    name='All',
    r=means_team_total,
    theta=labels_team,
    line=dict(color='rgb(255, 185, 80)')
))

fig.add_trace(go.Scatterpolar(
      name='Startup',
      r=means_team,
      theta=labels_team,
      fill='toself',
      fillcolor='rgba(47, 208, 239, 0.4)',
      line=dict(color='rgb(47, 208, 239)')
))

fig.update_layout(
  polar=dict(
    radialaxis=dict(
      visible=True,
      range=[0, 4]
    ))
)

with st.container(border=True):
    st.markdown(f"<h5>Team DD for {startup}</h5>", unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)

    cols = st.columns(3)
    with cols[1]:
        st.metric(label="Team mean", value=round(fields_mean_team, 2), delta=round(fields_mean_team - fields_mean_team_total, 2))

#=========================Parte de Individual=================================

with st.container(border=True):
    founders = startup_founders[startup]
    founders_clean = [founder.replace(" ", "").lower() for founder in startup_founders[startup]]

    df_team["Openness"] = (
        df_team["Workstations | Openness (Individual)"].dropna().astype(float).mean() +
        df_team["Paellas contest | Openness (Individual)"].dropna().astype(float).mean()
    ) / 2

    df_team["Purpose"] = (
        df_team["Workstations | Purpose (Individual)"].dropna().astype(float).mean() +
        df_team["1:1's | Purpose (Individual)"].dropna().astype(float).mean()
    ) / 2

    cols = st.columns(len(founders))
    openness_cols = ["Workstations | Openness (Individual)", "Paellas contest | Openness (Individual)"]
    purpose_cols = ["Workstations | Purpose (Individual)", "1:1's | Purpose (Individual)"]
    for col in openness_cols + purpose_cols:
        df_team[col] = pd.to_numeric(df_team[col], errors='coerce')

    df_team["Openness"] = df_team[openness_cols].mean(axis=1)
    df_team["Purpose"] = df_team[purpose_cols].mean(axis=1)

    for i, founder in enumerate(founders):
        with cols[i]:
            df_team_founder = df_team[df_team["Founder_str"].str.replace(" ", "").str.lower() == founders_clean[i]].copy()
            fields_individual = fields["individual"]
            means_individual = []
            means_individual_total = []

            for field in fields_individual:
                mean_individual = df_team_founder[field].dropna().astype(float).mean()
                means_individual.append(mean_individual)
                mean_individual_total = df_team[field].dropna().astype(float).mean()
                means_individual_total.append(mean_individual_total)
            
            numbers = [numero for numero in means_individual if not math.isnan(numero)]
            if numbers:
                founder_mean = statistics.mean(numbers)
            else:
                founder_mean = 0
            all_individual_mean = statistics.mean([numero for numero in means_individual_total if not math.isnan(numero)])

            labels_individual_closed = labels["individual"].copy()
            means_individual.append(means_individual[0])
            means_individual_total.append(means_individual_total[0])
            labels_individual_closed.append(labels_individual_closed[0])

            fig = go.Figure()

            fig.add_trace(go.Scatterpolar(
                name='All',
                r=means_individual_total,
                theta=labels_individual_closed,
                line=dict(color='rgb(255, 185, 80)')
            ))

            fig.add_trace(go.Scatterpolar(
                name='Founder',
                r=means_individual,
                theta=labels_individual_closed,
                fill='toself',
                fillcolor='rgba(47, 208, 239, 0.4)',
                line=dict(color='rgb(47, 208, 239)')
            ))

            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                    visible=True,
                    range=[0, 4]
                    )),
                height=375,
                width=375,
                title=f'Individual feedback for {founder}',
            )

            st.plotly_chart(fig)
            #vamos a intentar poner las metricas

            number_greens = (
                df_team_founder[df_team_founder['Talks | Unconventional thinking (Individual)'] == 'Bonus star']['Talks | Unconventional thinking (Individual)'].count() +
                df_team_founder[df_team_founder['Workstations | Unconventional thinking (Individual)'] == 'Bonus star']['Workstations | Unconventional thinking (Individual)'].count() +
                df_team_founder[df_team_founder['Founder arena | Unconventional thinking (Individual)'] == 'Bonus star']['Founder arena | Unconventional thinking (Individual)'].count()
            )

            number_reds = (
                df_team_founder[df_team_founder['Talks | Unconventional thinking (Individual)'] == 'Red flag']['Talks | Unconventional thinking (Individual)'].count() +
                df_team_founder[df_team_founder['Workstations | Unconventional thinking (Individual)'] == 'Red flag']['Workstations | Unconventional thinking (Individual)'].count() +
                df_team_founder[df_team_founder['Founder arena | Unconventional thinking (Individual)'] == 'Red flag']['Founder arena | Unconventional thinking (Individual)'].count()
            )

            subcols= st.columns(3)
            with subcols[0]:
                st.metric(label="Individual mean", value=round(founder_mean, 2), delta=round(founder_mean - all_individual_mean, 2))

            with subcols[1]:
                st.metric(label="Bonus Stars", value=number_greens)

            with subcols[2]:
                st.metric(label="Red Flags", value=number_reds)

#=========================Parte de Human DD Forms==================================

cleaned_founders_column = df_olbi["Founder--Select"].str.replace(" ", "").str.lower()
coincidence = cleaned_founders_column.isin(founders_clean)
if coincidence.any():
    with st.container(border=True):
        st.markdown("<h5>Human DD Forms</h5>", unsafe_allow_html=True)

        olbi_total_average = (
            df_olbi["BRS_Total_Score"].mean() +
            df_olbi["GRIT_Total_Score"].mean() +
            df_olbi["OLBI_Total_Score"].mean()
        ) / 3

        for i, founder in enumerate(founders_clean):
            
            df_olbi_founder = df_olbi[df_olbi["Founder--Select"].str.replace(" ", "").str.lower() == founder].copy()
            olbi_average = df_olbi_founder[["BRS_Total_Score", "GRIT_Total_Score", "OLBI_Total_Score"]].mean().mean()

            if not df_olbi_founder.empty:
                st.markdown(f"{founders[i]}")

                st.markdown(f"""
                <style>
                /* Contenedor principal para la fila de métricas */
                .metric-row {{
                    display: flex;
                    justify-content: space-between;
                    gap: 15px; /* Espacio entre las cajas */
                }}

                /* Estilo para la etiqueta (el título de la métrica) */
                .metric-label {{
                    font-size: 16px;
                    color: #555;
                    margin-bottom: 5px;
                }}

                /* Estilo para el valor (el número o texto principal) */
                .metric-value {{
                    font-size: 20px; /* <-- ¡CAMBIA ESTE VALOR PARA AJUSTAR EL TAMAÑO! */
                    font-weight: bold;
                    color: #1E293B;
                }}
                </style>

                <div class="metric-row">
                    <div class="metric-box">
                        <div class="metric-label">BRS</div>
                        <div class="metric-value">{df_olbi_founder["BRS_Calculation"].iloc[0]}</div>
                    </div>
                    <div class="metric-box">
                        <div class="metric-label">GRIT</div>
                        <div class="metric-value">{df_olbi_founder["GRIT_Calculation"].iloc[0]}</div>
                    </div>
                    <div class="metric-box">
                        <div class="metric-label">OLBI Exhaustion</div>
                        <div class="metric-value">{df_olbi_founder["OLBI_Exhaustion_Descriptor"].iloc[0]}</div>
                    </div>
                    <div class="metric-box">
                        <div class="metric-label">OLBI Disengagement</div>
                        <div class="metric-value">{df_olbi_founder["OLBI_Disengagement_Descriptor"].iloc[0]}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                continue