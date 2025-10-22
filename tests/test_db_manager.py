"""Unit tests for database manager."""
import pytest
import os
import tempfile
from datetime import date
from database.db_manager import DatabaseManager


@pytest.fixture
def db():
    """Create a temporary database for testing."""
    # Create a temporary file
    fd, path = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    
    # Initialize database
    db_manager = DatabaseManager(path)
    
    yield db_manager
    
    # Cleanup
    os.unlink(path)


class TestHandoverLogs:
    """Tests for handover log operations."""
    
    def test_create_handover_log(self, db):
        """Test creating a handover log."""
        log_id = db.create_handover_log("John Doe", "2024-01-15", "Test notes")
        assert log_id > 0
    
    def test_get_all_handover_logs(self, db):
        """Test retrieving all handover logs."""
        db.create_handover_log("John Doe", "2024-01-15", "Test notes 1")
        db.create_handover_log("Jane Smith", "2024-01-16", "Test notes 2")
        
        logs = db.get_all_handover_logs()
        assert len(logs) == 2
    
    def test_update_handover_log(self, db):
        """Test updating a handover log."""
        log_id = db.create_handover_log("John Doe", "2024-01-15", "Original notes")
        db.update_handover_log(log_id, "John Doe", "2024-01-15", "Updated notes")
        
        logs = db.get_all_handover_logs()
        assert logs.iloc[0]['notes'] == "Updated notes"
    
    def test_delete_handover_log(self, db):
        """Test deleting a handover log."""
        log_id = db.create_handover_log("John Doe", "2024-01-15", "Test notes")
        db.delete_handover_log(log_id)
        
        logs = db.get_all_handover_logs()
        assert len(logs) == 0


class TestPowerPositions:
    """Tests for power position operations."""
    
    def test_create_power_position(self, db):
        """Test creating a power position."""
        pos_id = db.create_power_position("2024-01-15", "Long 100MW", "Balanced")
        assert pos_id > 0
    
    def test_get_all_power_positions(self, db):
        """Test retrieving all power positions."""
        db.create_power_position("2024-01-15", "Long 100MW", "Balanced")
        db.create_power_position("2024-01-16", "Short 50MW", "Short")
        
        positions = db.get_all_power_positions()
        assert len(positions) == 2
    
    def test_get_latest_power_position(self, db):
        """Test retrieving the latest power position."""
        db.create_power_position("2024-01-15", "Long 100MW", "Balanced")
        db.create_power_position("2024-01-16", "Short 50MW", "Short")
        
        latest = db.get_latest_power_position()
        assert latest is not None
        assert latest['shift_date'] == "2024-01-16"
    
    def test_delete_power_position(self, db):
        """Test deleting a power position."""
        pos_id = db.create_power_position("2024-01-15", "Long 100MW", "Balanced")
        db.delete_power_position(pos_id)
        
        positions = db.get_all_power_positions()
        assert len(positions) == 0


class TestGasPositions:
    """Tests for gas position operations."""
    
    def test_create_gas_position(self, db):
        """Test creating a gas position."""
        pos_id = db.create_gas_position("2024-01-15", "Long 500 therm", "Balanced")
        assert pos_id > 0
    
    def test_get_latest_gas_position(self, db):
        """Test retrieving the latest gas position."""
        db.create_gas_position("2024-01-15", "Long 500 therm", "Balanced")
        db.create_gas_position("2024-01-16", "Short 200 therm", "Short")
        
        latest = db.get_latest_gas_position()
        assert latest is not None
        assert latest['shift_date'] == "2024-01-16"


class TestPlantStatus:
    """Tests for plant status operations."""
    
    def test_create_plant_status(self, db):
        """Test creating a plant status."""
        status_id = db.create_plant_status("Plant A", "operational", "All systems normal", "2024-01-15")
        assert status_id > 0
    
    def test_plant_status_constraints(self, db):
        """Test plant status constraints."""
        # Valid statuses should work
        db.create_plant_status("Plant A", "operational", "", "2024-01-15")
        db.create_plant_status("Plant B", "partial", "", "2024-01-15")
        db.create_plant_status("Plant C", "offline", "", "2024-01-15")
        
        statuses = db.get_all_plant_status()
        assert len(statuses) == 3


class TestNotifications:
    """Tests for notification operations."""
    
    def test_create_notification(self, db):
        """Test creating a notification."""
        notif_id = db.create_notification("Test Alert", "This is a test", "high", "2024-01-15")
        assert notif_id > 0
    
    def test_get_unresolved_notifications(self, db):
        """Test retrieving unresolved notifications."""
        db.create_notification("Alert 1", "Message 1", "critical", "2024-01-15")
        notif_id = db.create_notification("Alert 2", "Message 2", "high", "2024-01-15")
        
        # Resolve one
        db.resolve_notification(notif_id)
        
        unresolved = db.get_unresolved_notifications()
        assert len(unresolved) == 1
    
    def test_get_critical_notifications_count(self, db):
        """Test counting critical notifications."""
        db.create_notification("Critical 1", "Message", "critical", "2024-01-15")
        db.create_notification("Critical 2", "Message", "critical", "2024-01-15")
        db.create_notification("High", "Message", "high", "2024-01-15")
        
        count = db.get_critical_notifications_count()
        assert count == 2


class TestITIssues:
    """Tests for IT issue operations."""
    
    def test_create_it_issue(self, db):
        """Test creating an IT issue."""
        issue_id = db.create_it_issue("System Down", "Trading system is down", "open", "2024-01-15")
        assert issue_id > 0
    
    def test_get_open_it_issues_count(self, db):
        """Test counting open IT issues."""
        db.create_it_issue("Issue 1", "Description", "open", "2024-01-15")
        db.create_it_issue("Issue 2", "Description", "in_progress", "2024-01-15")
        db.create_it_issue("Issue 3", "Description", "resolved", "2024-01-15")
        
        count = db.get_open_it_issues_count()
        assert count == 2


class TestCompetitorActivity:
    """Tests for competitor activity operations."""
    
    def test_create_competitor_activity(self, db):
        """Test creating a competitor activity."""
        activity_id = db.create_competitor_activity("Competitor A", "Increased trading volume", "2024-01-15")
        assert activity_id > 0
    
    def test_get_all_competitor_activity(self, db):
        """Test retrieving all competitor activities."""
        db.create_competitor_activity("Competitor A", "Activity 1", "2024-01-15")
        db.create_competitor_activity("Competitor B", "Activity 2", "2024-01-16")
        
        activities = db.get_all_competitor_activity()
        assert len(activities) == 2


class TestComments:
    """Tests for comment operations."""
    
    def test_create_comment(self, db):
        """Test creating a comment."""
        comment_id = db.create_comment("This is a test comment", "2024-01-15")
        assert comment_id > 0
    
    def test_get_all_comments(self, db):
        """Test retrieving all comments."""
        db.create_comment("Comment 1", "2024-01-15")
        db.create_comment("Comment 2", "2024-01-16")
        
        comments = db.get_all_comments()
        assert len(comments) == 2
    
    def test_update_comment(self, db):
        """Test updating a comment."""
        comment_id = db.create_comment("Original comment", "2024-01-15")
        db.update_comment(comment_id, "Updated comment", "2024-01-15")
        
        comments = db.get_all_comments()
        assert comments.iloc[0]['comment_text'] == "Updated comment"
    
    def test_delete_comment(self, db):
        """Test deleting a comment."""
        comment_id = db.create_comment("Test comment", "2024-01-15")
        db.delete_comment(comment_id)
        
        comments = db.get_all_comments()
        assert len(comments) == 0
