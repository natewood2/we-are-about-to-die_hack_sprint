from flask import Flask, jsonify, render_template, request
import requests
from flask_cors import CORS

app = Flask(__name__, static_folder='/static')
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

# Get stock data based on its symbol. Will only be XOM, or CVX
@app.route('/stocks/<symbol>')
def get_stocks(symbol):
    API_KEY = '3NNK7H2SJTENFPZ8'
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}'
    # Make an HTTPS request to get data 
    response = requests.get(url)
    # Check if request was successful
    if response.status_code == 200: 
        # Parse the json response
        data = response.json()
        # Iterate over stock data and extract relevant info
        if 'Time Series (Daily)' in data:
            latest_data = next(iter(data['Time Series (Daily)'].values()))

            # Create a stock object
            stock = {
                'symbol': symbol,
                'lastRefreshed': data['Meta Data']['3. Last Refreshed'],
                'lastClose': latest_data['4. close'],
            }

            # Return the stock object as JSON
            return jsonify(stock)
        else:
            return jsonify({'error': 'Stock data not found'}), 404

# Get representative data for fetching representatives
@app.route('/representatives')
def get_representatives_by_address():
    # Get the zip from the index.html
    zip_code = request.args.get('zip_code')
    # Make an HTTP request to get data
    response = requests.get('https://www.googleapis.com/civicinfo/v2/representatives', params={
        'key': 'AIzaSyD9T84S66sWgnBtzj8b0Xc7gnpGNybNanA',
        'address': zip_code,
        'roles': ['legislatorLowerBody', 'legislatorUpperBody']
    })
    # Check if request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        # Iterate over the officials and extract relevant information
        representatives = []
        for official in data.get('officials', []):
            name = official.get('name')
            phones = official.get('phones', [])
            channels = official.get('channels', [])
            roles = official.get('roles', [])
            
            #Construct a representative object
            representative = {'name': name, 'phones': phones, 'roles': roles}
            representatives.append(representative)
        
        # Return the representative object as JSON
        return jsonify(representatives)
    else:
        # Handle error responses
        return jsonify({'error': 'Failed to fetch representatives data'}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)