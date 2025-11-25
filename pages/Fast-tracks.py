import streamlit as st
import pandas as pd
from pyairtable import Api
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="Fast-tracks - Dealflow Dashboard",
    page_icon="https://images.squarespace-cdn.com/content/v1/67811e8fe702fd5553c65249/c5500619-9712-4b9b-83ee-a697212735ae/Disen%CC%83o+sin+ti%CC%81tulo+%2840%29.png",
    layout="wide"
)

if "selected_year" not in st.session_state:
    st.session_state.selected_year = "2025"

# Custom CSS with Decelera colors
st.markdown("""
<style>
.outer-container {
    display: flex;
    justify-content: center;
    width: 100%;
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
    font-size: 2.5em;
    font-weight: bold;
}
</style>
<div class="outer-container">
<div class="container">
    <img class="logo-img" src="https://images.squarespace-cdn.com/content/v1/67811e8fe702fd5553c65249/c5500619-9712-4b9b-83ee-a697212735ae/Disen%CC%83o+sin+ti%CC%81tulo+%2840%29.png">
    <h1 class="title-text">Fast-tracks</h1>
</div>
</div>
""", unsafe_allow_html=True)

# Hide default Streamlit navigation elements and add custom styles
st.markdown("""
    <style>
        [data-testid="stSidebarNav"] {
            display: none;
        }
        
        /* Startup card styling */
        div[data-testid="stContainer"] > div {
            background-color: #f8f9fa;
        }
        
        /* Metrics styling */
        div[data-testid="stMetric"] {
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        div[data-testid="stMetricValue"] {
            color: #62CDEB;
            font-size: 2em;
            font-weight: bold;
        }
        
        /* Button styling */
        .stButton button {
            background-color: #62CDEB;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 5px;
            transition: all 0.3s ease;
        }
        
        .stButton button:hover {
            background-color: #5bb8d6;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(98, 205, 235, 0.3);
        }
        
        /* Filter styling */
        div[data-baseweb="select"] {
            border-radius: 5px;
        }
    </style>
""", unsafe_allow_html=True)

# Custom hierarchical navigation
with st.sidebar:
    # Home button at the top
    if st.button("🏠 Home", key="home_btn", use_container_width=True):
        st.switch_page("Home.py")
    
    # Fast-tracks button
    if st.button("⚡ Fast-tracks", key="fast_tracks_btn", use_container_width=True):
        st.switch_page("pages/Fast-tracks.py")
    
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

st.markdown("---")

# =============================================================================
# AIRTABLE DATA CONNECTION
# =============================================================================

@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_dealflow_data():
    """Load dealflow data from Airtable"""
    try:
        # You can configure which Airtable source to use here
        # Options: "airtable_mexico_investment" or create a new "airtable_dealflow" in secrets
        api_key = st.secrets["airtable_mexico_investment"]["api_key"]
        base_id = st.secrets["airtable_mexico_investment"]["base_id"]
        table_id_team = st.secrets["airtable_mexico_investment"]["table_id_team"]
        
        api = Api(api_key)
        table = api.table(base_id, table_id_team)
        
        # Fetch all records - you can specify a view if needed
        records = table.all()  # or use view="Fast-tracks" if you create one
        
        # Extract fields
        data = [record['fields'] for record in records]
        df = pd.DataFrame(data)
        
        return df
    except Exception as e:
        st.error(f"Error loading data from Airtable: {e}")
        return pd.DataFrame()

# Load data
df = load_dealflow_data()

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_founder_full_name(row, startup_name):
    """Combine founder name and surname"""
    # Try to get founder name and surname fields
    # The field names might vary, so we'll try different patterns
    name_field = f"PH1_founder_name_{startup_name}"
    surname_field = f"PH1_founder_surname_{startup_name}"
    
    name = row.get(name_field, "")
    surname = row.get(surname_field, "")
    
    if name or surname:
        return f"{name} {surname}".strip()
    
    # Fallback to generic fields if startup-specific ones don't exist
    name = row.get("PH1_founder_name", "")
    surname = row.get("PH1_founder_surname", "")
    
    return f"{name} {surname}".strip() if (name or surname) else "N/A"

