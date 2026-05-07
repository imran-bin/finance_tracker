import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def check_schema():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        cursor.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'catering_logs'")
        columns = cursor.fetchall()
        
        if not columns:
            print("Table 'catering_logs' not found!")
        else:
            print("Columns in 'catering_logs':")
            for col in columns:
                print(f"- {col[0]} ({col[1]})")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    check_schema()
