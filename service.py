from requests_html import HTMLSession
import json
from concurrent.futures import ThreadPoolExecutor
import datetime
from upcoming import upcoming_races

s = HTMLSession()

# url = 'https://www.formula1.com/en/results.html/2023/races.html'
# r = s.get(url)


def get_race_result(html):
    table = html.find('.resultsarchive-table')
    if len(table) == 0:
        return []
    table = table[0]
    tabledata = [[c.text for c in row.find('td')[:-1]] for row in table.find('tr')][1:]
    tableheader = [[c.text for c in row.find('th')[:-1]] for row in table.find('tr')][0]
    res = [dict(zip(tableheader, t)) for t in tabledata]
    return res

def get_race(link_race):
    result = {}
    url = link_race
    r = s.get(url)
    # title
    title = r.html.find('.ResultsArchiveTitle')[0].text
    # date
    date = ''
    # start_date = r.html.find('.start-date')
    full_date = r.html.find('.full-date')[0].text
    # if len(start_date) == 0: 
    date = full_date
    # else:
        # date = start_date[0].text + "-" + full_date
    # circuit
    circuit = r.html.find('.circuit-info')[0].text
    # race_result
    race_result = get_race_result(r.html)

    result['title'] = title
    result['date'] = date
    result['circuit'] = circuit
    result['race_result'] = race_result
    return result

def get_year(link_year):
    result = []
    url = link_year    
    r = s.get(url)
    listcountry = r.html.find('.resultsarchive-filter-wrap')[2]
    countries = [li.text for li in listcountry.find('li')]
    urls = [li.absolute_links for li in listcountry.find('li')]
    url_strings = [list(item)[0] for item in urls] 

    # # get races in a year 
    # for i in range(1, len(countries)):
    #     country_race = {}
    #     country_race['country'] = countries[i]
    #     country_race['race'] = get_race(url_strings[i])
    #     result.append(country_race)

    # OPTIMIZE
    def fetch_race_data(country, race_url):
        race_data = {}
        race_data['country'] = country
        race_data['race'] = get_race(race_url)
        return race_data
    
    with ThreadPoolExecutor() as executor:
        race_results = list(executor.map(lambda x: fetch_race_data(countries[x], url_strings[x]), range(1, len(countries))))
        result.extend(race_results)
    
    return result

def get_all_year(main_link):
    result = []
    url = main_link    
    r = s.get(url)
    listyear = r.html.find('.resultsarchive-filter-wrap')[0]
    years = [li.text for li in listyear.find('li')]
    urls = [li.absolute_links for li in listyear.find('li')]
    url_strings = [list(item)[0] for item in urls] 

    # get races in a year 
    for i in range(1, len(years)):
        year_races = {}
        year_races['year'] = years[i]
        year_races['race'] = get_year(url_strings[i])
        result.append(year_races)
        print(year_races['year'] , " Done")
    
    return result

def list_all_year(current_year):
    result = []
    url = current_year    
    r = s.get(url)
    listyear = r.html.find('.resultsarchive-filter-wrap')[0]
    years = [li.text for li in listyear.find('li')]
    urls = [li.absolute_links for li in listyear.find('li')]
    url_strings = [list(item)[0] for item in urls] 

    for i in range(0, len(years)):
        year_link = {}
        year_link['year'] = years[i]
        year_link['link'] = url_strings[i]
        result.append(year_link)
    
    return result

def get_upcoming():
    current_time = datetime.datetime.now()
    current_date = current_time.strftime("%d %B")
    
    # loop through all index and compare with current date, pick the closest one
    for i in upcoming_races:
        if i['date'] < current_date:
            print(i['title'])
            print(i['date'])
            print(i['image'])
            return i


def save_to_json(result, filename):
    with open(f'{filename}.json', 'w') as f:
        json.dump(result, f)