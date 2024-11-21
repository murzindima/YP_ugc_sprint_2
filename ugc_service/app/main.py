from http import HTTPStatus

from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_restx import Api
from pydantic import ValidationError

from api.v1.events import events_namespace
from app.core.config import app_settings

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = app_settings.jwt_secret_key

api = Api(
    app, version="1.0", title="UGC API", description="API for user generated content"
)
api.add_namespace(events_namespace, path="/events")

jwt = JWTManager()
jwt.init_app(app)


@app.errorhandler(ValidationError)
def handle_validation_error(e):
    return jsonify(error=str(e)), HTTPStatus.BAD_REQUEST


if __name__ == "__main__":
    app.run(debug=app_settings.debug)
