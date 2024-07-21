# cleanup_database.py

from sqlalchemy import create_engine, text

# Define the database file
DATABASE_FILE = 'finance_data.db'

# Create SQLAlchemy engine
engine = create_engine(f'sqlite:///{DATABASE_FILE}')

def cleanup_database():
    """Delete all entries from the stock_data and option_data tables."""
    with engine.connect() as conn:
        # Delete all rows from stock_data
        conn.execute(text("DELETE FROM stock_data"))
        # Delete all rows from option_data
        conn.execute(text("DELETE FROM option_data"))
        # Commit the transaction
        conn.commit()
        print("Database cleaned up successfully.")

# Main execution
if __name__ == "__main__":
    cleanup_database()
