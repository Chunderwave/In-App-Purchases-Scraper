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

def scrape_in_app_purchases(session, url, job_id):
    response = session.get(url)

    # Check the status code
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        print(f'This is Job {job_id} running.')

        #filter for English apps?
        lan_tags = soup.find_all(string="Languages")
        for result in lan_tags:
            if result.parent.name == 'dt':
                tag = result.parent
                parent = tag.find_parent()
                try: 
                    languages = parent.find('p').text
                    if "English" not in languages:
                        print("This app does not support English.")
                        return None
                except:
                    print("Not have language information")

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
            for tags in iap_headers: #if more than 1, there could be IAP plans
                if tags.parent.name == "span":
                    parent = tags.parent
                    block_tag = parent.find_parent()

                    spans = block_tag.find_all('span')
                        # The last one is the price, so the rest is the name
                    if len(spans) >= 2:
                        name_span = spans[0]  # or sometimes more robust to do: pick the span that is not the price span
                        results.append((name_span.text.strip(), tags.strip()))
            
        if len(results) != 0:
            return (appName,results)
            # each purchase price is stored as tuple in an array called results
        else:
            print("This app does not have In-App Purchases.")
            return None

    else:
        print("Failed to retrieve the page:", response.status_code)
        return None

def writeResults(iap_data, url,writer,i):
    if iap_data is not None:
        entry = {
            "Job_ID": i,
            "App Name": iap_data[0],
            "App URL": url,
            "IAP Data":json.dumps([{"name": n, "price": p} for n, p in iap_data[1]])}
        writer.writerow(entry)
        print("An entry is added")
    
def Sleep():
    sleepTime = random.uniform(2,5)
    # print(f"Sleeping for {sleepTime} seconds.")
    time.sleep(sleepTime)

def LoadTest(file_path, count=None):
    df = pd.read_csv(file_path, index_col=0,header =0)
    if count != None:
        if type(count) == int:
            df = df.head(count)
        else:
            raise TypeError('The second argument for LoadTest should be int type')
    return df

def script(input_path, output_path='InAppPurchases.csv'):

    if type(input_path) != str | type(output_path) != str:
        raise TypeError('Please input file path as a str')
    
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

    job_df = LoadTest(input_path)
    app_urls = job_df['url'].tolist()

    job_df['status']=job_df.get('status') #if status col doesn't exist, a column of None type is returned
    job_done_sr = job_df['status']

    startFrom = job_done_sr.size - job_done_sr.isnull().sum()
    if startFrom == 0:
        with open(output_path, mode='w',newline = '', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['Job_ID', 'App Name','App URL','IAP Data'])
            writer.writeheader()
    elif startFrom < 0:
        print("startFrom is negative.")
        return -1
    

    totalJobs = len(app_urls) # total number of jobs
    print(startFrom)
    print(totalJobs)
    if startFrom < totalJobs:
        for i in range(startFrom, totalJobs):
                # so iteration begins from startFrom and ends at totalJobs - 1 (which 
                # is the last job's index)
                url = app_urls[i]
                iap_data = scrape_in_app_purchases(session, url, i)

                with open(output_path, mode = 'a', newline='', encoding='utf-8') as f:
                    appender = csv.DictWriter(f, fieldnames=['Job_ID', 'App Name','App URL','IAP Data'])
                    writeResults(iap_data,url,appender,i)

                job_done_sr.at[i]='done'
                if i%10 == 9:
                    pd.DataFrame.to_csv(job_df,input_path,header=True)

                Sleep()
            
    pd.DataFrame.to_csv(job_df,input_path,header=True)
    print("All jobs are completed.")
    return 1
    
script('test_urls.csv')