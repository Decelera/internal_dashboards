import streamlit as st
import pandas as pd
from pyairtable import Api
import plotly.graph_objects as go
from datetime import datetime, timedelta

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
    """Load dealflow data from Airtable using a specific view"""
    try:
        # Load configuration from Streamlit secrets
        api_key = st.secrets["airtable_fast_tracks"]["api_key"]
        base_id = st.secrets["airtable_fast_tracks"]["base_id"]
        table_id = st.secrets["airtable_fast_tracks"]["table_id"]
        view_id = st.secrets["airtable_fast_tracks"]["view_id"]
        
        api = Api(api_key)
        table = api.table(base_id, table_id)
        
        # Fetch records from the specific view
        records = table.all(view=view_id)
        
        # Extract fields
        data = [record['fields'] for record in records]
        df = pd.DataFrame(data)
        
        return df
    except Exception as e:
        st.error(f"Error loading data from Airtable: {e}")
        st.info("Make sure to configure the following in your .streamlit/secrets.toml:\n\n"
                "[airtable_fast_tracks]\n"
                'api_key = "your_api_key"\n'
                'base_id = "your_base_id"\n'
                'table_id = "your_table_id"\n'
                'view_id = "your_view_id"')
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
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        total_startups = len(df)
        st.metric(label="Total Startups in Dealflow", value=total_startups)
    
    st.markdown("---")
    
    # =============================================================================
    # WEEKLY TRACKING TABLE
    # =============================================================================
    
    st.write("### Weekly Dealflow Tracking")
    
    # Calculate weeks: last 2 weeks, current week, next 4 weeks (7 weeks total)
    today = datetime.now()
    current_week_start = today - timedelta(days=today.weekday())  # Monday of current week
    
    # Find required columns once
    date_sourced_cols = [col for col in df.columns if 'date' in col.lower() and 'source' in col.lower()]
    if not date_sourced_cols:
        date_sourced_cols = [col for col in df.columns if col in ['Date Sourced', 'Date_Sourced', 'DateSourced']]
    
    contact_stage_cols = [col for col in df.columns if 'contact' in col.lower() and 'stage' in col.lower()]
    if not contact_stage_cols:
        contact_stage_cols = [col for col in df.columns if col in ['Contact_Stage', 'Contact Stage', 'ContactStage']]
    
    weeks_data = []
    for i in range(-2, 5):  # -2 (2 weeks ago) to 4 (4 weeks ahead)
        week_start = current_week_start + timedelta(weeks=i)
        week_end = week_start + timedelta(days=6)  # Sunday
        
        # Calculate week number
        week_num = week_start.isocalendar()[1]
        
        new_deals = 0
        not_contacted = 0
        no_response = 0
        videocall_done = 0
        videocall_pending = 0
        pending_info = 0
        
        if date_sourced_cols and contact_stage_cols:
            date_col = date_sourced_cols[0]
            stage_col = contact_stage_cols[0]
            
            for idx, row in df.iterrows():
                # Check if Date Sourced falls within this week
                date_sourced = row.get(date_col)
                if pd.notna(date_sourced):
                    try:
                        # Convert to datetime if it's a string
                        if isinstance(date_sourced, str):
                            sourced_date = pd.to_datetime(date_sourced)
                        else:
                            sourced_date = date_sourced
                        
                        # Check if date falls within this week
                        if week_start.date() <= sourced_date.date() <= week_end.date():
                            new_deals += 1
                            
                            # Count by contact stage
                            stage = row.get(stage_col, "")
                            if pd.notna(stage):
                                stage_lower = str(stage).lower()
                                if "not contacted" in stage_lower:
                                    not_contacted += 1
                                elif "no response" in stage_lower:
                                    no_response += 1
                                elif "videocall done" in stage_lower or "video call done" in stage_lower:
                                    videocall_done += 1
                                elif "videocall pending" in stage_lower or "video call pending" in stage_lower:
                                    videocall_pending += 1
                                elif "pending information" in stage_lower:
                                    pending_info += 1
                    except:
                        pass
        
        weeks_data.append({
            "Week": f"Week {week_num}",
            "Start": week_start.strftime("%d/%m/%Y"),
            "End": week_end.strftime("%d/%m/%Y"),
            "New Deals": new_deals,
            "Not contacted": not_contacted,
            "No Response": no_response,
            "Calls Done": videocall_done,
            "Calls Pending": videocall_pending,
            "Pending Info": pending_info
        })
    
    # Create DataFrame and display as table
    weeks_df = pd.DataFrame(weeks_data)
    
    # Add totals row
    totals = {
        "Week": "Totals",
        "Start": "",
        "End": "",
        "New Deals": weeks_df["New Deals"].sum(),
        "Not contacted": weeks_df["Not contacted"].sum(),
        "No Response": weeks_df["No Response"].sum(),
        "Calls Done": weeks_df["Calls Done"].sum(),
        "Calls Pending": weeks_df["Calls Pending"].sum(),
        "Pending Info": weeks_df["Pending Info"].sum()
    }
    weeks_df = pd.concat([weeks_df, pd.DataFrame([totals])], ignore_index=True)
    
    # Style the table
    st.markdown("""
        <style>
        .weekly-table {
            font-size: 14px;
        }
        .weekly-table th {
            background-color: #62CDEB;
            color: white;
            font-weight: bold;
            padding: 10px;
            text-align: center;
        }
        .weekly-table td {
            padding: 8px;
            text-align: center;
        }
        .weekly-table tr:last-child {
            background-color: #1e3a5f;
            color: white;
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Display the table
    st.dataframe(
        weeks_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Week": st.column_config.TextColumn("Week", width="small"),
            "Start": st.column_config.TextColumn("Start", width="small"),
            "End": st.column_config.TextColumn("End", width="small"),
            "New Deals": st.column_config.NumberColumn("New Deals", width="small"),
            "Not contacted": st.column_config.NumberColumn("Not contacted", width="small"),
            "No Response": st.column_config.NumberColumn("No Response", width="small"),
            "Calls Done": st.column_config.NumberColumn("Calls Done", width="small"),
            "Calls Pending": st.column_config.NumberColumn("Calls Pending", width="small"),
            "Pending Info": st.column_config.NumberColumn("Pending Info", width="small"),
        }
    )
    
    st.markdown("---")
    
    # =============================================================================
    # REFERENCE SOURCE TRACKING TABLE
    # =============================================================================
    
    st.write("### Deal Sources by Week")
    
    # Find reference field
    reference_cols = [col for col in df.columns if 'reference' in col.lower() and ('ph1' in col.lower() or 'startup' in col.lower())]
    if not reference_cols:
        reference_cols = [col for col in df.columns if col in ['PH1_reference', 'Reference', 'Source', 'Deal Source']]
    
    if reference_cols and date_sourced_cols:
        reference_col = reference_cols[0]
        date_col = date_sourced_cols[0]
        
        # Get all unique reference sources
        all_references = df[reference_col].dropna().unique().tolist()
        reference_sources = sorted([str(ref) for ref in all_references if str(ref).strip()])
        
        # Build weekly data by reference source
        reference_weeks_data = []
        reference_totals = {ref: 0 for ref in reference_sources}
        
        for i in range(-2, 5):  # -2 (2 weeks ago) to 4 (4 weeks ahead)
            week_start = current_week_start + timedelta(weeks=i)
            week_end = week_start + timedelta(days=6)  # Sunday
            week_num = week_start.isocalendar()[1]
            
            week_row = {
                "Week": f"Week {week_num}",
                "Start": week_start.strftime("%d/%m/%Y"),
                "End": week_end.strftime("%d/%m/%Y")
            }
            
            # Count deals by reference source for this week
            for ref_source in reference_sources:
                count = 0
                for idx, row in df.iterrows():
                    date_sourced = row.get(date_col)
                    reference = row.get(reference_col)
                    
                    if pd.notna(date_sourced) and pd.notna(reference):
                        try:
                            if isinstance(date_sourced, str):
                                sourced_date = pd.to_datetime(date_sourced)
                            else:
                                sourced_date = date_sourced
                            
                            if week_start.date() <= sourced_date.date() <= week_end.date():
                                if str(reference) == ref_source:
                                    count += 1
                                    reference_totals[ref_source] += 1
                        except:
                            pass
                
                week_row[ref_source] = count
            
            reference_weeks_data.append(week_row)
        
        # Create DataFrame
        reference_weeks_df = pd.DataFrame(reference_weeks_data)
        
        # Add totals row
        totals_row = {
            "Week": "Totals",
            "Start": "",
            "End": ""
        }
        for ref_source in reference_sources:
            totals_row[ref_source] = reference_totals[ref_source]
        
        reference_weeks_df = pd.concat([reference_weeks_df, pd.DataFrame([totals_row])], ignore_index=True)
        
        # Display the reference tracking table
        st.dataframe(
            reference_weeks_df,
            use_container_width=True,
            hide_index=True
        )
        
        # =============================================================================
        # PIE CHART - TOTAL DEAL SOURCES
        # =============================================================================
        
        st.write("#### Total Deal Sources Distribution")
        
        # Create pie chart data from totals
        pie_data = []
        pie_labels = []
        
        for ref_source, count in reference_totals.items():
            if count > 0:  # Only include sources with deals
                pie_labels.append(ref_source)
                pie_data.append(count)
        
        if pie_data:
            fig_references = go.Figure(data=[go.Pie(
                labels=pie_labels,
                values=pie_data,
                hole=0.4,
                marker=dict(colors=['#62CDEB', '#ACAFB9', '#5bb8d6', '#95a3a8', '#7fc9e0', '#8ab5c1', '#a3d5e8', '#c2e3f0'])
            )])
            fig_references.update_layout(
                showlegend=True,
                height=400,
                margin=dict(l=20, r=20, t=40, b=20)
            )
            st.plotly_chart(fig_references, use_container_width=True)
        else:
            st.info("No deal source data available yet.")
    else:
        st.warning("Reference field not found in data. Expected field: 'PH1_reference_$startups' or similar.")
    
    st.markdown("---")
    
    # =============================================================================
    # TOP 10 STARTUPS BY SIGNALS
    # =============================================================================
    
    st.write("### Top 10 Startups by Signals")
    
    # Signal scoring explanation
    st.info("**Signal Scoring:** 🟢 Green = 3 points | 🟡 Yellow = 2 points | 🔴 Red = 1 point | Maximum score: 21 points")
    
    # Find Signals field
    signals_cols = [col for col in df.columns if 'signal' in col.lower()]
    if not signals_cols:
        signals_cols = [col for col in df.columns if col in ['Signals', 'Signal', 'signals']]
    
    if signals_cols:
        signals_col = signals_cols[0]
        
        # Parse signals and calculate scores
        startup_scores = []
        
        for idx, row in df.iterrows():
            signals_text = row.get(signals_col, "")
            
            if pd.notna(signals_text) and str(signals_text).strip():
                # Count emojis in the signals text
                green_count = str(signals_text).count('🟢')
                yellow_count = str(signals_text).count('🟡')
                red_count = str(signals_text).count('🔴')
                
                # Calculate total score (Green=3, Yellow=2, Red=1)
                total_score = (green_count * 3) + (yellow_count * 2) + (red_count * 1)
                
                # Get startup info
                startup_name_cols = [col for col in df.columns if 'startup' in col.lower() and 'name' in col.lower()]
                if not startup_name_cols:
                    startup_name_cols = [col for col in df.columns if col == 'Name' or col == 'Startup' or col == 'Company']
                
                startup_name = get_field_value(row, startup_name_cols, "Unknown Startup") if startup_name_cols else "Unknown Startup"
                
                # Get founder name
                founder_name = get_founder_full_name(row, startup_name)
                
                # Get other fields
                one_liner_cols = [col for col in df.columns if 'one' in col.lower() and 'liner' in col.lower()]
                if not one_liner_cols:
                    one_liner_cols = [col for col in df.columns if col in ['One liner', 'One_liner', 'OneLiner', 'Tagline']]
                one_liner = get_field_value(row, one_liner_cols, "N/A") if one_liner_cols else "N/A"
                
                bm_patterns = [f"PH1_business_model_{startup_name}", "PH1_business_model", "Business Model", "business_model"]
                business_model = get_field_value(row, bm_patterns, "N/A")
                
                stage_patterns = [f"stage_{startup_name}", "stage", "Stage"]
                stage = get_field_value(row, stage_patterns, "N/A")
                
                location_patterns = ["PH1_Constitution_Location", "Constitution_Location", "Location", "location"]
                location = get_field_value(row, location_patterns, "N/A")
                
                startup_scores.append({
                    'name': startup_name,
                    'founder': founder_name,
                    'one_liner': one_liner,
                    'business_model': business_model,
                    'stage': stage,
                    'location': location,
                    'signals': signals_text,
                    'score': total_score,
                    'green': green_count,
                    'yellow': yellow_count,
                    'red': red_count
                })
        
        # Sort by score and get top 10
        startup_scores.sort(key=lambda x: x['score'], reverse=True)
        top_10 = startup_scores[:10]
        
        if top_10:
            # Display top 10 in a nice format
            for i, startup in enumerate(top_10, 1):
                with st.container(border=True):
                    # Header with rank and name
                    col_header1, col_header2 = st.columns([3, 1])
                    with col_header1:
                        st.markdown(f"### #{i} - {startup['name']}")
                    with col_header2:
                        st.markdown(f"### Score: {startup['score']}/21")
                    
                    # Startup details
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"**👤 Founder:** {startup['founder']}")
                        st.markdown(f"**💡 One Liner:** {startup['one_liner']}")
                        st.markdown(f"**💼 Business Model:** {startup['business_model']}")
                    
                    with col2:
                        st.markdown(f"**📊 Stage:** {startup['stage']}")
                        st.markdown(f"**📍 Location:** {startup['location']}")
                        st.markdown(f"**🎯 Signals:** {startup['green']} 🟢 | {startup['yellow']} 🟡 | {startup['red']} 🔴")
                    
                    # Display full signals breakdown
                    with st.expander("📊 View Signal Details"):
                        st.markdown(startup['signals'])
        else:
            st.info("No startups with signal data found.")
    else:
        st.warning("Signals field not found in data.")
    
    st.markdown("---")
    
    # Use full dataframe (no filters)
    filtered_df = df.copy()
    
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
    
    1. Add the following to your `.streamlit/secrets.toml`:
    
    ```toml
    [airtable_fast_tracks]
    api_key = "your_airtable_api_key"
    base_id = "your_base_id"
    table_id = "your_table_id"
    view_id = "your_view_id"
    ```
    
    2. Make sure the following fields are available in your Airtable view:
       - Startup name
       - PH1_founder_name_$startup and PH1_founder_surname_$startup
       - PH1_business_model_$startups
       - stage_$startup
       - PH1_Constitution_Location
    """)

