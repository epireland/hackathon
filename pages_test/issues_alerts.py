"""Issues & Alerts page - Manage notifications and IT issues."""
import streamlit as st
from datetime import date
from database.db_manager import DatabaseManager
from utils.helpers import show_success_message, validate_required_field, get_priority_emoji, get_status_emoji


def show(db: DatabaseManager):
    """Display issues and alerts page.
    
    Args:
        db: Database manager instance
    """
    st.markdown('<h1 class="main-header">🚨 Issues & Alerts</h1>', unsafe_allow_html=True)
    st.markdown("Monitor notifications and track IT issues")
    
    st.markdown("---")
    
    # Notifications Section
    with st.expander("🔔 Notifications", expanded=True):
        notif_tab1, notif_tab2 = st.tabs(["📋 View Notifications", "➕ Add Notification"])
        
        with notif_tab1:
            # Filter options
            col_filter1, col_filter2 = st.columns(2)
            
            with col_filter1:
                show_resolved = st.checkbox("Show Resolved", value=False)
            
            with col_filter2:
                priority_filter = st.multiselect(
                    "Filter by Priority",
                    options=['critical', 'high', 'medium', 'low'],
                    default=['critical', 'high', 'medium', 'low']
                )
            
            notifications = db.get_all_notifications()
            
            if not notifications.empty:
                # Apply filters
                if not show_resolved:
                    notifications = notifications[notifications['is_resolved'] == 0]
                
                if priority_filter:
                    notifications = notifications[notifications['priority'].isin(priority_filter)]
                
                st.markdown(f"**Total Notifications:** {len(notifications)}")
                
                for idx, notif in notifications.iterrows():
                    priority_emoji = get_priority_emoji(notif['priority'])
                    resolved_text = "✅ RESOLVED" if notif['is_resolved'] else "🔴 ACTIVE"
                    
                    with st.container():
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            st.markdown(f"### {priority_emoji} {notif['title']} - {resolved_text}")
                            st.markdown(f"**Priority:** {notif['priority'].upper()}")
                            st.markdown(f"**Message:** {notif['message']}")
                            st.markdown(f"**Shift Date:** {notif['shift_date']}")
                            st.caption(f"Updated: {notif['updated_at']}")
                        
                        with col2:
                            st.markdown("**Actions:**")
                            
                            if not notif['is_resolved']:
                                if st.button("✅ Resolve", key=f"resolve_notif_{notif['id']}", use_container_width=True):
                                    db.resolve_notification(notif['id'])
                                    show_success_message("Notification resolved!")
                                    st.rerun()
                            
                            if st.button("✏️ Edit", key=f"edit_notif_{notif['id']}", use_container_width=True):
                                st.session_state[f'edit_notif_{notif["id"]}'] = True
                            
                            if st.button("🗑️ Delete", key=f"del_notif_{notif['id']}", use_container_width=True):
                                st.session_state[f'confirm_delete_notif_{notif["id"]}'] = True
                            
                            if st.session_state.get(f'confirm_delete_notif_{notif["id"]}', False):
                                st.warning("Confirm?")
                                if st.button("✅ Yes", key=f"confirm_del_notif_{notif['id']}", use_container_width=True):
                                    db.delete_notification(notif['id'])
                                    show_success_message("Notification deleted!")
                                    st.session_state[f'confirm_delete_notif_{notif["id"]}'] = False
                                    st.rerun()
                        
                        if st.session_state.get(f'edit_notif_{notif["id"]}', False):
                            st.markdown("---")
                            with st.form(key=f"edit_notif_form_{notif['id']}"):
                                edit_title = st.text_input("Title *", value=notif['title'])
                                edit_message = st.text_area("Message *", value=notif['message'], height=100)
                                edit_priority = st.selectbox(
                                    "Priority *",
                                    options=['low', 'medium', 'high', 'critical'],
                                    index=['low', 'medium', 'high', 'critical'].index(notif['priority'])
                                )
                                edit_date = st.date_input("Shift Date *", value=date.fromisoformat(notif['shift_date']))
                                edit_resolved = st.checkbox("Resolved", value=bool(notif['is_resolved']))
                                
                                col_submit, col_cancel = st.columns(2)
                                
                                with col_submit:
                                    submit = st.form_submit_button("💾 Save", use_container_width=True)
                                
                                with col_cancel:
                                    cancel = st.form_submit_button("❌ Cancel", use_container_width=True)
                                
                                if submit:
                                    if validate_required_field(edit_title, "Title") and validate_required_field(edit_message, "Message"):
                                        db.update_notification(notif['id'], edit_title, edit_message, edit_priority, str(edit_date), edit_resolved)
                                        show_success_message("Notification updated!")
                                        st.session_state[f'edit_notif_{notif["id"]}'] = False
                                        st.rerun()
                                
                                if cancel:
                                    st.session_state[f'edit_notif_{notif["id"]}'] = False
                                    st.rerun()
                        
                        st.markdown("---")
            else:
                st.info("No notifications found.")
        
        with notif_tab2:
            with st.form(key="new_notif_form", clear_on_submit=True):
                title = st.text_input("Title *", placeholder="Enter notification title")
                message = st.text_area("Message *", placeholder="Enter notification message...", height=150)
                priority = st.selectbox("Priority *", options=['low', 'medium', 'high', 'critical'], index=2)
                shift_date = st.date_input("Shift Date *", value=date.today())
                
                submit = st.form_submit_button("💾 Create Notification", use_container_width=True)
                
                if submit:
                    if validate_required_field(title, "Title") and validate_required_field(message, "Message"):
                        notif_id = db.create_notification(title, message, priority, str(shift_date))
                        show_success_message(f"Notification created! (ID: {notif_id})")
                        st.rerun()
    
    st.markdown("---")
    
    # IT Issues Section
    with st.expander("💻 IT Issues", expanded=True):
        it_tab1, it_tab2 = st.tabs(["📋 View Issues", "➕ Add Issue"])
        
        with it_tab1:
            # Filter by status
            status_filter = st.multiselect(
                "Filter by Status",
                options=['open', 'in_progress', 'resolved'],
                default=['open', 'in_progress', 'resolved']
            )
            
            it_issues = db.get_all_it_issues()
            
            if not it_issues.empty:
                # Apply filter
                if status_filter:
                    it_issues = it_issues[it_issues['status'].isin(status_filter)]
                
                st.markdown(f"**Total IT Issues:** {len(it_issues)}")
                
                for idx, issue in it_issues.iterrows():
                    status_emoji = get_status_emoji(issue['status'])
                    
                    with st.container():
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            st.markdown(f"### {status_emoji} {issue['title']}")
                            st.markdown(f"**Status:** {issue['status'].replace('_', ' ').upper()}")
                            st.markdown(f"**Description:** {issue['description']}")
                            st.markdown(f"**Shift Date:** {issue['shift_date']}")
                            st.caption(f"Updated: {issue['updated_at']}")
                        
                        with col2:
                            st.markdown("**Actions:**")
                            
                            if st.button("✏️ Edit", key=f"edit_issue_{issue['id']}", use_container_width=True):
                                st.session_state[f'edit_issue_{issue["id"]}'] = True
                            
                            if st.button("🗑️ Delete", key=f"del_issue_{issue['id']}", use_container_width=True):
                                st.session_state[f'confirm_delete_issue_{issue["id"]}'] = True
                            
                            if st.session_state.get(f'confirm_delete_issue_{issue["id"]}', False):
                                st.warning("Confirm?")
                                if st.button("✅ Yes", key=f"confirm_del_issue_{issue['id']}", use_container_width=True):
                                    db.delete_it_issue(issue['id'])
                                    show_success_message("IT issue deleted!")
                                    st.session_state[f'confirm_delete_issue_{issue["id"]}'] = False
                                    st.rerun()
                        
                        if st.session_state.get(f'edit_issue_{issue["id"]}', False):
                            st.markdown("---")
                            with st.form(key=f"edit_issue_form_{issue['id']}"):
                                edit_title = st.text_input("Title *", value=issue['title'])
                                edit_description = st.text_area("Description *", value=issue['description'], height=100)
                                edit_status = st.selectbox(
                                    "Status *",
                                    options=['open', 'in_progress', 'resolved'],
                                    index=['open', 'in_progress', 'resolved'].index(issue['status'])
                                )
                                edit_date = st.date_input("Shift Date *", value=date.fromisoformat(issue['shift_date']))
                                
                                col_submit, col_cancel = st.columns(2)
                                
                                with col_submit:
                                    submit = st.form_submit_button("💾 Save", use_container_width=True)
                                
                                with col_cancel:
                                    cancel = st.form_submit_button("❌ Cancel", use_container_width=True)
                                
                                if submit:
                                    if validate_required_field(edit_title, "Title") and validate_required_field(edit_description, "Description"):
                                        db.update_it_issue(issue['id'], edit_title, edit_description, edit_status, str(edit_date))
                                        show_success_message("IT issue updated!")
                                        st.session_state[f'edit_issue_{issue["id"]}'] = False
                                        st.rerun()
                                
                                if cancel:
                                    st.session_state[f'edit_issue_{issue["id"]}'] = False
                                    st.rerun()
                        
                        st.markdown("---")
            else:
                st.info("No IT issues found.")
        
        with it_tab2:
            with st.form(key="new_issue_form", clear_on_submit=True):
                title = st.text_input("Title *", placeholder="Enter issue title")
                description = st.text_area("Description *", placeholder="Describe the IT issue...", height=150)
                status = st.selectbox("Status *", options=['open', 'in_progress', 'resolved'], index=0)
                shift_date = st.date_input("Shift Date *", value=date.today())
                
                submit = st.form_submit_button("💾 Create IT Issue", use_container_width=True)
                
                if submit:
                    if validate_required_field(title, "Title") and validate_required_field(description, "Description"):
                        issue_id = db.create_it_issue(title, description, status, str(shift_date))
                        show_success_message(f"IT issue created! (ID: {issue_id})")
                        st.rerun()
