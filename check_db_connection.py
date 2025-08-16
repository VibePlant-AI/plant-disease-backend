# scripts/check_db_connection.py
import os
import sys
import psycopg2

# Get the database URL from the environment variable passed by the CI/CD pipeline
db_url = os.environ.get('DATABASE_URL')

if not db_url:
    print("ERROR: DATABASE_URL_CI environment variable not set.")
    sys.exit(1) # Exit with a failure code

print("Attempting to connect to the database...")

try:
    # Attempt to establish a connection.
    # We set a short timeout to fail fast if the DB is unreachable.
    conn = psycopg2.connect(db_url, connect_timeout=10)
    
    # If we get here, the connection is good.
    print("✅ SUCCESS: Connection to the PostgreSQL database was successful!")
    
    conn.close()
    sys.exit(0) # Exit with a success code

except Exception as e:
    print("❌ FAILED: Unable to connect to the database.")
    print(f"Error details: {e}")
    sys.exit(1) # Exit with a failure code