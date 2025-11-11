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
