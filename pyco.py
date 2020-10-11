import time
import sys
import requests
import bs4

def get_global_infected_count(soup):
    total_count = soup.select('.maincounter-number')
    return total_count[0].text.strip()

def get_global_deaths_count(soup):
    total_count = soup.select('.maincounter-number')
    return total_count[1].text.strip()

def get_global_recovered_count(soup):
    total_count = soup.select('.maincounter-number')
    return total_count[2].text.strip()

def main():
    res = requests.get('https://www.worldometers.info/coronavirus/')
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    print(get_global_infected_count(soup))
    print(get_global_deaths_count(soup))
    print(get_global_recovered_count(soup))

if __name__ == '__main__':
    main()