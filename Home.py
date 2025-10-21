import streamlit as st
import os

# Page configuration
st.set_page_config(
    page_title="Decelera Dashboards",
    page_icon=".streamlit/static/favicon.png",
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
    if st.button("Home", key="home_btn", use_container_width=True):
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
            color: #62CDEB;
            padding: 1.5rem;
            margin-bottom: 0;
            border-radius: 10px 10px 0 0;
            border: 1px solid #e8e9eb;
            border-bottom: none;
            display: flex;
            align-items: center;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
        }
        
        .year-badge {
            display: inline-block;
            background-color: #62CDEB;
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
            background-color: #62CDEB !important;
            color: white !important;
            border-color: #62CDEB !important;
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
    <h1 class="title-text">Decelera Program and<br>Investment Dashboards</h1>
</div>
</div>
""", unsafe_allow_html=True)

# Mexico Location Block
with st.container():
    st.markdown("""
    <div class="location-header">
        🌎 Mexico
        <span class="year-badge">2025</span>
    </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="grey-box-start"></div>', unsafe_allow_html=True)
        col_mx_inv, col_mx_prog = st.columns(2)
        
        with col_mx_inv:
            st.markdown('<div class="section-title">Investment</div>', unsafe_allow_html=True)
            if st.button("General", key="mx_inv_gen_link", use_container_width=True):
                st.switch_page("pages/Mexico_Investment_General.py")
            if st.button("Per Startup", key="mx_inv_startup_link", use_container_width=True):
                st.switch_page("pages/Mexico_Investment_Per_Startup.py")
        
        with col_mx_prog:
            st.markdown('<div class="section-title">Program</div>', unsafe_allow_html=True)
            if st.button("General", key="mx_prog_gen_link", use_container_width=True):
                st.switch_page("pages/Mexico_Program_General.py")
            if st.button("Agenda", key="mx_prog_agenda_link", use_container_width=True):
                st.switch_page("pages/Mexico_Program_Agenda.py")
        
        st.markdown('<div class="grey-box-end"></div>', unsafe_allow_html=True)

# Menorca Location Block
with st.container():
    st.markdown("""
    <div class="location-header">
        🏝️ Menorca
        <span class="year-badge">2025</span>
    </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="grey-box-start"></div>', unsafe_allow_html=True)
        col_mn_inv, col_mn_prog = st.columns(2)
        
        with col_mn_inv:
            st.markdown('<div class="section-title">Investment</div>', unsafe_allow_html=True)
            if st.button("General", key="mn_inv_gen_link", use_container_width=True):
                st.switch_page("pages/Menorca_Investment_General.py")
            if st.button("Per Startup", key="mn_inv_startup_link", use_container_width=True):
                st.switch_page("pages/Menorca_Investment_Per_Startup.py")
        
        with col_mn_prog:
            st.markdown('<div class="section-title">Program</div>', unsafe_allow_html=True)
            if st.button("General", key="mn_prog_gen_link", use_container_width=True):
                st.switch_page("pages/Menorca_Program_General.py")
            if st.button("Agenda", key="mn_prog_agenda_link", use_container_width=True):
                st.switch_page("pages/Menorca_Program_Agenda.py")
        
        st.markdown('<div class="grey-box-end"></div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <strong>Decelera</strong> | Multi-Location Analytics Platform | 2025
</div>
""", unsafe_allow_html=True)

