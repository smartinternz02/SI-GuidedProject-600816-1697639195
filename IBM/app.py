from flask import Flask, render_template, request
#import numpy as np
import pickle
API_KEY = "PTWxyc0r5IrZ2agLuscrjOU3jELBXvj-jHdQk962_pT9"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}


app=Flask(__name__)

model = pickle.load(open('gwp.pkl', 'rb'))

@app.route("/")
def about():
    return render_template('home.html')


@app.route("/about")
def home():
    return render_template('about.html')


@app.route("/predict")
def home1():
    return render_template('predict.html')


@app.route("/submit")
def home2():
    return render_template('submit.html')


@app.route("/pred", methods=['POST'])
def predict():
    quarter = request.form['quarter']
    department = request.form['department']
    day = request.form['day']
    team = request.form['team']
    targeted_productivity = request.form['targeted_productivity']
    smv = request.form['smv']
    over_time = request.form['over_time']
    incentive = request.form['incentive']
    idle_time = request.form['idle_time']
    idle_men = request.form['idle_men']
    no_of_style_change = request.form['no_of_style_change']
    no_of_workers = request.form['no_of_workers']
    month = request.form['month']
    total = [[int(quarter), int(department), int(day), int(team),
              float(targeted_productivity),float(smv), int(over_time), int(incentive),
              float(idle_time), int(idle_men), int(no_of_style_change), float(no_of_workers), int(month)]]
   # print(total)
   # prediction = model.predict(total)
 #   print(prediction)
    payload_scoring = {"input_data": [{"field": ['date','quarter','department','day','team','targeted_productivity','smv','wip','over_time','incentive','idle_time','idle_men',	'no_of_style_change','no_of_workers','actual_productivity'
            ], "values": total}]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/7968b289-1d73-4ebe-be55-718202776899/predictions?version=2023-02-12', json=payload_scoring,
    headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    pred=response_scoring.json()
    prediction=pred['predictions'][0]['values'][0][0]
    if prediction <= 0.3:
        text = 'The employee is averagely productive.'
    elif prediction >0.3 and prediction <=0.8:
        text = 'The employee is medium productive'
    else:
        text = 'The employee is Highly productive'
        
    return render_template('submit.html', prediction_text=text)


if __name__ == "__main__":
    app.run(debug=False)
