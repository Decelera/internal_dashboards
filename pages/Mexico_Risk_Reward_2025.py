from plotly.graph_objs._figure import Figure
import numpy as np
from pyairtable import Api
import pandas as pd
import streamlit as st
import plotly.graph_objects as go


#=============================================PROGRAM CONFIGURATION===============================================
#=================================================================================================================

PROGRAM_YEAR = "2025"
PROGRAM_NAME = "Mexico 2025" #Hay que poner el programa en el formato "Localizacion Año"

#=====================================PAGE CONFIGURATION=======================================================
#=============================================================================================================


# Page configuration
st.set_page_config(
    page_title="Mexico - Investment - General",
    page_icon="https://images.squarespace-cdn.com/content/v1/67811e8fe702fd5553c65249/c5500619-9712-4b9b-83ee-a697212735ae/Disen%CC%83o+sin+ti%CC%81tulo+%2840%29.png",
    layout="wide"
)

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
    <h1 class="title-text">Program Feedback<br>México 2025</h1>
</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<style>
h5 {
text-align: center;
}
</style>

<h5>Risk - Reward Matrix</h5>
""", unsafe_allow_html=True)


#=====================================SIDEBAR CONFIGURATION======================================================
#================================================================================================================


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


#========================================================FUNCTIONS CONFIGURATION=================================================
#===============================================================================================================================

def grouped_means(df):

    # Calculate the mean of risk and reward scores
    risk_mean = df[risk_reward_fields["risk_scores"]].stack().mean()
    reward_mean = df[risk_reward_fields["reward_scores"]].stack().mean()

    return pd.Series({
        "risk_mean": risk_mean,
        "reward_mean": reward_mean
    })


#=======================================================DATOS DE AIRTABLE======================================================
#===============================================================================================================================

try: 
    api_key = st.secrets["airtable_mexico_investment"]["api_key"]
    base_id = st.secrets["airtable_mexico_investment"]["base_id"]

    table_id_team = st.secrets["airtable_mexico_investment"]["table_id_team"]
    table_id_em = st.secrets["airtable_mexico_investment"]["table_id_em"]

    api = Api(api_key)
    table_em = api.table(base_id, table_id_em)
    table_team = api.table(base_id, table_id_team)


    records_team = table_team.all(view=PROGRAM_NAME)
    records_em = table_em.all(view=PROGRAM_NAME)

    data_team = [record['fields'] for record in records_team]
    data_em = [record['fields'] for record in records_em]

    df_team = pd.DataFrame(data_team)
    df_em = pd.DataFrame(data_em)
except Exception as {e}:
    st.warning(f"Error al cargar los datos de Airtable (Error: {e})")
    df_team = pd.DataFrame()
    df_em = pd.DataFrame()

def fix_cell(val):
    if isinstance(val, dict) and "specialValue" in val:
        return float("nan")
    return val

df_team = df_team.map(fix_cell)
df_em = df_em.map(fix_cell)

#----------------------------------Voy a quitar a Sean--------------

if "EM_Name" in df_em.columns.tolist() and not df_em.empty:
    condition: bool = (df_em["EM_Name"].str.startswith("Sean"))
    df_em = df_em[~condition]
#-------------------------------------------------------------------


#=====================================FIELDS CONFIGURATION=====================================================
#=============================================================================================================


startup_founders = {
    "ROOK": ["Marco Benitez", "Jonas Ducker", "Daniel Martínez"],
    "Figuro": ["Juan Camilo Gonzalez"],
    "Admina": ["David Gomez", "Andres Gomez"],
    "Ecosis": ["Enrique Arredondo", "Roberto Riveroll"],
    "CALMIO": ["Andrés Ospina", "Camilo Ospina"],
    "Pitz": ["Natalia Salcedo"],
    "BondUp": ["Michelle Schintzer"],
    "Jelt": ["Sergio Ramirez"],
    "Moabits SL": ["Alejandro Ortiz", "David Santibanez", "Juan Martin Pawluszek"],
    "Ximple": ["Daniel Sujo", "Joao Ramos"],
    "Kuri": ["Ludwig Pucha Cofrep"],
    "CROMODATA": ["Juan Pablo  Merea Otermin", "Keila Barral Masri", "Matias  Karlsson"],
    "Ternadia": ["Angel Sanchez", "Raul Merino"],
    "Tu Cambio": ["Luis Saavedra", "Carla Leal"],
    "Airbag": ["Adrian Trucios"],
    "Handit.ai": ["Jose Manuel Ramirez", "Cristhian Camilo Gomez"],
    "Verticcal": ["Santiago Gallo Restrepo", "Pablo Sanchez Villamarin"],
    "Neat": ["Nicolas Chacon", "Javier Benavides"],
    "CIFRATO": ["Yerson Cacua", "Juan Pisco"],
    "Konvex": ["Andres Cristobal Sosa Tellez"]
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
        "Workstations | Openness (Individual)",
        "Paellas contest | Openness (Individual)",
        "Workstations | Purpose (Individual)",
        "1:1's | Purpose (Individual)",
        "Dilema 1", #Confidence
        "Dilema 2" #Ambition
    ]
}


#=======================================================CALCULO DE METRICAS Y GRAFICA=========================================================
#=============================================================================================================================================


# Vamos a darle la vuelta a risk 
if "Startup" in df_em.columns.tolist() and all(elem in df_em.columns.tolist() for elem in risk_reward_fields["risk_scores"]) \
    and all(elem in df_em.columns.tolist() for elem in risk_reward_fields["reward_scores"]) and not df_em.empty:

    df_em = df_em[df_em["Startup"].isin(startup_founders.keys())]
    df_em[risk_reward_fields["risk_scores"]] = 5 - df_em[risk_reward_fields["risk_scores"]]
    df_em[risk_reward_fields["risk_scores"]] = df_em[risk_reward_fields["risk_scores"]].replace(0, np.nan)
    df_em[risk_reward_fields["risk_scores"]] = df_em[risk_reward_fields["risk_scores"]].replace(0, np.nan)

    df_em_means = df_em.groupby("Startup").apply(grouped_means).reset_index() #DEFINIMOS AQUI df_em_means que es donde calcularemos las medias
else:
    df_em_means = pd.DataFrame()

if risk_reward_fields["reward_scores"] in df_em.columns.tolist():
    df_em[risk_reward_fields["reward_scores"]] = df_em[risk_reward_fields["reward_scores"]].replace(0, np.nan)


#vamosa calcular un par de medias
if all(elem in df_em_means.columns.tolist() for elem in ["Startup", "risk_mean", "reward_mean"]):

    df_em_means["Distance"] = np.sqrt((df_em_means["risk_mean"]) ** 2 + (4 - df_em_means["reward_mean"]) ** 2)
    num_feedback = df_em_means.groupby(by="Startup").size()
    df_em_means["num_feedback"] = df_em_means["Startup"].map(num_feedback)

    fig: Figure = go.Figure()

    fig.add_trace(go.Scatter(
        x=df_em_means["risk_mean"],
        y=df_em_means["reward_mean"],
        customdata=df_em_means["num_feedback"],
        hovertemplate="Feedback enviado: %{customdata}<br>Risk: %{x:.2f}<br>Reward: %{y:.2f}<extra></extra>",
        mode='markers+text',
        text=df_em_means["Startup"],
        textposition="top center",
        marker=dict(
            size=10,
            color=df_em_means["risk_mean"],
            colorscale='RdYlGn_r',
            showscale=False,
            colorbar=dict(
                title="Distance to (risk=0, reward=4)"
            )
        )
    ))

    fig.update_layout(
        xaxis_title='Risk mean',
        yaxis_title='Reward mean',
        font=dict(
            family="Arial, sans-serif",
            size=10,
            color="black"
        ),
        xaxis=dict(
            showline=True,
            linewidth=2,
            linecolor='black',
            gridcolor='lightgray',
            range=[df_em_means["risk_mean"].min() - 0.1, df_em_means["risk_mean"].max() + 0.1]
        ),
        yaxis=dict(
            showline=True,
            linewidth=2,
            linecolor='black',
            gridcolor='lightgray',
            range=[df_em_means["reward_mean"].min() - 0.2, df_em_means["reward_mean"].max() + 0.2]
        )
    )

    st.plotly_chart(fig)

    st.markdown("""
    <h4>Top Companies According to Risk-Reward Matrix</h4>
    """, unsafe_allow_html=True)
    df_em_ordered = df_em_means.sort_values(by="Distance", ascending=True)

    for startup in df_em_ordered["Startup"].tolist():

        #primero calculo las medias de individual y de team para ponerlas
        df_startup = df_team[df_team["Startup"] == startup]
        df_individual = df_team[df_team["Founder_str"].str.replace(" ", "").str.lower().isin([s.replace(" ", "").lower() for s in startup_founders[startup]])]
        
        mean_startup_individual = df_individual[fields["individual"]].astype(float).mean().mean()
        mean_startup_team = df_startup[fields["team"]].astype(float).mean().mean()
        mean_all_individual = df_team[fields["individual"]].astype(float).mean().mean()
        mean_all_team = df_team[fields["team"]].astype(float).mean().mean()

        row = df_startup.iloc[0]
        logo_data = row.get("original logo")
        if isinstance(logo_data, list) and len(logo_data) > 0 and 'url' in logo_data[0]:
            logo_url = logo_data[0]['url']
        else:
            logo_url = ""

        with st.container(border=True):

            st.markdown(f"""
                <div style="display: flex; align-items: left; margin-left: 0;">
                    <img src={logo_url} width="50">
                    <h4 style="margin-left: 10px; font-weight: bold; color: #333;"><a href="https://decelera-dashboards.streamlit.app/Mexico_Feedback_Details_{st.session_state.selected_year}?startup={startup}">{startup}</a></h4>
                </div>
                """,
                unsafe_allow_html=True)
            cols = st.columns(3)
            with cols[0]:
                st.metric(label="Distance to (risk=0, reward=4)", value=round(df_em_ordered[df_em_ordered["Startup"] == startup]["Distance"].values[0], 2))
            with cols[1]:
                st.metric(label="Individual Mean", value=round(mean_startup_individual, 2), delta=round(mean_startup_individual - mean_all_individual, 2))
            with cols[2]:
                st.metric(label="Team Mean", value=round(mean_startup_team, 2), delta=round(mean_startup_team - mean_all_team, 2))