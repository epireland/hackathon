"""Operations page - Manage plant and power system status."""
import streamlit as st
from datetime import date
from src.backend.database.db_manager import DatabaseManager
from src.utils.helpers import show_success_message, validate_required_field, get_status_emoji, get_status_color


def show(db: DatabaseManager):
    """Display operations page.
    
    Args:
        db: Database manager instance
    """
    st.markdown('<h1 class="main-header">🏭 Operations</h1>', unsafe_allow_html=True)
    st.markdown("Track plant status and power system infrastructure")
    
    st.markdown("---")
    
    # Plant Status Section
    with st.expander("🏭 Plant Status", expanded=True):
        plant_tab1, plant_tab2 = st.tabs(["📋 View Status", "➕ Add Status"])
        
        with plant_tab1:
            plant_status = db.get_all_plant_status()
            
            if not plant_status.empty:
                st.markdown(f"**Total Plant Records:** {len(plant_status)}")
                
                for idx, plant in plant_status.iterrows():
                    status_emoji = get_status_emoji(plant['status'])
                    status_color = get_status_color(plant['status'])
                    
                    with st.container():
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            st.markdown(f"### {status_emoji} {plant['plant_name']}")
                            st.markdown(f"**Status:** <span style='color: {status_color}; font-weight: bold;'>{plant['status'].upper()}</span>", unsafe_allow_html=True)
                            st.markdown(f"**Shift Date:** {plant['shift_date']}")
                            if plant['notes']:
                                st.markdown(f"**Notes:** {plant['notes']}")
                            st.caption(f"Updated: {plant['updated_at']}")
                        
                        with col2:
                            st.markdown("**Actions:**")
                            
                            if st.button("✏️ Edit", key=f"edit_plant_{plant['id']}", use_container_width=True):
                                st.session_state[f'edit_plant_{plant["id"]}'] = True
                            
                            if st.button("🗑️ Delete", key=f"del_plant_{plant['id']}", use_container_width=True):
                                st.session_state[f'confirm_delete_plant_{plant["id"]}'] = True
                            
                            if st.session_state.get(f'confirm_delete_plant_{plant["id"]}', False):
                                st.warning("Confirm?")
                                if st.button("✅ Yes", key=f"confirm_del_plant_{plant['id']}", use_container_width=True):
                                    db.delete_plant_status(plant['id'])
                                    show_success_message("Plant status deleted!")
                                    st.session_state[f'confirm_delete_plant_{plant["id"]}'] = False
                                    st.rerun()
                        
                        if st.session_state.get(f'edit_plant_{plant["id"]}', False):
                            st.markdown("---")
                            with st.form(key=f"edit_plant_form_{plant['id']}"):
                                edit_name = st.text_input("Plant Name *", value=plant['plant_name'])
                                edit_status = st.selectbox(
                                    "Status *",
                                    options=['operational', 'partial', 'offline'],
                                    index=['operational', 'partial', 'offline'].index(plant['status'])
                                )
                                edit_date = st.date_input("Shift Date *", value=date.fromisoformat(plant['shift_date']))
                                edit_notes = st.text_area("Notes", value=plant['notes'] or "", height=100)
                                
                                col_submit, col_cancel = st.columns(2)
                                
                                with col_submit:
                                    submit = st.form_submit_button("💾 Save", use_container_width=True)
                                
                                with col_cancel:
                                    cancel = st.form_submit_button("❌ Cancel", use_container_width=True)
                                
                                if submit:
                                    if validate_required_field(edit_name, "Plant Name"):
                                        db.update_plant_status(plant['id'], edit_name, edit_status, edit_notes, str(edit_date))
                                        show_success_message("Plant status updated!")
                                        st.session_state[f'edit_plant_{plant["id"]}'] = False
                                        st.rerun()
                                
                                if cancel:
                                    st.session_state[f'edit_plant_{plant["id"]}'] = False
                                    st.rerun()
                        
                        st.markdown("---")
            else:
                st.info("No plant status records found.")
        
        with plant_tab2:
            with st.form(key="new_plant_form", clear_on_submit=True):
                plant_name = st.text_input("Plant Name *", placeholder="Enter plant name")
                status = st.selectbox("Status *", options=['operational', 'partial', 'offline'])
                shift_date = st.date_input("Shift Date *", value=date.today())
                notes = st.text_area("Notes", placeholder="Additional information...", height=100)
                
                submit = st.form_submit_button("💾 Add Plant Status", use_container_width=True)
                
                if submit:
                    if validate_required_field(plant_name, "Plant Name"):
                        status_id = db.create_plant_status(plant_name, status, notes, str(shift_date))
                        show_success_message(f"Plant status added! (ID: {status_id})")
                        st.rerun()
    
    st.markdown("---")
    
    # Power System Status Section
    with st.expander("⚡ Power System Status", expanded=True):
        system_tab1, system_tab2 = st.tabs(["📋 View Status", "➕ Add Status"])
        
        with system_tab1:
            system_status = db.get_all_power_system_status()
            
            if not system_status.empty:
                st.markdown(f"**Total System Records:** {len(system_status)}")
                
                for idx, system in system_status.iterrows():
                    with st.container():
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            st.markdown(f"### ⚡ {system['system_name']}")
                            st.markdown(f"**Status:** {system['status']}")
                            st.markdown(f"**Shift Date:** {system['shift_date']}")
                            if system['notes']:
                                st.markdown(f"**Notes:** {system['notes']}")
                            st.caption(f"Updated: {system['updated_at']}")
                        
                        with col2:
                            st.markdown("**Actions:**")
                            
                            if st.button("✏️ Edit", key=f"edit_system_{system['id']}", use_container_width=True):
                                st.session_state[f'edit_system_{system["id"]}'] = True
                            
                            if st.button("🗑️ Delete", key=f"del_system_{system['id']}", use_container_width=True):
                                st.session_state[f'confirm_delete_system_{system["id"]}'] = True
                            
                            if st.session_state.get(f'confirm_delete_system_{system["id"]}', False):
                                st.warning("Confirm?")
                                if st.button("✅ Yes", key=f"confirm_del_system_{system['id']}", use_container_width=True):
                                    db.delete_power_system_status(system['id'])
                                    show_success_message("System status deleted!")
                                    st.session_state[f'confirm_delete_system_{system["id"]}'] = False
                                    st.rerun()
                        
                        if st.session_state.get(f'edit_system_{system["id"]}', False):
                            st.markdown("---")
                            with st.form(key=f"edit_system_form_{system['id']}"):
                                edit_name = st.text_input("System Name *", value=system['system_name'])
                                edit_status = st.text_input("Status *", value=system['status'])
                                edit_date = st.date_input("Shift Date *", value=date.fromisoformat(system['shift_date']))
                                edit_notes = st.text_area("Notes", value=system['notes'] or "", height=100)
                                
                                col_submit, col_cancel = st.columns(2)
                                
                                with col_submit:
                                    submit = st.form_submit_button("💾 Save", use_container_width=True)
                                
                                with col_cancel:
                                    cancel = st.form_submit_button("❌ Cancel", use_container_width=True)
                                
                                if submit:
                                    if validate_required_field(edit_name, "System Name") and validate_required_field(edit_status, "Status"):
                                        db.update_power_system_status(system['id'], edit_name, edit_status, edit_notes, str(edit_date))
                                        show_success_message("System status updated!")
                                        st.session_state[f'edit_system_{system["id"]}'] = False
                                        st.rerun()
                                
                                if cancel:
                                    st.session_state[f'edit_system_{system["id"]}'] = False
                                    st.rerun()
                        
                        st.markdown("---")
            else:
                st.info("No power system status records found.")
        
        with system_tab2:
            with st.form(key="new_system_form", clear_on_submit=True):
                system_name = st.text_input("System Name *", placeholder="Enter system name")
                status = st.text_input("Status *", placeholder="e.g., Normal, Degraded, Critical")
                shift_date = st.date_input("Shift Date *", value=date.today())
                notes = st.text_area("Notes", placeholder="Additional information...", height=100)
                
                submit = st.form_submit_button("💾 Add System Status", use_container_width=True)
                
                if submit:
                    if validate_required_field(system_name, "System Name") and validate_required_field(status, "Status"):
                        status_id = db.create_power_system_status(system_name, status, notes, str(shift_date))
                        show_success_message(f"System status added! (ID: {status_id})")
                        st.rerun()
