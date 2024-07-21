import sqlite3
import sys

DATABASE_FILE = 'finance_data.db'

def list_tables_and_counts(connection):
    """List all tables and their row counts."""
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    table_info = []
    for table in tables:
        table_name = table[0]
        cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
        row_count = cursor.fetchone()[0]
        table_info.append((table_name, row_count))
    
    return table_info

def confirm_and_drop_table(connection, table_name, row_count):
    """Prompt user to confirm if they want to drop the table and then drop it."""
    user_input = input(f"Table '{table_name}' has {row_count} rows. Are you sure you want to remove this table? Type 'Yes' to continue: ")
    if user_input.strip().lower() == 'yes':
        cursor = connection.cursor()
        cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
        print(f"Table '{table_name}' has been removed.")
    else:
        print(f"Table '{table_name}' was not removed.")

def main():
    """Main function to handle the script logic."""
    try:
        connection = sqlite3.connect(DATABASE_FILE)
        table_info = list_tables_and_counts(connection)
        
        if not table_info:
            print("No tables found in the database.")
            return

        print("Tables in the database:")
        for table_name, row_count in table_info:
            print(f"Table: {table_name}, Rows: {row_count}")
        
        for table_name, row_count in table_info:
            confirm_and_drop_table(connection, table_name, row_count)
        
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    finally:
        if connection:
            connection.close()

if __name__ == "__main__":
    main()
