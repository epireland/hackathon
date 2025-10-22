# Design Documentation
## Power & Gas Trader Shift Handover Application

## User Interface Design

### Layout Strategy: Multi-Tab Layout with Dashboard Overview

#### Rationale:
1. **Information Density**: The application has 6 distinct functional areas - displaying all on one screen would be overwhelming.
2. **User Workflow**: Traders need to quickly scan previous shift information and add new entries. A tabbed interface allows focused data entry and review.

### User Interface Structure

#### Main Dashboard (Landing Page)
- Display summary cards showing critical alerts and recent entries
- Show quick stats: open IT issues, active notifications, latest positions
- List recent handover log entries (last 5-10)
- Provide at-a-glance view of current state

#### Navigation Tabs:
1. **Handover Log** - Core shift handover details (trader, date, summary notes)
2. **Trading Positions** - Power & Gas positions in expandable sections
3. **Operations** - Plant Status & Power System Status
4. **Issues & Alerts** - Notifications & IT Issues combined
5. **Market Activity** - Competitor Activity tracking
6. **Comments** - General observations

### UI Design Guidelines

#### For Data Entry (Traders):
- Use forms with clear sections and field labels
- Implement auto-save or "Save Draft" functionality
- Provide visual confirmation when data is saved
- Use date/time pickers for consistency

#### For Data Display:
- Use tables with sorting and filtering capabilities
- Color-code status indicators (green/yellow/red for plant status)
- Show timestamps for all entries
- Implement search functionality for historical data

#### General UI Guidelines:
- **Sidebar Navigation**: Persistent left sidebar with tab navigation
- **Top Bar**: Current shift time display
- **Responsive Design**: Use Streamlit's column layout for tablet compatibility
- **Visual Hierarchy**: Most critical information at the top
- **Action Buttons**: Clearly distinguish between "Add New", "Edit", "Delete"

### Component Specifications

#### Dashboard Summary Cards:
- **Critical Alerts Card**: Red border, shows count of urgent notifications
- **IT Issues Card**: Yellow border, shows count of open issues
- **Recent Activity Card**: Blue border, shows last 5 handover entries
- **Positions Summary Card**: Green border, shows latest power/gas positions

#### Navigation Sidebar:
- Fixed left sidebar (250px width)
- Logo/app name at top
- Radio buttons or tabs for navigation

#### Data Entry Forms:
- Consistent field widths
- Required fields marked with asterisk (*)
- Help text below complex fields
- Submit/Cancel buttons at bottom
- Success/Error messages at top of form

#### Data Tables:
- Sortable columns
- Filter/search box above table
- Pagination for large datasets
- Row actions (Edit/Delete) on right side
- Color coding for status fields

## Database Design

### Proposed Schema:

#### Handover Logs Table:
```sql
CREATE TABLE handover_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    trader_name TEXT NOT NULL,
    shift_date DATE NOT NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Power Positions Table:
```sql
CREATE TABLE power_positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    shift_date DATE NOT NULL,
    position_details TEXT NOT NULL,
    portfolio_status TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Gas Positions Table:
```sql
CREATE TABLE gas_positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    shift_date DATE NOT NULL,
    position_details TEXT NOT NULL,
    portfolio_status TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Plant Status Table:
```sql
CREATE TABLE plant_status (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    plant_name TEXT NOT NULL,
    status TEXT NOT NULL CHECK(status IN ('operational', 'partial', 'offline')),
    notes TEXT,
    shift_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Power System Status Table:
```sql
CREATE TABLE power_system_status (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    system_name TEXT NOT NULL,
    status TEXT NOT NULL,
    notes TEXT,
    shift_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Notifications Table:
```sql
CREATE TABLE notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    message TEXT NOT NULL,
    priority TEXT CHECK(priority IN ('low', 'medium', 'high', 'critical')),
    is_resolved BOOLEAN DEFAULT 0,
    shift_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### IT Issues Table:
```sql
CREATE TABLE it_issues (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    status TEXT CHECK(status IN ('open', 'in_progress', 'resolved')),
    shift_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Competitor Activity Table:
```sql
CREATE TABLE competitor_activity (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    competitor_name TEXT NOT NULL,
    activity_details TEXT NOT NULL,
    shift_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Comments Table:
```sql
CREATE TABLE comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    comment_text TEXT NOT NULL,
    shift_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Technical Architecture

### Application Structure:
```
copilot_proj/
├── app.py                 # Main Streamlit application
├── database/
│   ├── __init__.py
│   ├── db_manager.py      # Database connection and queries
│   └── schema.sql         # Database schema
├── pages/
│   ├── dashboard.py       # Main dashboard
│   ├── handover_log.py    # Handover log tab
│   ├── positions.py       # Trading positions tab
│   ├── operations.py      # Operations tab
│   ├── issues_alerts.py   # Issues & alerts tab
│   ├── market.py          # Market activity tab
│   └── comments.py        # Comments tab
├── utils/
│   ├── __init__.py
│   └── helpers.py         # Utility functions
├── requirements.txt       # Python dependencies
└── README.md             # Setup instructions
```

### Dependencies:
```
streamlit
pandas
```

## Design Notes

- **Color Scheme**: Professional, easy on eyes for long shifts
  - Primary: Blue (#1f77b4)
  - Success: Green (#2ca02c)
  - Warning: Yellow/Orange (#ff7f0e)
  - Danger: Red (#d62728)
  - Neutral: Gray (#7f7f7f)

- **Typography**: Clear, readable fonts
  - Headers: Sans-serif, bold
  - Body: Sans-serif, regular
  - Monospace for data/numbers

- **Spacing**: Generous padding for comfortable reading
- **Icons**: Use Streamlit's built-in emoji or simple text indicators
