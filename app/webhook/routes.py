from flask import Blueprint, request, render_template
from datetime import datetime
from app.extensions import mongo

webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')


@webhook.route('/receiver', methods=["POST"])
def receiver():
    data = request.get_json()
    event_type = request.headers.get("X-GitHub-Event", "unknown")
    author = data.get('sender', {}).get('login', 'Unknown')
    timestamp = datetime.utcnow().strftime('%d %B %Y - %I:%M %p UTC')

    payload = {
        "author": author,
        "action_type": event_type,
        "timestamp": timestamp
    }

    if event_type == 'push':
        payload["to_branch"] = data.get('ref', '').split('/')[-1]

    elif event_type == 'pull_request':
        pr = data.get('pull_request', {})
        payload["from_branch"] = pr.get('head', {}).get('ref')
        payload["to_branch"] = pr.get('base', {}).get('ref')

        # ✅ Check if the PR is merged
        if pr.get('merged') is True and pr.get('state') == 'closed':
            payload["action_type"] = "merge"
        else:
            payload["action_type"] = "pull_request"

    mongo.db.events.insert_one(payload)
    return {"status": "success"}, 200



@webhook.route('/events', methods=["GET"])
def get_events():
    events = list(mongo.db.events.find().sort("_id", -1).limit(10))

    formatted = []
    for e in events:
        author = e.get("author", "Unknown")
        to_branch = e.get("to_branch", "")
        from_branch = e.get("from_branch", "")
        ts = e.get("timestamp", "")
        action = e.get("action_type", "")

        if action == "push":
            msg = f'{author} pushed to {to_branch} on {ts}'
        elif action == "pull_request":
            msg = f'{author} submitted a pull request from {from_branch} to {to_branch} on {ts}'
        elif action == "merge":
            msg = f'{author} merged branch {from_branch} to {to_branch} on {ts}'
        else:
            msg = f'{author} did {action} on {ts}'

        formatted.append(msg)

    return {"events": formatted}



@webhook.route('/', methods=["GET"])
def home():
    return render_template("index.html")
