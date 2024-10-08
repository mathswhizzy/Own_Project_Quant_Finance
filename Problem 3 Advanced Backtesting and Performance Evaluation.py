
import yfinance as yf
import matplotlib.pyplot as plt
from tabulate import tabulate

# Define the ticker symbol (e.g., 'AAPL' for Apple Inc.)
ticker_symbol = 'AAPL'

# Get the stock data for the defined ticker
stock_data = yf.download(ticker_symbol, start="2024-01-01", end="2024-12-31")

# Extract the closing prices
closing_prices = stock_data['Close']

# Plot the closing prices
plt.figure(figsize=(10, 6))  # Set the size of the plot
plt.plot(closing_prices.index, closing_prices, label='Closing Price')

# Add title and labels
plt.title(f'{ticker_symbol} Closing Prices in 2022')
plt.xlabel('Date')
plt.ylabel('Closing Price (USD)')

# Rotate the x-axis labels for better readability
plt.xticks(rotation=45)

# Add a grid and a legend
plt.grid(True)
plt.legend()

# Show the plot
plt.show()

# Calculate and print the 5-number summary
min_val = round(closing_prices.min(), 2)
mean_val = round(closing_prices.mean(), 2)
median_val = round(closing_prices.median(), 2)
std_dev = round(closing_prices.std(), 2)
max_val = round(closing_prices.max(), 2)

# Create data for the table
table = [
    ["Min", min_val],
    ["Mean", mean_val],
    ["Median", median_val],
    ["Standard Deviation", std_dev],
    ["Max", max_val]
]

# Print the table
print(tabulate(table, headers=["Statistic", "Value"], tablefmt="grid"))

# Calculate 20-day simple moving average
stock_data['SMA_20'] = stock_data['Close'].rolling(window=20).mean()
print(stock_data['SMA_20'])

# Calculate Bollinger Bands
stock_data['Upper_Band'] = stock_data['SMA_20'] + (2 * stock_data['Close'].rolling(window=20).std())
stock_data['Lower_Band'] = stock_data['SMA_20'] - (2 * stock_data['Close'].rolling(window=20).std())

# Plot closing prices, SMA, and Bollinger Bands
plt.plot(stock_data['Close'], label='Closing Price')
plt.plot(stock_data['SMA_20'], label='20-Day SMA')
plt.plot(stock_data['Upper_Band'], label='Upper Bollinger Band')
plt.plot(stock_data['Lower_Band'], label='Lower Bollinger Band')
plt.legend(loc='best')
plt.title('AAPL with Bollinger Bands')
plt.show()


initial_cash = 10000
stock_data['Position'] = 0  # Position: 1 means holding the stock, 0 means no position

# Buy when price closes below lower band, sell when price closes above upper band
stock_data.loc[stock_data['Close'] < stock_data['Lower_Band'], 'Position'] = 1  # Buy signal
stock_data.loc[stock_data['Close'] > stock_data['Upper_Band'], 'Position'] = 0  # Sell signal

stock_data['Returns'] = stock_data['Close'].pct_change()
stock_data['Strategy_Returns'] = stock_data['Returns'] * stock_data['Position'].shift(1)

# Calculate cumulative returns
stock_data['Cumulative_Returns'] = (1 + stock_data['Returns']).cumprod()
stock_data['Cumulative_Strategy'] = (1 + stock_data['Strategy_Returns']).cumprod()

# Plot cumulative returns
plt.plot(stock_data['Cumulative_Returns'], label='Buy & Hold')
plt.plot(stock_data['Cumulative_Strategy'], label='Strategy')
plt.legend(loc='best')
plt.title('Cumulative Returns vs. Strategy Returns')
plt.show()

# Calculate performance metrics: total return, Sharpe ratio, max drawdown
total_return = stock_data['Cumulative_Strategy'].iloc[-1] - 1
sharpe_ratio = (stock_data['Strategy_Returns'].mean() - 0.02 / 252) / stock_data['Strategy_Returns'].std() * np.sqrt(252)
