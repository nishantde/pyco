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

URL = 'https://www.worldometers.info/coronavirus/'
ACCEPTED_GLOBAL_PARAMS = ['g', 'global', '-g', '-global']
ACCEPTED_LOCAL_PARAMS = ['l', 'local', '-l', '-local']

def get_global_infected_count(global_case_info):
    '''Returns global total infected count'''
    return global_case_info[0].text.strip()

def get_global_deaths_count(global_case_info):
    '''Returns global total death count'''
    return global_case_info[1].text.strip()

def get_global_recovered_count(global_case_info):
    '''Returns global total recovery count'''
    return global_case_info[2].text.strip()

def get_global_active_cases(global_active_case_info):
    '''Returns global active case count'''
    return global_active_case_info[0].text.strip()

def get_global_closed_cases(global_active_case_info):
    '''Returns global closed case count'''
    return global_active_case_info[1].text.strip()

def get_local_infected_count(local_case_info):
    '''Returns state-wise total infected count'''
    return local_case_info[0].text.strip()

def get_local_death_count(local_case_info):
    '''Returns state-wise total death count'''
    return local_case_info[1].text.strip()

def get_local_recovered_count(local_case_info):
    '''Returns state-wise total recovery count'''
    return local_case_info[2].text.strip()

def display_cases(infected, deaths, recovered):
    '''Displays the infected count, death count, and recovery count'''
    print('Total infected:', infected)
    print('Total deaths:', deaths)
    print('Total recovered:', recovered)

def display_active_cases(active, closed):
    '''Displays active case count and closed case count'''
    print('Current active cases:', active)
    print('Closed cases:', closed)

def main():
    res = requests.get(URL, headers=headers)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'html.parser')

    global_case_info = soup.select('.maincounter-number')
    global_active_case_info = soup.select('.panel_flip .panel_front .number-table-main')
    
    # Global info
    infected_count = get_global_infected_count(global_case_info)
    death_count = get_global_deaths_count(global_case_info)
    recovered_count = get_global_recovered_count(global_case_info)
    active_cases = get_global_active_cases(global_active_case_info)
    closed_cases = get_global_closed_cases(global_active_case_info)

    # Retrieve global info if no parameters are given or acceptable global parameters are given
    if (len(sys.argv) == 1) or (len(sys.argv) == 2 and sys.argv[1] in ACCEPTED_GLOBAL_PARAMS):
        print('Global cases')
        display_cases(infected_count, death_count, recovered_count)
        display_active_cases(active_cases, closed_cases)

    if len(sys.argv) == 2:
        if sys.argv[1] in ACCEPTED_LOCAL_PARAMS:
            # Retrieving local info
            g = geocoder.ip('me')
            city, state, country = g.city, g.state, g.country
            STATE_NAME, COUNTRY_NAME = state, country
            
            # Handling discrepancy between nomenclature
            if country == 'US': 
                country = 'USA'

            # Resolving URL for retrieving local info
            state = '-'.join(name for name in state.split())
            local_url = URL + '/' + country.lower() + '/' + state.lower() + '/'
            local_res = requests.get(local_url, headers=headers)
            local_res.raise_for_status()
            local = bs4.BeautifulSoup(local_res.text, 'html.parser')

            local_case_info = local.select('#maincounter-wrap .maincounter-number')
            
            local_infected_count = get_local_infected_count(local_case_info)
            local_death_count = get_local_death_count(local_case_info)
            local_recovered_count = get_local_recovered_count(local_case_info)

            print('State: {0} & Country: {1}'.format(STATE_NAME, COUNTRY_NAME))
            display_cases(local_infected_count, local_death_count, local_recovered_count)

if __name__ == '__main__':
    main()