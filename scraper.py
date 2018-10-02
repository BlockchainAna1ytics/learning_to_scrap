"""
Module that implements the scraper which reads a web page, parses it and stores the data in a CSV file.
In order for this to function properly, you will have to install beautiful soup4 and be able to import
DictToCsvWriter and urllib.
"""

from csv_writer import DictToCsvWriter
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as get


url = 'https://coinmarketcap.com/all/views/all/'
retlist = []
outfile = 'test.csv'
header = ['coin_name', 'market_cap', 'price', 'price_change']

print(f"Connecting to: '{url}'")
with get(url) as u_page:
    html_page = u_page.read()
    print('Parsing the retrieved web page')
    parsed_page = soup(html_page, 'html.parser')
    table = parsed_page.findAll('table', {'id': 'currencies-all'})
    t_rows = table[0].tbody.findAll('tr')

for tr in t_rows:
    table_list = list()
    try:
        table_list.append(tr.find('a', {'class': 'currency-name-container'}).text.strip())
        table_list.append(tr.find('td', {'class': 'market-cap'}).text.strip())
        table_list.append(tr.find('a', {'class': 'price'}).text.strip())
        table_list.append(tr.find('td', {'data-timespan': '7d'}).text.strip('%'))
    except Exception:
        continue
    retlist.append({k: v for k, v in zip(header, table_list)})

print(f"Writing the scraped data to '{outfile}'")
with DictToCsvWriter(outfile, header=header) as writer:
    writer.add_lines(retlist)
    writer.write()
