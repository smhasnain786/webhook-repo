from flask import Blueprint, json, jsonify, request, render_template
from app.extensions import mongo
from datetime import datetime
import humanize

webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')


def format_timestamp(ts):
    try:
        # Parse UTC timestamp properly
        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))

        day_ord = humanize.ordinal(dt.day)
        return dt.strftime(f"{day_ord} %B %Y - %I:%M %p UTC")

    except Exception:
        return ts

@webhook.route('/events', methods=["GET"])
def get_events():
    try:
        events = list(mongo.db.events.find().sort("timestamp", -1))
        for event in events:
            event['_id'] = str(event['_id'])  
            event['timestamp'] = format_timestamp(event['timestamp'])
        return jsonify(events), 200
    except Exception as e:
        print("Error retrieving events:", e)
        return jsonify({"error": "An error occurred while retrieving events."}), 500 

@webhook.route('', methods=["GET"])
def home_page():
    try:
    # Retrieve all events from MongoDB
        events = list(mongo.db.events.find())
        for event in events: 
            event['timestamp'] = format_timestamp(event['timestamp'])
        print("Events found:", events)
        return render_template("index.html", event=events)
    except Exception as e:
        print("Error retrieving events:", e)
        return "An error occurred while retrieving events.", 500

@webhook.route('/receiver', methods=["POST"])
def receiver():
    if request.method == "POST":
        event_type = request.headers.get('X-Github-Event')
        payload = request.json

        if event_type == "push":
            doc = {
            "request_id": payload["head_commit"]["id"],  # commit hash
            "author": payload["pusher"]["name"],
            "action": "PUSH",
            "from_branch": None,
            "to_branch": payload["ref"].split("/")[-1],
            "timestamp": payload["head_commit"]["timestamp"]
            }

            mongo.db.events.insert_one(doc)
            return jsonify({"status": "stored", "type": "push"}), 200
        
        elif event_type == "pull_request":
            pr= payload['pull_request']
            action = payload['action']

            if action == 'closed' and pr['merged']:
                doc = {
                "request_id": str(pr["id"]),
                "author": pr["user"]["login"],
                "action": "MERGE",
                "from_branch": pr["head"]["ref"],
                "to_branch": pr["base"]["ref"],
                "timestamp": pr["merged_at"]
                }

                mongo.db.events.insert_one(doc)
                return jsonify({"status": "stored", "type": "merge"}), 200
            
            elif action == 'opened':
                doc = {
                "request_id": str(pr["id"]),
                "author": pr["user"]["login"],
                "action": "PULL_REQUEST",
                "from_branch": pr["head"]["ref"],
                "to_branch": pr["base"]["ref"],
                "timestamp": pr["created_at"]
                }
                 
                mongo.db.events.insert_one(doc)
                return jsonify({"status": "stored", "type": "pull_request"}), 200
             
            return jsonify({"msg": "PR event ignored"}), 200