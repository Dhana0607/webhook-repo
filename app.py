from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=".env")
app = Flask(__name__)

#Mongo db setup
client = MongoClient(os.getenv("MONGO_URI"))
db = client.github_events
collection = db.events

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/webhook", methods = ["POST"])
def webhook():
    return jsonify({"status" : "ok"})

@app.route("/events")
def events():
    return jsonify([])

if __name__ == "__main__" :
    app.run(debug=True)