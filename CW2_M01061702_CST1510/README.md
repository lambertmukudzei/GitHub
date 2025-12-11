## Week 8: Data Pipeline & CRUD (SQL)
Student Name: [Mukudzei Kunyetu-Lambert]
Student ID: [M01061702]
Course: CST1510 - CW2 - Multi-Domain Intelligence Platform

## Project Description
This week I upgraded from text files to a real database! I built a SQLite database system that stores users, cyber incidents, datasets, and IT tickets. This was my first time working with databases and it was really cool to see how much better they are than text files.

## Features
Professional database with 4 tables (users, cyber_incidents, datasets_metadata, it_tickets)

Migrated users from Week 7's users.txt to the database

Loaded real data from CSV files (115 incidents, 5 datasets, 150 tickets)

Secure authentication now works with the database instead of text files

CRUD operations - Create, Read, Update, Delete for all data

Analytical queries to get insights from the data

## How It Works
Database setup creates all the tables automatically

User migration moves Week 7 users from users.txt to the database

CSV loading takes data from spreadsheets and puts it in the database

Authentication checks passwords against the database instead of text files

CRUD operations let you add, view, update, and delete records

## Technical Stuff
SQLite database - Built into Python, no extra installation needed

Pandas library - For loading CSV files into the database

bcrypt - Still used for password security (from Week 7)

File structure - Organized code into multiple files like professionals do

Parameterized queries - Prevents SQL injection attacks

## How to Run
Make sure you have Python installed

Install dependencies: pip install -r requirements.txt

Run the setup: python main.py

Test analytics: python analytics.py
## Screenshots
![alt text](image.png)
![alt text](image-1.png)
![alt text](image-2.png)
![alt text](image-3.png)

## Week 9: Multi-Page Streamlit Web Application
Student Name: [Mukudzei Kunyetu-Lambert]
Student ID: [M01061702]
Course: CST1510 - CW2 - Multi-Domain Intelligence Platform

## Project Description
A complete multi-page web application built with Streamlit that showcases my Week 7 authentication system and Week 8 database. Features secure login, protected pages, and interactive data visualization.

## Features
- **Secure Login/Register System** using Week 7 bcrypt authentication
- **Multi-Page Navigation** with protected routes
- **Real-Time Data Visualization** from Week 8 database
- **Session Management** with persistent login state
- **Professional Dashboard Layout** with sidebars and columns
- **Interactive Filters** and charts

## Pages in the Application

## 1. Home Page (`Home.py`)
- Login/Register tabs
- Secure password validation
- Database-backed user authentication
- Session state management

## 2. Main Dashboard (`pages/1_Dashboard.py`)
- Platform overview with key metrics
- Quick navigation to other pages
- Real-time data visualization
- Protected route (requires login)

## 3. Cyber Security Dashboard (`pages/2_Cyber_Security.py`)
- Visualization of 115 cyber incidents
- Filter by severity, category, and status
- Interactive bar charts
- Real data from Week 8 database

## 4. IT Support Dashboard (`pages/3_IT_Support.py`)
- Management of 150 IT tickets
- Priority and status filtering
- Support team assignment analysis
- Resolution time tracking

## 5. Data Management Dashboard (`pages/4_Data_Management.py`)
- Overview of 5 datasets
- Size and metadata analysis
- Uploader statistics
- Data quality metrics

## How to Run

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt


## Multi-Domain Intelligence Platform
## M01061702
## Week 11 ReadME.md

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
#Key things to note
-When Downloading my folders to mark, seperate my files from outside the folder and the ones in the folder.
-The CW2_M01061702_CST1510 folder is the final submission
-I noticed if the files are mixed, it can cause confusion with my Code.
-If streamlit run Home.py does not work, use python -m streamlit run Home.py
