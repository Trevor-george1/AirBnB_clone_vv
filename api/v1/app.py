#!/usr/bin/python3
"""createing a flask app and
    Starting my api
"""
import os
from flask import Flask
from models import storage
from api.v1.views import app_views
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)


CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
@app.teardown_appcontext
def teardown(exception):
    """closes the current SQLalchemy session"""
    storage.close()


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
