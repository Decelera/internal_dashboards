# Joint Dashboard

A hierarchical Streamlit dashboard for multi-location Investment and Program analytics with custom navigation.

## Structure

### Navigation Hierarchy

The sidebar displays a custom hierarchical navigation structure for two locations:

```
Mexico (Title 1 - Display only)
  └── 2025 (Title 2 - Display only)
      ├── Investment (Title 4 - Display only)
      │   ├── General (Title 5 - Clickable)
      │   └── Per Startup (Title 5 - Clickable)
      └── Program (Title 4 - Display only)
          ├── General (Title 5 - Clickable)
          └── Agenda (Title 5 - Clickable)

Menorca (Title 1 - Display only)
  └── 2025 (Title 2 - Display only)
      ├── Investment (Title 4 - Display only)
      │   ├── General (Title 5 - Clickable)
      │   └── Per Startup (Title 5 - Clickable)
      └── Program (Title 4 - Display only)
          ├── General (Title 5 - Clickable)
          └── Agenda (Title 5 - Clickable)
```

## Pages

### Home
- **Home** - Minimalistic landing page with links to all pages and section explanations

### Mexico
- **Mexico - Investment - General** - General investment metrics and analytics (placeholder)
- **Mexico - Investment - Per Startup** - Individual startup investment details (placeholder)
- **Mexico - Program - General** - General program metrics and analytics (placeholder)
- **Mexico - Program - Agenda** - Program schedule and agenda (placeholder)

### Menorca
- **Menorca - Investment - General** - General investment metrics and analytics (placeholder)
- **Menorca - Investment - Per Startup** - Individual startup investment details (placeholder)
- **Menorca - Program - General** - General program metrics and analytics (placeholder)
- **Menorca - Program - Agenda** - Program schedule and agenda (placeholder)

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

### Logo & Favicon Placement

**To add your Decelera logo:**

1. Save your logo file as: `.streamlit/static/decelera_logo.png`
2. Recommended size: 300-500px width
3. Supported formats: PNG (recommended), JPG, SVG

**Exact path:** `/.streamlit/static/decelera_logo.png`

The logo will appear at the top of the landing page next to the title.

**To add your favicon (browser tab icon):**

1. Save your favicon file as: `.streamlit/static/favicon.png`
2. Recommended size: 32x32px or 64x64px
3. Format: PNG (recommended for transparency)

**Exact path:** `.streamlit/static/favicon.png`

The favicon will appear in the browser tab for all pages of the dashboard.

### Secrets Management

The dashboard uses Streamlit's secrets management for API keys and sensitive information:

1. Add your secrets to `.streamlit/secrets.toml`
2. This file is already in `.gitignore` and will never be committed
3. Access secrets in your code using `st.secrets["key_name"]`

Example usage:
```python
import streamlit as st

# Access a simple key
api_key = st.secrets["api_keys"]["service_1"]

# Access nested keys
db_password = st.secrets["database"]["password"]
```

## Running the Dashboard

```bash
cd "/Joint Dashboard"
streamlit run Home.py
```

The dashboard will open in your default browser at `http://localhost:8501`

## Features

- **Custom Hierarchical Navigation**: The sidebar shows the full navigation structure with non-clickable parent levels
- **Consistent Navigation**: Same navigation structure across all pages
- **Breadcrumb Navigation**: Each page shows its location in the hierarchy
- **Home Button**: Easy return to landing page from any subpage
- **Brand Colors**: 
  - Main color: #62CDEB (RGB: 98, 205, 235)
  - Secondary color: #ACAFB9 (RGB: 172, 175, 185)
- **Visual Hierarchy**: Interactive cards showing the structure with hover effects
- **Responsive Design**: Works on different screen sizes

## Development

### File Structure

```
Joint Dashboard/
├── .streamlit/
│   ├── config.toml                      # Streamlit configuration (hides default navigation)
│   └── secrets.toml                     # API keys and secrets (NOT in git)
├── .gitignore                            # Git ignore file (includes secrets.toml)
├── Home.py                               # Minimalistic landing page
├── pages/
│   ├── Menorca_Investment_General.py    # Menorca - Investment - General
│   ├── Menorca_Investment_Per_Startup.py # Menorca - Investment - Per Startup
│   ├── Menorca_Program_Agenda.py        # Menorca - Program - Agenda
│   ├── Menorca_Program_General.py       # Menorca - Program - General
│   ├── Mexico_Investment_General.py     # Mexico - Investment - General
│   ├── Mexico_Investment_Per_Startup.py # Mexico - Investment - Per Startup
│   ├── Mexico_Program_Agenda.py         # Mexico - Program - Agenda
│   └── Mexico_Program_General.py        # Mexico - Program - General
├── requirements.txt
└── README.md
```

### Adding Your Code

The placeholder pages are ready for your code. Simply edit the respective files:

**Mexico:**
- `pages/Mexico_Investment_General.py` - Mexico investment general analytics
- `pages/Mexico_Investment_Per_Startup.py` - Mexico per-startup analytics
- `pages/Mexico_Program_General.py` - Mexico program general analytics
- `pages/Mexico_Program_Agenda.py` - Mexico program agenda content

**Menorca:**
- `pages/Menorca_Investment_General.py` - Menorca investment general analytics
- `pages/Menorca_Investment_Per_Startup.py` - Menorca per-startup analytics
- `pages/Menorca_Program_General.py` - Menorca program general analytics
- `pages/Menorca_Program_Agenda.py` - Menorca program agenda content

Each page already includes:
- The custom hierarchical navigation in the sidebar
- Breadcrumb navigation
- Page header and structure
- Placeholder sections for your content

### Customizing Navigation

The navigation code is at the top of each file in the `with st.sidebar:` block. To modify the hierarchy, update this section consistently across all files.

