from flask import Flask, request, jsonify
import util
import os

app = Flask(__name__)
# Removed: CORS(app)

# Manual CORS handling
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# Get the directory where this file is located
base_dir = os.path.dirname(os.path.abspath(__file__))
artifacts_path = os.path.join(base_dir, 'artifacts')

print(f"Loading artifacts from: {artifacts_path}")
util.load_saved_artifacts(artifacts_path)

# Added a home route to test if API is working
@app.route('/')
def home():
    return jsonify({
        'message': 'Bangalore Home Price Prediction API is running!',
        'endpoints': [
            '/get_location_names',
            '/search_locations?query=<search_term>',
            '/predict_home_price'
        ]
    })

@app.route('/get_location_names', methods=['GET'])
def get_location_names():
    """Get all location names"""
    response = jsonify({
        'locations': util.get_location_names()
    })
    return response


@app.route('/search_locations', methods=['GET'])
def search_locations():
    """Search for locations based on query"""
    query = request.args.get('query', '')
    limit = int(request.args.get('limit', 6))

    results = util.search_locations(query, limit)

    # If no results, suggest "Other"
    if not results and query:
        results = ['Other']

    response = jsonify({
        'locations': results
    })
    return response


@app.route('/predict_home_price', methods=['GET', 'POST'])
def predict_home_price():
    """Predict home price"""
    try:
        total_sqft = float(request.form['total_sqft'])
        location = request.form['location']
        bhk = int(request.form['bhk'])
        bath = int(request.form['bath'])

        response = jsonify({
            'estimated_price': util.get_estimated_price(location, total_sqft, bhk, bath)
        })
        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == "__main__":
    # This part won't run on PythonAnywhere, but keeping it for local testing
    print("Starting Python Flask Server For Home Price Prediction...")
    app.run(debug=False)  # Changed to False for production