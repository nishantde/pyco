import time
import sys
import requests
import bs4

def get_global_count(soup):
    total_count = soup.select('.maincounter-number')
    return total_count[0].text.strip()

def main():
    res = requests.get('https://www.worldometers.info/coronavirus/')
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    print(get_global_count(soup))

if __name__ == '__main__':
    main()