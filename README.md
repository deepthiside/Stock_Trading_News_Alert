📈 Stock Price & News Alert
A Python script that checks the stock price of a company (like Tesla), and if there's a big change (±3%), it fetches top 3 news articles about the company.

Optional: You can also send the news via SMS using Twilio.

⚙️ Features
Gets latest stock data (via Alpha Vantage)

Gets news if stock changes ≥ 3% (via NewsAPI)

Shows output in the terminal

(Optional) Sends SMS alerts via Twilio (commented in code)

▶️ How to Run
Add your API keys in the script

Install required packages
pip install requests twilio

Run the script
python stock_news_alert.py

📝 Optional
To send SMS alerts, add your Twilio credentials and uncomment the code block.
