"""Comments page - General observations and comments."""
import streamlit as st
from datetime import date
from database.db_manager import DatabaseManager
from utils.helpers import show_success_message, validate_required_field


def show(db: DatabaseManager):
    """Display comments page.
    
    Args:
        db: Database manager instance
    """
    st.markdown('<h1 class="main-header">💬 Comments</h1>', unsafe_allow_html=True)
    st.markdown("Add general comments and observations during your shift")
    
    # Tabs for viewing and adding
    tab1, tab2 = st.tabs(["📋 View Comments", "➕ Add Comment"])
    
    with tab1:
        st.subheader("All Comments")
        
        # Search functionality
        search = st.text_input("🔍 Search comments", "")
        
        comments = db.get_all_comments()
        
        if not comments.empty:
            # Apply search filter
            if search:
                comments = comments[
                    comments['comment_text'].str.contains(search, case=False, na=False)
                ]
            
            st.markdown(f"**Total Comments:** {len(comments)}")
            
            for idx, comment in comments.iterrows():
                with st.container():
                    col1, col2 = st.columns([4, 1])
                    
                    with col1:
                        st.markdown(f"**📅 {comment['shift_date']}**")
                        st.markdown(f"{comment['comment_text']}")
                        st.caption(f"Created: {comment['created_at']} | Updated: {comment['updated_at']}")
                    
                    with col2:
                        st.markdown("**Actions:**")
                        
                        if st.button("✏️ Edit", key=f"edit_comment_{comment['id']}", use_container_width=True):
                            st.session_state[f'edit_comment_{comment["id"]}'] = True
                        
                        if st.button("🗑️ Delete", key=f"del_comment_{comment['id']}", use_container_width=True):
                            st.session_state[f'confirm_delete_comment_{comment["id"]}'] = True
                        
                        if st.session_state.get(f'confirm_delete_comment_{comment["id"]}', False):
                            st.warning("Confirm?")
                            if st.button("✅ Yes", key=f"confirm_del_comment_{comment['id']}", use_container_width=True):
                                db.delete_comment(comment['id'])
                                show_success_message("Comment deleted!")
                                st.session_state[f'confirm_delete_comment_{comment["id"]}'] = False
                                st.rerun()
                            if st.button("❌ Cancel", key=f"cancel_del_comment_{comment['id']}", use_container_width=True):
                                st.session_state[f'confirm_delete_comment_{comment["id"]}'] = False
                                st.rerun()
                    
                    # Edit form
                    if st.session_state.get(f'edit_comment_{comment["id"]}', False):
                        st.markdown("---")
                        with st.form(key=f"edit_comment_form_{comment['id']}"):
                            edit_date = st.date_input("Shift Date *", value=date.fromisoformat(comment['shift_date']))
                            edit_text = st.text_area("Comment *", value=comment['comment_text'], height=150)
                            
                            col_submit, col_cancel = st.columns(2)
                            
                            with col_submit:
                                submit = st.form_submit_button("💾 Save Changes", use_container_width=True)
                            
                            with col_cancel:
                                cancel = st.form_submit_button("❌ Cancel", use_container_width=True)
                            
                            if submit:
                                if validate_required_field(edit_text, "Comment"):
                                    db.update_comment(
                                        comment['id'],
                                        edit_text,
                                        str(edit_date)
                                    )
                                    show_success_message("Comment updated!")
                                    st.session_state[f'edit_comment_{comment["id"]}'] = False
                                    st.rerun()
                            
                            if cancel:
                                st.session_state[f'edit_comment_{comment["id"]}'] = False
                                st.rerun()
                    
                    st.markdown("---")
        else:
            st.info("No comments found. Add your first comment using the 'Add Comment' tab.")
    
    with tab2:
        st.subheader("Add New Comment")
        
        with st.form(key="new_comment_form", clear_on_submit=True):
            shift_date = st.date_input("Shift Date *", value=date.today())
            comment_text = st.text_area(
                "Comment *",
                placeholder="Enter your general observations, notes, or comments about the shift...",
                height=200
            )
            
            submit = st.form_submit_button("💾 Add Comment", use_container_width=True)
            
            if submit:
                if validate_required_field(comment_text, "Comment"):
                    comment_id = db.create_comment(
                        comment_text,
                        str(shift_date)
                    )
                    show_success_message(f"Comment added successfully! (ID: {comment_id})")
                    st.rerun()
