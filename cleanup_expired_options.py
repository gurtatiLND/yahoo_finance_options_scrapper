import pandas as pd
from sqlalchemy import create_engine, text
from datetime import datetime
import logging

# Define the database file
DATABASE_FILE = 'finance_data.db'

# Create SQLAlchemy engine
engine = create_engine(f'sqlite:///{DATABASE_FILE}')

# Configure logging
logging.basicConfig(level=logging.INFO)

def cleanup_expired_options():
    """Remove expired options from the SQLite database."""
    try:
        # Get the current date
        today = datetime.now().date()

        with engine.connect() as connection:
            # Query to delete expired options
            delete_query = text('DELETE FROM option_data WHERE expiration_date < :today')
            result = connection.execute(delete_query, {'today': today})

            logging.info(f"Deleted {result.rowcount} expired options.")

    except Exception as e:
        logging.error(f"An error occurred while cleaning up expired options: {e}")

# Main execution
if __name__ == "__main__":
    cleanup_expired_options()
