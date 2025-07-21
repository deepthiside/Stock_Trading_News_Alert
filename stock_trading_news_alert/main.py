import requests
from datetime import datetime
# from twilio.rest import Client  # Uncomment when using SMS

# === Constants ===
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
ALPHAVANTAGE_API_KEY = "9N0V03YWMTPSTFN8"
NEWS_API_KEY = "79800b6f5c1447c09d695e815b144303"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

# === Twilio Config (Commented for now) ===
# TWILIO_SID = "ACcae9bf5*********affdf16f3f67a24b"
# TWILIO_AUTH_TOKEN = "95797c8c6db******77436ac5d9f80c3"
# TWILIO_PHONE_NUMBER = "+1845***5609"
# MY_PHONE_NUMBER = "+91 958***0269"

# === Get Stock Data ===
stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": ALPHAVANTAGE_API_KEY
}

try:
    stock_response = requests.get(STOCK_ENDPOINT, params=stock_params)
    stock_response.raise_for_status()
    data = stock_response.json().get("Time Series (Daily)", {})
    sorted_dates = sorted(data.keys(), reverse=True)

    if len(sorted_dates) < 2:
        print("❌ Not enough stock data available.")
        exit()

    yesterday = sorted_dates[0]
    day_before = sorted_dates[1]
    close_yesterday = float(data[yesterday]["4. close"])
    close_day_before = float(data[day_before]["4. close"])

    difference = close_yesterday - close_day_before
    percent_change = (abs(difference) / close_day_before) * 100
    arrow = "🔺" if difference > 0 else "🔻"

    print("\n📊 STOCK UPDATE")
    print(f"{yesterday}: ${close_yesterday}")
    print(f"{day_before}: ${close_day_before}")
    print(f"Change: {arrow} {percent_change:.2f}%")

    if percent_change >= 3:
        news_params = {
            "qInTitle": COMPANY_NAME,
            "apiKey": NEWS_API_KEY,
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": 3
        }

        news_response = requests.get(NEWS_ENDPOINT, params=news_params)
        news_response.raise_for_status()
        articles = news_response.json().get("articles", [])

        print("\n📰 RELEVANT NEWS:")
        formatted_articles = []

        for i, article in enumerate(articles[:3], start=1):
            title = article.get("title", "No title")
            desc = article.get("description", "No description")
            message = f"{STOCK_NAME}: {arrow}{percent_change:.2f}%\nHeadline: {title}\nBrief: {desc}"
            formatted_articles.append(message)

            print(f"\n📌 Article {i}")
            print(f"Headline: {title}")
            print(f"Brief: {desc}")

        # === Twilio Messaging (Uncomment to send SMS) ===
        """
        client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
        for msg in formatted_articles:
            sms = client.messages.create(
                body=msg,
                from_=TWILIO_PHONE_NUMBER,
                to=MY_PHONE_NUMBER
            )
            print(f"✅ SMS sent: {sms.sid}")
        """
    else:
        print("\nℹ️ Change < 3% — no news fetched.")

except requests.exceptions.RequestException as e:
    print(f"\n❌ API Request failed: {e}")
except Exception as e:
    print(f"\n❌ Unexpected error: {e}")
