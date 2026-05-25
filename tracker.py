import requests
from bs4 import BeautifulSoup
import os


# ✅ Telegram function
def send_telegram(message):
    token = os.getenv("BOT_TOKEN")
    chat_id = os.getenv("CHAT_ID")

    print("TOKEN:", token)
    print("CHAT_ID:", chat_id)
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"

    data = {
        "chat_id": chat_id,
        "text": message
    }

    requests.post(url, data=data)


# ✅ Add your products here
PRODUCTS = [
    {
        "name": "Monitor",
        "url": "https://www.amazon.in/dp/B0DKFDM413"
    },
    {
        "name": "Another Product",
        "url": "https://amzn.in/d/0d5XmS8m"
    }
]


headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
}


# ✅ Get price function
def get_price(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    price = soup.find("span", {"class": "a-price-whole"})

    if price:
        clean_price = price.text.replace(",", "").replace(".", "")
        return int(clean_price)
    return None


# ✅ Main logic
def main():
    for product in PRODUCTS:
        name = product["name"]
        url = product["url"]

        current_price = get_price(url)

        if current_price is None:
            print(f"Couldn't fetch price for {name}")
            continue

        filename = f"{name}.txt"

        if os.path.exists(filename):
            with open(filename, "r") as f:
                old_price = int(f.read())

            if True:
                msg = f"🔥 {name} test alert\nPrice: ₹{current_price}\n{url}"
                send_telegram(msg)

        else:
            print(f"First time tracking {name}")

        with open(filename, "w") as f:
            f.write(str(current_price))

        print(f"{name} current price: {current_price}")


if __name__ == "__main__":
    main()
send_telegram("Test alert working")
