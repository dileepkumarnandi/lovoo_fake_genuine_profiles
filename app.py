# -*- coding: utf-8 -*-
"""
Created on Sun Mar 28 12:24:20 2021

@author: saikrishna
"""


import scrape as scrape
from flask import Flask, request, render_template
import pickle


app = Flask(__name__)
random_forest = pickle.load(open('random_forest.pkl', 'rb'))
decision_tree = pickle.load(open('decision_tree.pkl', 'rb'))
gaussian = pickle.load(open('gaussian.pkl', 'rb'))
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    data=request.form
    int_features = list(data.values())
    df = scrape.login(int_features[0],int_features[1])
    list2 =scrape.image_url_list
    list3 = scrape.username_list
    random_forest_predict = random_forest.predict(df)
    decision_tree_predict = decision_tree.predict(df)
    gaussian_predict = gaussian.predict(df)
    return render_template('temp.html',usernames = list3,len=len(list2),user_images=list2, features=int_features,rfr_prediction=random_forest_predict,dt_prediction=decision_tree_predict,gnb_prediction=gaussian_predict)
    
    #return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)