import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def migrate():
    try:
        print("Connecting to Remote Database...")
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        print("Migrating 'extra' column to INTEGER...")
        # This command converts the boolean/existing data to integer
        cursor.execute("ALTER TABLE catering_logs ALTER COLUMN extra SET DEFAULT 0;")
        cursor.execute("ALTER TABLE catering_logs ALTER COLUMN extra TYPE INTEGER USING (CASE WHEN extra='t' THEN 1 WHEN extra='f' THEN 0 ELSE extra::integer END);")
        
        conn.commit()
        print("✅ SUCCESS! Remote Database migrated. Extra meals will now count correctly (2, 3, etc.)")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("If the column was already an integer, this error is normal.")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    migrate()
