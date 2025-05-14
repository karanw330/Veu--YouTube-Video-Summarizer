import google.generativeai as genai
import requests
from flask import Flask, render_template, request, jsonify
import datetime
from secret_data import *

from google.auth.exceptions import DefaultCredentialsError


app = Flask(__name__)

genai.configure(api_key=googleapi_key)

model = genai.GenerativeModel("gemini-1.5-flash")

@app.route('/')
def home():
    return render_template("dash.html")

@app.route('/response', methods=['POST', 'GET'])
def response():
    if request.method == 'POST':
        try:
            message = request.form['input']
            reply = model.generate_content(message).text
            print(reply)
            return jsonify(reply)
        except DefaultCredentialsError:
            return jsonify('sorry')


if __name__ == "__main__":
    app.run(debug=True)