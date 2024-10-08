################################################################################
#
#  Permission is hereby granted, free of charge, to any person obtaining a
#  copy of this software and associated documentation files (the "Software"),
#  to deal in the Software without restriction, including without limitation
#  the rights to use, copy, modify, merge, publish, distribute, sublicense,
#  and/or sell copies of the Software, and to permit persons to whom the
#  Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
#  OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.

import json
import random
import urllib.request

# Server API URLs
QUERY = "http://localhost:8080/query?id={}"

# Number of server requests
N = 500

def getDataPoint(quote):
    """ Produce all the needed values to generate a datapoint """
    stock = quote['stock']
    bid_price = float(quote['top_bid']['price'])
    ask_price = float(quote['top_ask']['price'])
    price = (bid_price + ask_price) / 2
    return stock, bid_price, ask_price, price

def getRatio(price_a, price_b):
    """ Get ratio of price_a and price_b, return None if price_b is 0 """
    if price_b == 0:
        return None  # Return None to avoid division by zero
    return price_a / price_b

# Main
if __name__ == "__main__":
    # Query the price once every N seconds.
    for _ in range(N):
        try:
            # Fetch stock data from server
            quotes = json.loads(urllib.request.urlopen(QUERY.format(random.random())).read())
        except Exception as e:
            print(f"Error fetching data: {e}")
            continue

        prices = {}

        # Process each stock quote and store the price
        for quote in quotes:
            stock, bid_price, ask_price, price = getDataPoint(quote)
            prices[stock] = price
            print(f"Quoted {stock} at (bid: {bid_price}, ask: {ask_price}, price: {price})")

        # Calculate the ratio between two stocks (e.g., 'ABC' and 'DEF')
        stock_a = 'ABC'
        stock_b = 'DEF'

        if stock_a in prices and stock_b in prices:
            ratio = getRatio(prices[stock_a], prices[stock_b])
            if ratio is None:
                print(f"Cannot calculate ratio for {stock_a} and {stock_b} due to division by zero.")
            else:
                print(f"Ratio {stock_a}/{stock_b}: {ratio}")
        else:
            print(f"Insufficient data to calculate ratio for {stock_a} and {stock_b}.")
