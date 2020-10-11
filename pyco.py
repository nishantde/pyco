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
    infected_count = get_global_infected_count(soup)
    death_count = get_global_deaths_count(soup)
    recovered_count = get_global_recovered_count(soup)
    print('Total infected cases: {0} | Total deaths: {1} | Total recovered: {2}'.format(infected_count, death_count, recovered_count))

if __name__ == '__main__':
    main()