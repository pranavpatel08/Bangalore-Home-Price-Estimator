from flask import Flask, request, jsonify
from flask_cors import CORS
import util

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

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
    total_sqft = float(request.form['total_sqft'])
    location = request.form['location']
    bhk = int(request.form['bhk'])
    bath = int(request.form['bath'])

    response = jsonify({
        'estimated_price': util.get_estimated_price(location, total_sqft, bhk, bath)
    })
    return response


if __name__ == "__main__":
    print("Starting Python Flask Server For Home Price Prediction...")
    util.load_saved_artifacts()
    app.run(debug=True)