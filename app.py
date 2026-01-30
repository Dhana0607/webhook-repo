from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv(dotenv_path=".env")

app = Flask(__name__)

# ---------------- MongoDB Setup ----------------
MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise Exception("MONGO_URI not found")

client = MongoClient(MONGO_URI)
db = client.github_events
collection = db.events
# ---------------------------------------------


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/events", methods=["GET"])
def get_events():
    events = list(
        collection.find({}, {"_id": 0})
        .sort("timestamp", -1)
        .limit(20)
    )
    return jsonify(events)


@app.route("/webhook", methods=["POST"])
def github_webhook():
    event_type = request.headers.get("X-GitHub-Event")
    payload = request.json  

    # Ignore ping
    if event_type == "ping":
        return jsonify({"msg": "pong"}), 200

    # ---------------- PUSH ----------------
    if event_type == "push":
        commit = payload.get("head_commit")
        if not commit:
            return jsonify({"msg": "no commit"}), 200

        request_id = commit.get("id")

        if collection.find_one({"request_id": request_id}):
            return jsonify({"msg": "duplicate"}), 200

        event_doc = {
            "request_id": request_id,
            "author": payload.get("pusher", {}).get("name"),
            "action": "PUSH",
            "from_branch": None,
            "to_branch": payload.get("ref", "").split("/")[-1],
            "timestamp": commit.get("timestamp")
        }

        collection.insert_one(event_doc)
        return jsonify({"msg": "push stored"}), 201

    # ---------------- PULL REQUEST & MERGE ----------------
    if event_type == "pull_request":
        action = payload.get("action")
        pr = payload.get("pull_request")

        print("PR EVENT:", action)  # Debug log

        if not pr:
            return jsonify({"msg": "no pr"}), 200

        # ----- PULL REQUEST OPENED -----
        if action == "opened":
            request_id = f"pr_{pr['id']}"

            if collection.find_one({"request_id": request_id}):
                return jsonify({"msg": "duplicate pr"}), 200

            event_doc = {
                "request_id": request_id,
                "author": pr["user"]["login"],
                "action": "PULL_REQUEST",
                "from_branch": pr["head"]["ref"],
                "to_branch": pr["base"]["ref"],
                "timestamp": pr["created_at"]
            }

            collection.insert_one(event_doc)
            return jsonify({"msg": "pull request stored"}), 201

        # ----- MERGE (Bonus) -----
        if action == "closed" and pr.get("merged"):
            merge_id = f"merge_{pr['id']}"

            if collection.find_one({"request_id": merge_id}):
                return jsonify({"msg": "duplicate merge"}), 200

            event_doc = {
                "request_id": merge_id,
                "author": pr["user"]["login"],
                "action": "MERGE",
                "from_branch": pr["head"]["ref"],
                "to_branch": pr["base"]["ref"],
                "timestamp": pr["merged_at"]
            }

            collection.insert_one(event_doc)
            return jsonify({"msg": "merge stored"}), 201

    return jsonify({"msg": "event ignored"}), 200


if __name__ == "__main__":
    # IMPORTANT: debug=False to avoid Windows socket errors
    app.run(host="127.0.0.1", port=5000, debug=False)
