from lxml.html import soupparser
from pathlib import Path
from . import fields
import pandas as pd
import subprocess
import requests
import time
rawpath = Path(__file__).parent / 'raw'


def download(n=50):
    for i in range(1, n+1):
        content = requests.get(
            f'https://www.hemnet.se/salda/bostader?item_types%5B%5D=bostadsratt&location_ids%5B%5D=898741&page={i}'
            ).content
        (rawpath / f'page{i}.html').open('wb').write(content)
        time.sleep(1)



def rawpages():
    for page in rawpath.iterdir():
        if page.suffix == '.html':
            yield page.open('rb')


def listings():
    for page in rawpages():
        tree = soupparser.parse(page)
        _listings = tree.xpath('//*[@id="search-results"]/li[*]/div')
        for listing in _listings:
            yield listing


def clean(df):
    # df = df.dropna(subset=['address', 'price'])
    df = df.dropna()
    df = df.loc[df.sqm > 7]
    return df


def getdf():
    hems = []
    for listing in listings():
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
    df = clean(df)
    return df
