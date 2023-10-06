import pickle
from flask import Flask, request, jsonify , render_template ,redirect ,url_for
import numpy as np


app = Flask(__name__)

# Load your pickled model here
with open('heart_disease_prediction_random_forest.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

@app.route('/')
def home():
    return render_template('base.html',title="Doc-Co")



@app.route('/prediction')
def predict_form():
    return render_template('prediction_form.html',title="Prediction Form")

@app.route('/heart-disease', methods=['POST'])
def predict():
    try:
         # Get the form data from the request
        data = request.form
        print("data-item",data)
        
        keys = []
        values = []

        for key, value in data.items():
          keys.append(key)
          values.append(value)

        # Now 'keys' contains the keys and 'values' contains the corresponding values
        print("Keys:", keys)
        print("Values:", values)     
        
        # convert the list to array and reshape it to predict
        np_array=np.asarray(values)
        
        # reshape
        data=np_array.reshape(-1,1).T

        # Perform prediction using your model
        prediction = model.predict(data)
        
        # Map the prediction to "0" as "no disease" and "1" as "disease"
        result = []
        for p in prediction:
            if p == 0:
                result.append("No Disease")
                return redirect(url_for('result', result="No-Disease"))
            elif p == 1:
                result.append("Disease")
                return redirect(url_for('result', result="Disease"))
            else:
                result.append("Unknown")
                return redirect(url_for('result', result="Unknown"))
        
        print("predict",result)
        
        # Return the prediction as JSON response
        response = {'prediction': result[0]}
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': str(e)})


# @app.route('/result/<result>')
# def result(result):
#     return render_template('result.html',result=result)

@app.route('/result')
def result():
    return render_template('result.html')

if __name__ == '__main__':
    app.run(debug=True)
