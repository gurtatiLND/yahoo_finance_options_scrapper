import sqlite3

# Define the database file
DATABASE_FILE = 'finance_data.db'

def inspect_database():
    """Fetch and print data from the 'option_data' table in the SQLite database."""
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        
        # Query to fetch all rows from the 'option_data' table
        query = 'SELECT * FROM option_data'
        cursor.execute(query)
        
        # Fetch all rows from the query result
        rows = cursor.fetchall()
        
        # Print column names
        column_names = [description[0] for description in cursor.description]
        print(f"{' | '.join(column_names)}")
        print('-' * (len(column_names) * 20))
        
        # Print each row
        for row in rows:
            print(' | '.join(map(str, row)))
        
        # Close the database connection
        conn.close()
    
    except sqlite3.Error as e:
        print(f"An error occurred while accessing the database: {e}")

if __name__ == "__main__":
    inspect_database()
