"""Trading Positions page - Manage power and gas positions."""
import streamlit as st
from datetime import date
from database.db_manager import DatabaseManager
from utils.helpers import show_success_message, show_error_message, validate_required_field


def show(db: DatabaseManager):
    """Display trading positions page.
    
    Args:
        db: Database manager instance
    """
    st.markdown('<h1 class="main-header">💼 Trading Positions</h1>', unsafe_allow_html=True)
    st.markdown("Track and manage power and gas trading positions")
    
    # Create two main sections
    st.markdown("---")
    
    # Power Positions Section
    with st.expander("⚡ Power Positions", expanded=True):
        power_tab1, power_tab2 = st.tabs(["📋 View Positions", "➕ Add Position"])
        
        with power_tab1:
            power_positions = db.get_all_power_positions()
            
            if not power_positions.empty:
                st.markdown(f"**Total Power Positions:** {len(power_positions)}")
                
                for idx, pos in power_positions.iterrows():
                    with st.container():
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            st.markdown(f"### 📅 {pos['shift_date']}")
                            st.markdown(f"**Position Details:**")
                            st.text_area("", value=pos['position_details'], height=100, key=f"power_view_{pos['id']}", disabled=True)
                            st.markdown(f"**Portfolio Status:** {pos['portfolio_status'] if pos['portfolio_status'] else 'N/A'}")
                            st.caption(f"Updated: {pos['updated_at']}")
                        
                        with col2:
                            st.markdown("**Actions:**")
                            
                            if st.button("✏️ Edit", key=f"edit_power_{pos['id']}", use_container_width=True):
                                st.session_state[f'edit_power_{pos["id"]}'] = True
                            
                            if st.button("🗑️ Delete", key=f"del_power_{pos['id']}", use_container_width=True):
                                st.session_state[f'confirm_delete_power_{pos["id"]}'] = True
                            
                            if st.session_state.get(f'confirm_delete_power_{pos["id"]}', False):
                                st.warning("Confirm?")
                                if st.button("✅ Yes", key=f"confirm_del_power_{pos['id']}", use_container_width=True):
                                    db.delete_power_position(pos['id'])
                                    show_success_message("Power position deleted!")
                                    st.session_state[f'confirm_delete_power_{pos["id"]}'] = False
                                    st.rerun()
                        
                        if st.session_state.get(f'edit_power_{pos["id"]}', False):
                            st.markdown("---")
                            with st.form(key=f"edit_power_form_{pos['id']}"):
                                edit_date = st.date_input("Shift Date *", value=date.fromisoformat(pos['shift_date']))
                                edit_details = st.text_area("Position Details *", value=pos['position_details'], height=150)
                                edit_status = st.text_input("Portfolio Status", value=pos['portfolio_status'] or "")
                                
                                col_submit, col_cancel = st.columns(2)
                                
                                with col_submit:
                                    submit = st.form_submit_button("💾 Save", use_container_width=True)
                                
                                with col_cancel:
                                    cancel = st.form_submit_button("❌ Cancel", use_container_width=True)
                                
                                if submit:
                                    if validate_required_field(edit_details, "Position Details"):
                                        db.update_power_position(pos['id'], str(edit_date), edit_details, edit_status)
                                        show_success_message("Power position updated!")
                                        st.session_state[f'edit_power_{pos["id"]}'] = False
                                        st.rerun()
                                
                                if cancel:
                                    st.session_state[f'edit_power_{pos["id"]}'] = False
                                    st.rerun()
                        
                        st.markdown("---")
            else:
                st.info("No power positions recorded.")
        
        with power_tab2:
            with st.form(key="new_power_form", clear_on_submit=True):
                shift_date = st.date_input("Shift Date *", value=date.today())
                position_details = st.text_area(
                    "Position Details *",
                    placeholder="Enter power trading position details...",
                    height=150
                )
                portfolio_status = st.text_input("Portfolio Status", placeholder="e.g., Balanced, Long, Short")
                
                submit = st.form_submit_button("💾 Add Power Position", use_container_width=True)
                
                if submit:
                    if validate_required_field(position_details, "Position Details"):
                        pos_id = db.create_power_position(str(shift_date), position_details, portfolio_status)
                        show_success_message(f"Power position added! (ID: {pos_id})")
                        st.rerun()
    
    st.markdown("---")
    
    # Gas Positions Section
    with st.expander("🔥 Gas Positions", expanded=True):
        gas_tab1, gas_tab2 = st.tabs(["📋 View Positions", "➕ Add Position"])
        
        with gas_tab1:
            gas_positions = db.get_all_gas_positions()
            
            if not gas_positions.empty:
                st.markdown(f"**Total Gas Positions:** {len(gas_positions)}")
                
                for idx, pos in gas_positions.iterrows():
                    with st.container():
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            st.markdown(f"### 📅 {pos['shift_date']}")
                            st.markdown(f"**Position Details:**")
                            st.text_area("", value=pos['position_details'], height=100, key=f"gas_view_{pos['id']}", disabled=True)
                            st.markdown(f"**Portfolio Status:** {pos['portfolio_status'] if pos['portfolio_status'] else 'N/A'}")
                            st.caption(f"Updated: {pos['updated_at']}")
                        
                        with col2:
                            st.markdown("**Actions:**")
                            
                            if st.button("✏️ Edit", key=f"edit_gas_{pos['id']}", use_container_width=True):
                                st.session_state[f'edit_gas_{pos["id"]}'] = True
                            
                            if st.button("🗑️ Delete", key=f"del_gas_{pos['id']}", use_container_width=True):
                                st.session_state[f'confirm_delete_gas_{pos["id"]}'] = True
                            
                            if st.session_state.get(f'confirm_delete_gas_{pos["id"]}', False):
                                st.warning("Confirm?")
                                if st.button("✅ Yes", key=f"confirm_del_gas_{pos['id']}", use_container_width=True):
                                    db.delete_gas_position(pos['id'])
                                    show_success_message("Gas position deleted!")
                                    st.session_state[f'confirm_delete_gas_{pos["id"]}'] = False
                                    st.rerun()
                        
                        if st.session_state.get(f'edit_gas_{pos["id"]}', False):
                            st.markdown("---")
                            with st.form(key=f"edit_gas_form_{pos['id']}"):
                                edit_date = st.date_input("Shift Date *", value=date.fromisoformat(pos['shift_date']))
                                edit_details = st.text_area("Position Details *", value=pos['position_details'], height=150)
                                edit_status = st.text_input("Portfolio Status", value=pos['portfolio_status'] or "")
                                
                                col_submit, col_cancel = st.columns(2)
                                
                                with col_submit:
                                    submit = st.form_submit_button("💾 Save", use_container_width=True)
                                
                                with col_cancel:
                                    cancel = st.form_submit_button("❌ Cancel", use_container_width=True)
                                
                                if submit:
                                    if validate_required_field(edit_details, "Position Details"):
                                        db.update_gas_position(pos['id'], str(edit_date), edit_details, edit_status)
                                        show_success_message("Gas position updated!")
                                        st.session_state[f'edit_gas_{pos["id"]}'] = False
                                        st.rerun()
                                
                                if cancel:
                                    st.session_state[f'edit_gas_{pos["id"]}'] = False
                                    st.rerun()
                        
                        st.markdown("---")
            else:
                st.info("No gas positions recorded.")
        
        with gas_tab2:
            with st.form(key="new_gas_form", clear_on_submit=True):
                shift_date = st.date_input("Shift Date *", value=date.today())
                position_details = st.text_area(
                    "Position Details *",
                    placeholder="Enter gas trading position details...",
                    height=150
                )
                portfolio_status = st.text_input("Portfolio Status", placeholder="e.g., Balanced, Long, Short")
                
                submit = st.form_submit_button("💾 Add Gas Position", use_container_width=True)
                
                if submit:
                    if validate_required_field(position_details, "Position Details"):
                        pos_id = db.create_gas_position(str(shift_date), position_details, portfolio_status)
                        show_success_message(f"Gas position added! (ID: {pos_id})")
                        st.rerun()
