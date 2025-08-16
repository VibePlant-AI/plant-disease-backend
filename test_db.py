# test_db.py
import psycopg2
from dotenv import load_dotenv
import os

# Load the environment variables from your .env file
load_dotenv()

# Get the full database URL from the environment
db_url = os.environ.get('DATABASE_URL')

if not db_url:
    print("❌ ERROR: DATABASE_URL not found in .env file. Please check your .env file.")
else:
    print(f"Attempting to connect to the database...")
    print(f"Connection URL found: {db_url[:db_url.find('@')]}:********@{db_url[db_url.find('@')+1:]}") # Print URL safely

    try:
        # Attempt to establish a connection
        # psycopg2 can parse the full URL directly
        conn = psycopg2.connect(db_url)

        # If the connection is successful, print a success message
        print("\n✅ SUCCESS: Connection to the PostgreSQL database was successful!")

        # You can optionally execute a simple query to be 100% sure
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        print(f"PostgreSQL Database Version: {db_version[0]}")

        # Close the connection
        cursor.close()
        conn.close()
        print("Connection closed.")

    except Exception as e:
        # If the connection fails, print a detailed error message
        print("\n❌ FAILED: Unable to connect to the database.")
        print(f"\nDETAILS:")
        print(e)
        print("\n--- TROUBLESHOOTING ---")
        print("1. Is the database status 'Available' in the AWS RDS Console?")
        print("2. Is the database set to 'Publicly accessible: Yes'?")
        print("3. Does the database's Security Group have an Inbound Rule for 'PostgreSQL' from 'My IP'?")
        print("4. Does the Route Table for the database's Subnet have a route for 0.0.0.0/0 to an Internet Gateway?")
        print("5. Are the username, password, host, and database name in your .env file's DATABASE_URL correct?")