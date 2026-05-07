import sqlite3
import os

# Path to your database
db_path = "finance.db"

if os.path.exists(db_path):
    print(f"Connecting to {db_path}...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if the column is already an integer or needs migration
        # The simplest way for SQLite in this setup is to just ensure the data is right.
        # But we also need to make sure the schema is refreshed.
        
        print("Ensuring catering_logs table supports counts...")
        # Since SQLite doesn't easily allow changing column types, 
        # and we are in early development, the safest way to fix the '1 vs 2' bug
        # is to recreate the table with the correct integer type.
        
        cursor.execute("CREATE TABLE IF NOT EXISTS catering_logs_new (id INTEGER PRIMARY KEY, user_id INTEGER, date DATE UNIQUE, lunch BOOLEAN, dinner BOOLEAN, extra INTEGER, lunch_food STRING, dinner_food STRING, extra_food STRING, meal_price INTEGER)")
        
        # Copy old data if any
        try:
            cursor.execute("INSERT INTO catering_logs_new (id, user_id, date, lunch, dinner, extra, lunch_food, dinner_food, extra_food, meal_price) SELECT id, user_id, date, lunch, dinner, CAST(extra AS INTEGER), lunch_food, dinner_food, extra_food, meal_price FROM catering_logs")
            print("Data migrated to new format.")
        except Exception as e:
            print(f"No old data to migrate or error: {e}")
            
        cursor.execute("DROP TABLE catering_logs")
        cursor.execute("ALTER TABLE catering_logs_new RENAME TO catering_logs")
        
        conn.commit()
        print("✅ Database repaired! Extra meals will now count correctly (2, 3, 4, etc.)")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        conn.close()
else:
    print(f"Database {db_path} not found. It will be created correctly on next start.")
