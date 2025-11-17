from app.data.db import connect_database
from app.data.schema import create_all_tables
from app.services.user_service import migrate_users_from_file, register_user, login_user
from app.data.incidents import load_all_csv_data, insert_incident, get_all_incidents, update_incident_status, delete_incident
from app.data.datasets import get_all_datasets
from app.data.tickets import get_all_tickets
#These import modules from the necessary files to set up our databse and test its functions.

def setup_database():
    """This is my Complete database setup for Week 8 of my Coursework."""
    print("Starting Complete Database Setup for CW2 Week 8.")
    
    # The first thing we need to do is Connect to database
    conn = connect_database()
    
    # After connecting to the database with conn = connect_database, we have to Create all tables
    create_all_tables(conn)
    
    # The next step after the tables is to Migrate users from users.txt from week 7.
    migrate_users_from_file()
    
    # Thdn after that I have to Load CSV data
    load_all_csv_data(conn)
    
    # Close connection
    conn.close()
    
    print("Database setup is complete!")

def test_authentication():
    """I must Test user authentication First."""
    print("\nTesting Authentication.")
    
    # Now I must Test registration
    success, message = register_user("test_user", "password123", "user")
    print(f"Register: {message}")
    
    # Okay now we must Test login
    success, message = login_user("test_user", "password123")
    print(f"Login: {message}")

def test_crud_operations():
    """Test CRUD operations."""
    print("\nTesting CRUD Operations...")
    
    # This makes sure I use the correct column names that exist in the database schema.
    # Create
    incident_id = insert_incident(
        "2024-11-05 12:00:00",
        "High", 
        "Phishing",
        "Open",
        "Test incident for CRUD operations"
    )
    print(f"Create: Incident #{incident_id} created")
    
    # Read
    incidents = get_all_incidents()
    print(f"Read: Found {len(incidents)} incidents")
    
    # Update
    update_incident_status(incident_id, "Resolved")
    print(f"Update: Incident #{incident_id} status updated")
    
    # Delete
    delete_incident(incident_id)
    print(f"Delete: Incident #{incident_id} deleted")

def show_database_status():
    """It is now wise for me to Show the current database status."""
    print("\nDatabase Status:")
    
    conn = connect_database()
    cursor = conn.cursor()
    
    tables = ['users', 'cyber_incidents', 'datasets_metadata', 'it_tickets']
    
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"   {table}: {count} rows")
    
    conn.close()

if __name__ == "__main__":
    print("=" * 50)
    print("   INTELLIGENCE PLATFORM - WEEK 8 SETUP")
    print("=" * 50)
    
    setup_database()
    test_authentication()
    test_crud_operations()
    show_database_status()
    
    print("\nWeek 8 Lab Complete! Ready for my Week 9 Streamlit!")
    print("The database is at: DATA/intelligence_platform.db")