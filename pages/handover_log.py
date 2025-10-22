"""Handover Log page - Manage shift handover entries."""
import streamlit as st
from datetime import date
from database.db_manager import DatabaseManager
from utils.helpers import show_success_message, show_error_message, validate_required_field


def show(db: DatabaseManager):
    """Display handover log page.
    
    Args:
        db: Database manager instance
    """
    st.markdown('<h1 class="main-header">📝 Handover Log</h1>', unsafe_allow_html=True)
    st.markdown("Manage shift handover details and notes")
    
    # Tabs for different actions
    tab1, tab2 = st.tabs(["📋 View Logs", "➕ Add New Log"])
    
    with tab1:
        st.subheader("All Handover Logs")
        
        # Get all logs
        logs = db.get_all_handover_logs()
        
        if not logs.empty:
            # Search/filter
            search = st.text_input("🔍 Search by trader name or notes", "")
            
            if search:
                logs = logs[
                    logs['trader_name'].str.contains(search, case=False, na=False) |
                    logs['notes'].str.contains(search, case=False, na=False)
                ]
            
            st.markdown(f"**Total Logs:** {len(logs)}")
            
            # Display logs
            for idx, log in logs.iterrows():
                with st.expander(f"👤 {log['trader_name']} - {log['shift_date']}"):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.markdown(f"**Shift Date:** {log['shift_date']}")
                        st.markdown(f"**Notes:**")
                        st.text_area("", value=log['notes'], height=100, key=f"view_{log['id']}", disabled=True)
                        st.caption(f"Created: {log['created_at']} | Updated: {log['updated_at']}")
                    
                    with col2:
                        st.markdown("**Actions:**")
                        
                        # Edit button
                        if st.button("✏️ Edit", key=f"edit_btn_{log['id']}", use_container_width=True):
                            st.session_state[f'edit_log_{log["id"]}'] = True
                        
                        # Delete button
                        if st.button("🗑️ Delete", key=f"del_btn_{log['id']}", type="secondary", use_container_width=True):
                            st.session_state[f'confirm_delete_{log["id"]}'] = True
                        
                        # Confirm delete
                        if st.session_state.get(f'confirm_delete_{log["id"]}', False):
                            st.warning("Are you sure?")
                            if st.button("✅ Yes, Delete", key=f"confirm_del_{log['id']}", use_container_width=True):
                                db.delete_handover_log(log['id'])
                                show_success_message("Handover log deleted successfully!")
                                st.session_state[f'confirm_delete_{log["id"]}'] = False
                                st.rerun()
                            if st.button("❌ Cancel", key=f"cancel_del_{log['id']}", use_container_width=True):
                                st.session_state[f'confirm_delete_{log["id"]}'] = False
                                st.rerun()
                    
                    # Edit form
                    if st.session_state.get(f'edit_log_{log["id"]}', False):
                        st.markdown("---")
                        st.markdown("### Edit Log")
                        
                        with st.form(key=f"edit_form_{log['id']}"):
                            edit_trader = st.text_input("Trader Name *", value=log['trader_name'])
                            edit_date = st.date_input("Shift Date *", value=date.fromisoformat(log['shift_date']))
                            edit_notes = st.text_area("Notes", value=log['notes'], height=150)
                            
                            col_submit, col_cancel = st.columns(2)
                            
                            with col_submit:
                                submit = st.form_submit_button("💾 Save Changes", use_container_width=True)
                            
                            with col_cancel:
                                cancel = st.form_submit_button("❌ Cancel", use_container_width=True)
                            
                            if submit:
                                if validate_required_field(edit_trader, "Trader Name"):
                                    db.update_handover_log(
                                        log['id'],
                                        edit_trader,
                                        str(edit_date),
                                        edit_notes
                                    )
                                    show_success_message("Handover log updated successfully!")
                                    st.session_state[f'edit_log_{log["id"]}'] = False
                                    st.rerun()
                            
                            if cancel:
                                st.session_state[f'edit_log_{log["id"]}'] = False
                                st.rerun()
        else:
            st.info("No handover logs found. Create your first log using the 'Add New Log' tab.")
    
    with tab2:
        st.subheader("Create New Handover Log")
        
        with st.form(key="new_log_form", clear_on_submit=True):
            trader_name = st.text_input("Trader Name *", placeholder="Enter trader name")
            shift_date = st.date_input("Shift Date *", value=date.today())
            notes = st.text_area(
                "Notes",
                placeholder="Enter shift handover notes, key events, and important information...",
                height=200
            )
            
            submit = st.form_submit_button("💾 Create Handover Log", use_container_width=True)
            
            if submit:
                if validate_required_field(trader_name, "Trader Name"):
                    log_id = db.create_handover_log(
                        trader_name,
                        str(shift_date),
                        notes
                    )
                    show_success_message(f"Handover log created successfully! (ID: {log_id})")
                    st.rerun()
