import streamlit as st
import os

# Initialize session state for selected year if not exists
if 'selected_year' not in st.session_state:
    st.session_state.selected_year = "2025"

# Page configuration
st.set_page_config(
    page_title="Decelera Dashboards",
    page_icon="https://images.squarespace-cdn.com/content/v1/67811e8fe702fd5553c65249/c5500619-9712-4b9b-83ee-a697212735ae/Disen%CC%83o+sin+ti%CC%81tulo+%2840%29.png",
    layout="centered"
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

# Custom CSS with Decelera colors
st.markdown("""
    <style>
        /* Main color: #62CDEB (RGB: 98, 205, 235) */
        /* Secondary color: #ACAFB9 (RGB: 172, 175, 185) */
        
        .main-container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .header-container {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 2rem;
            padding: 0.5rem 0 1rem 0;
            margin-bottom: 1rem;
            margin-top: -1rem;
        }
        
        .logo-container {
            display: flex;
            align-items: center;
        }
        
        .page-title {
            font-size: 2.8rem;
            font-weight: 700;
            color: #1f1f1f;
            margin: 0;
        }
        
        .page-subtitle {
            text-align: center;
            font-size: 1.3rem;
            color: #ACAFB9;
            font-weight: 400;
            margin-bottom: 3rem;
        }
        
        .location-header {
            background: white;
            font-size: 1.8rem;
            font-weight: 700;
            color: black;
            padding: 1.5rem;
            margin-bottom: 0;
            border-radius: 10px 10px 0 0;
            border: none;
            border-bottom: none;
            display: flex;
            align-items: center;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
        }
        
        .year-badge {
            display: inline-block;
            background-color: #1FD0EF;
            color: white;
            padding: 0.3rem 1rem;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: 600;
            margin-left: 1rem;
        }
        
        /* Style container with grey box content */
        .grey-box-start + .element-container,
        .grey-box-start + .element-container + .element-container,
        .grey-box-start ~ [data-testid="stHorizontalBlock"],
        .grey-box-start ~ [data-testid="stVerticalBlock"] {
            background-color: #f8f9fa !important;
        }
        
        /* Ensure the grey box styling */
        .grey-box-start {
            height: 0;
            margin: 0;
        }
        
        .grey-box-start ~ * {
            background-color: #f8f9fa;
        }
        
        /* Style the container holding the columns */
        .element-container:has(.grey-box-start) + .element-container [data-testid="stHorizontalBlock"] {
            padding: 1.5rem !important;
            background-color: #f8f9fa !important;
            border: 1px solid #e8e9eb !important;
            border-top: none !important;
            border-radius: 0 0 10px 10px !important;
            margin-top: 0 !important;
        }
        
        /* Alternative selector for wider browser support */
        .grey-box-start ~ .element-container [data-testid="stHorizontalBlock"] {
            padding: 1.5rem !important;
            background-color: #f8f9fa !important;
            border: 1px solid #e8e9eb !important;
            border-top: none !important;
            border-radius: 0 0 10px 10px !important;
            margin-top: 0 !important;
        }
        
        .grey-box-end {
            height: 0;
            margin: 0;
        }
        
        .section-title {
            font-size: 1.1rem;
            font-weight: 600;
            color: #1f1f1f;
            margin-bottom: 0.8rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid #ACAFB9;
        }
        
        /* Button styling inside grey boxes */
        .stButton button {
            background-color: white !important;
            border: 1px solid #e8e9eb !important;
            color: #495057 !important;
            padding: 0.6rem 1rem !important;
            text-align: center !important;
            font-size: 0.95rem !important;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05) !important;
            width: 100% !important;
            transition: all 0.3s ease !important;
            border-radius: 6px !important;
            margin-bottom: 0.5rem !important;
        }
        
        .stButton button:hover {
            background-color: #1FD0EF !important;
            color: white !important;
            border-color: #1FD0EF !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 8px rgba(98, 205, 235, 0.3) !important;
        }
        
        /* Add margin between location blocks */
        [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlock"] {
            margin-bottom: 2rem;
        }
        
        .info-section {
            background: linear-gradient(135deg, #62CDEB 0%, #5bb8d6 100%);
            color: white;
            border-radius: 10px;
            padding: 2rem;
            margin: 2rem 0;
        }
        
        .info-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 1.5rem;
            margin-top: 1.5rem;
        }
        
        .info-card {
            background-color: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(10px);
            border-radius: 8px;
            padding: 1.2rem;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .info-card h4 {
            margin: 0 0 0.5rem 0;
            font-size: 1.1rem;
            font-weight: 600;
        }
        
        .info-card p {
            margin: 0;
            font-size: 0.9rem;
            line-height: 1.6;
            opacity: 0.95;
        }
        
        .footer {
            text-align: center;
            padding: 2rem 0;
            color: #ACAFB9;
            font-size: 0.9rem;
            border-top: 1px solid #e8e9eb;
            margin-top: 3rem;
        }
    </style>
""", unsafe_allow_html=True)

#CSS para el container
st.markdown(body="""
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

#========LOGO Y EL TÍTULO============
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
    <h1 class="title-text">Decelera<br>Dashboards</h1>
</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
    <p>Here you will find the different dashboards available, for INVESTMENT and PROGRAM.</p>
    <ol>
        <li>Investment</li>
            <ul>
                <li style='padding-left: 40px; list-style-position: inside;'>Risk-Reward: Risk-Reward analysis for each startup.</li>
                <li style='padding-left: 40px; list-style-position: inside;'>Feedback details: Human and Business Due Diligence carried out throughout the program.<br></li>
            </ul>
        <li>Program</li>
            <ul>
                <li style='padding-left: 40px; list-style-position: inside;'>Guests feedback: Feedback received from guests about the program.</li>
                <li style='padding-left: 40px; list-style-position: inside;'>Breathe-Focus-Grow: Feedback received from Founders about the different phases of the program.<br></li>
            </ul>
    </ol>
    """,
unsafe_allow_html=True)

# Year selection buttons
st.markdown("### Select Year", unsafe_allow_html=True)

# Add custom CSS to enhance the primary button color
st.markdown("""
<style>
    /* Style for all year buttons */
    .stButton > button[data-testid="stButton"] {
        transition: all 0.3s ease;
    }
    .stButton > button[data-testid="stButton"]:hover {
        transform: translateY(-2px);
    }
    /* Enhance the primary button color for better visibility */
    .stButton > button[kind="primary"] {
        background-color: #1FD0EF !important;
        border-color: #1FD0EF !important;
        color: white !important;
    }
    .stButton > button[kind="primary"]:hover {
        background-color: #17a0c9 !important;
        border-color: #17a0c9 !important;
    }
</style>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    btn_label = "2025"
    btn_type = "primary" if st.session_state.selected_year == "2025" else "secondary"
    if st.button(btn_label, key="year_2025", use_container_width=True, type=btn_type):
        st.session_state.selected_year = "2025"
        st.rerun()
with col2:
    btn_label = "2026"
    btn_type = "primary" if st.session_state.selected_year == "2026" else "secondary"
    if st.button(btn_label, key="year_2026", use_container_width=True, type=btn_type):
        st.session_state.selected_year = "2026"
        st.rerun()

st.markdown("---")

# Mexico Location Block
with st.container(border=True):
    st.markdown(body=f"""
    <div class="location-header">
        🌎 Mexico
        <span class="year-badge">{st.session_state.selected_year}</span>
    </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="grey-box-start"></div>', unsafe_allow_html=True)
        col_mx_inv, col_mx_prog = st.columns(2)
        
        with col_mx_inv:
            st.markdown('<div class="section-title">Investment</div>', unsafe_allow_html=True)
            if st.button("Risk-Reward", key="mx_inv_gen_link", use_container_width=True):
                st.switch_page(f"pages/Mexico_Risk_Reward_{st.session_state.selected_year}.py")
            if st.button("Feedback details", key="mx_inv_startup_link", use_container_width=True):
                st.switch_page(f"pages/Mexico_Feedback_Details_{st.session_state.selected_year}.py")
        
        with col_mx_prog:
            st.markdown('<div class="section-title">Program</div>', unsafe_allow_html=True)
            if st.button("Guests feedback", key="mx_prog_gen_link", use_container_width=True):
                st.switch_page(f"pages/Mexico_Guests_Feedback_{st.session_state.selected_year}.py")
            if st.button("Breathe-Focus-Grow", key="mx_prog_agenda_link", use_container_width=True):
                st.switch_page(f"pages/Mexico_Breathe-Focus-Grow_{st.session_state.selected_year}.py")
        
        st.markdown(body='<div class="grey-box-end"></div>', unsafe_allow_html=True)

# Menorca Location Block
with st.container(border=True):
    st.markdown(body=f"""
    <div class="location-header">
        🏝️ Menorca
        <span class="year-badge">{st.session_state.selected_year}</span>
    </div>
    """, unsafe_allow_html=True)
    
    with st.container(border=True):
        st.markdown('<div class="grey-box-start"></div>', unsafe_allow_html=True)
        col_mn_inv, col_mn_prog = st.columns(2)
        
        with col_mn_inv:
            st.markdown('<div class="section-title">Investment</div>', unsafe_allow_html=True)
            if st.button("Risk-Reward", key="mn_inv_gen_link", use_container_width=True):
                st.switch_page(f"pages/Menorca_Risk_Reward_{st.session_state.selected_year}.py")
            if st.button("Feedback details", key="mn_inv_startup_link", use_container_width=True):
                st.switch_page(f"pages/Menorca_Feedback_Details_{st.session_state.selected_year}.py")
        
        with col_mn_prog:
            st.markdown('<div class="section-title">Program</div>', unsafe_allow_html=True)
            if st.button("Guests feedback", key="mn_prog_gen_link", use_container_width=True):
                st.switch_page(f"pages/Menorca_Guests_Feedback_{st.session_state.selected_year}.py")
            if st.button("Breathe-Focus-Grow", key="mn_prog_agenda_link", use_container_width=True):
                st.switch_page(f"pages/Menorca_Breathe-Focus-Grow_{st.session_state.selected_year}.py")
        
        st.markdown('<div class="grey-box-end"></div>', unsafe_allow_html=True)

# Footer
st.markdown(f"""
<div class="footer">
    <strong>Decelera</strong> | Multi-Location Analytics Platform | {st.session_state.selected_year}
</div>
""", unsafe_allow_html=True)

