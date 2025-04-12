#!/usr/bin/env python3

import pandas as pd

def read_public_google_sheet(public_url):
    """
    Reads the contents of a publicly viewable Google Sheet into a pandas DataFrame.

    Args:
      public_url: The public URL of the Google Sheet.

    Returns:
      A pandas DataFrame containing the sheet data, or None if an error occurs.
    """
    df = None
    try:
        # The key part is to modify the URL to the CSV export format
        csv_export_url = public_url.replace('/edit#gid=', '/export?format=csv&gid=')
        csv_export_url = public_url.replace('/edit?gid=', '/export?format=csv&gid=')

        # Read the CSV data directly into a pandas DataFrame
        df = pd.read_csv(csv_export_url)
    except Exception as e:
        print(f"An error occurred: {e}")
    return df

def main(argv):
    if len(argv) > 0:
        sheet_url = argv[0]
    else:
        # Replace with the actual public URL of your Google Sheet
        sheet_url = "https://docs.google.com/spreadsheets/d/1IyUI18bP2hPjsvZhADDYe93q4QACJ97tpbn8P9CwNE0/edit?gid=0#gid=0"
    
    # Read the Google Sheet
    data_frame = read_public_google_sheet(sheet_url)
    
    # Print the DataFrame if it was read successfully
    if data_frame is not None:
        print("Contents of the Google Sheet:")
        print(data_frame)
    return

import sys
if __name__ == "__main__":
    main(sys.argv[1:])
