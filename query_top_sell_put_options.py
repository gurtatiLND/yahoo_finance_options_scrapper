import sqlite3
import pandas as pd
import time
from display import display_results  # Import the display_results function

# Constants
DATABASE_FILE = 'finance_data.db'

def get_passed_hours_epoch_timestamp(hours=24):
    """Get the epoch timestamp for the specified number of hours ago."""
    return int(time.time()) - 60 * 60 * hours

def query_options_data():
    """Query the options data from the database with the specified requirements and join with stock data."""
    conn = sqlite3.connect(DATABASE_FILE)

    # Calculate the timestamp for filtering
    passed_hours_timestamp = get_passed_hours_epoch_timestamp()

    # Define the SQL query with the specified requirements
    query = f"""
    SELECT o.contractSymbol, o.ticker, o.expiration_date, o.option_type, o.strike, o.lastPrice, 
           o.lastTradeDate, o.bid, o.ask, o.volume, o.openInterest, o.stock_price, o.delta, 
           o.gamma, o.rho, o.theta, o.vega, o.spread, o.tPrice, o.pSpread, o.priceDiff, 
           o.pProfit, o.nProfit, o.pbProfit, o.nbProfit, o.paProfit, o.naProfit, o.spbProfit, 
           o.snbProfit, o.spaProfit, o.snaProfit, o.strikeDiff, s.industry
    FROM option_data o
    JOIN stock_data s ON o.ticker = s.ticker
    WHERE o.option_type = 'puts'
      AND o.strikeDiff <= -0.1
      AND o.lastTradeDate >= datetime({passed_hours_timestamp}, 'unixepoch')
      AND o.stock_price < o.strike
      AND o.delta BETWEEN -0.3 AND 0
      AND o.ask > 0
      AND o.bid > 0
      AND o.spread >= 0
      AND o.pSpread <= 0.2
      AND o.tPrice >= 0.07
      AND o.nProfit >= 0.0005
      AND o.volume >= 4
      AND o.openInterest >= 4
      AND o.impliedVolatility >= 0.01
      AND o.priceDiff <= 0.15
    """

    # Execute the query and fetch the results
    df = pd.read_sql_query(query, conn)

    # Close the connection
    conn.close()

    return df

if __name__ == "__main__":
    results_df = query_options_data()
    display_results(results_df)
