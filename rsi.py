import pandas as pd

def calculate_rsi(data, window=14):
    """
    Calculates the Relative Strength Index (RSI) for a given DataFrame.

    Args:
        data (pd.DataFrame): DataFrame with at least a '<CLOSE>' column.
        window (int): The lookback period for RSI calculation. Defaults to 14.

    Returns:
        pd.DataFrame: DataFrame with an added 'RSI' column.
    """
    df = data.copy()
    
    # Calculate price changes
    df['PriceChange'] = df['<CLOSE>'].diff()

    # Separate gains and losses
    df['Gain'] = df['PriceChange'].apply(lambda x: x if x > 0 else 0)
    df['Loss'] = df['PriceChange'].apply(lambda x: abs(x) if x < 0 else 0)

    # Calculate average gain and loss using Wilder's smoothing method
    # This is a common way to calculate RSI, which is similar to EMA but slightly different
    # For a simpler EMA calculation, you can use df['Gain'].ewm(com=window-1, adjust=False).mean()
    
    # Initialize first average gain and loss
    avg_gain = df['Gain'].rolling(window=window).mean()
    avg_loss = df['Loss'].rolling(window=window).mean()

    # Calculate subsequent averages
    for i in range(window, len(df)):
        avg_gain[i] = (avg_gain[i-1] * (window-1) + df['Gain'][i]) / window
        avg_loss[i] = (avg_loss[i-1] * (window-1) + df['Loss'][i]) / window

    df['AvgGain'] = avg_gain
    df['AvgLoss'] = avg_loss
    
    # Calculate Relative Strength (RS)
    # Avoid division by zero if AvgLoss is 0
    df['RS'] = df['AvgGain'] / df['AvgLoss'].replace(0, 1e-9) # Adding a small epsilon to prevent division by zero

    # Calculate RSI
    df['RSI'] = 100 - (100 / (1 + df['RS']))

    # Handle cases where AvgLoss is 0 (RSI should be 100)
    df.loc[df['AvgLoss'] == 0, 'RSI'] = 100
    # Handle cases where AvgGain is 0 (RSI should be 0)
    df.loc[df['AvgGain'] == 0, 'RSI'] = 0
    
    # Drop intermediate columns if you want a cleaner DataFrame
    df = df.drop(columns=['PriceChange', 'Gain', 'Loss', 'AvgGain', 'AvgLoss', 'RS'])
    
    return df

# --- Main execution ---
try:
    # Load the dataset
    df = pd.read_csv('Iran.Khodro.csv')

    # It's good practice to sort by date to ensure correct calculation
    # Assuming '<DTYYYYMMDD>' is the date column and needs to be converted to datetime objects
    df['<DTYYYYMMDD>'] = pd.to_datetime(df['<DTYYYYMMDD>'], format='%Y%m%d')
    df = df.sort_values(by='<DTYYYYMMDD>', ascending=True) # Ascending for chronological order

    # Calculate RSI(14)
    df_with_rsi = calculate_rsi(df, window=14)

    # Display the first 20 rows with the new RSI column
    # RSI will have NaN values for the first 'window' periods as it needs historical data
    print(df_with_rsi[['<DTYYYYMMDD>', '<CLOSE>', 'RSI']].head(20).to_markdown(index=False))

    # If you want to save the dataframe with RSI:
    # df_with_rsi.to_csv('Iran.Khodro_with_RSI.csv', index=False)
    # print("\nDataFrame with RSI saved to 'Iran.Khodro_with_RSI.csv'")

except FileNotFoundError:
    print("Error: Iran.Khodro.csv not found. Please make sure the file is in the correct directory.")
except KeyError as e:
    print(f"Error: Missing expected column - {e}. Please check the CSV column names.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
