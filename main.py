import yfinance as yf
import pandas as pd
import json as json
from sqlalchemy import create_engine, text
from create_tables import create_tables
import logging
from backoff import fetch_with_backoff
from greeks_calculations import calculate_delta, calculate_gamma, calculate_rho, calculate_theta, calculate_vega
import math

# Define constants
COMMISSION_PER_SHARE = 0.65  # Example commission value, adjust as needed

# Define the database file
DATABASE_FILE = 'finance_data.db'

# Create SQLAlchemy engine
engine = create_engine(f'sqlite:///{DATABASE_FILE}')

# Configure logging
logging.basicConfig(level=logging.INFO)

def save_stock_data(ticker):
    """Fetch and save stock data to the SQLite database."""
    def fetch_stock_info(ticker):
        stock = yf.Ticker(ticker)
        return stock.info

    stock_info = fetch_with_backoff(ticker, fetch_stock_info)
    if stock_info is None:
        return

    try:
        data = {
            'ticker': ticker,
            'company_name': stock_info.get('longName', 'N/A'),
            'market_cap': stock_info.get('marketCap', 0),
            'sector': stock_info.get('sector', 'N/A'),
            'industry': stock_info.get('industry', 'N/A')
        }

        df = pd.DataFrame([data])
        with engine.begin() as connection:
            # Delete existing data for the ticker
            connection.execute(text('DELETE FROM stock_data WHERE ticker = :ticker'), {'ticker': ticker})

            df.to_sql('stock_data', connection, if_exists='append', index=False)
    except Exception as e:
        logging.error(f"An error occurred while saving stock data for {ticker}: {e}")

