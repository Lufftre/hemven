from flask import Flask
from flask import request
import json
import pickle
import numpy as np
import re

app = Flask(__name__)
model = pickle.load(open('../../model/out/linear-regression.pkl', 'rb'))


def keep_digits(text, default=0):
    text = str(text)
    text = re.sub(r'[^\d,\.]', '', text.strip())
    text = text.replace(',', '.')
    if not text:
        return default
    return float(text)

def getPrice(listing):
    address_floor = listing['address'].split(',') + ['', '']
    address, floor = address_floor[:2]
    match = re.search(r'\d+', floor)
    if match:
        floor = match.group()
    else:
        floor = 2

    data = np.array([[
        keep_digits(floor),
        keep_digits(listing['sqm'], 30),
        keep_digits(listing['rent'], 3000),
        keep_digits(listing['rooms'], 2)]])
    
    pred = model.predict(data)[0]
    formatted = f'{int(pred):,}'.replace(',', ' ')
    return formatted


@app.route('/one', methods=['POST'])
def index():
    address_floor = request.json['address'].split(',') + ['', '']
    address, floor = address_floor[:2]
    match = re.search(r'\d+', floor)
    if match:
        floor = match.group()
    else:
        floor = 2

    data = np.array([[
        keep_digits(floor),
        keep_digits(request.json['sqm']),
        keep_digits(request.json['rent']),
        keep_digits(request.json['rooms'])]])

    pred = model.predict(data)[0]
    formatted = f'{int(pred):,}'.replace(',', ' ')
    return json.dumps({'price': formatted})

@app.route('/', methods=['POST'])
def index2():
    try:
        prices  = [getPrice(x) for x in request.json]
    except Exception as error:
        prices = [x for x in range(len(request.json))]
    return json.dumps(prices)

app.run('0.0.0.0', port=8080, debug=True)
