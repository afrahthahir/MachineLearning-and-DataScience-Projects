from flask import Flask, request, jsonify
import util
import os

app = Flask(__name__)

@app.route('/get_location_names')
def get_location_names():
   response = jsonify({
       'locations': util.get_location_names()
   })

   response.headers.add("Access-Control-Allow-Origin", "*")
   return response

@app.route('/predict_home_price', methods=['POST'])
def predict_home_price():
    total_sqft = float(request.form['total_sqft'])
    bhk = int(request.form['bhk'])
    bath = int(request.form['bath'])
    location = request.form['location']

    response = jsonify({
       'estimated_price': util.get_estimated_price(
           input_data = {
            'total_sqft': total_sqft,
            'bath': bath,
            'bhk': bhk,
            'location': location
           }
       )
   })

    response.headers.add("Access-Control-Allow-Origin", "*")
    return response



if __name__ == '__main__':
    print("Starting Flask server for Banglore House Price Predictor....")
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
