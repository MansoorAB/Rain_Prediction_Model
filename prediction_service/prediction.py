import os
import json
import pickle
import numpy as np
import pandas as pd

schema_path = os.path.join("prediction_service", "schema_in.json")
actual_cols = []

class NotInRange(Exception):
    def __init__(self, message="Values provided are not in expected range"):
        self.message = message
        super().__init__(self.message)


class NotInCols(Exception):
    def __init__(self, message="Entered key is not a valid column name!"):
        self.message = message
        super().__init__(self.message)


class InvalidColValue(Exception):
    def __init__(self, message="Value for a column is blank or invalid data type"):
        self.message = message
        super().__init__(self.message)

class InvalidColCount(Exception):
    def __init__(self, message="Argument count mismatch"):
        self.message = message
        super().__init__(self.message)

# class LabelEncoderExt(object):
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


def predict(data):
    
    encoder_path = os.path.join("prediction_service", "model", "labelencoder.pkl" )
    scaler_path = os.path.join("prediction_service", "model", "scaler.pkl" )
    model_path = os.path.join("prediction_service", "model", "dtclassifier.pkl")

    print('4.', actual_cols)
    data = pd.DataFrame(data, columns=actual_cols)
    print(data)   

    print ('41. opening lencoder file')

    with open(encoder_path, 'rb') as f:
        le = pickle.load(f)
        print('42. lencoder open success.')

    col = 'WindGustDir'
    data[col] = le[col].transform(data[col].astype('str'))
    print ('43. transformation success')

    with open(scaler_path, 'rb') as file:
        sc = pickle.load(file)

    for col in actual_cols[1:-1]:
        data[col]  = sc[col].transform(np.array(data[col]).reshape(-1, 1))

    print(data)

    with open(model_path, 'rb') as f:
        model = pickle.load(f)

    prediction = model.predict(data).tolist()[0]
    proba = model.predict_proba(data)[0, 1]
    print('*** Prediction: %d' %prediction)
    print('*** Probability', proba)
    
    return prediction, round(proba, 4)


def get_schema(schema_path=schema_path):
    with open(schema_path) as json_file:
        schema = json.load(json_file)
    return schema

def validate_input(dict_request):

    global actual_cols
    cols_list_path = os.path.join("prediction_service", "model", 
                                    "column_names.pkl")
    with open(cols_list_path, 'rb') as f:
        actual_cols = pickle.load(f)
    
    def _validate_cols(col):

        if col not in actual_cols:
            raise NotInCols

    def _validate_values(col, val):
        schema = get_schema()

        try:
            if col in schema.keys():
                if not (schema[col]["min"] <= float(dict_request[col]) <= schema[col]["max"]):
                    raise NotInRange
        except ValueError:
            raise InvalidColValue

    if len(dict_request.keys()) != len(actual_cols):
        raise InvalidColCount

    for col, val in dict_request.items():
        _validate_cols(col)
        # print('validation of col: %s is complete' %col)
        _validate_values(col, val)
        # print('validate values is complete')
    
    return True


def form_response(dict_request):
    global actual_cols
    if validate_input(dict_request):
        print('form_response input validation passed')
        data = [list(dict_request.values())] 
        print('3. ', data)
        cls, prob = predict(data)
        print('5. ', cls, prob)
        # data = [list(map(float, data))]
        # response = predict(data)
        if prob == 1:
                response = "It will most likely rain tomorrow!"
        elif prob >= 0.5:
            response = "It shall rain tomorrow, the probability is high at %.2f %%" %(prob*100)
        elif prob == 0:
            response = "Most likely, it won't rain tomorrow!"                             
        else:
            response = "It mayn't rain tomorrow as the probability is low at %.2f %%" %(prob*100)
        return response


def api_response(dict_request):
    global actual_cols

    try:        
        if validate_input(dict_request):
            print('api_response input validation passed')
            # Optional to convert to array, has to be a 2D array, hence [list(...)]
            data = [list(dict_request.values())] 
            cls, prob = predict(data)
            print(cls, prob)
            if prob == 1:
                response = "It will most likely rain tomorrow!"
            elif prob >= 0.5:
                response = "It shall rain tomorrow, the probability is high at %.2f %%" %(prob*100)
            else:                             
                response = "It maynt rain tomorrow as the probability is low at %.2f %%" %(prob*100)

            response = {"response": response}
            return response
            
    except NotInRange as e:
        response = {"the_expected_range": get_schema(), "response": str(e)}
        return response

    except (NotInCols, InvalidColCount) as e:
        # k = list(get_schema().keys())
        response = {"the_expected_cols": json.dumps(str(actual_cols))[1:-1],           "response": str(e)}
        return response

    except Exception as e:
        response = {"the_expected_cols_values": get_schema(), "response": str(e)}
        return response

