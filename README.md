# Week 7: Secure Authentication System
Student Name: [Mukudzei Kunyetu-Lambert]
Student ID: [M01061702]
Course: CST1510 - CW2 - Multi-Domain Intelligence Platform

## Project Description
A command-line authentication system implementing secure password hashing using bcrypt. 
This system allows users to register accounts and log in with proper passwords.

## Features
- Secure password hashing with bcrypt
- User registration and login
- Input validation
- File-based data storage

## Technical implementation
- Hashing Algorithm: bcrypt with automatic salting
- Data Storage: Plain text file (`users.txt`) with comma-separated values
- Password Security: One-way hashing, no plaintext storage
- Validation: Username (3-20 alphanumeric characters), Password (6-50 characters)
## Installation

```bash
pip install -r requirements.txt

## Week 8: Database Implementation & CRUD Operations
Student Name: Mukudzei Kunyetu-Lambert
Student ID: M01061702
Course: CST1510 - CW2 - Multi-Domain Intelligence Platform

## Project Description
A professional database system implementing SQLite with secure CRUD operations for a multi-domain intelligence platform. This system transitions from file-based storage to a robust database architecture.

## Features
SQLite Database with 4 relational tables

Secure CRUD Operations (Create, Read, Update, Delete)

User Authentication with bcrypt password hashing

Data Migration from CSV files to database

Parameterized Queries to prevent SQL injection

Multi-domain Data Management (Cyber Incidents, Datasets, IT Tickets)

## Technical Implementation
Database Schema
## Security Features
Password Hashing: bcrypt with automatic salting

SQL Injection Protection: Parameterized queries using ? placeholders

Input Validation: Type checking and constraint enforcement

Unique Constraints: Prevent duplicate usernames and primary keys

## Data Storage
Database: SQLite (intelligence_platform.db)

Source Data: CSV files for initial data loading

User Accounts: Migrated from users.txt to database table
CW2_M01061702_CST1510/
├── app/
│   ├── data/               # Database layer
│   │   ├── db.py          # Database connection
│   │   ├── schema.py      # Table definitions
│   │   ├── users.py       # User CRUD operations
│   │   ├── incidents.py   # Incident CRUD operations
│   │   ├── datasets.py    # Dataset CRUD operations
│   │   └── tickets.py     # Ticket CRUD operations
│   └── services/
│       └── user_service.py # Authentication logic
├── DATA/                   # Data files
│   ├── users.txt          # User accounts (migrated to DB)
│   ├── cyber_incidents.csv # 115 security incidents
│   ├── datasets_metadata.csv # 5 datasets metadata
│   └── it_tickets.csv     # 150 IT support tickets
├── docs/
├── main.py                # Demo application

└── requirements.txt       # Dependencies

## Installation
Install dependencies: pip install -r requirements.txt

Run setup: python main.py

Database automatically created and populated

Test authentication and CRUD operations
<img width="947" height="416" alt="image" src="https://github.com/user-attachments/assets/5c4343a3-0743-4184-8630-fc29de5e67a0" />



