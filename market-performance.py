import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta

# Define the tickers we are interested in
TICKERS = ['QQQ', 'SPY', 'DIA']

# Define the month and day for the target date (e.g., January 2nd)
TARGET_MONTH_DAY = (1, 2)  # Target is January 2nd for all years
START_YEAR = 2014
END_YEAR = 2024

def fetch_data(year, tickers):
    """
    Fetch historical stock data for a given year, including cross-year data for accurate trading day lookups.

    @param year The target year to fetch data for.
    @param tickers A list of stock ticker symbols to fetch data for.
    @return A pandas DataFrame containing the stock data.
    """
    print(f"Fetching data for {year}...")
    start_date = f'{year - 1}-12-01'  # Start from December of the previous year
    end_date = f'{year + 1}-01-31'    # Extend into January of the next year

    # Ensure we don't fetch data beyond today's date
    today = datetime.now().date()
    if datetime.strptime(end_date, "%Y-%m-%d").date() > today:
        end_date = today.strftime('%Y-%m-%d')

    data = yf.download(tickers, start=start_date, end=end_date)['Close']
    return data

def get_previous_trading_day(target_month_day, year, data_index):
    """
    Find the most recent trading day before the target date.

    @param target_month_day A tuple containing the target month and day (e.g., (1, 2)).
    @param year The year of the target date.
    @param data_index The index of the stock data DataFrame, containing valid trading dates.
    @return A datetime object representing the previous trading day.
    """
    target_date = datetime(year, target_month_day[0], target_month_day[1]) - timedelta(days=1)
    print(f"Checking for trading day before {target_date.strftime('%Y-%m-%d')}")

    # Move backward until a valid trading day is found
    while target_date not in data_index:
        target_date -= timedelta(days=1)

    print(f"Previous valid trading day is: {target_date.strftime('%Y-%m-%d')}")
    return target_date

def get_next_trading_day(target_month_day, year, data_index):
    """
    Find the next valid trading day after the target date.

    @param target_month_day A tuple containing the target month and day (e.g., (1, 2)).
    @param year The year of the target date.
    @param data_index The index of the stock data DataFrame, containing valid trading dates.
    @return A datetime object representing the next trading day, or None if not found.
    """
    target_date = datetime(year, target_month_day[0], target_month_day[1])
    print(f"Checking for trading day after {target_date.strftime('%Y-%m-%d')}")

    # Move forward until a valid trading day is found
    while target_date not in data_index:
        target_date += timedelta(days=1)

        # Prevent looking into the future
        if target_date.date() > datetime.now().date():
            print(f"Reached the current date. No future trading days available.")
            return None

    print(f"Next valid trading day is: {target_date.strftime('%Y-%m-%d')}")
    return target_date

def calculate_percentage_changes(data, tickers, target_date):
    """
    Calculate the percentage changes in stock prices for each ticker on the given target date.

    @param data A pandas DataFrame containing stock data.
    @param tickers A list of stock ticker symbols.
    @param target_date The target date for which percentage changes are calculated.
    @return A dictionary containing percentage changes for each ticker.
    """
    percentage_changes = {ticker: [] for ticker in tickers}

    if target_date in data.index:
        # Find the previous trading day by starting one day earlier
        previous_trading_day = get_previous_trading_day((target_date.month, target_date.day), target_date.year, data.index)

        if previous_trading_day:
            # Calculate percentage changes
            for ticker in tickers:
                close_price = data[ticker].loc[target_date]
                prev_day_close = data[ticker].loc[previous_trading_day]
                percentage_change = (close_price - prev_day_close) / prev_day_close * 100
                percentage_changes[ticker].append(percentage_change)
        else:
            print(f"No valid previous trading day found for {target_date}!")
    else:
        print(f"{target_date} is not a trading day!")

    return percentage_changes

def plot_percentage_changes(percentage_changes, years, target_month_day, trading_dates):
    """
    Plot the percentage changes in stock prices for the specified years.

    @param percentage_changes A dictionary of percentage changes for each ticker.
    @param years A range of years for the plot.
    @param target_month_day A tuple containing the target month and day.
    @param trading_dates A list of trading dates for the x-axis labels.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    width = 0.2
    index = range(len(years))

    for i, ticker in enumerate(TICKERS):
        bars = ax.bar([x + i * width for x in index], percentage_changes[ticker], width=width, label=ticker)
        
        # Add labels above each bar
        for bar in bars:
            height = bar.get_height()
            if height != 0:
                ax.text(bar.get_x() + bar.get_width() / 2, height, f'{height:.2f}%', ha='center', va='bottom', fontsize=8)

    # Create the title dynamically based on TARGET_MONTH_DAY
    target_date_str = f"{['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][target_month_day[0] - 1]} {target_month_day[1]}"
    
    # Add labels and title
    ax.set_xlabel('Year and Date')
    ax.set_ylabel('Percentage Change')
    ax.set_title(f'Percentage Change for QQQ, SPY, and DIA after {target_date_str}')

    # Use trading_dates as x-axis labels
    ax.set_xticks([x + width for x in index])
    ax.set_xticklabels([
        f'{year}\n{pd.to_datetime(date).strftime("%b %d")}' if date else f'{year}\nNo Data'
        for year, date in zip(years, trading_dates)
    ])

    # Add horizontal grid lines
    ax.grid(True, axis='y', linestyle='--', alpha=0.7)
    ax.legend()
    plt.tight_layout()
    plt.show()

def main():
    """
    Main entry point of the program. Fetches data, calculates percentage changes, and plots results.
    """
    years = range(START_YEAR, END_YEAR)
    percentage_changes = {ticker: [] for ticker in TICKERS}
    trading_dates = []

    for year in years:
        data = fetch_data(year, TICKERS)
        if not data.empty:
            # Get the next trading day after the target date (month, day) for this year
            next_trading_day = get_next_trading_day(TARGET_MONTH_DAY, year, data.index)
            if next_trading_day:
                trading_dates.append(next_trading_day.strftime('%Y-%m-%d'))
                yearly_percentage_changes = calculate_percentage_changes(data, TICKERS, next_trading_day)
                for ticker in TICKERS:
                    percentage_changes[ticker].extend(yearly_percentage_changes[ticker])
        else:
            print(f"No data found for {year}!")
            trading_dates.append(None)

    plot_percentage_changes(percentage_changes, years, TARGET_MONTH_DAY, trading_dates)

if __name__ == '__main__':
    main()