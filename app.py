from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)

#Mongo db setup
MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise Exception("MONGO_URI not found in environment variables")

client = MongoClient(MONGO_URI)
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

@app.route("/test-db")
def test_db():
    collection.insert_one({"test": "atlas_connection"})
    return "MongoDB Atlas connected!"


if __name__ == "__main__" :
    app.run(debug=True)