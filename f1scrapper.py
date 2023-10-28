from requests_html import HTMLSession
import json

s = HTMLSession()

url = 'https://www.formula1.com/en/results.html/2023/races.html'
r = s.get(url)

table = r.html.find('table')[0]

# tabledata = [[c.text for c in row.find('td')[:-1]] for row in table.find('tr')][1:]
# tableheader = [[c.text for c in row.find('th')[:-1]] for row in table.find('tr')][0]

# res = [dict(zip(tableheader, t)) for t in tabledata]

# with open('f1.json', 'w') as f:
# #     json.dump(res, f)

div = r.html.find('.resultsarchive-filter-wrap')[0]
urls = [li.text for li in div.find('li')]
# url_strings = [list(item)[0] for item in urls] 


print(urls)