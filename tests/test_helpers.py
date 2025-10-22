"""Tests for helper functions."""
import pytest
from utils.helpers import (
    get_status_color,
    get_status_emoji,
    get_priority_emoji,
    format_date,
    validate_required_field
)
from datetime import date, datetime


class TestHelperFunctions:
    """Tests for utility helper functions."""
    
    def test_get_status_color(self):
        """Test status color retrieval."""
        assert get_status_color('operational') == '#2ca02c'
        assert get_status_color('partial') == '#ff7f0e'
        assert get_status_color('offline') == '#d62728'
        assert get_status_color('unknown') == '#7f7f7f'
    
    def test_get_status_emoji(self):
        """Test status emoji retrieval."""
        assert get_status_emoji('operational') == '✅'
        assert get_status_emoji('partial') == '⚠️'
        assert get_status_emoji('offline') == '❌'
        assert get_status_emoji('open') == '🔴'
        assert get_status_emoji('resolved') == '✅'
    
    def test_get_priority_emoji(self):
        """Test priority emoji retrieval."""
        assert get_priority_emoji('low') == '🔵'
        assert get_priority_emoji('medium') == '🟡'
        assert get_priority_emoji('high') == '🟠'
        assert get_priority_emoji('critical') == '🔴'
    
    def test_format_date_string(self):
        """Test date formatting from string."""
        result = format_date('2024-01-15')
        assert result == '2024-01-15'
    
    def test_format_date_object(self):
        """Test date formatting from date object."""
        test_date = date(2024, 1, 15)
        result = format_date(test_date)
        assert result == '2024-01-15'
    
    def test_format_date_datetime(self):
        """Test date formatting from datetime object."""
        test_datetime = datetime(2024, 1, 15, 10, 30)
        result = format_date(test_datetime)
        assert result == '2024-01-15'
    
    def test_validate_required_field_valid(self):
        """Test required field validation with valid input."""
        # Note: This function uses streamlit, so it will return True
        # but we can't fully test the error message without streamlit context
        result = validate_required_field("Valid input", "Field Name")
        assert result is True
    
    def test_validate_required_field_empty(self):
        """Test required field validation with empty input."""
        result = validate_required_field("", "Field Name")
        assert result is False
    
    def test_validate_required_field_whitespace(self):
        """Test required field validation with whitespace."""
        result = validate_required_field("   ", "Field Name")
        assert result is False
