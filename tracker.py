import requests

def send_telegram(message):
	token = os.getenv("BOT_TOKEN")
	chat_id = os.getenv("CHAT_ID")

	url = f"https://api.telegram.org/bot8888509378:AAGJvyLuBQtEZvwABvYa2Oz9Eu5BvtH3NAc/sendMessage"

	data = {
		"chat_id": chat_id,
		"text": message
	}

	requests.post(url, data=data)

from bs4 import BeautifulSoup
import os

URL = "https://www.amazon.in/Lenovo-Monitor-FreeSync-Speakers-1xUSB-C/dp/B0DKFDM413/ref=pd_ci_mcx_mh_mcx_views_0_image?pd_rd_w=v7J7E&content-id=amzn1.sym.41279fa1-dd23-4c70-9745-af6d0ebf3670%3Aamzn1.symc.30e3dbb4-8dd8-4bad-b7a1-a45bcdbc49b8&pf_rd_p=41279fa1-dd23-4c70-9745-af6d0ebf3670&pf_rd_r=KHGWW3089BGQQ93HBM15&pd_rd_wg=VJ07t&pd_rd_r=c013706e-8b28-4dac-bfda-3ffab35cb62c&pd_rd_i=B0DKFDM413&th=1"

headers = {
	"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
}

def get_price():
	response = requests.get(URL, headers=headers)
	soup = BeautifulSoup(response.content, "html.parser")
	
	price = soup.find("span", {"class": "a-price-whole"})
	
	if price:
		clean_price = price.text.replace(",", "").replace(".", "")
		return int(clean_price)
	return None


def main():
	current_price = get_price()

	if current_price is None:
		print ("Couldn't fetch price")
		return

	# Check if previous price file exists
	if os.path.exists("price.txt"):
		with open("price.txt", "r") as f:
			old_price = int(f.read())

		if old_price - current_price >= 500:
			msg = f"🔥  Price dropped!\nOld: ₹{old_price}\nNew: ₹{current_price}\n{URL}"
			print(msg)

	else:
		print("First time tracking. Saving price...")

	# Save current price
	with open("price.txt", "w") as f:
		f.write(str(current_price))

	print("Current price:", current_price)

if __name__ == "__main__":
	main()
