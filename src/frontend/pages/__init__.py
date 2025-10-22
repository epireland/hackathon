"""Pages package initialization."""
from . import dashboard
from . import handover_log
from . import positions
from . import operations
from . import issues_alerts
from . import market
from . import comments

__all__ = [
    'dashboard',
    'handover_log',
    'positions',
    'operations',
    'issues_alerts',
    'market',
    'comments'
]
