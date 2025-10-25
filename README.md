# Fleetwise - Fleet Management System

A modern fleet management application built with **Reflex** (Python web framework) and **Flask** (REST API backend).

## 🚀 Quick Start

### Prerequisites
- Python 3.10+ (3.11+ recommended)
- pip (Python package manager)
- Git

### Installation

1. **Clone or download this project**
   ```bash
   cd Fleetwise-Next-to-Reflex-Migration
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize the database**
   ```bash
   python -m backend.app
   # Press Ctrl+C after you see "Running on http://127.0.0.1:8000"
   ```

### Running the Application

#### Option A: Use the startup scripts (Recommended)

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

**Windows:**
```batch
start.bat
```

#### Option B: Manual startup

**Terminal 1 - Backend:**
```bash
python -m backend.app
```

**Terminal 2 - Frontend:**
```bash
reflex run
```

### Access the Application

Open your browser and go to:
- **http://localhost:3000** (preferred)
- **http://127.0.0.1:3000** (alternative)
- **http://0.0.0.0:3000** (WSL users)

**Login credentials:**
- Email: `admin@fleetwise.com`
- Password: `admin123`

## 📋 Features

- ✅ User authentication with JWT tokens
- ✅ Driver management (CRUD operations)
- ✅ Secure password hashing
- ✅ RESTful API backend
- ✅ Modern, responsive UI with Material Design
- ✅ Form validation
- ✅ Toast notifications
- ✅ Modal dialogs
- ✅ Protected routes

## 🏗️ Architecture

```
┌─────────────────┐
│  Browser        │
│  (Port 3000)    │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  Reflex         │
│  Frontend       │
│  (FastAPI)      │
│  Port 8001      │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  Flask API      │
│  Backend        │
│  Port 8000      │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  SQLite         │
│  Database       │
└─────────────────┘
```

**Note:** Reflex runs two servers:
- **Port 3000**: Frontend (Next.js) - what you see in the browser
- **Port 8001**: Backend state management (FastAPI) - handles Reflex state

The Flask API on **Port 8000** is separate and provides the actual data API.

## 📁 Project Structure

```
Fleetwise-Next-to-Reflex-Migration/
├── app/
│   ├── __init__.py
│   ├── app.py                 # Main Reflex app and routing
│   ├── components/
│   │   ├── sidebar.py         # Navigation sidebar
│   │   └── ui.py              # Reusable UI components
│   ├── pages/
│   │   ├── login.py           # Login page
│   │   └── drivers.py         # Driver management page
│   └── states/
│       ├── base_state.py      # Base state class
│       ├── auth_state.py      # Authentication state
│       └── driver_state.py    # Driver management state
├── backend/
│   ├── __init__.py
│   ├── app.py                 # Flask API server
│   ├── models.py              # SQLAlchemy models
│   ├── config.py              # Configuration
│   └── fleetwise.db           # SQLite database (created on first run)
├── assets/                     # Static assets
├── requirements.txt            # Python dependencies
├── rxconfig.py                # Reflex configuration
├── start.sh                   # Linux/Mac startup script
├── start.bat                  # Windows startup script
└── setup_verify.py            # Setup verification script

```

## 🔧 Configuration

### Backend API URL
The frontend connects to the backend via the URL defined in `app/states/base_state.py`:

```python
API_BASE_URL = "http://127.0.0.1:8000/api"
```

### Reflex Configuration
Frontend and backend ports are configured in `rxconfig.py`:

```python
config = rx.Config(
    frontend_host="localhost",  # or "0.0.0.0" for WSL/Docker
    frontend_port=3000,
    backend_port=8001,
    api_url="http://localhost:8001",
)
```

## 🔐 API Endpoints

### Authentication
- `POST /api/auth/login` - Login with email and password

### Drivers
- `GET /api/drivers` - List all drivers
- `GET /api/drivers/:id` - Get single driver
- `POST /api/drivers` - Create new driver
- `PUT /api/drivers/:id` - Update driver
- `DELETE /api/drivers/:id` - Delete driver

All driver endpoints require JWT authentication via `Authorization: Bearer <token>` header.

## 🧪 Testing Your Setup

Run the verification script:

```bash
python setup_verify.py
```

This will check:
- Python version
- Dependencies
- File structure
- Database
- Backend server
- Authentication

## 🐛 Troubleshooting

### Cannot access localhost:3000

**Try these URLs:**
- http://localhost:3000
- http://127.0.0.1:3000
- http://0.0.0.0:3000

**Or change rxconfig.py:**
```python
frontend_host="localhost"  # instead of "0.0.0.0"
```

### "Cannot connect to backend" error

1. Check if Flask is running:
   ```bash
   curl http://127.0.0.1:8000/health
   ```

2. Restart the backend:
   ```bash
   # Press Ctrl+C in the backend terminal
   python -m backend.app
   ```

### Drivers page is empty

1. Check browser console (F12) for errors
2. Verify you're logged in
3. Check backend logs for API errors
4. Try adding a test driver via the UI

### Database issues

Delete and recreate:
```bash
rm backend/fleetwise.db
python -m backend.app
```

### Clear Reflex cache

```bash
reflex clean
rm -rf .web
reflex run
```

### Port already in use

**Find and kill process on port 8000:**
```bash
# Linux/Mac
lsof -ti:8000 | xargs kill -9

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**Find and kill process on port 3000:**
```bash
# Linux/Mac
lsof -ti:3000 | xargs kill -9

# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

## 📚 Common Issues

### Warning: "Event handler on_submit expects..."
This is just a warning and can be safely ignored. The app works correctly.

### Warning: "Python 3.10 is deprecated"
Consider upgrading to Python 3.11+, but 3.10 will work for now.

### WSL Users
For better performance and compatibility:
1. Use WSL2 (not WSL1)
2. Access via `http://<WSL_IP>:3000` from Windows browser
3. Or set `frontend_host="0.0.0.0"` in rxconfig.py

## 🔄 Development Workflow

1. **Make changes to Python files**
2. **Reflex auto-reloads** (you'll see compilation in terminal)
3. **Refresh browser** to see changes
4. **Backend changes** require manual restart

### Hot Reload
Reflex supports hot reload for most changes. Just save your Python files and refresh the browser.

## 🎯 Next Steps

Once you have the basic app running:

1. **Add more drivers** via the UI
2. **Explore the code** to understand the structure
3. **Customize the UI** in `app/components/` and `app/pages/`
4. **Add new features** (see plan.md for ideas)

## 📖 Documentation

- [Reflex Documentation](https://reflex.dev/docs/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)

## 🤝 Support

If you encounter issues:

1. Run `python setup_verify.py` to diagnose
2. Check the TROUBLESHOOTING.md file
3. Review backend and frontend terminal output
4. Check browser console (F12) for errors

## 📝 License

This is a demo/POC project for learning purposes.

## ✨ Credits

Built with:
- [Reflex](https://reflex.dev/) - Python web framework
- [Flask](https://flask.palletsprojects.com/) - Python web framework
- [SQLAlchemy](https://www.sqlalchemy.org/) - SQL toolkit
- [Tailwind CSS](https://tailwindcss.com/) - CSS framework