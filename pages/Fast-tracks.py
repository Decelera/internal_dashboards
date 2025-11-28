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
    # Try generic fields first (most common)
    name = row.get("PH1_founder_name", "")
    surname = row.get("PH1_founder_surname", "")
    
    if pd.notna(name) or pd.notna(surname):
        first = str(name) if pd.notna(name) else ""
        last = str(surname) if pd.notna(surname) else ""
        full_name = f"{first} {last}".strip()
        if full_name:
            return full_name
    
    # Try startup-specific fields as fallback
    name_field = f"PH1_founder_name_{startup_name}"
    surname_field = f"PH1_founder_surname_{startup_name}"
    
    name = row.get(name_field, "")
    surname = row.get(surname_field, "")
    
    if pd.notna(name) or pd.notna(surname):
        first = str(name) if pd.notna(name) else ""
        last = str(surname) if pd.notna(surname) else ""
        full_name = f"{first} {last}".strip()
        if full_name:
            return full_name
    
    return "N/A"

def get_field_value(row, field_patterns, default="N/A"):
    """Try multiple field patterns and return the first non-empty value"""
    for pattern in field_patterns:
        if pattern in row and pd.notna(row[pattern]):
            value = row[pattern]
            # Handle list values (e.g., ['Spain'] should become 'Spain')
            if isinstance(value, list):
                if len(value) > 0:
                    return str(value[0])
                else:
                    continue
            # Handle regular values
            value_str = str(value).strip()
            if value_str and value_str != 'nan':
                return value_str
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
    current_week_index = None  # Track which row is the current week
    
    for i in range(-2, 5):  # -2 (2 weeks ago) to 4 (4 weeks ahead)
        week_start = current_week_start + timedelta(weeks=i)
        week_end = week_start + timedelta(days=6)  # Sunday
        
        # Calculate week number
        week_num = week_start.isocalendar()[1]
        
        # Mark current week (when i == 0)
        if i == 0:
            current_week_index = len(weeks_data)
        
        new_deals = 0
        not_contacted = 0
        no_response = 0
        videocall_done = 0
        videocall_pending = 0
        pending_info = 0
        
        if date_sourced_cols and contact_stage_cols:
            date_col = date_sourced_cols[0]
            stage_col = contact_stage_cols[0]
            
            # Look for Date_First_Contact field (when the contact/call happened)
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
                                    if "not contacted" in stage_lower:
                                        not_contacted += 1
                                    elif "no response" in stage_lower:
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
    
    # Style the dataframe to highlight current week
    def highlight_current_week(row):
        """Apply highlighting to the current week row"""
        if row.name == current_week_index:
            return ['background-color: #62CDEB; color: white; font-weight: bold'] * len(row)
        elif row.name == len(weeks_df) - 1:  # Totals row
            return ['background-color: #1e3a5f; color: white; font-weight: bold'] * len(row)
        else:
            return [''] * len(row)
    
    # Apply styling
    styled_df = weeks_df.style.apply(highlight_current_week, axis=1)
    
    # Display the styled table
    st.dataframe(
        styled_df,
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
                    if current_week_start.date() <= sourced_date.date() <= (current_week_start + timedelta(days=6)).date():
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
                st.write(f"**📍 Current Week:** {current_week_start.strftime('%d/%m/%Y')} - {(current_week_start + timedelta(days=6)).strftime('%d/%m/%Y')}")
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
    # QUALIFIED STARTUPS TABLE
    # =============================================================================
    
    st.write("### Qualified Startups")
    
    # Find stage field - be more specific
    stage_field_cols = [col for col in df.columns if col == 'Stage' or col == 'stage']
    if not stage_field_cols:
        # Fallback: any field containing 'stage' but not other words
        stage_field_cols = [col for col in df.columns if 'stage' in col.lower() and 'contact' not in col.lower()]
    
    if stage_field_cols:
        stage_field = stage_field_cols[0]
        
        # Debug: Show what stage values exist
        unique_stages = df[stage_field].dropna().unique().tolist()
        st.write(f"**Debug - Stage field used:** `{stage_field}`")
        st.write(f"**Debug - Unique stage values found:** {unique_stages}")
        
        # Filter for "Qualified" stage - try multiple matching strategies
        # First try exact match
        qualified_df = df[df[stage_field].astype(str).str.strip().str.lower() == 'qualified']
        
        # If empty, try contains
        if qualified_df.empty:
            qualified_df = df[df[stage_field].astype(str).str.lower().str.contains('qualified', na=False)]
        
        if not qualified_df.empty:
            # Get startup name field
            startup_name_cols = [col for col in df.columns if 'startup' in col.lower() and 'name' in col.lower()]
            if not startup_name_cols:
                startup_name_cols = [col for col in df.columns if col in ['Name', 'Startup', 'Company']]
            
            # Build table data
            qualified_table_data = []
            
            for idx, row in qualified_df.iterrows():
                # Get startup name
                startup_name = get_field_value(row, startup_name_cols, "Unknown Startup") if startup_name_cols else "Unknown Startup"
                
                # Get founder name
                founder_first = row.get(f"PH1_founder_name_{startup_name}", "")
                founder_last = row.get(f"PH1_founder_surname_{startup_name}", "")
                
                if pd.notna(founder_first) or pd.notna(founder_last):
                    first = str(founder_first) if pd.notna(founder_first) else ""
                    last = str(founder_last) if pd.notna(founder_last) else ""
                    founder_name = f"{first} {last}".strip()
                    if not founder_name:
                        founder_name = "N/A"
                else:
                    founder_name = "N/A"
                
                # Get one liner
                one_liner_cols = [col for col in df.columns if 'one' in col.lower() and 'liner' in col.lower()]
                if not one_liner_cols:
                    one_liner_cols = [col for col in df.columns if col in ['One liner', 'One_liner', 'OneLiner', 'Tagline']]
                one_liner = get_field_value(row, one_liner_cols, "N/A") if one_liner_cols else "N/A"
                
                # Get business model
                bm_patterns = [f"PH1_business_model_{startup_name}", "PH1_business_model", "Business Model", "business_model"]
                business_model = get_field_value(row, bm_patterns, "N/A")
                
                # Get location
                location_patterns = ["PH1_Constitution_Location", "Constitution_Location", "Location", "location"]
                location = get_field_value(row, location_patterns, "N/A")
                
                # Get round size
                round_size = get_field_value(row, ["Round_Size", "Round Size", "round_size"], "N/A")
                
                # Get valuation
                valuation_patterns = [f"PH1_current_valuation_{startup_name}", "PH1_current_valuation", "Current_Valuation", "Valuation"]
                current_valuation = get_field_value(row, valuation_patterns, "N/A")
                
                # Get stake
                stake = get_field_value(row, ["Stake_Formula", "Stake Formula", "stake_formula", "Stake"], "N/A")
                
                qualified_table_data.append({
                    "Startup": startup_name,
                    "Founder": founder_name,
                    "One Liner": one_liner,
                    "Business Model": business_model,
                    "Location": location,
                    "Round Size": round_size,
                    "Valuation": current_valuation,
                    "Stake": stake
                })
            
            # Create and display DataFrame
            qualified_table_df = pd.DataFrame(qualified_table_data)
            
            st.write(f"**Total Qualified Startups:** {len(qualified_table_df)}")
            st.dataframe(
                qualified_table_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Startup": st.column_config.TextColumn("Startup", width="medium"),
                    "Founder": st.column_config.TextColumn("Founder", width="medium"),
                    "One Liner": st.column_config.TextColumn("One Liner", width="large"),
                    "Business Model": st.column_config.TextColumn("Business Model", width="medium"),
                    "Location": st.column_config.TextColumn("Location", width="small"),
                    "Round Size": st.column_config.TextColumn("Round Size", width="small"),
                    "Valuation": st.column_config.TextColumn("Valuation", width="small"),
                    "Stake": st.column_config.TextColumn("Stake", width="small"),
                }
            )
        else:
            st.info("No startups with 'Qualified' stage found.")
    else:
        st.warning("Stage field not found in data.")

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

