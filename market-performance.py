import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta

# Define the tickers we are interested in
TICKERS = ['QQQ', 'SPY', 'DIA']

# Define the month and day for the target date (e.g., December 25)
TARGET_MONTH_DAY = (12, 25)  # Target is December 25 for all years
START_YEAR = 2014
END_YEAR = 2024

# Function to fetch data for all tickers in a given year
def fetch_data(year, tickers):
    print(f"Fetching data for {year}...")
    data = yf.download(tickers, start=f'{year}-01-01', end=f'{year}-12-31')['Close']
    return data

# Function to find the next valid trading day after the given target date (month, day)
def get_next_trading_day(target_month_day, year, data_index):
    target_date = datetime(year, target_month_day[0], target_month_day[1])
    print(f"Checking for trading day after {target_date.strftime('%Y-%m-%d')}")
    
    # Ensure we are checking weekends, just to be thorough
    while target_date not in data_index:
        target_date += timedelta(days=1)  # Check the next day
    
    print(f"Next valid trading day is: {target_date.strftime('%Y-%m-%d')}")
    return target_date

# Function to calculate percentage change for each ticker on the next trading day after the target date
def calculate_percentage_changes(data, tickers, target_date):
    percentage_changes = {ticker: [] for ticker in tickers}
    
    if target_date in data.index:
        for ticker in tickers:
            close_price = data[ticker].loc[target_date]
            prev_day_close = data[ticker].iloc[data.index.get_loc(target_date) - 1]
            percentage_change = (close_price - prev_day_close) / prev_day_close * 100
            percentage_changes[ticker].append(percentage_change)
    return percentage_changes

# Function to plot the percentage changes for each ticker
def plot_percentage_changes(percentage_changes, years, target_month_day):
    fig, ax = plt.subplots(figsize=(10, 6))
    width = 0.2  # width of the bars
    years_list = list(years)
    index = range(len(years_list))

    # Plot bars for each ticker
    for i, ticker in enumerate(TICKERS):
        ax.bar([x + i * width for x in index], percentage_changes[ticker], width=width, label=ticker)

    # Create the title dynamically based on TARGET_MONTH_DAY
    target_date_str = f"{['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][target_month_day[0] - 1]} {target_month_day[1]}"
    
    # Add labels and title
    ax.set_xlabel('Year')
    ax.set_ylabel('Percentage Change')
    ax.set_title(f'Percentage Change for QQQ, SPY, and DIA after {target_date_str}')
    ax.set_xticks([x + width for x in index])
    ax.set_xticklabels([f'{year}' for year in years_list])

    # Set y-ticks to show increments of 0.25%
    ax.set_yticks([x * 0.25 for x in range(int(min(min(percentage_changes[ticker] for ticker in TICKERS)) // 0.25), 
                                        int(max(max(percentage_changes[ticker] for ticker in TICKERS)) // 0.25) + 1)])

    # Add horizontal grid lines
    ax.grid(True, axis='y', linestyle='--', alpha=0.7)

    ax.legend()

    # Add the percentage labels inside the bars
    for i, ticker in enumerate(TICKERS):
        for j, percentage in enumerate(percentage_changes[ticker]):
            ax.text(index[j] + i * width, percentage + 0.1, f'{percentage:.2f}%', ha='center')

    # Display the plot
    plt.tight_layout()
    plt.show()

# Main function to orchestrate the entire process
def main():
    years = range(START_YEAR, END_YEAR)
    percentage_changes = {ticker: [] for ticker in TICKERS}

    for year in years:
        data = fetch_data(year, TICKERS)
        if not data.empty:
            # Get the next trading day after the target date (month, day) for this year
            next_trading_day = get_next_trading_day(TARGET_MONTH_DAY, year, data.index)
            yearly_percentage_changes = calculate_percentage_changes(data, TICKERS, next_trading_day)
            for ticker in TICKERS:
                percentage_changes[ticker].extend(yearly_percentage_changes[ticker])
        else:
            print(f"No data found for {year}!")

    # Plot the results with the updated title
    plot_percentage_changes(percentage_changes, years, TARGET_MONTH_DAY)

if __name__ == '__main__':
    main()
