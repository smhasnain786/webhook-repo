from flask import Flask

from app.webhook.routes import webhook
from app.extensions import mongo


# Creating our flask app
def create_app():

    app = Flask(__name__)
    app.config["MONGO_URI"] = "mongodb+srv://admin:admin@cluster0.mrabfka.mongodb.net/github_events?retryWrites=true&w=majority"
    mongo.init_app(app)
    # registering all the blueprints
    app.register_blueprint(webhook)
    
    return app
