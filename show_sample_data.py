# show_sample_data.py

from sqlalchemy import create_engine, text
import json

# Define the database file
DATABASE_FILE = 'finance_data.db'

# Create SQLAlchemy engine
engine = create_engine(f'sqlite:///{DATABASE_FILE}')

def fetch_sample_data():
    """Fetch one sample row from each table and print the results."""
    with engine.connect() as conn:
        # Fetch one row from stock_data
        stock_data_result = conn.execute(text("SELECT * FROM stock_data LIMIT 1"))
        stock_data_sample = stock_data_result.fetchone()
        if stock_data_sample:
            stock_data_dict = {column: value for column, value in zip(stock_data_result.keys(), stock_data_sample)}
            print("Sample row from stock_data:")
            print(json.dumps(stock_data_dict, indent=4))
        else:
            print("No data found in stock_data table.")

        # Fetch one row from option_data
        option_data_result = conn.execute(text("SELECT * FROM option_data LIMIT 1"))
        option_data_sample = option_data_result.fetchone()
        if option_data_sample:
            option_data_dict = {column: value for column, value in zip(option_data_result.keys(), option_data_sample)}
            print("\nSample row from option_data:")
            print(json.dumps(option_data_dict, indent=4))
        else:
            print("No data found in option_data table.")

# Main execution
if __name__ == "__main__":
    fetch_sample_data()
