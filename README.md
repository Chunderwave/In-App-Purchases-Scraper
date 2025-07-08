# In-App-Purchases-Scraper
This script scrapes apps on Apple AppStore using the list of urls provided in urls.csv.
It scrapes only apps supporting English. If an app has In-App Purchases data, its information will be stored at its own row in the InAppPurchases.csv.

InAppPurchases.csv contains app name, app url, and the In-App Purchases data.

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