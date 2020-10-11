import time
import sys
import requests
import bs4
import geocoder

headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
}

ACCEPTED_GLOBAL_PARAMS = ['g', 'global', '-g', '-global']
ACCEPTED_LOCAL_PARAMS = ['l', 'local', '-l', '-local']

def get_global_infected_count(soup):
    total_count = soup.select('.maincounter-number')
    return total_count[0].text.strip()

def get_global_deaths_count(soup):
    total_count = soup.select('.maincounter-number')
    return total_count[1].text.strip()

def get_global_recovered_count(soup):
    total_count = soup.select('.maincounter-number')
    return total_count[2].text.strip()

def get_global_active_cases(soup):
    active_cases = soup.select('.panel_flip .panel_front .number-table-main')
    return active_cases[0].text.strip()

def get_global_closed_cases(soup):
    closed_cases = soup.select('.panel_flip .panel_front .number-table-main')
    return closed_cases[1].text.strip()

def get_local_page():
    pass

def main():
    res = requests.get('https://www.worldometers.info/coronavirus/', headers=headers)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'html.parser')

    infected_count = get_global_infected_count(soup)
    death_count = get_global_deaths_count(soup)
    recovered_count = get_global_recovered_count(soup)
    active_cases = get_global_active_cases(soup)
    closed_cases = get_global_closed_cases(soup)

    g = geocoder.ip('me')
    city, state, country = g.city, g.state, g.country
    
    if country == 'US': # Handling discrepancy between nomenclature
        country = 'USA'

    print(city, ',', state, ',', country)

    state = '-'.join(name for name in state.split())

    if (len(sys.argv) == 1) or (len(sys.argv) == 2 and sys.argv[1] in ACCEPTED_GLOBAL_PARAMS):
        print('Total infected cases: {0} | Total deaths: {1} | Total recovered: {2}'.format(infected_count, death_count, recovered_count))
        print('Active cases: {0} | Closed cases: {1}'.format(active_cases, closed_cases))


if __name__ == '__main__':
    main()