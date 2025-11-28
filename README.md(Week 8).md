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