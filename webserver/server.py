from flask import Flask, request
import json
import pandas as pd
import pickle

app = Flask(__name__)
model = pickle.load(open('../model/out/linear-regression.pkl', 'rb'))

def price_format(price):
    return f'{int(price):,}'.replace(',', ' ')


@app.route('/', methods=['GET', 'POST'])
def index():
    return 'LightNet'


@app.route('/prices', methods=['POST'])
def prices():
    df = pd.DataFrame(request.json)
    X = df[['sqm', 'rent', 'rooms']]
    pred = list(model.predict(X))
    return json.dumps([price_format(p) for p in pred])


if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
