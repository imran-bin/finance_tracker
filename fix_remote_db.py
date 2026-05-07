import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def fix_schema():
    try:
        print("Connecting to Remote Database...")
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        print("Adding 'extra' and 'extra_food' columns...")
        # Add columns if they don't exist
        cursor.execute("ALTER TABLE catering_logs ADD COLUMN IF NOT EXISTS extra INTEGER DEFAULT 0;")
        cursor.execute("ALTER TABLE catering_logs ADD COLUMN IF NOT EXISTS extra_food VARCHAR;")
        
        conn.commit()
        print("✅ SUCCESS! Columns added to 'catering_logs'. Extra meals will now save correctly.")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    fix_schema()
