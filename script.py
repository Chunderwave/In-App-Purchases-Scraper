import requests
from bs4 import BeautifulSoup
import re
import csv
import json
import time
import random
import pandas as pd

#IAP = In-App Purchases

'''
input: a string that is the url of the app

output: a tuple containing appName and an array of tuples ("plan name", "price"), or None

description: it takes the url of an app on AppStore, scrapes the In-App Purchases
information from the website and store it in an array. 

mechanism: it searches for "$" string in the website, determine
if the returned tag contains desired info (based on whether the tag is <span>)
'''
def scrape_in_app_purchases(session, url):
    response = session.get(url)

    # Check the status code
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        print("Requests made successfully.")

        #filter for English apps?
        lan_tags = soup.find_all(string="Languages")
        for result in lan_tags:
            if result.parent.name == 'dt':
                tag = result.parent
                parent = tag.find_parent()
                languages = parent.find('p').text
                if "English" not in languages:
                    print("This app does not support English.")
                    return None

        h1 = soup.find('h1')
        if h1 == None:
            appName = soup.title.text.strip()
        else:
            nameContents = [pt for pt in h1.contents if isinstance(pt,str)]
            appName = ' '.join(nameContents).strip()
        
        # Find the "$" anchor text to locate IAP
        iap_headers = soup.find_all(string=re.compile(r'\$\d+(\.\d{2})?'))
        cnt = len(iap_headers)
        print(f"Found {cnt} elements with $ sign.")
        results = []

        # Search for plan name (may not exist)
        if iap_headers: 
            for tags in iap_headers:
                if tags.parent.name == "span":
                    parent = tags.parent
                    block_tag = parent.find_parent()

                    spans = block_tag.find_all('span')
                        # The last one is the price, so the rest is the name
                    if len(spans) >= 2:
                        name_span = spans[0]  # or sometimes more robust to do: pick the span that is not the price span
                        results.append((name_span.text.strip(), tags.strip()))
                    return (appName,results)
            # each purchase price is stored as tuple in an array called results
            print("This app does not have In-App Purchases.")

    else:
        print("Failed to retrieve the page:", response.status_code)

def writeResults(iap_data, url,writer):
    if iap_data is not None:
        entry = {"app_name": iap_data[0],
            "app_url": url,
            "iap_data":json.dumps([{"name": n, "price": p} for n, p in iap_data[1]])}
        writer.writerow(entry) 
    
def Sleep():
    sleepTime = random.uniform(2,5)
    print(f"Sleeping for {sleepTime} seconds.")
    time.sleep(sleepTime)

def TeskLinks():
    hasIAP = "https://apps.apple.com/us/app/fantastical-calendar/id718043190"
    notHasIAP = "https://apps.apple.com/me/app/google-translate/id414706506"
    notEnglish = "https://apps.apple.com/us/app/%E5%A4%A7%E7%B9%81%E7%9B%9B-%E3%81%BE%E3%82%93%E3%81%B7%E3%81%8F%E3%83%9E%E3%83%AB%E3%82%B7%E3%82%A73/id1301811479"
    return [hasIAP,notHasIAP,notEnglish]

def loadLargerTest():
    df = pd.read_csv('urls.csv', index_col=0)
    urls_series = df['url'].head(50)

    return urls_series.tolist()

app_urls=TeskLinks()

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9"
}
session = requests.Session()
session.headers.update(headers)

# response = session.get("https://apps.apple.com/me/app/google-translate/id414706506")
# if response.status_code == 200:
#     soup = BeautifulSoup(response.text,'lxml')
        # lan_tags = soup.find_all(string="Languages")
        # for result in lan_tags:
        #     if result.parent.name == 'dt':
        #         tag = result.parent
        #         parent = tag.find_parent()
        #         languages = parent.find('p').text
                # if languages.


with open('InAppPurchases.csv', mode = 'a', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['app_name','app_url', 'iap_data'])

    for url in app_urls:
        iap_data = scrape_in_app_purchases(session, url)
        writeResults(iap_data,url,writer)
        Sleep()

print("Saved to InAppPurchases.csv ✅")
