import time
import logging

def fetch_with_backoff(ticker, func, max_retries=5, initial_wait=1, max_wait=16):
    """Fetch data with exponential backoff in case of failure."""
    attempt = 0
    while attempt < max_retries:
        try:
            return func(ticker)
        except Exception as e:
            attempt += 1
            wait_time = min(initial_wait * (2 ** (attempt - 1)), max_wait)
            logging.error(f"Attempt {attempt} failed for {ticker}: {e}. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
    logging.error(f"Failed to fetch data for {ticker} after {max_retries} attempts.")
    return None
