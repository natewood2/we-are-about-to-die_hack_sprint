from flask import Flask, jsonify, render_template, request
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/representatives')
def get_representatives_by_address():
    # Get the zip from the index.html
    zip_code = request.args.get('zip_code')
    # Make an HTTP request to the external API
    response = requests.get('https://www.googleapis.com/civicinfo/v2/representatives', params={
        'key': 'AIzaSyD9T84S66sWgnBtzj8b0Xc7gnpGNybNanA',
        'address': zip_code,
        'roles': ['legislatorLowerBody', 'legislatorUpperBody']
    })
    # Check if the request was successful (status code 200)
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
            
            # Construct a representative object without 'ids'
            representative = {'name': name, 'phones': phones, 'roles': roles}
            representatives.append(representative)
        
        # Return the representative data as JSON response
        return jsonify(representatives)
    else:
        # Handle error responses
        return jsonify({'error': 'Failed to fetch representatives data'}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)