# Multi-Domain Intelligence Platform
# M01061702
# Week 11 ReadME.md

## Project Overview
A Streamlit-based intelligence platform integrating cybersecurity, data science, and IT operations with AI assistance.

## Architecture
- **Models:** User, SecurityIncident, Dataset, ITTicket
- **Services:** DatabaseManager, AuthManager, AIAssistant
- **Pages:** Login + 4 domain dashboards

## Installation
1. Clone repository
2. Create virtual environment: `python -m venv venv`
3. Activate: `.\venv\Scripts\Activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run: `streamlit run Home.py`

## Database
- Uses SQLite database populated from CSV files
- Contains 115 security incidents, 5 datasets, 150 IT tickets
- Thread-safe database connections

## Authentication
- Secure login/register with bcrypt password hashing
- Session-based authentication
- Demo credentials: test_user / SecurePass123!