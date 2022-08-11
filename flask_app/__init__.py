from newsapi import NewsApiClient
from flask import Flask
import os
app = Flask(__name__)
newsapi = NewsApiClient(api_key=os.environ.get("API_KEY"))
app.secret_key =  os.environ.get("FLASK_KEY")
