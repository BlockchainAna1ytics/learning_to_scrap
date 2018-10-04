"""
Module that implements the scraper which reads a web page, parses it and stores the data in a CSV file.
In order for this to function properly, you will have to install beautiful soup4 and be able to import
DictToCsvWriter, urllib and html_finder.
"""

from csv_writer import DictToCsvWriter
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as get
from html_finder import find_text_in_tag


url = 'https://coinmarketcap.com/all/views/all/'
retlist = []
outfile = 'test.csv'
header = ['coin_name', 'market_cap', 'price', 'price_change']

print(f"Connecting to: '{url}'")
with get(url) as web_page:
    html_page = web_page.read()

print('Parsing the retrieved web page')
parsed_page = soup(html_page, 'html.parser')
table = parsed_page.find('table', {'id': 'currencies-all'})
t_rows = table.tbody.findAll('tr')

for tr in t_rows:
    table_line = list()
    try:
        table_line.append(find_text_in_tag(tr, 'a', {'class': 'currency-name-container'}))
        table_line.append(find_text_in_tag(tr, 'td', {'class': 'market-cap'}))
        table_line.append(find_text_in_tag(tr, 'a', {'class': 'price'}))
        table_line.append(find_text_in_tag(tr, 'td', {'data-timespan': '7d', 'data-sort': '-0.0001'}).strip('%'))
    except Exception:
        print(f"Could not parse data for {' '.join(table_line)}")
        continue
    retlist.append({k: v for k, v in zip(header, table_line)})

print(f"Writing the scraped data to '{outfile}'")
with DictToCsvWriter(outfile, header=header) as writer:
    writer.add_lines(retlist)
    writer.write()
