from lxml.html import soupparser
import fields
import pandas as pd
import os
from pathlib import Path

def files():
    pages = Path('../slutpriser/')
    for page in pages.iterdir():
        if page.suffix == '.html':
            yield page.open('rb')


hems = []
for page in files():
    tree = soupparser.parse(page)
    listings = tree.xpath('//*[@id="search-results"]/li[*]/div')
    for listing in listings:
        hem = {
            'address': fields.address(listing),
            'floor': fields.floor(listing),
            'area': fields.area(listing),
            'rent': fields.rent(listing),
            'price': fields.price(listing),
            'date': fields.date(listing),
            'kr_sqm': fields.kr_sqm(listing),
            'change': fields.change(listing),
            'sqm': fields.sqm(listing),
            'rooms': fields.rooms(listing),
        }
        hems += [hem]

df = pd.DataFrame(hems)
df = df.dropna(subset=['address', 'price'])
df = df.loc[df.sqm > 7]
df.to_csv('slutpriser.csv', index=False)
