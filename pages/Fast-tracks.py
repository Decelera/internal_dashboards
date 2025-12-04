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

def get_current_week_range() -> tuple[datetime, datetime]:
    """Devuelve inicio y fin de la semana actual lunes-domingo"""
    today = datetime.today()

    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    return start_of_week, end_of_week

def get_founder_full_name(row, startup_name):
    """Combine founder name and surname"""
    # List of possible name field patterns
    name_patterns = [
        "PH1_founder_name_$startup",
        "PH1_founder_name",
        f"PH1_founder_name_{startup_name}",
        "founder_name"
    ]
    
    # List of possible surname field patterns (note: sur_name vs surname)
    surname_patterns = [
        "PH1_founder_sur_name_$startup",
        "PH1_founder_surname_$startup",
        "PH1_founder_sur_name",
        "PH1_founder_surname",
        f"PH1_founder_sur_name_{startup_name}",
        f"PH1_founder_surname_{startup_name}",
        "founder_surname",
        "founder_sur_name"
    ]
    
    # Try to find name
    first_name = ""
    for pattern in name_patterns:
        value = row.get(pattern, "")
        if pd.notna(value) and str(value).strip():
            first_name = str(value).strip()
            break
    
    # Try to find surname
    last_name = ""
    for pattern in surname_patterns:
        value = row.get(pattern, "")
        if pd.notna(value) and str(value).strip():
            last_name = str(value).strip()
            break
    
    # Combine if we found at least one part
    if first_name or last_name:
        full_name = f"{first_name} {last_name}".strip()
        return full_name if full_name else "N/A"
    
    return "N/A"

def get_field_value(row, field_patterns, default="N/A"):
    """Return the first non-empty value from multiple field name patterns."""
    
    for pattern in field_patterns:
        if pattern not in row:
            continue
        
        value = row[pattern]

        # 1) Si es NaN (float), saltar
        if isinstance(value, float) and pd.isna(value):
            continue

        # 2) Si es array de numpy → convertir a lista
        if isinstance(value, (list, tuple)):
            pass  # se gestiona abajo
        elif hasattr(value, "__array__"):  # numpy array
            value = value.tolist()

        # 3) Si es lista (Airtable multiselect o attachments)
        if isinstance(value, list):
            if len(value) == 0:
                continue

            first = value[0]

            # 3.1 Caso attachment (dict con url y filename)
            if isinstance(first, dict):
                if "url" in first:
                    return first["url"]
                if "filename" in first:
                    return first["filename"]
                # fallback
                return str(first)

            # 3.2 Caso multiselect simple
            first_str = str(first).strip()
            if first_str and first_str.lower() != "nan":
                return first_str
            continue

        # 4) Valor escalar válido
        value_str = str(value).strip()
        if value_str and value_str.lower() != "nan":
            return value_str

    return default


# =============================================================================
# DASHBOARD METRICS
# =============================================================================

# Calculamos el inicio y fin de la semana actual
start_of_week, end_of_week = get_current_week_range()

