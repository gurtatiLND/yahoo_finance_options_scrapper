import sqlite3
from sqlalchemy import create_engine, text
import pandas as pd
from datetime import datetime

# Define the database file
DATABASE_FILE = 'finance_data.db'

# Create SQLAlchemy engine
engine = create_engine(f'sqlite:///{DATABASE_FILE}')

def get_statistics():
    """Fetch statistics from the SQLite database."""
    with engine.connect() as conn:
        # Count the number of options
        options_count = conn.execute(text("SELECT COUNT(*) FROM option_data")).scalar()

        # Count the number of distinct stocks
        stocks_count = conn.execute(text("SELECT COUNT(DISTINCT ticker) FROM option_data")).scalar()

        # Count the number of non-expired options
        today = datetime.today().strftime('%Y-%m-%d')
        non_expired_options_count = conn.execute(
            text("SELECT COUNT(*) FROM option_data WHERE expiration_date >= :today"),
            {'today': today}
        ).scalar()

        # Calculate the percentage of non-expired options
        if options_count > 0:
            non_expired_percentage = (non_expired_options_count / options_count) * 100
        else:
            non_expired_percentage = 0

    return options_count, stocks_count, non_expired_options_count, non_expired_percentage

# Main execution
if __name__ == "__main__":
    options_count, stocks_count, non_expired_options_count, non_expired_percentage = get_statistics()
    
    print(f"Total number of options in the database: {options_count}")
    print(f"Number of distinct stocks: {stocks_count}")
    print(f"Number of non-expired options: {non_expired_options_count}")
    print(f"Percentage of non-expired options: {non_expired_percentage:.2f}%")
