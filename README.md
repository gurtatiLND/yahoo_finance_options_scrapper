# Finance Data Analysis

## Overview

This project retrieves, processes, and analyzes financial data, focusing on options trading. The project consists of several Python scripts for fetching data, calculating Greek metrics, managing the database, and displaying results.

## Project Files

- **`main.py`** The main script for fetching data from Yahoo Finance and saving it to an SQLite database. It handles both stock and options data, applies calculations for various Greek metrics, and stores the results in the database.
- **`calc_stats.py`** Contains functions for calculating various database statistical metrics.
- **`show_sample_data.py`** Used to display a sample of the data stored in the SQLite database. This script helps in inspecting the data and ensuring that it has been correctly saved and formatted.
- **`cleanup_database.py`** Responsible for performing general cleanup operations on the SQLite database.
- **`cleanup_expired_options.py`** Specifically targets the cleanup of expired options data from the database.
- **`remove_tables.py`** Provides functionality to remove specific tables from the SQLite database. This can be useful when restructuring the database schema or when certain tables are no longer needed.
- **`create_tables.py`** Contains the schema definitions and SQL commands to create the necessary tables in the SQLite database.
- **`greek_calculation.py`** Implements functions to calculate the Greek metrics for financial options. This includes Delta, Gamma, Theta, Vega, and Rho, which are crucial for options trading and analysis.

## Prerequisites

- Python 3.6+

## Setup Instructions

### 1. Create a Virtual Environment (Optional but Recommended)

```bash
python -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`
```

### 2. Install Dependencies

Ensure you have requests, youtube-transcript-api, and nltk installed:

```bash
pip install -r requirements.txt
```
### 3. Load financel data

```bash
python main.py
INFO:root:Successfully saved option data for GOOG
INFO:root:Successfully saved option data for AAPL
INFO:root:Successfully saved option data for MSFT
```

### 4. Prepare query or use existing one

```bash
python query_all_sell_put_options.py
Filtered Options Data with Industry Information (Highest nProfit First):

╒═════════════════════╤══════════╤════════════════════════════════╤═══════════════════╤═══════════════╤══════════╤══════════╤═════════════╕
│ contractSymbol      │ ticker   │ industry                       │ expiration_date   │ option_type   │   strike │   volume │     nProfit │
╞═════════════════════╪══════════╪════════════════════════════════╪═══════════════════╪═══════════════╪══════════╪══════════╪═════════════╡
│ GOOG240726P00235000 │ GOOG     │ Internet Content & Information │ 2024-07-26        │ puts          │      235 │        1 │   0.0587234 │
├─────────────────────┼──────────┼────────────────────────────────┼───────────────────┼───────────────┼──────────┼──────────┼─────────────┤
│ AAPL240726P00285000 │ AAPL     │ Consumer Electronics           │ 2024-07-26        │ puts          │      285 │        2 │   0.0532895 │
├─────────────────────┼──────────┼────────────────────────────────┼───────────────────┼───────────────┼──────────┼──────────┼─────────────┤
│ GOOG240726P00225000 │ GOOG     │ Internet Content & Information │ 2024-07-26        │ puts          │      225 │       10 │   0.0502222 │
├─────────────────────┼──────────┼────────────────────────────────┼───────────────────┼───────────────┼──────────┼──────────┼─────────────┤
│ AAPL240726P00280000 │ AAPL     │ Consumer Electronics           │ 2024-07-26        │ puts          │      280 │        3 │   0.0497768 │
├─────────────────────┼──────────┼────────────────────────────────┼───────────────────┼───────────────┼──────────┼──────────┼─────────────┤

```


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


## Setup and Installation