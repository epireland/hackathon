"""Dashboard page - Main overview of shift handover system."""
import streamlit as st
import pandas as pd
from src.backend.database.db_manager import DatabaseManager
from src.utils.helpers import get_status_emoji, get_priority_emoji


def show(db: DatabaseManager):
    """Display dashboard page.
    
    Args:
        db: Database manager instance
    """
    st.markdown('<h1 class="main-header">📊 Dashboard</h1>', unsafe_allow_html=True)
    st.markdown("Welcome to the Shift Handover System - Your at-a-glance overview")
    
    # Summary metrics in columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        critical_count = db.get_critical_notifications_count()
        st.metric(
            label="🔴 Critical Alerts",
            value=critical_count,
            delta=None,
            help="Unresolved critical notifications"
        )
    
    with col2:
        it_issues_count = db.get_open_it_issues_count()
        st.metric(
            label="🟡 Open IT Issues",
            value=it_issues_count,
            delta=None,
            help="IT issues that are open or in progress"
        )
    
    with col3:
        recent_logs = db.get_recent_handover_logs(limit=10)
        st.metric(
            label="📝 Recent Handovers",
            value=len(recent_logs),
            delta=None,
            help="Handover logs from last 10 entries"
        )
    
    with col4:
        # Get latest positions count
        power_pos = db.get_latest_power_position()
        gas_pos = db.get_latest_gas_position()
        positions_count = (1 if power_pos else 0) + (1 if gas_pos else 0)
        st.metric(
            label="💼 Active Positions",
            value=positions_count,
            delta=None,
            help="Current trading positions tracked"
        )
    
    st.markdown("---")
    
    # Main content area with two columns
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.subheader("📋 Recent Handover Logs")
        
        recent_logs = db.get_recent_handover_logs(limit=5)
        
        if not recent_logs.empty:
            # Display as cards
            for _, log in recent_logs.iterrows():
                with st.container():
                    st.markdown(f"""
                    <div style="border: 1px solid #1f77b4; border-radius: 5px; padding: 15px; margin-bottom: 10px; background-color: #f0f8ff;">
                        <h4 style="margin: 0; color: #1f77b4;">👤 {log['trader_name']}</h4>
                        <p style="margin: 5px 0; color: #666;">📅 {log['shift_date']}</p>
                        <p style="margin: 5px 0;">{log['notes'][:100]}{'...' if len(str(log['notes'])) > 100 else ''}</p>
                        <small style="color: #999;">Created: {log['created_at']}</small>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("No handover logs available. Create your first log in the Handover Log section.")
    
    with col_right:
        # Critical Notifications
        st.subheader("🚨 Critical Alerts")
        
        unresolved = db.get_unresolved_notifications()
        
        if not unresolved.empty:
            critical = unresolved[unresolved['priority'] == 'critical'].head(3)
            
            if not critical.empty:
                for _, notif in critical.iterrows():
                    st.warning(f"""
                    **{get_priority_emoji(notif['priority'])} {notif['title']}**  
                    {notif['message'][:80]}{'...' if len(str(notif['message'])) > 80 else ''}  
                    *{notif['shift_date']}*
                    """)
            else:
                st.success("✅ No critical alerts at this time")
        else:
            st.success("✅ No active alerts")
        
        st.markdown("---")
        
        # IT Issues Summary
        st.subheader("💻 IT Issues")
        
        it_issues = db.get_all_it_issues()
        
        if not it_issues.empty:
            open_issues = it_issues[it_issues['status'].isin(['open', 'in_progress'])].head(3)
            
            if not open_issues.empty:
                for _, issue in open_issues.iterrows():
                    status_emoji = get_status_emoji(issue['status'])
                    st.info(f"""
                    **{status_emoji} {issue['title']}**  
                    Status: {issue['status'].replace('_', ' ').title()}  
                    *{issue['shift_date']}*
                    """)
            else:
                st.success("✅ All IT issues resolved")
        else:
            st.success("✅ No IT issues reported")
    
    st.markdown("---")
    
    # Latest Positions Summary
    st.subheader("💼 Latest Trading Positions")
    
    pos_col1, pos_col2 = st.columns(2)
    
    with pos_col1:
        st.markdown("#### ⚡ Power Position")
        power_pos = db.get_latest_power_position()
        
        if power_pos:
            st.success(f"""
            **Date:** {power_pos['shift_date']}  
            **Position:** {power_pos['position_details'][:100]}{'...' if len(str(power_pos['position_details'])) > 100 else ''}  
            **Portfolio Status:** {power_pos['portfolio_status'] if power_pos['portfolio_status'] else 'N/A'}
            """)
        else:
            st.info("No power position data available")
    
    with pos_col2:
        st.markdown("#### 🔥 Gas Position")
        gas_pos = db.get_latest_gas_position()
        
        if gas_pos:
            st.success(f"""
            **Date:** {gas_pos['shift_date']}  
            **Position:** {gas_pos['position_details'][:100]}{'...' if len(str(gas_pos['position_details'])) > 100 else ''}  
            **Portfolio Status:** {gas_pos['portfolio_status'] if gas_pos['portfolio_status'] else 'N/A'}
            """)
        else:
            st.info("No gas position data available")
    
    # Quick actions
    st.markdown("---")
    st.subheader("⚡ Quick Actions")
    
    action_col1, action_col2, action_col3 = st.columns(3)
    
    with action_col1:
        if st.button("➕ New Handover Log", use_container_width=True):
            st.info("Navigate to '📝 Handover Log' to create a new entry")
    
    with action_col2:
        if st.button("🚨 Add Alert", use_container_width=True):
            st.info("Navigate to '🚨 Issues & Alerts' to add a notification")
    
    with action_col3:
        if st.button("📈 Update Positions", use_container_width=True):
            st.info("Navigate to '💼 Trading Positions' to update positions")