def save_option_data(ticker):
    """Fetch and save option data to the SQLite database."""
    def fetch_option_chain(ticker):
        stock = yf.Ticker(ticker)
        expiration_dates = stock.options
        option_data = []

        # Get the most recent price from the history
        hist = stock.history(period="1d")
        stock_price = hist['Close'].iloc[-1] if not hist.empty else 0

        for date in expiration_dates:
            options = stock.option_chain(date)
            for option_type, option_df in zip(['calls', 'puts'], [options.calls, options.puts]):
                option_df['ticker'] = ticker
                option_df['expiration_date'] = date
                option_df['option_type'] = option_type
                option_df['stock_price'] = stock_price
                # Calculate the Greeks
                time_to_expiration = (pd.to_datetime(date) - pd.Timestamp.now()).days
                
                option_df['delta'] = option_df.apply(
                    lambda row: calculate_delta(
                        stock_price,
                        row['strike'],
                        time_to_expiration,
                        row['impliedVolatility'],
                        option_type
                    ),
                    axis=1
                )
                
                option_df['gamma'] = option_df.apply(
                    lambda row: calculate_gamma(
                        stock_price,
                        row['strike'],
                        time_to_expiration,
                        row['impliedVolatility']
                    ),
                    axis=1
                )
                
                option_df['rho'] = option_df.apply(
                    lambda row: calculate_rho(
                        stock_price,
                        row['strike'],
                        time_to_expiration,
                        row['impliedVolatility'],
                        option_type
                    ),
                    axis=1
                )
                
                option_df['theta'] = option_df.apply(
                    lambda row: calculate_theta(
                        stock_price,
                        row['strike'],
                        time_to_expiration,
                        row['impliedVolatility'],
                        option_type
                    ),
                    axis=1
                )
                
                option_df['vega'] = option_df.apply(
                    lambda row: calculate_vega(
                        stock_price,
                        row['strike'],
                        time_to_expiration,
                        row['impliedVolatility']
                    ),
                    axis=1
                )

                # Calculate additional option properties
                def get_value_or_zero(value):
                    """Return the value or zero if it's None."""
                    return value if value is not None else 0

                def get_percent_spread(spread, ask):
                    """Calculate the percentage spread."""
                    return (spread / get_value_or_zero(ask)) * 100 if ask > 0 else 0

                def get_diff(price1, price2):
                    """Calculate the difference between two prices."""
                    return price1 - price2

                def get_strike_diff(strike, symbol_price):
                    """Calculate the difference between strike and symbol price."""
                    return abs(strike - symbol_price)

                option_df['spread'] = option_df.apply(lambda row: get_value_or_zero(row['ask']) - get_value_or_zero(row['bid']), axis=1)
                option_df['tPrice'] = option_df.apply(lambda row: get_value_or_zero(row['bid']) + row['spread'] / 2, axis=1)
                option_df['pSpread'] = option_df.apply(lambda row: get_percent_spread(row['spread'], row['ask']), axis=1)
                option_df['priceDiff'] = option_df.apply(lambda row: get_diff(row['tPrice'], get_value_or_zero(row['lastPrice'])), axis=1)

                option_df['pProfit'] = option_df.apply(lambda row: row['tPrice'] / row['strike'], axis=1)
                option_df['nProfit'] = option_df.apply(lambda row: row['pProfit'] / math.ceil(time_to_expiration), axis=1)

                option_df['pbProfit'] = option_df.apply(lambda row: get_value_or_zero(row['bid']) / row['strike'], axis=1)
                option_df['nbProfit'] = option_df.apply(lambda row: row['pbProfit'] / math.ceil(time_to_expiration), axis=1)
                option_df['paProfit'] = option_df.apply(lambda row: get_value_or_zero(row['ask']) / row['strike'], axis=1)
                option_df['naProfit'] = option_df.apply(lambda row: row['paProfit'] / math.ceil(time_to_expiration), axis=1)

                option_df['spbProfit'] = option_df.apply(lambda row: (get_value_or_zero(row['bid']) - COMMISSION_PER_SHARE) / row['strike'], axis=1)
                option_df['snbProfit'] = option_df.apply(lambda row: row['spbProfit'] / math.ceil(time_to_expiration), axis=1)
                option_df['spaProfit'] = option_df.apply(lambda row: (get_value_or_zero(row['ask']) - COMMISSION_PER_SHARE) / row['strike'], axis=1)
                option_df['snaProfit'] = option_df.apply(lambda row: row['spaProfit'] / math.ceil(time_to_expiration), axis=1)

                option_df['strikeDiff'] = option_df.apply(lambda row: get_strike_diff(row['strike'], stock_price), axis=1)

                option_data.append(option_df[['contractSymbol', 'ticker', 'expiration_date', 'option_type', 'strike', 
                                              'lastPrice', 'lastTradeDate', 'bid', 'ask', 'volume', 'openInterest', 
                                              'stock_price', 'delta', 'gamma', 'rho', 'theta', 'vega', 
                                              'spread', 'tPrice', 'pSpread', 'priceDiff', 
                                              'pProfit', 'nProfit', 'pbProfit', 'nbProfit', 
                                              'paProfit', 'naProfit', 'spbProfit', 'snbProfit', 
                                              'spaProfit', 'snaProfit', 'strikeDiff', 'impliedVolatility']])
        return pd.concat(option_data) if option_data else None

    option_data = fetch_with_backoff(ticker, fetch_option_chain)
    if option_data is None:
        return

    logging.debug(f"Option data for {ticker}: {option_data.head()}")
    try:
        with engine.begin() as connection:
             # Delete existing data for the ticker
            connection.execute(text('DELETE FROM option_data WHERE ticker = :ticker'), {'ticker': ticker})

            option_data.to_sql('option_data', connection, if_exists='append', index=False)
            logging.info(f"Successfully saved option data for {ticker}")
    except Exception as e:
        logging.error(f"An error occurred while saving option data for {ticker}: {e}")

# Main execution
if __name__ == "__main__":
    create_tables()
    
    # List of tickers
    tickers = ['GOOG', 'AAPL', 'MSFT']
    
    # Save stock and options data to the database
    for ticker in tickers:
        save_stock_data(ticker)
        save_option_data(ticker)
