"""Database manager for SQLite operations."""
import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Optional, Any
import pandas as pd


class DatabaseManager:
    """Manages all database operations for the shift handover application."""
    
    def __init__(self, db_path: str = "shift_handover.db"):
        """Initialize database manager.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self) -> sqlite3.Connection:
        """Create and return a database connection."""
        conn = sqlite3.Connection(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        """Initialize database with schema."""
        schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
        
        with open(schema_path, 'r') as f:
            schema = f.read()
        
        with self.get_connection() as conn:
            conn.executescript(schema)
            conn.commit()
    
    # Handover Logs Methods
    def create_handover_log(self, trader_name: str, shift_date: str, notes: str) -> int:
        """Create a new handover log entry."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO handover_logs (trader_name, shift_date, notes)
                   VALUES (?, ?, ?)""",
                (trader_name, shift_date, notes)
            )
            conn.commit()
            return cursor.lastrowid
    
    def get_all_handover_logs(self) -> pd.DataFrame:
        """Get all handover logs."""
        with self.get_connection() as conn:
            return pd.read_sql_query(
                "SELECT * FROM handover_logs ORDER BY shift_date DESC, created_at DESC",
                conn
            )
    
    def get_recent_handover_logs(self, limit: int = 5) -> pd.DataFrame:
        """Get recent handover logs."""
        with self.get_connection() as conn:
            return pd.read_sql_query(
                f"SELECT * FROM handover_logs ORDER BY shift_date DESC, created_at DESC LIMIT {limit}",
                conn
            )
    
    def update_handover_log(self, log_id: int, trader_name: str, shift_date: str, notes: str):
        """Update an existing handover log."""
        with self.get_connection() as conn:
            conn.execute(
                """UPDATE handover_logs 
                   SET trader_name = ?, shift_date = ?, notes = ?, updated_at = CURRENT_TIMESTAMP
                   WHERE id = ?""",
                (trader_name, shift_date, notes, log_id)
            )
            conn.commit()
    
    def delete_handover_log(self, log_id: int):
        """Delete a handover log."""
        with self.get_connection() as conn:
            conn.execute("DELETE FROM handover_logs WHERE id = ?", (log_id,))
            conn.commit()
    
    # Power Positions Methods
    def create_power_position(self, shift_date: str, position_details: str, portfolio_status: str) -> int:
        """Create a new power position entry."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO power_positions (shift_date, position_details, portfolio_status)
                   VALUES (?, ?, ?)""",
                (shift_date, position_details, portfolio_status)
            )
            conn.commit()
            return cursor.lastrowid
    
    def get_all_power_positions(self) -> pd.DataFrame:
        """Get all power positions."""
        with self.get_connection() as conn:
            return pd.read_sql_query(
                "SELECT * FROM power_positions ORDER BY shift_date DESC",
                conn
            )
    
    def get_latest_power_position(self) -> Optional[Dict]:
        """Get the most recent power position."""
        with self.get_connection() as conn:
            cursor = conn.execute(
                "SELECT * FROM power_positions ORDER BY shift_date DESC LIMIT 1"
            )
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def update_power_position(self, position_id: int, shift_date: str, position_details: str, portfolio_status: str):
        """Update an existing power position."""
        with self.get_connection() as conn:
            conn.execute(
                """UPDATE power_positions 
                   SET shift_date = ?, position_details = ?, portfolio_status = ?, updated_at = CURRENT_TIMESTAMP
                   WHERE id = ?""",
                (shift_date, position_details, portfolio_status, position_id)
            )
            conn.commit()
    
    def delete_power_position(self, position_id: int):
        """Delete a power position."""
        with self.get_connection() as conn:
            conn.execute("DELETE FROM power_positions WHERE id = ?", (position_id,))
            conn.commit()
    
    # Gas Positions Methods
    def create_gas_position(self, shift_date: str, position_details: str, portfolio_status: str) -> int:
        """Create a new gas position entry."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO gas_positions (shift_date, position_details, portfolio_status)
                   VALUES (?, ?, ?)""",
                (shift_date, position_details, portfolio_status)
            )
            conn.commit()
            return cursor.lastrowid
    
    def get_all_gas_positions(self) -> pd.DataFrame:
        """Get all gas positions."""
        with self.get_connection() as conn:
            return pd.read_sql_query(
                "SELECT * FROM gas_positions ORDER BY shift_date DESC",
                conn
            )
    
    def get_latest_gas_position(self) -> Optional[Dict]:
        """Get the most recent gas position."""
        with self.get_connection() as conn:
            cursor = conn.execute(
                "SELECT * FROM gas_positions ORDER BY shift_date DESC LIMIT 1"
            )
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def update_gas_position(self, position_id: int, shift_date: str, position_details: str, portfolio_status: str):
        """Update an existing gas position."""
        with self.get_connection() as conn:
            conn.execute(
                """UPDATE gas_positions 
                   SET shift_date = ?, position_details = ?, portfolio_status = ?, updated_at = CURRENT_TIMESTAMP
                   WHERE id = ?""",
                (shift_date, position_details, portfolio_status, position_id)
            )
            conn.commit()
    
    def delete_gas_position(self, position_id: int):
        """Delete a gas position."""
        with self.get_connection() as conn:
            conn.execute("DELETE FROM gas_positions WHERE id = ?", (position_id,))
            conn.commit()
    
    # Plant Status Methods
    def create_plant_status(self, plant_name: str, status: str, notes: str, shift_date: str) -> int:
        """Create a new plant status entry."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO plant_status (plant_name, status, notes, shift_date)
                   VALUES (?, ?, ?, ?)""",
                (plant_name, status, notes, shift_date)
            )
            conn.commit()
            return cursor.lastrowid
    
    def get_all_plant_status(self) -> pd.DataFrame:
        """Get all plant status entries."""
        with self.get_connection() as conn:
            return pd.read_sql_query(
                "SELECT * FROM plant_status ORDER BY shift_date DESC",
                conn
            )
    
    def update_plant_status(self, status_id: int, plant_name: str, status: str, notes: str, shift_date: str):
        """Update an existing plant status."""
        with self.get_connection() as conn:
            conn.execute(
                """UPDATE plant_status 
                   SET plant_name = ?, status = ?, notes = ?, shift_date = ?, updated_at = CURRENT_TIMESTAMP
                   WHERE id = ?""",
                (plant_name, status, notes, shift_date, status_id)
            )
            conn.commit()
    
    def delete_plant_status(self, status_id: int):
        """Delete a plant status."""
        with self.get_connection() as conn:
            conn.execute("DELETE FROM plant_status WHERE id = ?", (status_id,))
            conn.commit()
    
    # Power System Status Methods
    def create_power_system_status(self, system_name: str, status: str, notes: str, shift_date: str) -> int:
        """Create a new power system status entry."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO power_system_status (system_name, status, notes, shift_date)
                   VALUES (?, ?, ?, ?)""",
                (system_name, status, notes, shift_date)
            )
            conn.commit()
            return cursor.lastrowid
    
    def get_all_power_system_status(self) -> pd.DataFrame:
        """Get all power system status entries."""
        with self.get_connection() as conn:
            return pd.read_sql_query(
                "SELECT * FROM power_system_status ORDER BY shift_date DESC",
                conn
            )
    
    def update_power_system_status(self, status_id: int, system_name: str, status: str, notes: str, shift_date: str):
        """Update an existing power system status."""
        with self.get_connection() as conn:
            conn.execute(
                """UPDATE power_system_status 
                   SET system_name = ?, status = ?, notes = ?, shift_date = ?, updated_at = CURRENT_TIMESTAMP
                   WHERE id = ?""",
                (system_name, status, notes, shift_date, status_id)
            )
            conn.commit()
    
    def delete_power_system_status(self, status_id: int):
        """Delete a power system status."""
        with self.get_connection() as conn:
            conn.execute("DELETE FROM power_system_status WHERE id = ?", (status_id,))
            conn.commit()
    
    # Notifications Methods
    def create_notification(self, title: str, message: str, priority: str, shift_date: str) -> int:
        """Create a new notification."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO notifications (title, message, priority, shift_date)
                   VALUES (?, ?, ?, ?)""",
                (title, message, priority, shift_date)
            )
            conn.commit()
            return cursor.lastrowid
    
    def get_all_notifications(self) -> pd.DataFrame:
        """Get all notifications."""
        with self.get_connection() as conn:
            return pd.read_sql_query(
                "SELECT * FROM notifications ORDER BY shift_date DESC, priority DESC",
                conn
            )
    
    def get_unresolved_notifications(self) -> pd.DataFrame:
        """Get unresolved notifications."""
        with self.get_connection() as conn:
            return pd.read_sql_query(
                "SELECT * FROM notifications WHERE is_resolved = 0 ORDER BY shift_date DESC, priority DESC",
                conn
            )
    
    def get_critical_notifications_count(self) -> int:
        """Get count of critical unresolved notifications."""
        with self.get_connection() as conn:
            cursor = conn.execute(
                "SELECT COUNT(*) FROM notifications WHERE priority = 'critical' AND is_resolved = 0"
            )
            return cursor.fetchone()[0]
    
    def update_notification(self, notif_id: int, title: str, message: str, priority: str, shift_date: str, is_resolved: bool):
        """Update an existing notification."""
        with self.get_connection() as conn:
            conn.execute(
                """UPDATE notifications 
                   SET title = ?, message = ?, priority = ?, shift_date = ?, is_resolved = ?, updated_at = CURRENT_TIMESTAMP
                   WHERE id = ?""",
                (title, message, priority, shift_date, is_resolved, notif_id)
            )
            conn.commit()
    
    def resolve_notification(self, notif_id: int):
        """Mark a notification as resolved."""
        with self.get_connection() as conn:
            conn.execute(
                "UPDATE notifications SET is_resolved = 1, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                (notif_id,)
            )
            conn.commit()
    
    def delete_notification(self, notif_id: int):
        """Delete a notification."""
        with self.get_connection() as conn:
            conn.execute("DELETE FROM notifications WHERE id = ?", (notif_id,))
            conn.commit()
    
    # IT Issues Methods
    def create_it_issue(self, title: str, description: str, status: str, shift_date: str) -> int:
        """Create a new IT issue."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO it_issues (title, description, status, shift_date)
                   VALUES (?, ?, ?, ?)""",
                (title, description, status, shift_date)
            )
            conn.commit()
            return cursor.lastrowid
    
    def get_all_it_issues(self) -> pd.DataFrame:
        """Get all IT issues."""
        with self.get_connection() as conn:
            return pd.read_sql_query(
                "SELECT * FROM it_issues ORDER BY shift_date DESC",
                conn
            )
    
    def get_open_it_issues_count(self) -> int:
        """Get count of open IT issues."""
        with self.get_connection() as conn:
            cursor = conn.execute(
                "SELECT COUNT(*) FROM it_issues WHERE status IN ('open', 'in_progress')"
            )
            return cursor.fetchone()[0]
    
    def update_it_issue(self, issue_id: int, title: str, description: str, status: str, shift_date: str):
        """Update an existing IT issue."""
        with self.get_connection() as conn:
            conn.execute(
                """UPDATE it_issues 
                   SET title = ?, description = ?, status = ?, shift_date = ?, updated_at = CURRENT_TIMESTAMP
                   WHERE id = ?""",
                (title, description, status, shift_date, issue_id)
            )
            conn.commit()
    
    def delete_it_issue(self, issue_id: int):
        """Delete an IT issue."""
        with self.get_connection() as conn:
            conn.execute("DELETE FROM it_issues WHERE id = ?", (issue_id,))
            conn.commit()
    
    # Competitor Activity Methods
    def create_competitor_activity(self, competitor_name: str, activity_details: str, shift_date: str) -> int:
        """Create a new competitor activity entry."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO competitor_activity (competitor_name, activity_details, shift_date)
                   VALUES (?, ?, ?)""",
                (competitor_name, activity_details, shift_date)
            )
            conn.commit()
            return cursor.lastrowid
    
    def get_all_competitor_activity(self) -> pd.DataFrame:
        """Get all competitor activity entries."""
        with self.get_connection() as conn:
            return pd.read_sql_query(
                "SELECT * FROM competitor_activity ORDER BY shift_date DESC",
                conn
            )
    
    def update_competitor_activity(self, activity_id: int, competitor_name: str, activity_details: str, shift_date: str):
        """Update an existing competitor activity."""
        with self.get_connection() as conn:
            conn.execute(
                """UPDATE competitor_activity 
                   SET competitor_name = ?, activity_details = ?, shift_date = ?, updated_at = CURRENT_TIMESTAMP
                   WHERE id = ?""",
                (competitor_name, activity_details, shift_date, activity_id)
            )
            conn.commit()
    
    def delete_competitor_activity(self, activity_id: int):
        """Delete a competitor activity."""
        with self.get_connection() as conn:
            conn.execute("DELETE FROM competitor_activity WHERE id = ?", (activity_id,))
            conn.commit()
    
    # Comments Methods
    def create_comment(self, comment_text: str, shift_date: str) -> int:
        """Create a new comment."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO comments (comment_text, shift_date)
                   VALUES (?, ?)""",
                (comment_text, shift_date)
            )
            conn.commit()
            return cursor.lastrowid
    
    def get_all_comments(self) -> pd.DataFrame:
        """Get all comments."""
        with self.get_connection() as conn:
            return pd.read_sql_query(
                "SELECT * FROM comments ORDER BY shift_date DESC, created_at DESC",
                conn
            )
    
    def update_comment(self, comment_id: int, comment_text: str, shift_date: str):
        """Update an existing comment."""
        with self.get_connection() as conn:
            conn.execute(
                """UPDATE comments 
                   SET comment_text = ?, shift_date = ?, updated_at = CURRENT_TIMESTAMP
                   WHERE id = ?""",
                (comment_text, shift_date, comment_id)
            )
            conn.commit()
    
    def delete_comment(self, comment_id: int):
        """Delete a comment."""
        with self.get_connection() as conn:
            conn.execute("DELETE FROM comments WHERE id = ?", (comment_id,))
            conn.commit()
