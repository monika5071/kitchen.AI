import pandas as pd
from flask import Flask, request, render_template, jsonify
import pickle

# Load the trained recipe recommender model
with open('models/recipe_recommender.pkl', 'rb') as f:
    recipe_recommender = pickle.load(f)

# Initialize the Flask application
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    user_input = request.form['ingredients']
    recommendations = recipe_recommender.recommend(user_input)
    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(debug=True)