def get_field_value(row, field_patterns, default="N/A"):
    """Try multiple field patterns and return the first non-empty value"""
    for pattern in field_patterns:
        if pattern in row and pd.notna(row[pattern]) and str(row[pattern]).strip():
            return row[pattern]
    return default

# =============================================================================
# DASHBOARD METRICS
# =============================================================================

if not df.empty:
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_startups = len(df)
        st.metric(label="Total Startups", value=total_startups)
    
    with col2:
        # Count unique stages if available
        stage_cols = [col for col in df.columns if 'stage' in col.lower()]
        if stage_cols:
            unique_stages = df[stage_cols[0]].nunique()
            st.metric(label="Stages", value=unique_stages)
        else:
            st.metric(label="Stages", value="-")
    
    with col3:
        # Count unique locations
        location_cols = [col for col in df.columns if 'constitution_location' in col.lower() or 'location' in col.lower()]
        if location_cols:
            unique_locations = df[location_cols[0]].nunique()
            st.metric(label="Locations", value=unique_locations)
        else:
            st.metric(label="Locations", value="-")
    
    with col4:
        # Count unique business models
        bm_cols = [col for col in df.columns if 'business_model' in col.lower()]
        if bm_cols:
            unique_bm = df[bm_cols[0]].nunique()
            st.metric(label="Business Models", value=unique_bm)
        else:
            st.metric(label="Business Models", value="-")
    
    st.markdown("---")
    
    # =============================================================================
    # FILTERS
    # =============================================================================
    
    st.write("### Filters")
    
    filter_col1, filter_col2, filter_col3 = st.columns(3)
    
    with filter_col1:
        # Stage filter
        stage_cols = [col for col in df.columns if 'stage' in col.lower()]
        if stage_cols:
            stages = df[stage_cols[0]].dropna().unique().tolist()
            selected_stages = st.multiselect("Filter by Stage", ["All"] + stages, default="All")
        else:
            selected_stages = ["All"]
    
    with filter_col2:
        # Location filter
        location_cols = [col for col in df.columns if 'constitution_location' in col.lower() or 'location' in col.lower()]
        if location_cols:
            locations = df[location_cols[0]].dropna().unique().tolist()
            selected_locations = st.multiselect("Filter by Location", ["All"] + locations, default="All")
        else:
            selected_locations = ["All"]
    
    with filter_col3:
        # Business Model filter
        bm_cols = [col for col in df.columns if 'business_model' in col.lower()]
        if bm_cols:
            business_models = df[bm_cols[0]].dropna().unique().tolist()
            selected_bm = st.multiselect("Filter by Business Model", ["All"] + business_models, default="All")
        else:
            selected_bm = ["All"]
    
    # Apply filters
    filtered_df = df.copy()
    
    if "All" not in selected_stages and stage_cols:
        filtered_df = filtered_df[filtered_df[stage_cols[0]].isin(selected_stages)]
    
    if "All" not in selected_locations and location_cols:
        filtered_df = filtered_df[filtered_df[location_cols[0]].isin(selected_locations)]
    
    if "All" not in selected_bm and bm_cols:
        filtered_df = filtered_df[filtered_df[bm_cols[0]].isin(selected_bm)]
    
    st.markdown("---")
    
    # =============================================================================
    # STARTUP CARDS
    # =============================================================================
    
    st.write(f"### Dealflow Overview ({len(filtered_df)} startups)")
    
    # Get the startup name field
    startup_name_cols = [col for col in df.columns if 'startup' in col.lower() and 'name' in col.lower()]
    if not startup_name_cols:
        startup_name_cols = [col for col in df.columns if col == 'Name' or col == 'Startup' or col == 'Company']
    
    if filtered_df.empty:
        st.info("No startups match the selected filters.")
    else:
        # Display startups in a grid
        num_cols = 2
        rows = [filtered_df.iloc[i:i+num_cols] for i in range(0, len(filtered_df), num_cols)]
        
        for row_data in rows:
            cols = st.columns(num_cols)
            for idx, (_, startup) in enumerate(row_data.iterrows()):
                with cols[idx]:
                    # Get startup name
                    startup_name = "Unknown Startup"
                    if startup_name_cols:
                        startup_name = get_field_value(startup, startup_name_cols, "Unknown Startup")
                    
                    # Create card
                    with st.container(border=True):
                        st.markdown(f"### 🚀 {startup_name}")
                        
                        # Founder info
                        founder_name = get_founder_full_name(startup, startup_name)
                        st.markdown(f"**👤 Founder:** {founder_name}")
                        
                        # Business Model
                        bm_patterns = [f"PH1_business_model_{startup_name}", "PH1_business_model", "Business Model", "business_model"]
                        business_model = get_field_value(startup, bm_patterns)
                        st.markdown(f"**💼 Business Model:** {business_model}")
                        
                        # Stage
                        stage_patterns = [f"stage_{startup_name}", "stage", "Stage"]
                        stage = get_field_value(startup, stage_patterns)
                        st.markdown(f"**📊 Stage:** {stage}")
                        
                        # Location
                        location_patterns = ["PH1_Constitution_Location", "Constitution_Location", "Location", "location"]
                        location = get_field_value(startup, location_patterns)
                        st.markdown(f"**📍 Location:** {location}")
                        
                        # Optional: Add a button for more details
                        if st.button(f"View Details", key=f"btn_{startup_name}_{idx}"):
                            with st.expander("Full Details", expanded=True):
                                st.json(startup.to_dict())
        
        # =============================================================================
        # ANALYTICS SECTION
        # =============================================================================
        
        st.markdown("---")
        st.write("### Analytics")
        
        analytics_col1, analytics_col2 = st.columns(2)
        
        with analytics_col1:
            # Stage distribution
            if stage_cols:
                st.write("#### Distribution by Stage")
                stage_counts = filtered_df[stage_cols[0]].value_counts()
                
                fig_stage = go.Figure(data=[go.Pie(
                    labels=stage_counts.index,
                    values=stage_counts.values,
                    hole=0.4,
                    marker=dict(colors=['#62CDEB', '#ACAFB9', '#5bb8d6', '#95a3a8'])
                )])
                fig_stage.update_layout(
                    showlegend=True,
                    height=400,
                    margin=dict(l=20, r=20, t=40, b=20)
                )
                st.plotly_chart(fig_stage, use_container_width=True)
        
        with analytics_col2:
            # Location distribution
            if location_cols:
                st.write("#### Distribution by Location")
                location_counts = filtered_df[location_cols[0]].value_counts()
                
                fig_location = go.Figure(data=[go.Bar(
                    x=location_counts.index,
                    y=location_counts.values,
                    marker=dict(color='#62CDEB')
                )])
                fig_location.update_layout(
                    showlegend=False,
                    height=400,
                    xaxis_title="Location",
                    yaxis_title="Count",
                    margin=dict(l=20, r=20, t=40, b=100)
                )
                fig_location.update_xaxes(tickangle=45)
                st.plotly_chart(fig_location, use_container_width=True)

else:
    st.warning("No data available. Please check your Airtable configuration.")
    st.info("""
    **To configure this dashboard:**
    
    1. Make sure your Airtable secrets are configured in `.streamlit/secrets.toml`
    2. The following fields should be available in your Airtable table:
       - Startup name
       - PH1_founder_name_$startup
       - PH1_founder_surname_$startup
       - PH1_business_model_$startups
       - stage_$startup
       - PH1_Constitution_Location
    
    3. You can also create a specific view called "Fast-tracks" in Airtable
    """)

