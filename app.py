from flask import Flask, render_template, request, jsonify
import os
import numpy as np

from prediction_service import prediction
from prediction_service.lencoderext import LabelEncoderExt

webapp_root = "webapp"

static_dir = os.path.join(webapp_root, "static")
template_dir = os.path.join(webapp_root, "templates")
image_dir = os.path.join(webapp_root, "img")

app = Flask(__name__, static_folder=static_dir,template_folder=template_dir)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/predict", methods=["GET", "POST"])
def predict():
    '''
        For rendering results on HTML GUI
    '''

    print('Mansoor: ', request.method, request.form, request.json)
    try:
        if request.form:
            print('in request.form')
            dict_req = dict(request.form)
            print('2. ', dict_req)
            response = prediction.form_response(dict_req)
            print('6. ', response)
            return render_template("index.html", prediction_text=response)
        elif request.json:
            response = prediction.api_response(request.json)
            return jsonify(response)

    except Exception as e:
        print(e)
        # error = {"error": "Something went wrong!! Try again later!"}
        error = {"error": e}
        return render_template("404.html", error=error)

if __name__ == "__main__":

    # app.run(host='127.0.0.1', port=5000, debug=True)
    # app.run(host='0.0.0.0', port=8080, debug=True)
    app.run(debug=True)