# Power & Gas Trader Shift Handover System

A comprehensive web application built with Streamlit for managing shift handover logs in power and gas trading operations.

## 🎯 Overview

This application enables traders to efficiently log, track, and review shift handover information including:
- Shift handover logs
- Power and gas trading positions
- Plant and power system operational status
- Critical notifications and IT issues
- Competitor market activity
- General shift comments

## 📋 Features

### Dashboard
- At-a-glance overview of critical metrics
- Recent handover logs
- Active alerts and IT issues
- Latest trading positions

### Core Modules
1. **📝 Handover Log**: Create, view, edit, and delete shift handover entries
2. **💼 Trading Positions**: Track power and gas trading positions and portfolio status
3. **🏭 Operations**: Monitor plant status and power system infrastructure
4. **🚨 Issues & Alerts**: Manage notifications and IT issues with priority levels
5. **📈 Market Activity**: Log competitor activities and market observations
6. **💬 Comments**: Add general shift comments and observations

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- uv (ultrafast Python package installer) - already installed

### Setup Instructions

1. **Navigate to the project directory**
   ```cmd
   cd d:\SB_MICROHACK\hackathon
   ```

2. **Create a virtual environment with uv**
   ```cmd
   uv venv
   ```

3. **Install dependencies**
   ```cmd
   uv pip install -e .
   ```

   Or install with dev dependencies for testing:
   ```cmd
   uv pip install -e ".[dev]"
   ```

## 🎮 Usage

### Running the Application

1. **Start the Streamlit application**
   ```cmd
   uv run streamlit run app.py
   ```
   
   Or use the quick start script:
   ```cmd
   start.bat
   ```
   
   Or if you've activated the virtual environment:
   ```cmd
   .venv\Scripts\activate.bat
   streamlit run app.py
   ```

2. **Access the application**
   - The application will automatically open in your default web browser
   - If not, navigate to: `http://localhost:8501`

### Using the Application

1. **Navigation**: Use the sidebar to switch between different modules
2. **Creating Entries**: Navigate to the desired module and use the "Add New" tab
3. **Viewing Data**: Use the "View" tabs to see all entries with search/filter options
4. **Editing**: Click the "✏️ Edit" button on any entry to modify it
5. **Deleting**: Click the "🗑️ Delete" button and confirm to remove entries

## 📁 Project Structure

```
hackathon/
├── app.py                      # Main Streamlit application
├── database/
│   ├── __init__.py
│   ├── db_manager.py           # Database manager with all CRUD operations
│   └── schema.sql              # SQLite database schema
├── pages/
│   ├── __init__.py
│   ├── dashboard.py            # Dashboard page
│   ├── handover_log.py         # Handover log management
│   ├── positions.py            # Trading positions
│   ├── operations.py           # Operations status
│   ├── issues_alerts.py        # Notifications and IT issues
│   ├── market.py               # Competitor activity
│   └── comments.py             # General comments
├── utils/
│   ├── __init__.py
│   └── helpers.py              # Utility functions
├── tests/
│   ├── __init__.py
│   ├── test_db_manager.py      # Database tests
│   └── test_helpers.py         # Helper function tests
├── requirements.txt            # Python dependencies
├── AGENTS.md                   # Project specification
├── DESIGN.md                   # Design documentation
└── README.md                   # This file
```

## 🧪 Testing

### Running Tests

The project includes comprehensive unit tests for all core functionality.

1. **Install dev dependencies first**
   ```cmd
   uv pip install -e ".[dev]"
   ```

2. **Run all tests**
   ```cmd
   uv run pytest
   ```

3. **Run tests with coverage**
   ```cmd
   uv run pytest --cov=database --cov=utils --cov-report=html
   ```

4. **View coverage report**
   ```cmd
   start htmlcov\index.html
   ```

4. **View coverage report**
   - Open `htmlcov/index.html` in your browser

### Test Coverage

Tests include:
- Database CRUD operations for all tables
- Helper functions and utilities
- Data validation
- Edge cases and error handling

## 💾 Database

The application uses SQLite for data persistence with the following tables:

- `handover_logs`: Core shift handover entries
- `power_positions`: Power trading positions
- `gas_positions`: Gas trading positions
- `plant_status`: Plant operational status
- `power_system_status`: Power system infrastructure status
- `notifications`: Alerts and notifications
- `it_issues`: IT-related issues
- `competitor_activity`: Competitor market activities
- `comments`: General shift comments

**Database file**: `shift_handover.db` (created automatically on first run)

## 🛠️ Technologies

- **Framework**: Streamlit 1.28.0
- **Database**: SQLite3 (built-in)
- **Data Processing**: Pandas 2.1.0
- **Testing**: pytest 7.4.0, pytest-cov 4.1.0
- **Package Manager**: uv (ultrafast Python package installer)
- **Language**: Python 3.8+

## 📝 Data Management

### Backup
To backup your data, simply copy the `shift_handover.db` file to a safe location.

### Reset Database
To reset the database:
1. Stop the application
2. Delete `shift_handover.db`
3. Restart the application (a fresh database will be created)

## 🎨 Features & Highlights

- **Responsive Design**: Works on desktop and tablet devices
- **Real-time Updates**: Changes are immediately reflected in the UI
- **Search & Filter**: Easily find specific entries
- **Color-coded Status**: Visual indicators for status and priority levels
- **Timestamps**: Automatic tracking of creation and update times
- **Data Validation**: Required field validation
- **Confirmation Dialogs**: Prevent accidental deletions

## 🔧 Configuration

The application works out-of-the-box with default settings. Advanced users can modify:

- Database location: Edit `db_path` in `app.py`
- UI styling: Modify CSS in `app.py`
- Color scheme: Update colors in `utils/helpers.py`

## 📄 Documentation

- See [`AGENTS.md`](AGENTS.md) for detailed project requirements and specifications
- See [`DESIGN.md`](DESIGN.md) for UI/UX design and database schema details

## 🤝 Contributing

This is a hackathon project. For modifications:
1. Follow the existing code structure
2. Add tests for new features
3. Update documentation as needed

## 📞 Support

For issues or questions, please refer to the project documentation in `AGENTS.md` and `DESIGN.md`.

## 📜 License

This project was created for the SB Microhack Hackathon.

---

**Happy Trading! ⚡🔥**

