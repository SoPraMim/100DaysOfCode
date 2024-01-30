# --- Imports --- #
import os
from stock_manager import StockManager

# --- Global Variables --- #
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

# # --- Program --- #
# ## STEP 1: Use https://www.alphavantage.co
# # When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
stock_manager = StockManager(STOCK, COMPANY_NAME)
price_variation = stock_manager.check_price_variation() 
if abs(price_variation) > 0.05:
## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 
    stock_manager.request_news()
    recipients = [os.environ.get("TO_TEST_EMAIL")]

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 
    stock_manager.send_news(recipients)
    print(f"Price variation: {price_variation*100:.2f} %. \nPrice variation above 5%. Message sent.")

else:
    print(f"Price variation: {price_variation*100:.2f} %. \nPrice variation below 5%. No message sent.")