# Week 8 Database Setup - This is my main file that runs everything
# Student No: [M01061702]
# This file sets up our database and loads all the data

# First we need to import all the tools we'll use
# These are like the building blocks for our program
import os  # This helps us work with files and folders
import sys  # This helps with System-specific parameters and functions
from pathlib import Path  # This makes working with file paths less complicated
import pandas as pd  # This is for working with data tables (like Excel) with huge libraries

# This line helps Python find our other code files
# It's like telling Python "look in this folder for our other programs"
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# No we Let the user know that we're starting
print("Starting Week 8 Database Setup...")
print("This might takes some time...")

# Try to run our main program
# We use try/except to catch any errors that might happen
try:
    # Tell the user we're loading our code modules
    print("Loading our code modules...")
    
    # Import our own functions that we wrote in other files
    # These are like calling helpers from different rooms
    from app.data.db import connect_database  # This connects to our database
    from app.data.schema import create_all_tables  # This creates the tables
    from app.services.user_service import migrate_users_from_file  # This moves users from text file to database
    from app.services.user_service import register_user, login_user  # These handle user signup and login
    from app.data.incidents import insert_incident, delete_incident  # These add and remove incidents
    
    print("All code modules loaded successfully!")
    
    # Make sure our DATA folder exists
    # If it doesn't exist, we create it
    DATA_DIR = Path("DATA")  # This is where we store our data files
    DATA_DIR.mkdir(exist_ok=True)  # Create folder if missing
    print("DATA folder is ready for use")
    
    # This function loads CSV files into our database
    # CSV files are like Excel spreadsheets but in text format
    def load_all_csv_data(conn):
        """This function takes data from CSV files and puts it into our database"""
        print("\n[3/5] Loading data from CSV files...")
        print("   (CSV files are like Excel spreadsheets but in text format)")
        
        # List of all the CSV files we want to load
        # Each file goes into a different table in the database
        csv_files = {
            'cyber_incidents': DATA_DIR / 'cyber_incidents.csv',  # Security incidents data
            'datasets_metadata': DATA_DIR / 'datasets_metadata.csv',  # Information about datasets
            'it_tickets': DATA_DIR / 'it_tickets.csv'  # IT support tickets
        }
        
        total_rows = 0  # We'll count how many rows we add
        
        # Go through each CSV file and load it
        for table_name, csv_path in csv_files.items():
            # First check if the file exists
            if csv_path.exists():
                try:
                    # Read the CSV file using pandas
                    # Pandas is like a super-powered Excel for programmers, handles huge libraries
                    df = pd.read_csv(csv_path)
                    
                    # Put the data into our database table
                    # to_sql is a pandas function that does this for us
                    df.to_sql(table_name, conn, if_exists='append', index=False)
                    
                    # Count how many rows we added
                    rows_loaded = len(df)
                    total_rows += rows_loaded
                    print(f"Loaded {rows_loaded} rows into {table_name} table")
                    
                except Exception as e:
                    # If something goes wrong, tell the user
                    print(f"OopS! Error loading {csv_path.name}: {e}")
            else:
                # If the file is missing, tell the user
                print(f"Error: Couldn't find this file: {csv_path.name}")
        
        # Tell the user how much data we loaded in total
        return total_rows

    # This is our main function that does everything within the database setup
    def setup_database_complete():
        """This is the main function that sets up our entire database"""
        
        print("\n" + "="*60)
        print("STARTING COMPLETE DATABASE SETUP")
        print("We're going to build our database in 5 steps...")
        print("="*60)
        
        # STEP 1: Create the database tables
        # Tables are like different spreadsheets in our database
        print("\n[1/5] Step 1: Creating database tables...")
        print("   (Tables are like different spreadsheets in our database)")
        
        # Connect to the database (creates the file if it doesn't exist)
        conn = connect_database()
        
        # Create all the tables we need
        create_all_tables(conn)
        
        # Close the connection
        conn.close()
        print("Database tables created successfully!")
        
        # STEP 2: Move users from text file to database
        print("\n[2/5] Step 2: Moving users from text file to database...")
        print("   (Moving users from Week 7 into our new database)")
        
        # This function reads users.txt and puts them in the database
        user_count = migrate_users_from_file()
        print(f"Moved {user_count} users into the database")
        
        # STEP 3: Load data from CSV files
        print("\n[3/5] Step 3: Loading data from CSV files...")
        
        # Connect to database again
        conn = connect_database()
        
        # Load all the CSV data
        total_rows = load_all_csv_data(conn)
        print(f"Loaded {total_rows} rows of data in total")
        
        # STEP 4: Check that everything worked
        print("\n[4/5] Step 4: Checking that everything worked...")
        print("   Let's count how many rows are in each table:")
        
        # List of all our tables
        tables = ['users', 'cyber_incidents', 'datasets_metadata', 'it_tickets']
        
        # Print a nice header
        print(f"\n {'Table Name':<20} {'Row Count':<10}")
        print("-" * 35)
        
        # Count rows in each table
        for table in tables:
            try:
                # This SQL query counts rows in each table
                count = pd.read_sql_query(f"SELECT COUNT(*) as count FROM {table}", conn).iloc[0]['count']
                print(f" {table:<20} {count:<10}")
            except Exception as e:
                # If we can't count a table, show an error
                print(f" {table:<20} {'Error':<10}")
        
        # Close the database connection
        conn.close()
        
        # STEP 5: Test that everything works
        print("\n[5/5] Step 5: Testing that everything works...")
        print("   Let's test user registration and adding incidents:")
        
        # Test 1: Register a new user
        print("   Testing user registration...")
        success, msg = register_user("test_user", "SecurePass123!", "analyst")
        print(f"   Authentication: {msg}")
        
        # Test 2: Add and delete an incident (CRUD test)
        print("   Testing if we can add and delete incidents...")
        incident_id = insert_incident(
            "2024-11-05",  # Date
            "Test Incident",  # Type of incident
            "Low",  # How serious it is
            "Open",  # Current status
            "This is a test incident to make sure everything works",  # Description
            "test_user"  # Who reported it
        )
        
        # If we successfully added an incident...
        if incident_id:
            print(f"   CRUD Test: Created incident #{incident_id}")
            # Now delete it to clean up
            delete_incident(incident_id)
            print(f"   CRUD Test: Deleted incident #{incident_id} (cleanup)")
        
        # Show completion message
        print("\n" + "="*60)
        print("AWESOME! DATABASE SETUP IS COMPLETE!")
        print("="*60)
        print(f"\n Your database is saved here: {DATA_DIR / 'intelligence_platform.db'}")
        print("\nThe next steps for the program")
        print("• we can now Run analytics to see cool data insights")
        print("• Build a streamlit web interface (Week 9)")
        print("\nGreat job! ")

    # This line actually runs our main function
    # Everything above was just defining functions, this line EXECUTES them
    setup_database_complete()

# If anything goes wrong, this part catches the error
except Exception as e:
    print(f"\n OH NO! Something went wrong: {e}")
    print("Here's what happened:")
    import traceback
    traceback.print_exc()  # This shows the technical details of the error
    
    print("\nTroubleshooting tips for my Main.py program")
    print("1. Make sure all the files are in the right places")
    print("2. Check that that CSV files have the right column names")
    print("3. Try running: python reset_database.py to start fresh")
   