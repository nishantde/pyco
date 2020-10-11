import time
import sys
import requests
import bs4

def main():
    res = requests.get('https://www.worldometers.info/coronavirus/')
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    total_count = soup.select('#maincounter-wrap .maincounter-number')
    print(len(total_count))
