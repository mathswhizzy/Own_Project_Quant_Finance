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
