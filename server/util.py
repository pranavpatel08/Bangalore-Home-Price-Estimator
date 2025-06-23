import pickle
import json
import numpy as np
import os

__locations = None
__data_columns = None
__model = None

def get_estimated_price(location, sqft, bhk, bath):
    """Calculate the estimated price for a home"""
    try:
        loc_index = __data_columns.index(location.lower())
    except:
        loc_index = -1

    x = np.zeros(len(__data_columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    if loc_index >= 0:
        x[loc_index] = 1

    return round(__model.predict([x])[0], 2)


def load_saved_artifacts(artifacts_path='./artifacts'):  # Added default parameter
    """Load the saved model and data columns"""
    print("loading saved artifacts...start")
    global __data_columns
    global __locations
    global __model

    # Use the provided path
    columns_path = os.path.join(artifacts_path, "columns.json")
    model_path = os.path.join(artifacts_path, "bangalore_RE_Price_model.pickle")
    
    print(f"Loading columns from: {columns_path}")
    print(f"Loading model from: {model_path}")

    with open(columns_path, "r") as f:
        __data_columns = json.load(f)['data_columns']
        __locations = __data_columns[3:]  # first 3 columns are sqft, bath, bhk

    with open(model_path, 'rb') as f:
        __model = pickle.load(f)
    
    print(f"Loaded {len(__locations)} locations")
    print("loading saved artifacts...done")


def get_location_names():
    """Get all location names"""
    return __locations


def get_data_columns():
    """Get all data columns"""
    return __data_columns


def search_locations(query, limit=5):
    """Search for locations that match the query"""
    if not query:
        return []
    
    query = query.lower()
    matches = []
    
    # First, add locations that start with the query
    for loc in __locations:
        if loc.lower().startswith(query):
            matches.append(loc)
            if len(matches) >= limit:
                break
    
    # If we need more results, add locations that contain the query
    if len(matches) < limit:
        for loc in __locations:
            if query in loc.lower() and loc not in matches:
                matches.append(loc)
                if len(matches) >= limit:
                    break
    
    return matches


if __name__ == '__main__':
    load_saved_artifacts()
    print(get_location_names())
    print(get_estimated_price('1st Phase JP Nagar', 1000, 3, 3))
    print(get_estimated_price('1st Phase JP Nagar', 1000, 2, 2))
    print(get_estimated_price('Kalhalli', 1000, 2, 2))
    print(get_estimated_price('Ejipura', 1000, 2, 2))