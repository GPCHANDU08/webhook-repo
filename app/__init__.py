from flask import Flask
from app.webhook.routes import webhook
from app.extensions import mongo
import os

def create_app():
    # ✅ Force Flask to look in the correct absolute templates folder
    base_dir = os.path.abspath(os.path.dirname(__file__))
    template_path = os.path.join(base_dir, '..', 'templates')
    app = Flask(__name__, template_folder=template_path)

    app.config["MONGO_URI"] = "mongodb+srv://starkC2084:Chandu2084@cluster0.nimw62u.mongodb.net/webhook_db?retryWrites=true&w=majority&appName=Cluster0"
    mongo.init_app(app)

    app.register_blueprint(webhook)

    return app
