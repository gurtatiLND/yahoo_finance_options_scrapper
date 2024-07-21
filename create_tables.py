from sqlalchemy import create_engine, text

DATABASE_FILE = 'finance_data.db'
engine = create_engine(f'sqlite:///{DATABASE_FILE}')

def create_tables():
    """Create or update database tables with comments for each field."""
    with engine.begin() as connection:
        # Create or update stock_data table
        connection.execute(text('''
            CREATE TABLE IF NOT EXISTS stock_data (
                ticker TEXT PRIMARY KEY,           -- Stock ticker symbol
                company_name TEXT,                 -- Name of the company
                market_cap INTEGER,                -- Market capitalization of the company
                sector TEXT,                       -- Sector of the company
                industry TEXT                      -- Industry of the company
            )
        '''))

        # Create or update option_data table
        connection.execute(text('''
            CREATE TABLE IF NOT EXISTS option_data (
                contractSymbol TEXT PRIMARY KEY,  -- Option ticker symbol [x]
                ticker TEXT,                      -- Stock ticker symbol [x]
                expiration_date TEXT,             -- Expiration date of the option [x]
                option_type TEXT,                 -- Type of the option ('call' or 'put') [x]
                strike REAL,                      -- Strike price of the option [x]
                lastPrice REAL,                   -- Last traded price of the option [x]
                lastTradeDate TEXT,               -- Last trade date of the option [x]
                bid REAL,                         -- Bid price of the option [x]
                ask REAL,                         -- Ask price of the option [x]
                volume INTEGER,                   -- Trading volume of the option [x]
                openInterest INTEGER,             -- Open interest of the option [x]
                stock_price REAL,                 -- Stock price [x]
                impliedVolatility REAL,           -- Implied Volatility [x]
                strikeDiff REAL,                  -- Strike difference [x]
                tPrice REAL,                      -- Theoretical price of the option
                priceDiff REAL,                   -- Percent difference between theoretical price and last market price
                spread REAL,                      -- Difference between ask and bid prices
                pSpread REAL,                     -- Percent spread relative to the ask price
                daysLeft INTEGER,                 -- Number of days left until expiration
                pProfit REAL,                     -- Profit based on theoretical price, normalized by the number of days
                nProfit REAL,                     -- Normalized profit based on theoretical price
                pbProfit REAL,                    -- Profit based on bid price
                nbProfit REAL,                    -- Normalized profit based on bid price
                paProfit REAL,                    -- Profit based on ask price
                naProfit REAL,                    -- Normalized profit based on ask price
                spbProfit REAL,                   -- Profit based on bid price after commission
                snbProfit REAL,                   -- Normalized profit based on bid price after commission
                spaProfit REAL,                   -- Profit based on ask price after commission
                snaProfit REAL,                   -- Normalized profit based on ask price after commission
                delta REAL,                       -- Delta Greek for the option
                gamma REAL,                       -- Gamma Greek for the option
                rho REAL,                         -- Rho Greek for the option
                theta REAL,                       -- Theta Greek for the option
                vega REAL                         -- Vega Greek for the option
            )
        '''))
