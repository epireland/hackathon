"""Market Activity page - Track competitor activities."""
import streamlit as st
from datetime import date
from database.db_manager import DatabaseManager
from utils.helpers import show_success_message, validate_required_field


def show(db: DatabaseManager):
    """Display market activity page.
    
    Args:
        db: Database manager instance
    """
    st.markdown('<h1 class="main-header">📈 Market Activity</h1>', unsafe_allow_html=True)
    st.markdown("Monitor and log competitor activities in the market")
    
    # Tabs for viewing and adding
    tab1, tab2 = st.tabs(["📋 View Activities", "➕ Add Activity"])
    
    with tab1:
        st.subheader("Competitor Activity Log")
        
        # Search functionality
        search = st.text_input("🔍 Search by competitor name or activity details", "")
        
        activities = db.get_all_competitor_activity()
        
        if not activities.empty:
            # Apply search filter
            if search:
                activities = activities[
                    activities['competitor_name'].str.contains(search, case=False, na=False) |
                    activities['activity_details'].str.contains(search, case=False, na=False)
                ]
            
            st.markdown(f"**Total Activities:** {len(activities)}")
            
            for idx, activity in activities.iterrows():
                with st.expander(f"🏢 {activity['competitor_name']} - {activity['shift_date']}"):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.markdown(f"**Competitor:** {activity['competitor_name']}")
                        st.markdown(f"**Shift Date:** {activity['shift_date']}")
                        st.markdown(f"**Activity Details:**")
                        st.text_area("", value=activity['activity_details'], height=150, key=f"view_activity_{activity['id']}", disabled=True)
                        st.caption(f"Created: {activity['created_at']} | Updated: {activity['updated_at']}")
                    
                    with col2:
                        st.markdown("**Actions:**")
                        
                        if st.button("✏️ Edit", key=f"edit_activity_{activity['id']}", use_container_width=True):
                            st.session_state[f'edit_activity_{activity["id"]}'] = True
                        
                        if st.button("🗑️ Delete", key=f"del_activity_{activity['id']}", use_container_width=True):
                            st.session_state[f'confirm_delete_activity_{activity["id"]}'] = True
                        
                        if st.session_state.get(f'confirm_delete_activity_{activity["id"]}', False):
                            st.warning("Are you sure?")
                            if st.button("✅ Yes, Delete", key=f"confirm_del_activity_{activity['id']}", use_container_width=True):
                                db.delete_competitor_activity(activity['id'])
                                show_success_message("Competitor activity deleted!")
                                st.session_state[f'confirm_delete_activity_{activity["id"]}'] = False
                                st.rerun()
                            if st.button("❌ Cancel", key=f"cancel_del_activity_{activity['id']}", use_container_width=True):
                                st.session_state[f'confirm_delete_activity_{activity["id"]}'] = False
                                st.rerun()
                    
                    # Edit form
                    if st.session_state.get(f'edit_activity_{activity["id"]}', False):
                        st.markdown("---")
                        st.markdown("### Edit Activity")
                        
                        with st.form(key=f"edit_activity_form_{activity['id']}"):
                            edit_competitor = st.text_input("Competitor Name *", value=activity['competitor_name'])
                            edit_date = st.date_input("Shift Date *", value=date.fromisoformat(activity['shift_date']))
                            edit_details = st.text_area("Activity Details *", value=activity['activity_details'], height=150)
                            
                            col_submit, col_cancel = st.columns(2)
                            
                            with col_submit:
                                submit = st.form_submit_button("💾 Save Changes", use_container_width=True)
                            
                            with col_cancel:
                                cancel = st.form_submit_button("❌ Cancel", use_container_width=True)
                            
                            if submit:
                                if validate_required_field(edit_competitor, "Competitor Name") and validate_required_field(edit_details, "Activity Details"):
                                    db.update_competitor_activity(
                                        activity['id'],
                                        edit_competitor,
                                        edit_details,
                                        str(edit_date)
                                    )
                                    show_success_message("Competitor activity updated!")
                                    st.session_state[f'edit_activity_{activity["id"]}'] = False
                                    st.rerun()
                            
                            if cancel:
                                st.session_state[f'edit_activity_{activity["id"]}'] = False
                                st.rerun()
        else:
            st.info("No competitor activities recorded. Add your first activity using the 'Add Activity' tab.")
    
    with tab2:
        st.subheader("Log New Competitor Activity")
        
        with st.form(key="new_activity_form", clear_on_submit=True):
            competitor_name = st.text_input(
                "Competitor Name *",
                placeholder="Enter competitor or company name"
            )
            shift_date = st.date_input("Shift Date *", value=date.today())
            activity_details = st.text_area(
                "Activity Details *",
                placeholder="Describe the competitor's market activity, trading patterns, or notable actions...",
                height=200
            )
            
            submit = st.form_submit_button("💾 Log Activity", use_container_width=True)
            
            if submit:
                if validate_required_field(competitor_name, "Competitor Name") and validate_required_field(activity_details, "Activity Details"):
                    activity_id = db.create_competitor_activity(
                        competitor_name,
                        activity_details,
                        str(shift_date)
                    )
                    show_success_message(f"Competitor activity logged successfully! (ID: {activity_id})")
                    st.rerun()
