import requests
from bs4 import BeautifulSoup
import os


# ✅ Telegram function
def send_telegram(message):
    token = os.getenv("BOT_TOKEN")
    chat_id = os.getenv("CHAT_ID")

     # Debug (optional)
    print("TOKEN:", token)
    print("CHAT_ID:", chat_id)

    
    if not token or not chat_id:
        print("Missing Telegram credentials")
        return
    
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
        "url": "https://www.amazon.in/Lenovo-Monitor-FreeSync-Speakers-1xUSB-C/dp/B0DKFDM413/ref=sr_1_2?crid=2UBUMG3C43MIN&dib=eyJ2IjoiMSJ9.9X7DWuVfXeHT5PHgq_UkVvBc-MbnQb6IAaXdZkM0sQ4-J4u92lXVwGk1EvnwSQUMNdCnNLRxU6iiVY9er7CHbrydxnIHiDJ5XH9hZYBEQ4n6qmxShlk9SlrZGCp_8xx8PAIJ2ibmP9BeTup-JyyZtvVgCAOTC-PLqDosJKTcQQMoQi4LiRMOlQiUxE7HYH0VOJgm8RY8b6ysgYTk8RcrDB095az6dzn4B9LrQ8siMxkUsXD1zv4H-wZgwo3pSfqEU-iupml-NWgqTiAiazrkt5GrAR6Lnu_7xQ-RhbEkN4I.dZe2Y_Wzvz0LKPzZIB4MwyXTjF6ZdbZdD2Fh-xZN5DU&dib_tag=se&keywords=L27h-4A&qid=1779719373&s=computers&sprefix=l27h-4a%2Ccomputers%2C411&sr=1-2&th=1"
    },
    {
        "name": "Another Product",
        "url": "https://www.amazon.in/dp/B0BJMJ4ZQP?ref=cm_sw_r_cp_ud_dp_0GZRHESGTDZ5XSCAYK43&ref_=cm_sw_r_cp_ud_dp_0GZRHESGTDZ5XSCAYK43&social_share=cm_sw_r_cp_ud_dp_0GZRHESGTDZ5XSCAYK43&th=1"
    }
]


headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Accept-Language": "en-US,en;q=0.9"
}


# ✅ Get price function
def get_price(url):
    try:
        response = requests.get(url, headers=headers, timeout=10)

        print("STATUS:", response.status_code)
        print(response.text[:1000])

        soup = BeautifulSoup(response.content, "html.parser")

        price = soup.find("span", {"class": "a-price-whole"})

        if price:
            clean_price = price.text.replace(",", "").replace(".", "")
            return int(clean_price)

        print("Price not found in HTML")
        return None

    except Exception as e:
        print("Error fetching price:", e)
        return None        

# ✅ Main logic

def main():
    for product in PRODUCTS:
        name = product["name"]
        url = product["url"]

        current_price = get_price(url)

        if current_price is None:
            print(f"Couldn't fetch price for {name}")

            # ✅ TEST MESSAGE (so you know Telegram works)
            send_telegram(f"⚠️ Failed to fetch price for {name}")
            continue

        filename = f"{name}.txt"

        if os.path.exists(filename):
            with open(filename, "r") as f:
                old_price = int(f.read())

            # ✅ For testing (change back later)
            if True:
                msg = f"🔥 {name} test alert\nPrice: ₹{current_price}\n{url}"
                print(msg)
                send_telegram(msg)

        else:
            print(f"First time tracking {name}")

        with open(filename, "w") as f:
            f.write(str(current_price))

        print(f"{name} current price: {current_price}")


if __name__ == "__main__":
    main()