if not df.empty:

    # =============================================================================
    # URGENCY METRICS (THIS WEEK)
    # =============================================================================
    
    # 1. Identify the necessary columns dynamically
    urgency_col = next((col for col in df.columns if col.lower() == 'urgency'), None)

    if urgency_col:
        df_metrics = df.copy()

        urgency_series = df_metrics[urgency_col].astype(str).str.lower().str.strip()

        hot_count = len(urgency_series[urgency_series == 'hot'])
        warm_count = len(urgency_series[urgency_series == 'warm'])
        cold_count = len(urgency_series[urgency_series == 'cold'])

    else:
        # Fallback if columns are missing
        st.warning("Could not display Urgency metrics: 'Urgency' or 'Date Sourced' column not found.")

    # =============================================================================
    # LOCATION METRICS (ALL RECORDS)
    # =============================================================================

    # 1. Find Location column
    location_col = next((col for col in df.columns if col.lower() in ['location', 'constitution_location', 'country', 'ph1_constitution_location', "PH1_Constitution_Location"]), None)

    if location_col:
        # 2. Define Keywords for Classification
        europe_keywords = [
            'spain', 'espana', 'españa', 'uk', 'united kingdom', 'england', 'london', 
            'germany', 'france', 'italy', 'portugal', 'greece', 'poland', 'lithuania', 
            'ukraine', 'estonia', 'hungary', 'netherlands', 'holand', 'ireland', 
            'norway', 'sweden', 'finland', 'denmark', 'switzerland', 'europe', 
            'baltics', 'nordics', 'slovakia', 'eslovaquia', 'barcelona', 'czech', 
            'romania', 'belgium', 'austria', 'luxembourg', 'turkey', 'türkiye'
        ]

        americas_keywords = [
            'united states', 'usa', 'us', 'america', 'mexico', 'brazil', 'brasil', 
            'argentina', 'colombia', 'chile', 'panama', 'cayman', 'uruguay', 
            'guatemala', 'peru', 'ecuador', 'canada', 'latam', 'latin america', 
            'washington', 'kentucky', 'porto alegre', 'sao paulo', 'costa rica',
            'bolivia', 'venezuela', 'mclean', 'ny', 'sf'
        ]

        # 3. Counting Function - using all records
        europe_count = 0
        americas_count = 0
        other_count = 0

        for location_raw in df[location_col]:
            # --- CORRECCIÓN AQUÍ ---
            # Primero verificamos si es una lista (caso común en Airtable)
            if isinstance(location_raw, list):
                if not location_raw: # Si la lista está vacía
                    continue
                # Unimos los elementos de la lista en un solo string
                loc_str = " ".join([str(item) for item in location_raw]).lower()
            
            # Si no es lista, verificamos si es nulo (NaN/None)
            elif pd.isna(location_raw):
                continue
            
            # Si es un string o número normal
            else:
                loc_str = str(location_raw).lower()
            # -----------------------
            
            # Check for matches
            is_europe = any(k in loc_str for k in europe_keywords)
            is_americas = any(k in loc_str for k in americas_keywords)

            if is_europe:
                europe_count += 1
            elif is_americas:
                americas_count += 1
            else:
                other_count += 1
    else:
        # Define defaults to avoid errors later if columns are missing
        europe_count = 0
        americas_count = 0
        st.warning("Could not display Geographic metrics: 'Location' column not found.")

    st.markdown("---")

    # Find required columns once
    date_sourced_cols = [col for col in df.columns if 'date' in col.lower() and 'source' in col.lower()]
    if not date_sourced_cols:
        date_sourced_cols = [col for col in df.columns if col in ['Date Sourced', 'Date_Sourced', 'DateSourced']]
    
    contact_stage_cols = [col for col in df.columns if 'contact' in col.lower() and 'stage' in col.lower()]
    if not contact_stage_cols:
        contact_stage_cols = [col for col in df.columns if col in ['Contact_Stage', 'Contact Stage', 'ContactStage']]
    
    weeks_data = []
    current_week_index = None  # Track which row is the current week
    
    for i in range(-2, 5):  # -2 (2 weeks ago) to 4 (4 weeks ahead)
        week_start = start_of_week + timedelta(weeks=i)
        week_end = week_start + timedelta(days=6)  # Sunday
        
        # Calculate week number
        week_num = week_start.isocalendar()[1]
        
        # Mark current week (when i == 0)
        if i == 0:
            current_week_index = len(weeks_data)
        
        new_deals = 0
        contacted = 0
        no_response = 0
        videocall_done = 0
        videocall_pending = 0
        pending_info = 0
        
        if date_sourced_cols and contact_stage_cols:
            date_col = date_sourced_cols[0]
            stage_col = contact_stage_cols[0]
            
            # Look for Date_First_Contact field (when the contact/call happened)
            last_contacted_cols = [col for col in df.columns if 'last' in col.lower() and 'contacted' in col.lower()]
            first_contact_date_cols = [col for col in df.columns if 'first' in col.lower() and 'contact' in col.lower() and 'date' in col.lower()]
            if not first_contact_date_cols:
                first_contact_date_cols = [col for col in df.columns if col in ['Date_First_Contact', 'Date First Contact', 'First_Contact_Date', 'First Contact Date']]
            
            for idx, row in df.iterrows():
                # Count New Deals based on Date Sourced
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
                    except:
                        pass
                
                # Count Contacted based on Date_First_Contact
                if last_contacted_cols:
                    last_contacted_date = row.get(last_contacted_cols[0])
                    if pd.notna(last_contacted_date):
                        try:
                            # Convert to datetime if it's a string
                            if isinstance(last_contacted_date, str):
                                contact_date_obj = pd.to_datetime(last_contacted_date)
                            else:
                                contact_date_obj = last_contacted_date
                            
                            # Check if date falls within this week
                            if week_start.date() <= contact_date_obj.date() <= week_end.date():
                                contacted += 1
                        except:
                            pass
                
                # For contact stage statuses: use Date_First_Contact for timing
                stage = row.get(stage_col, "")
                if pd.notna(stage):
                    stage_lower = str(stage).lower()
                    
                    # Get the contact date for this status
                    contact_date = None
                    if first_contact_date_cols:
                        contact_date = row.get(first_contact_date_cols[0])
                    
                    # For videocall statuses, use Date_First_Contact
                    if "videocall done" in stage_lower or "video call done" in stage_lower:
                        if pd.notna(contact_date):
                            try:
                                if isinstance(contact_date, str):
                                    contact_date_obj = pd.to_datetime(contact_date)
                                else:
                                    contact_date_obj = contact_date
                                
                                if week_start.date() <= contact_date_obj.date() <= week_end.date():
                                    videocall_done += 1
                            except:
                                pass
                    
                    elif "videocall pending" in stage_lower or "video call pending" in stage_lower:
                        if pd.notna(contact_date):
                            try:
                                if isinstance(contact_date, str):
                                    contact_date_obj = pd.to_datetime(contact_date)
                                else:
                                    contact_date_obj = contact_date
                                
                                if week_start.date() <= contact_date_obj.date() <= week_end.date():
                                    videocall_pending += 1
                            except:
                                pass
                    
                    # For other statuses, use Date_First_Contact if available, else Date Sourced
                    else:
                        status_date = contact_date if pd.notna(contact_date) else date_sourced
                        if pd.notna(status_date):
                            try:
                                if isinstance(status_date, str):
                                    status_date_obj = pd.to_datetime(status_date)
                                else:
                                    status_date_obj = status_date
                                
                                if week_start.date() <= status_date_obj.date() <= week_end.date():
                                    if "no response" in stage_lower:
                                        no_response += 1
                                    elif "pending information" in stage_lower:
                                        pending_info += 1
                            except:
                                pass
        
        # Add marker for current week
        week_label = f"Week {week_num}"
        if i == 0:
            week_label = f"📍 Week {week_num} (Current)"
        
        weeks_data.append({
            "Week": week_label,
            "Start": week_start.strftime("%d/%m/%Y"),
            "End": week_end.strftime("%d/%m/%Y"),
            "New Deals": new_deals,
            "Contacted": contacted,
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
        "Contacted": weeks_df["Contacted"].sum(),
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
    
    # Style the dataframe to highlight current week
    def highlight_current_week(row):
        """Apply highlighting to the current week row"""
        if row.name == current_week_index:
            return ['background-color: #62CDEB; color: white; font-weight: bold'] * len(row)
        elif row.name == len(weeks_df) - 1:  # Totals row
            return ['background-color: #1e3a5f; color: white; font-weight: bold'] * len(row)
        else:
            return [''] * len(row)

    # Fila de la semana actual
    current_row = weeks_df.iloc[current_week_index]

    # Fila de la semana anterior (si existe)
    prev_row = weeks_df.iloc[current_week_index - 1] if current_week_index > 0 else None

    # Valores de las metrics
    current_new_deals = int(current_row["New Deals"])
    current_contacted = int(current_row["Contacted"])
    current_calls_pending = int(current_row["Calls Pending"])

    prev_new_deals = int(prev_row["New Deals"]) if prev_row is not None else 0
    prev_contacted = int(prev_row["Contacted"]) if prev_row is not None else 0
    prev_calls_pending = int(prev_row["Calls Pending"]) if prev_row is not None else 0

    delta_new_deals = f"{round((current_new_deals - prev_new_deals) / prev_new_deals * 100, 2)} %" if prev_new_deals != 0 else ""
    delta_contacted = f"{round((current_contacted - prev_contacted) / prev_contacted * 100, 2)} %" if prev_contacted != 0 else ""
    delta_calls_pending = f"{round((current_calls_pending - prev_calls_pending) / prev_calls_pending * 100, 2)} %" if prev_calls_pending != 0 else ""

    # Métricas arriba de la tabla

    st.markdown("### General metrics")

    columns_tags = st.columns(3)

    with columns_tags[1]:
        st.metric(
            label="Total number of leads",
            value=df.shape[0],
        )

    with columns_tags[0]:
        st.metric(
            label="New deals this week",
            value=current_new_deals,
            delta=delta_new_deals,  # comparación con la semana anterior
        )

    with columns_tags[2]:
        st.metric(
            label="Contacted this week",
            value=current_contacted,
            delta=delta_contacted,  # comparación con la semana anterior
        )  

    st.markdown("---")

    st.markdown("### Geographic metrics")

    g_col1, g_col2 = st.columns(2)

    if location_col:
        with g_col1:
            st.metric(label="Europe", value=europe_count)
        
        with g_col2:
            st.metric(label="Americas", value=americas_count)

    st.markdown("---")
    
    st.markdown("### Urgency metrics")
    
    m_col1, m_col2, m_col3 = st.columns(3)
        
    if date_col and urgency_col:
        with m_col1:
            st.metric(label="🔥 Hot Deals", value=hot_count)
        
        with m_col2:
            st.metric(label="🌤️ Warm Deals", value=warm_count)
            
        with m_col3:
            st.metric(label="❄️ Cold Deals", value=cold_count)
    
    # Apply styling
    styled_df = weeks_df.style.apply(highlight_current_week, axis=1)

    st.markdown("---")

    # Display the styled table
    with st.expander("View table of weekly fast-tracks"):
        st.dataframe(
            styled_df,
            use_container_width=True,
            hide_index=True,
            column_config={
            "Week": st.column_config.TextColumn("Week", width="small"),
            "Start": st.column_config.TextColumn("Start", width="small"),
            "End": st.column_config.TextColumn("End", width="small"),
            "New Deals": st.column_config.NumberColumn("New Deals", width="small"),
            "Contacted": st.column_config.NumberColumn("Contacted", width="small"),
            "No Response": st.column_config.NumberColumn("No Response", width="small"),
            "Calls Done": st.column_config.NumberColumn("Calls Done", width="small"),
            "Calls Pending": st.column_config.NumberColumn("Calls Pending", width="small"),
            "Pending Info": st.column_config.NumberColumn("Pending Info", width="small"),
        }
    )
    
    st.markdown("---")
    
    # =============================================================================
    # CURRENT WEEK REFERENCES
    # =============================================================================
    
    st.write("### Who Referenced Deals This Week?")
    
    # Find reference fields
    reference_cols = [col for col in df.columns if 'ph1_reference' in col.lower() and 'startup' in col.lower() and 'other' not in col.lower()]
    reference_other_cols = [col for col in df.columns if 'ph1_reference_other' in col.lower() and 'startup' in col.lower()]
    
    if not reference_cols:
        reference_cols = [col for col in df.columns if col in ['PH1_reference', 'Reference']]
    if not reference_other_cols:
        reference_other_cols = [col for col in df.columns if col in ['PH1_reference_other', 'Reference Other']]
    
    if reference_cols and date_sourced_cols:
        reference_col = reference_cols[0]
        reference_other_col = reference_other_cols[0] if reference_other_cols else None
        date_col = date_sourced_cols[0]
        
        # Get deals from current week only
        # Store as dict with main reference as key and dict of details as value
        current_week_references = {}
        
        for idx, row in df.iterrows():
            date_sourced = row.get(date_col)
            
            if pd.notna(date_sourced):
                try:
                    if isinstance(date_sourced, str):
                        sourced_date = pd.to_datetime(date_sourced)
                    else:
                        sourced_date = date_sourced
                    
                    # Check if date falls within current week
                    if start_of_week.date() <= sourced_date.date() <= (start_of_week + timedelta(days=6)).date():
                        reference = row.get(reference_col)
                        reference_other = row.get(reference_other_col) if reference_other_col else None
                        
                        # Get main reference value
                        ref_value = ""
                        if pd.notna(reference):
                            ref_value = str(reference).strip()
                            # Handle list format
                            if isinstance(reference, list) and len(reference) > 0:
                                ref_value = str(reference[0]).strip()
                        
                        # Get additional reference details (optional)
                        ref_other_value = ""
                        if reference_other_col and pd.notna(reference_other):
                            ref_other_value = str(reference_other).strip()
                            if isinstance(reference_other, list) and len(reference_other) > 0:
                                ref_other_value = str(reference_other[0]).strip()
                        
                        if ref_value:
                            # Use main reference as key
                            if ref_value not in current_week_references:
                                current_week_references[ref_value] = {
                                    'count': 0,
                                    'details': set()  # Store unique detail values
                                }
                            
                            current_week_references[ref_value]['count'] += 1
                            
                            # Add detail if present
                            if ref_other_value:
                                current_week_references[ref_value]['details'].add(ref_other_value)
                except:
                    pass
        
        if current_week_references:
            # Calculate total
            total_deals = sum(ref_data['count'] for ref_data in current_week_references.values())
            
            # Display header with total
            col_header1, col_header2 = st.columns([2, 1])
            with col_header1:
                st.write(f"**📍 Current Week:** {start_of_week.strftime('%d/%m/%Y')} - {end_of_week.strftime('%d/%m/%Y')}")
            with col_header2:
                st.write(f"**Total: {total_deals} deal{'s' if total_deals != 1 else ''}**")
            
            st.write("")
            
            # Sort by count
            sorted_refs = sorted(current_week_references.items(), key=lambda x: x[1]['count'], reverse=True)
            
            # Add custom CSS for fixed height containers
            st.markdown("""
                <style>
                .reference-card {
                    min-height: 140px;
                    display: flex;
                    flex-direction: column;
                }
                </style>
            """, unsafe_allow_html=True)
            
            # Display in columns
            num_cols = 3
            cols = st.columns(num_cols)
            
            for i, (ref_name, ref_data) in enumerate(sorted_refs):
                with cols[i % num_cols]:
                    with st.container(border=True):
                        # Main reference as prominent metric
                        count = ref_data['count']
                        st.metric(label=ref_name, value=f"{count} deal{'s' if count != 1 else ''}")
                        
                        # Show details as secondary info if present
                        if ref_data['details']:
                            details_list = sorted(list(ref_data['details']))
                            st.caption("")  # Add spacing
                            for detail in details_list:
                                st.caption(f"• {detail}")
                        else:
                            # Add empty space to maintain alignment
                            st.caption("")
                            st.caption("")
        else:
            st.info("No deals were referenced this week yet.")
    else:
        st.warning("Reference fields not found in data. Expected: 'PH1_reference_$startups' and 'PH1_reference_other_$startups'")
    
    st.markdown("---")
    
    # =============================================================================
    # WEEKLY TRACKING TABLE - LEADERBOARD
    # =============================================================================
    
    st.write("### Weekly Dealflow Tracking")

    df_leaders = df.copy()
    df_leaders["date_sourced"] = pd.to_datetime(df_leaders["date_sourced"])
    df_leaders["Date_First_Contact"] = pd.to_datetime(df_leaders["Date_First_Contact"])
    df_leaders["Last Contacted"] = pd.to_datetime(df_leaders["Last Contacted"])
    
    # Leaderboard
    df_leaders = df_leaders.groupby("Responsible", as_index=False).agg(
        source_count=(
            "date_sourced",
            lambda s: ((s.dropna().dt.date >= start_of_week.date()) & (s.dropna().dt.date <= end_of_week.date())).sum()
        ),  
        contacted=(
            "Last Contacted",
            lambda s: ((s.dropna().dt.date >= start_of_week.date()) & (s.dropna().dt.date <= end_of_week.date())).sum()
        ),
    )

    df_leaders["leader_score"] = (df_leaders["source_count"] + df_leaders["contacted"]) / 2
    leader_row = df_leaders.loc[df_leaders["leader_score"].idxmax()]
    leader = leader_row["Responsible"]
    leader_sources = leader_row["source_count"]
    leader_contacted = leader_row["contacted"]

    leader_cols = st.columns(3)
    with leader_cols[1]:
        with st.container(border=True):
            st.markdown(f"#### 👑 Current week leader: {leader}")
            secondary_cols = st.columns(2)
            with secondary_cols[0]:
                st.metric("Sourced", leader_sources)
            with secondary_cols[1]:
                st.metric("Contact", leader_contacted)

    with st.expander("View table of the team leaderboard"):
        # Prepare dataframe with totals row
        df_leaderboard = df_leaders.sort_values(by="leader_score", ascending=False).drop(columns=["leader_score"])
        
        # Add totals row
        totals_row = pd.DataFrame({
            "Responsible": ["Total"],
            "source_count": [df_leaderboard["source_count"].sum()],
            "contacted": [df_leaderboard["contacted"].sum()]
        })
        df_leaderboard_with_totals = pd.concat([df_leaderboard, totals_row], ignore_index=True)
        
        # Style the totals row (last row) with different background and bold
        def highlight_totals_row(row):
            if row.name == len(df_leaderboard_with_totals) - 1:
                return ['background-color: #1e3a5f; color: white; font-weight: bold'] * len(row)
            return [''] * len(row)
        
        styled_leaderboard = df_leaderboard_with_totals.style.apply(highlight_totals_row, axis=1)
        
        st.dataframe(
            styled_leaderboard,
            use_container_width=True,
            hide_index=True,
            column_config={
            "Responsible": st.column_config.TextColumn("Responsible", width="small"),
            "source_count": st.column_config.NumberColumn("Sourced", width="small"),
            "contacted": st.column_config.NumberColumn("Contact", width="small"),
        }
    )
    
    st.markdown("---")
    
    # =============================================================================
    # QUALIFIED STARTUPS TABLE
    # =============================================================================
    
    st.write("### 🎯 Qualified Startups")
    st.caption("These startups have passed initial screening and can be used in VC meetings to exchange dealflow.")
    st.write("")
    
    # Find stage field - be more specific
    stage_field_cols = [col for col in df.columns if col == 'Stage' or col == 'stage']
    if not stage_field_cols:
        # Fallback: any field containing 'stage' but not other words
        stage_field_cols = [col for col in df.columns if 'stage' in col.lower() and 'contact' not in col.lower()]
    
    if stage_field_cols:
        stage_field = stage_field_cols[0]
        
        # Filter for "Qualified" stage - try multiple matching strategies
        # First try exact match
        qualified_df = df[df[stage_field].astype(str).str.strip().str.lower() == 'qualified']
        
        # If empty, try contains
        if qualified_df.empty:
            qualified_df = df[df[stage_field].astype(str).str.lower().str.contains('qualified', na=False)]
        
        if not qualified_df.empty:
            st.write(f"**Total:** {len(qualified_df)} startups")
            st.write("")
            
            # Display in a 2-column grid with cards
            num_cols = 2
            rows = [qualified_df.iloc[i:i+num_cols] for i in range(0, len(qualified_df), num_cols)]
            
            for row_idx, row_data in enumerate(rows):
                cols = st.columns(num_cols)
                for col_idx, (_, startup_row) in enumerate(row_data.iterrows()):
                    with cols[col_idx]:
                        # Get startup name - use "Startup name" field specifically
                        startup_name = "Unknown Startup"
                        
                        # Try exact match first: "Startup name"
                        if 'Startup name' in df.columns:
                            val = startup_row.get('Startup name')
                            if pd.notna(val):
                                startup_name = str(val)
                        # Try variations
                        elif 'Startup_name' in df.columns:
                            val = startup_row.get('Startup_name')
                            if pd.notna(val):
                                startup_name = str(val)
                        elif 'startup_name' in df.columns:
                            val = startup_row.get('startup_name')
                            if pd.notna(val):
                                startup_name = str(val)
                        else:
                            # Fallback: find any column with "startup" and "name"
                            startup_name_cols = [col for col in df.columns if 'startup' in col.lower() and 'name' in col.lower()]
                            if startup_name_cols:
                                val = startup_row.get(startup_name_cols[0])
                                if pd.notna(val):
                                    startup_name = str(val)
                        
                        # Get founder name using helper function
                        founder_name = get_founder_full_name(startup_row, startup_name)
                        
                        # Get one liner
                        one_liner_cols = [col for col in df.columns if 'one' in col.lower() and 'liner' in col.lower()]
                        one_liner = get_field_value(startup_row, one_liner_cols, "N/A") if one_liner_cols else "N/A"
                        
                        # Get business model
                        bm_patterns = ["PH1_business_model", "Business Model", "business_model"]
                        business_model = get_field_value(startup_row, bm_patterns, "N/A")
                        
                        # Get location
                        location_patterns = ["PH1_Constitution_Location", "Constitution_Location", "Location", "location"]
                        location = get_field_value(startup_row, location_patterns, "N/A")

                        # Get stage
                        stage_patterns = ["stage", "stage_$startup"]
                        stage = get_field_value(startup_row, stage_patterns, "N/A")

                        # Get round size
                        round_size_patterns = ["PH1_Round_Size", "Round_Size", "round_size"]
                        round_size = get_field_value(startup_row, round_size_patterns, "N/A")

                        # Get stake
                        stake_patterns = ["PH1_Stake", "Stake", "stake"]
                        stake = get_field_value(startup_row, stake_patterns, "N/A")

                        # Get reference
                        reference_patterns = ["PH1_Reference", "Reference", "reference", "PH1_reference_$startups"]
                        reference = get_field_value(startup_row, reference_patterns, "N/A")

                        # Get reference details
                        reference_details_patterns = ["PH1_Reference_Details", "Reference_Details", "reference_details", "PH1_reference_other_$startups"]
                        reference_details = get_field_value(startup_row, reference_details_patterns, "N/A")

                        # Get signals
                        signals_patterns = ["Signals"]
                        signals = get_field_value(startup_row, signals_patterns, "N/A")
                        signals_list = [sign.strip() for sign in signals.split("|") if signals != "N/A"]

                        # Get red and green flags
                        red_flags = get_field_value(startup_row, ["redflags_summary"], "N/A")
                        red_flags_list = [s.strip() for s in red_flags.split("\n")]

                        green_flags = get_field_value(startup_row, ["greenflags_summary"], "N/A")
                        green_flags_list = [s.strip() for s in green_flags.split("\n")]
                        
                        # Create card with main info
                        with st.container(border=True):
                            st.markdown(f"### {startup_name}")
                            
                            # Show founder name above one liner
                            if founder_name and founder_name != "N/A":
                                st.markdown(f"**👤 {founder_name}**")
                            
                            # Show one liner if available
                            if one_liner and one_liner != "N/A":
                                st.markdown(f"*{one_liner}*")
                            
                            # Expandable details section - ALL OTHER info goes here
                            with st.expander("📊 View Full Details"):
                                
                                # Show stage
                                if (stage and stage != "N/A"):
                                    st.markdown(f"**🚀 Stage**  \n{stage}")

                                # Show business model and location
                                if (business_model and business_model != "N/A") or (location and location != "N/A"):
                                    info_col1, info_col2 = st.columns(2)
                                    with info_col1:
                                        if business_model and business_model != "N/A":
                                            st.markdown(f"**💼 Business Model**  \n{business_model}")
                                    with info_col2:
                                        if location and location != "N/A":
                                            st.markdown(f"**📍 Location**  \n{location}")
                                    st.markdown("")
                                
                                # Get financial details
                                round_size = get_field_value(startup_row, ["Round_Size", "Round Size", "round_size"], "N/A")
                                valuation_patterns = ["PH1_current_valuation", "Current_Valuation", "Valuation"]
                                current_valuation = get_field_value(startup_row, valuation_patterns, "N/A")
                                stake = get_field_value(startup_row, ["Stake_Formula", "Stake Formula", "stake_formula", "Stake"], "N/A")
                                
                                # Get deck links
                                deck_url = get_field_value(startup_row, ["deck_URL", "Deck_URL", "Deck URL"], "")
                                deck_startup = get_field_value(startup_row, ["deck_$startup", "deck_startup", "Deck"], "")
                                if isinstance(deck_startup, dict):
                                    deck_attachment_url = deck_startup["url"]
                                else:
                                    deck_attachment_url = ""
                                
                                # Show financial info
                                if (round_size and round_size != "N/A") or (current_valuation and current_valuation != "N/A") or (stake and stake != "N/A"):
                                    detail_col1, detail_col2 = st.columns(2)
                                    with detail_col1:
                                        if round_size and round_size != "N/A":
                                            st.markdown(f"**💰 Round Size**  \n{round_size}")
                                        if current_valuation and current_valuation != "N/A":
                                            st.markdown(f"**📈 Current Valuation**  \n{current_valuation}")
                                    with detail_col2:
                                        if stake and stake != "N/A":
                                            st.markdown(f"**🎯 Stake**  \n{stake}")
                                    st.markdown("")
                                
                                # Show referal info
                                if (reference and reference != "N/A") or (reference_details and referenece_details != "N/A"):
                                    col1, col2 = st.columns(2)
                                    with col1:
                                        if reference and reference != "N/A":
                                            st.markdown(f"**🔗 Reference**  \n{reference}")
                                    with col2:
                                        if reference_details and reference_details != "N/A":
                                            st.markdown(f"**🔗 Reference Details**  \n{reference_details}")
                                    st.markdown("")
                                
                                # Show signals and red flags
                                cols_signals = st.columns(2)
                                if (signals_list and signals_list != "N/A"):
                                    with cols_signals[0]:
                                        st.markdown("**Signals:**")
                                        for signal in signals_list:
                                            st.markdown(f"{signal}")
                                
                                if (red_flags_list and red_flags_list != ["N/A"]) or (green_flags_list and green_flags_list != ["N/A"]):
                                    with cols_signals[1]:
                                        st.markdown("**Red Flags:**")
                                        for red_flag in red_flags_list:
                                            st.markdown(f"{red_flag}")
                                        st.markdown("**Green Flags:**")
                                        for green_flag in green_flags_list:
                                            st.markdown(f"{green_flag}")
                                
                                # Show alternativo de los links de los decks
                                if deck_attachment_url and not deck_url:
                                    st.markdown(f'<a href="{deck_attachment_url}">📄 Deck</a>', unsafe_allow_html=True)

                                elif deck_url and not deck_attachment_url:
                                    st.markdown(f'<a href="{deck_url}">📄 Deck</a>', unsafe_allow_html=True)

                                elif deck_url and deck_attachment_url:
                                    st.markdown(
                                        f'<a href="{deck_url}">📄 Deck</a> | '
                                        f'<a href="{deck_attachment_url}">📄 Deck (Attachment)</a>',
                                        unsafe_allow_html=True
                                    )
        else:
            st.info("No startups with 'Qualified' stage found.")
    else:
        st.warning("Stage field not found in data.")
    
    st.markdown("---")
    
    # =============================================================================
    # HOT DEALS
    # =============================================================================
    
    st.write("### 🔥 Hot Deals")

    # Find stage field - be more specific
    urgency_field_cols = [col for col in df.columns if col == 'Urgency' or col == 'urgency']
    if not urgency_field_cols:
        # Fallback: any field containing 'stage' but not other words
        urgency_field_cols = [col for col in df.columns if 'urgency' in col.lower() and 'contact' not in col.lower()]
    
    if urgency_field_cols:
        urgency_field = urgency_field_cols[0]
        
        # Filter for "Qualified" stage - try multiple matching strategies
        # First try exact match
        hot_df = df[df[urgency_field].astype(str).str.strip().str.lower() == 'hot']
        
        # If empty, try contains
        if hot_df.empty:
            hot_df = df[df[urgency_field].astype(str).str.lower().str.contains('hot', na=False)]
        
        if not hot_df.empty:
            st.write(f"**Total:** {len(hot_df)} startups")
            st.write("")
            
            # Display in a 2-column grid with cards
            num_cols = 2
            rows = [hot_df.iloc[i:i+num_cols] for i in range(0, len(hot_df), num_cols)]
            
            for row_idx, row_data in enumerate(rows):
                cols = st.columns(num_cols)
                for col_idx, (_, startup_row) in enumerate(row_data.iterrows()):
                    with cols[col_idx]:
                        # Get startup name - use "Startup name" field specifically
                        startup_name = "Unknown Startup"
                        
                        # Try exact match first: "Startup name"
                        if 'Startup name' in df.columns:
                            val = startup_row.get('Startup name')
                            if pd.notna(val):
                                startup_name = str(val)
                        # Try variations
                        elif 'Startup_name' in df.columns:
                            val = startup_row.get('Startup_name')
                            if pd.notna(val):
                                startup_name = str(val)
                        elif 'startup_name' in df.columns:
                            val = startup_row.get('startup_name')
                            if pd.notna(val):
                                startup_name = str(val)
                        else:
                            # Fallback: find any column with "startup" and "name"
                            startup_name_cols = [col for col in df.columns if 'startup' in col.lower() and 'name' in col.lower()]
                            if startup_name_cols:
                                val = startup_row.get(startup_name_cols[0])
                                if pd.notna(val):
                                    startup_name = str(val)
                        
                        # Get founder name using helper function
                        founder_name = get_founder_full_name(startup_row, startup_name)
                        
                        # Get one liner
                        one_liner_cols = [col for col in df.columns if 'one' in col.lower() and 'liner' in col.lower()]
                        one_liner = get_field_value(startup_row, one_liner_cols, "N/A") if one_liner_cols else "N/A"
                        
                        # Get business model
                        bm_patterns = ["PH1_business_model", "Business Model", "business_model"]
                        business_model = get_field_value(startup_row, bm_patterns, "N/A")
                        
                        # Get location
                        location_patterns = ["PH1_Constitution_Location", "Constitution_Location", "Location", "location"]
                        location = get_field_value(startup_row, location_patterns, "N/A")

                        # Get stage
                        stage_patterns = ["stage", "stage_$startup"]
                        stage = get_field_value(startup_row, stage_patterns, "N/A")

                        # Get round size
                        round_size_patterns = ["PH1_Round_Size", "Round_Size", "round_size"]
                        round_size = get_field_value(startup_row, round_size_patterns, "N/A")

                        # Get stake
                        stake_patterns = ["PH1_Stake", "Stake", "stake"]
                        stake = get_field_value(startup_row, stake_patterns, "N/A")

                        # Get reference
                        reference_patterns = ["PH1_Reference", "Reference", "reference", "PH1_reference_$startups"]
                        reference = get_field_value(startup_row, reference_patterns, "N/A")

                        # Get reference details
                        reference_details_patterns = ["PH1_Reference_Details", "Reference_Details", "reference_details", "PH1_reference_other_$startups"]
                        reference_details = get_field_value(startup_row, reference_details_patterns, "N/A")

                        # Get signals
                        signals_patterns = ["Signals"]
                        signals = get_field_value(startup_row, signals_patterns, "N/A")
                        signals_list = [sign.strip() for sign in signals.split("|") if signals != "N/A"]

                        # Get red and green flags
                        red_flags = get_field_value(startup_row, ["redflags_summary"], "N/A")
                        red_flags_list = [s.strip() for s in red_flags.split("\n")]

                        green_flags = get_field_value(startup_row, ["greenflags_summary"], "N/A")
                        green_flags_list = [s.strip() for s in green_flags.split("\n")]
                        
                        # Create card with main info
                        with st.container(border=True):
                            st.markdown(f"### {startup_name}")
                            
                            # Show founder name above one liner
                            if founder_name and founder_name != "N/A":
                                st.markdown(f"**👤 {founder_name}**")
                            
                            # Show one liner if available
                            if one_liner and one_liner != "N/A":
                                st.markdown(f"*{one_liner}*")
                            
                            # Expandable details section - ALL OTHER info goes here
                            with st.expander("📊 View Full Details"):
                                
                                # Show stage
                                if (stage and stage != "N/A"):
                                    st.markdown(f"**🚀 Stage**  \n{stage}")

                                # Show business model and location
                                if (business_model and business_model != "N/A") or (location and location != "N/A"):
                                    info_col1, info_col2 = st.columns(2)
                                    with info_col1:
                                        if business_model and business_model != "N/A":
                                            st.markdown(f"**💼 Business Model**  \n{business_model}")
                                    with info_col2:
                                        if location and location != "N/A":
                                            st.markdown(f"**📍 Location**  \n{location}")
                                    st.markdown("")
                                
                                # Get financial details
                                round_size = get_field_value(startup_row, ["Round_Size", "Round Size", "round_size"], "N/A")
                                valuation_patterns = ["PH1_current_valuation", "Current_Valuation", "Valuation"]
                                current_valuation = get_field_value(startup_row, valuation_patterns, "N/A")
                                stake = get_field_value(startup_row, ["Stake_Formula", "Stake Formula", "stake_formula", "Stake"], "N/A")
                                
                                # Get deck links
                                deck_url = get_field_value(startup_row, ["deck_URL", "Deck_URL", "Deck URL"], "")
                                deck_startup = get_field_value(startup_row, ["deck_$startup", "deck_startup", "Deck"], "")
                                if isinstance(deck_startup, dict):
                                    deck_attachment_url = deck_startup["url"]
                                else:
                                    deck_attachment_url = ""
                                
                                # Show financial info
                                if (round_size and round_size != "N/A") or (current_valuation and current_valuation != "N/A") or (stake and stake != "N/A"):
                                    detail_col1, detail_col2 = st.columns(2)
                                    with detail_col1:
                                        if round_size and round_size != "N/A":
                                            st.markdown(f"**💰 Round Size**  \n{round_size}")
                                        if current_valuation and current_valuation != "N/A":
                                            st.markdown(f"**📈 Current Valuation**  \n{current_valuation}")
                                    with detail_col2:
                                        if stake and stake != "N/A":
                                            st.markdown(f"**🎯 Stake**  \n{stake}")
                                    st.markdown("")
                                
                                # Show referal info
                                if (reference and reference != "N/A") or (reference_details and referenece_details != "N/A"):
                                    col1, col2 = st.columns(2)
                                    with col1:
                                        if reference and reference != "N/A":
                                            st.markdown(f"**🔗 Reference**  \n{reference}")
                                    with col2:
                                        if reference_details and reference_details != "N/A":
                                            st.markdown(f"**🔗 Reference Details**  \n{reference_details}")
                                    st.markdown("")
                                
                                # Show signals and red flags
                                cols_signals = st.columns(2)
                                if (signals_list and signals_list != "N/A"):
                                    with cols_signals[0]:
                                        st.markdown("**Signals:**")
                                        for signal in signals_list:
                                            st.markdown(f"{signal}")
                                
                                if (red_flags_list and red_flags_list != ["N/A"]) or (green_flags_list and green_flags_list != ["N/A"]):
                                    with cols_signals[1]:
                                        st.markdown("**Red Flags:**")
                                        for red_flag in red_flags_list:
                                            st.markdown(f"{red_flag}")
                                        st.markdown("**Green Flags:**")
                                        for green_flag in green_flags_list:
                                            st.markdown(f"{green_flag}")
                                        
                                # Show alternativo de links
                                if deck_attachment_url and not deck_url:
                                    st.markdown(f'<a href="{deck_attachment_url}">📄 Deck</a>', unsafe_allow_html=True)

                                elif deck_url and not deck_attachment_url:
                                    st.markdown(f'<a href="{deck_url}">📄 Deck</a>', unsafe_allow_html=True)

                                elif deck_url and deck_attachment_url:
                                    st.markdown(
                                        f'<a href="{deck_url}">📄 Deck</a> | '
                                        f'<a href="{deck_attachment_url}">📄 Deck (Attachment)</a>',
                                        unsafe_allow_html=True
                                    )

        else:
            st.info("No startups with 'Qualified' stage found.")
    else:
        st.warning("Stage field not found in data.")
    
    st.markdown("---")
    
    # =============================================================================
    # ZOMBIE DEALS
    # =============================================================================
    
    st.write("### 🧟 Zombie Deals")
    st.caption("Startups that haven't been updated in the last 7 days. An automated email reminder will be sent to the responsible person to follow up on these deals.")
    st.write("")
    
    # Find Last Modified field
    last_modified_cols = [col for col in df.columns if 'last' in col.lower() and 'modified' in col.lower()]
    if not last_modified_cols:
        last_modified_cols = [col for col in df.columns if col in ['Last Modified', 'Last_Modified', 'LastModified', 'Modified']]
    
    if last_modified_cols:
        last_modified_field = last_modified_cols[0]
        
        # Calculate cutoff date (7 days ago)
        cutoff_date = datetime.now() - timedelta(days=7)
        
        # Filter for startups not modified in last 7 days
        zombie_records = []
        for idx, row in df.iterrows():
            last_modified = row.get(last_modified_field)
            if pd.notna(last_modified):
                try:
                    # Convert to datetime if it's a string
                    if isinstance(last_modified, str):
                        modified_date = pd.to_datetime(last_modified)
                    else:
                        modified_date = last_modified
                    
                    # Check if last modified is older than 7 days
                    if modified_date < cutoff_date:
                        zombie_records.append(row)
                except:
                    pass
        
        if zombie_records:
            zombie_df = pd.DataFrame(zombie_records)
            st.write(f"**Total:** {len(zombie_df)} startups")
            st.write("")
            
            # Display in a 2-column grid with cards
            num_cols = 2
            rows = [zombie_df.iloc[i:i+num_cols] for i in range(0, len(zombie_df), num_cols)]
            
            for row_idx, row_data in enumerate(rows):
                cols = st.columns(num_cols)
                for col_idx, (_, startup_row) in enumerate(row_data.iterrows()):
                    with cols[col_idx]:
                        # Get startup name - use "Startup name" field specifically
                        startup_name = "Unknown Startup"
                        
                        # Try exact match first: "Startup name"
                        if 'Startup name' in df.columns:
                            val = startup_row.get('Startup name')
                            if pd.notna(val):
                                startup_name = str(val)
                        # Try variations
                        elif 'Startup_name' in df.columns:
                            val = startup_row.get('Startup_name')
                            if pd.notna(val):
                                startup_name = str(val)
                        elif 'startup_name' in df.columns:
                            val = startup_row.get('startup_name')
                            if pd.notna(val):
                                startup_name = str(val)
                        else:
                            # Fallback: find any column with "startup" and "name"
                            startup_name_cols = [col for col in df.columns if 'startup' in col.lower() and 'name' in col.lower()]
                            if startup_name_cols:
                                val = startup_row.get(startup_name_cols[0])
                                if pd.notna(val):
                                    startup_name = str(val)
                        
                        # Get founder name using helper function
                        founder_name = get_founder_full_name(startup_row, startup_name)
                        
                        # Get one liner
                        one_liner_cols = [col for col in df.columns if 'one' in col.lower() and 'liner' in col.lower()]
                        one_liner = get_field_value(startup_row, one_liner_cols, "N/A") if one_liner_cols else "N/A"
                        
                        # Get last modified date for display
                        last_modified = startup_row.get(last_modified_field)
                        last_modified_str = "N/A"
                        if pd.notna(last_modified):
                            try:
                                if isinstance(last_modified, str):
                                    modified_date = pd.to_datetime(last_modified)
                                else:
                                    modified_date = last_modified
                                last_modified_str = modified_date.strftime("%d/%m/%Y")
                            except:
                                pass
                        
                        # Get stage
                        stage_patterns = ["Stage", "stage"]
                        stage = get_field_value(startup_row, stage_patterns, "N/A")
                        
                        # Get contact stage
                        contact_stage_patterns = ["Contact_Stage", "Contact Stage", "contact_stage"]
                        contact_stage = get_field_value(startup_row, contact_stage_patterns, "N/A")
                        
                        # Create card with main info
                        with st.container(border=True):
                            st.markdown(f"### {startup_name}")
                            
                            # Show founder name above one liner
                            if founder_name and founder_name != "N/A":
                                st.markdown(f"**👤 {founder_name}**")
                            
                            # Show one liner if available
                            if one_liner and one_liner != "N/A":
                                st.markdown(f"*{one_liner}*")
                            
                            # Show last modified date prominently
                            st.markdown(f"**⏰ Last Modified:** {last_modified_str}")
                            
                            # Expandable details section - ALL OTHER info goes here
                            with st.expander("📊 View Full Details"):
                                
                                # Show stage and contact stage
                                if (stage and stage != "N/A") or (contact_stage and contact_stage != "N/A"):
                                    info_col1, info_col2 = st.columns(2)
                                    with info_col1:
                                        if stage and stage != "N/A":
                                            st.markdown(f"**📊 Stage**  \n{stage}")
                                    with info_col2:
                                        if contact_stage and contact_stage != "N/A":
                                            st.markdown(f"**📞 Contact Stage**  \n{contact_stage}")
                                    st.markdown("")
                                
                                # Get business model and location
                                bm_patterns = ["PH1_business_model", "Business Model", "business_model"]
                                business_model = get_field_value(startup_row, bm_patterns, "N/A")
                                location_patterns = ["PH1_Constitution_Location", "Constitution_Location", "Location", "location"]
                                location = get_field_value(startup_row, location_patterns, "N/A")
                                
                                if (business_model and business_model != "N/A") or (location and location != "N/A"):
                                    detail_col1, detail_col2 = st.columns(2)
                                    with detail_col1:
                                        if business_model and business_model != "N/A":
                                            st.markdown(f"**💼 Business Model**  \n{business_model}")
                                    with detail_col2:
                                        if location and location != "N/A":
                                            st.markdown(f"**📍 Location**  \n{location}")
                                    st.markdown("")
                                
                                # Get deck links
                                deck_url = get_field_value(startup_row, ["deck_URL", "Deck_URL", "Deck URL"], "")
                                deck_startup = get_field_value(startup_row, ["deck_$startup", "deck_startup", "Deck"], "")
                                
                                # Show deck links
                                deck_links = []
                                if deck_url and deck_url not in ["N/A", "", " "]:
                                    deck_links.append(f"[Deck URL]({deck_url})")
                                if deck_startup and deck_startup not in ["N/A", "", " "]:
                                    deck_links.append(f"[Deck Attachment]({deck_startup})")
                                
                                if deck_links:
                                    st.markdown(f"**📄 Deck:** {' | '.join(deck_links)}")
        else:
            st.info("No zombie deals found. All startups have been updated recently!")
    else:
        st.warning("Last Modified field not found in data.")

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

