import pandas as pd
from tabulate import tabulate

def display_results(df):
    """Display the results with a limited number of columns sorted by nProfit in descending order."""
    if not df.empty:
        # Sort DataFrame by 'nProfit' in descending order
        df_sorted = df.sort_values(by='nProfit', ascending=False)
        
        # Select a limited number of columns to display
        columns_to_display = [
            'contractSymbol', 'ticker', 'industry', 'expiration_date', 'option_type', 'strike', 'volume', 'nProfit'
        ]
        
        # Ensure that the selected columns are present in the DataFrame
        columns_to_display = [col for col in columns_to_display if col in df_sorted.columns]
        
        df_limited = df_sorted[columns_to_display]
        
        print("Filtered Options Data with Industry Information (Highest nProfit First):\n")
        
        # Configure pandas display options for better readability
        pd.set_option('display.max_rows', 20)  # Limit the number of rows shown
        pd.set_option('display.max_columns', None)  # Show all columns
        pd.set_option('display.width', 1000)  # Set a width to handle wider tables
        pd.set_option('display.max_colwidth', 150)  # Set max column width to handle longer text

        # Print DataFrame in a tabular format using tabulate
        print(tabulate(df_limited, headers='keys', tablefmt='fancy_grid', showindex=False, numalign='right'))
    else:
        print("No records found matching the criteria.")
