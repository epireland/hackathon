"""Main Streamlit application for Power & Gas Trader Shift Handover."""
import streamlit as st
from datetime import datetime
from src.backend.database.db_manager import DatabaseManager
from src.frontend.pages import (
    dashboard,
    handover_log,
    positions,
    operations,
    issues_alerts,
    market,
    comments
)
from src.utils.helpers import get_current_shift_time


# Page configuration
st.set_page_config(
    page_title="Shift Handover System",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database
@st.cache_resource
def init_db():
    """Initialize database connection."""
    return DatabaseManager()

db = init_db()

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar navigation
with st.sidebar:
    st.markdown("# ⚡ Shift Handover")
    st.markdown(f"**Current Time:** {get_current_shift_time()}")
    st.markdown("---")
    
    page = st.radio(
        "Navigation",
        [
            "📊 Dashboard",
            "📝 Handover Log",
            "💼 Trading Positions",
            "🏭 Operations",
            "🚨 Issues & Alerts",
            "📈 Market Activity",
            "💬 Comments"
        ],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("### About")
    st.info("Power & Gas Trader Shift Handover System - Track and manage shift information efficiently.")

# Main content area
if page == "📊 Dashboard":
    dashboard.show(db)
elif page == "📝 Handover Log":
    handover_log.show(db)
elif page == "💼 Trading Positions":
    positions.show(db)
elif page == "🏭 Operations":
    operations.show(db)
elif page == "🚨 Issues & Alerts":
    issues_alerts.show(db)
elif page == "📈 Market Activity":
    market.show(db)
elif page == "💬 Comments":
    comments.show(db)
