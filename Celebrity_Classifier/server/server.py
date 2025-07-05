from flask import Flask, request, jsonify
import util

util.load_saved_artifacts()
app = Flask(__name__)

@app.route("/classify_image", methods = ["GET", "POST"])
def classify_image():
    image_data = request.form['image_data']
    response = jsonify(util.classify_image(image_data))
    response.headers.add("Access-Control-Allow-Origin", '*')
    return response



if __name__ == "__main__":
    print("Starting flask server for celebrity classifier")
    app.run(host="0.0.0.0", port=5001)