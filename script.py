import requests
from bs4 import BeautifulSoup
import re

# Replace this with your App Store URL
url = "https://apps.apple.com/us/app/sleep-cycle-tracker-sounds/id320606217"

# Set a User-Agent header to mimic a browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

response = requests.get(url, headers=headers)
print("ran requests.get()")

# Check the status code
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'lxml')
    print("Requests made successfully.")
    
    # 1. Find the "In-App Purchases" anchor text
    iap_headers = soup.find_all(string=re.compile(r'\$\d+(\.\d{2})?'))
    cnt = len(iap_headers)
    print(f"Found {cnt} elements with $ sign.")

    for i, price in enumerate(iap_headers):
        if price.parent.name == "span":
            print(f"\nPrice {i+1}:")
            print("Text:", price)

else:
    print("Failed to retrieve the page:", response.status_code)
