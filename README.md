# In-App-Purchases-Scraper
This script scrapes apps on Apple AppStore. You may provide a list of urls stored in csv file and input the file path to script function in script.py.
It scrapes only apps supporting English. If an app has In-App Purchases data, its information will be stored at its own row in the output file.

The urls must be under a column named ***'url'*** in the input file. 

The default output file path is "InAppPurchases.csv" contains 'Job_ID', 'App Name','App URL','IAP Data' columns. You can also modify the file by type a 2nd argument in script().


**Setting up environment to run the scraper***
Create your virtual environment with:
python -m venv venv
(venv is the name of your virtual environment, you can modify the last argument to make your own name)

activate the virtual environment
Mac/Linux: source [virtual environment's name]/bin/activate
Windows: [venv name]\Scripts\activate(.bat)

Install the necessary dependencies that makes the script run on your computer
pip install -r requirements.txt

Exiting venv:
deactivate