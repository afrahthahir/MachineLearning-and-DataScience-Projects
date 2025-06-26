import json
import pickle
import numpy as np
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="sklearn")


__locations = None
__model = None
__data_columns = None


def get_location_names():
    load_saved_artifacts()
    return __locations

def get_estimated_price(input_data):
    load_saved_artifacts()
    
    global __data_columns
    global __model

    columns = __data_columns

    # Start with zero for all columns
    x = np.zeros(len(columns))

    # Fill numerical columns
    x[columns.index('total_sqft')] = input_data['total_sqft']
    x[columns.index('bath')] = input_data['bath']
    x[columns.index('bhk')] = input_data['bhk']

    # Fill location column (one-hot encoding)
    loc_col = input_data['location'].lower()
    if loc_col in columns:
        x[columns.index(loc_col)] = 1

    # Predict
    return round(__model.predict([x])[0],2)



def load_saved_artifacts():
    global __locations
    global __model
    global __data_columns

    print("Loading saved artifacts...start")

    with open("./artifacts/columns.json", "r") as f:
        __data_columns = json.load(f)['data_columns']
        __locations = __data_columns[3:]
    
    with open("./artifacts/banglore_home_price_predictor.pickle", "rb") as f:
        __model = pickle.load(f)

    print("Loading saved artifacts...done")
    

if __name__ == "__main__":
    load_saved_artifacts()
    print(get_location_names())
    print("Predicted price",get_estimated_price(
        input_data = {
        'total_sqft': 1000,
        'bath': 2,
        'bhk': 2,
        'location': 'Indira Nagar'
        }
    ))
    print("Predicted price", get_estimated_price(
        input_data = {
        'total_sqft': 1500,
        'bath': 3,
        'bhk': 2,
        'location': 'Hebbal'
        }
    ))
    print("Predicted price", get_estimated_price(
        input_data = {
        'total_sqft': 2300,
        'bath': 3,
        'bhk': 4,
        'location': 'vittasandra'
        }
    ))