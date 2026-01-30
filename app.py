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

@app.route("/webhook", methods=["POST"])
def github_webhook():
    event_type = request.headers.get("X-GitHub-Event")

    # Ignore ping event
    if event_type == "ping":
        return jsonify({"msg": "pong"}), 200

    # Handle PUSH event
    if event_type == "push":
        payload = request.json

        author = payload.get("pusher", {}).get("name")
        ref = payload.get("ref", "")
        to_branch = ref.split("/")[-1]

        commit = payload.get("head_commit", {})
        timestamp = commit.get("timestamp")
        request_id = commit.get("id")

        # Prevent duplicates
        if collection.find_one({"request_id": request_id}):
            return jsonify({"msg": "duplicate event"}), 200

        event_doc = {
            "request_id": request_id,
            "author": author,
            "action": "PUSH",
            "from_branch": None,
            "to_branch": to_branch,
            "timestamp": timestamp
        }

        collection.insert_one(event_doc)
        return jsonify({"msg": "push event stored"}), 201

    return jsonify({"msg": "event ignored"}), 200

@app.route("/events")
def events():
    return jsonify([])


if __name__ == "__main__" :
    app.run(debug=True)