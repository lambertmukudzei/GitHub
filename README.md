# Week 7: Secure Authentication System
Student Name: [Mukudzei Kunyetu-Lambert]
Student ID: [M01061702]
Course: CST1510 - CW2 - Multi-Domain Intelligence Platform

## Project Description
A command-line authentication system that lets users register and login securely. This was my first time using bcrypt for password hashing and it was really interesting to learn about security.

## Features
- Passwords are hashed with bcrypt (it automatically adds salt!)
- Users can register with unique usernames
- Login system checks passwords securely
- Basic input validation for usernames and passwords
- Data is saved in a text file

## How It Works
1. When you register, your password gets converted to a hash
2. The hash is saved instead of the actual password
3. When you login, it hashes your input and compares it to the stored hash
4. bcrypt handles all the complicated security stuff for us

## Technical Stuff
- Uses bcrypt library for hashing
- Stores data in users.txt file
- Usernames: 3-20 characters, letters and numbers only
- Passwords: 6-50 characters, needs uppercase, lowercase, and numbers

## How to Run
1. Make sure you have Python installed
2. Install bcrypt: `pip install bcrypt`
3. Run: `python auth.py`

## What I Learned
- How password hashing works
- Why we never store plain text passwords
- How to use external libraries in Python
- File handling for data storage
