"""Helper functions for the shift handover application."""
from datetime import datetime, date
import streamlit as st


def get_status_color(status: str) -> str:
    """Get color for status indicator.
    
    Args:
        status: Status value
        
    Returns:
        Color code
    """
    status_colors = {
        'operational': '#2ca02c',  # Green
        'partial': '#ff7f0e',      # Orange
        'offline': '#d62728',      # Red
        'open': '#d62728',         # Red
        'in_progress': '#ff7f0e',  # Orange
        'resolved': '#2ca02c',     # Green
        'low': '#7f7f7f',          # Gray
        'medium': '#ff7f0e',       # Orange
        'high': '#d62728',         # Red
        'critical': '#d62728'      # Red
    }
    return status_colors.get(status.lower(), '#7f7f7f')


def format_date(date_value) -> str:
    """Format date for display.
    
    Args:
        date_value: Date to format
        
    Returns:
        Formatted date string
    """
    if isinstance(date_value, str):
        try:
            date_obj = datetime.strptime(date_value, '%Y-%m-%d')
            return date_obj.strftime('%Y-%m-%d')
        except ValueError:
            return date_value
    elif isinstance(date_value, (datetime, date)):
        return date_value.strftime('%Y-%m-%d')
    return str(date_value)


def format_datetime(datetime_value) -> str:
    """Format datetime for display.
    
    Args:
        datetime_value: Datetime to format
        
    Returns:
        Formatted datetime string
    """
    if isinstance(datetime_value, str):
        try:
            dt = datetime.strptime(datetime_value, '%Y-%m-%d %H:%M:%S')
            return dt.strftime('%Y-%m-%d %H:%M')
        except ValueError:
            return datetime_value
    elif isinstance(datetime_value, datetime):
        return datetime_value.strftime('%Y-%m-%d %H:%M')
    return str(datetime_value)


def show_success_message(message: str):
    """Display success message.
    
    Args:
        message: Message to display
    """
    st.success(f"✅ {message}")


def show_error_message(message: str):
    """Display error message.
    
    Args:
        message: Message to display
    """
    st.error(f"❌ {message}")


def show_info_message(message: str):
    """Display info message.
    
    Args:
        message: Message to display
    """
    st.info(f"ℹ️ {message}")


def show_warning_message(message: str):
    """Display warning message.
    
    Args:
        message: Message to display
    """
    st.warning(f"⚠️ {message}")


def get_current_shift_time() -> str:
    """Get current shift time for display.
    
    Returns:
        Formatted current time
    """
    return datetime.now().strftime('%Y-%m-%d %H:%M')


def validate_required_field(value: str, field_name: str) -> bool:
    """Validate required field.
    
    Args:
        value: Field value
        field_name: Name of field
        
    Returns:
        True if valid, False otherwise
    """
    if not value or value.strip() == '':
        show_error_message(f"{field_name} is required.")
        return False
    return True


def get_priority_emoji(priority: str) -> str:
    """Get emoji for priority level.
    
    Args:
        priority: Priority level
        
    Returns:
        Emoji string
    """
    priority_emojis = {
        'low': '🔵',
        'medium': '🟡',
        'high': '🟠',
        'critical': '🔴'
    }
    return priority_emojis.get(priority.lower(), '⚪')


def get_status_emoji(status: str) -> str:
    """Get emoji for status.
    
    Args:
        status: Status value
        
    Returns:
        Emoji string
    """
    status_emojis = {
        'operational': '✅',
        'partial': '⚠️',
        'offline': '❌',
        'open': '🔴',
        'in_progress': '🟡',
        'resolved': '✅'
    }
    return status_emojis.get(status.lower(), '⚪')
