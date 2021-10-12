from flask import Flask, render_template, request, jsonify
import os
import numpy as np
from prediction_service import prediction
# from prediction_service.lencoderext import LabelEncoderExt
from sklearn.preprocessing import LabelEncoder

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
    
    class LabelEncoderExt(object):
        def __init__(self):
            """
            It differs from LabelEncoder by handling new classes and providing a value for it [Unknown]
            Unknown will be added in fit and transform will take care of new item. It gives unknown class id
            """
            self.label_encoder = LabelEncoder()
        # self.classes_ = self.label_encoder.classes_

        def fit(self, data_list):
            """
            This will fit the encoder for all the unique values and introduce unknown value
            :param data_list: A list of string
            :return: self
            """
            self.label_encoder = self.label_encoder.fit(list(data_list) + ['Unknown'])
            self.classes_ = self.label_encoder.classes_

            return self

        def transform(self, data_list):
            """
            This will transform the data_list to id list where the new values get assigned to Unknown class
            :param data_list:
            :return:
            """
            new_data_list = list(data_list)
            for unique_item in np.unique(data_list):
                if unique_item not in self.label_encoder.classes_:
                    new_data_list = ['Unknown' if x==unique_item else x for x in new_data_list]

            print('*** - lencoder.py is working fine')
            return self.label_encoder.transform(new_data_list)

    # app.run(host='127.0.0.1', port=5000, debug=True)
    # app.run(host='0.0.0.0', port=8080, debug=True)
    app.run(debug=True)