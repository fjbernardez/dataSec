from flask import Flask

from app.config.mongodb_connection.database_connection import mongo_connection
from app.add_database import add_database
from app.scan_database import scan_database



# Active endpoints noted as following:
# (url_prefix, blueprint_object)
ACTIVE_ENDPOINTS = (
    ("/api/v1/database", add_database),
    ("/api/v1/database/scan", scan_database)
)


def create_app():
    app = Flask(__name__)

    # mongodb initialization  
    #app.secret_key = 'myawesomesecretkey'
    app.config['MONGO_URI'] = 'mongodb://localhost:5000/databases_scan'
    mongo_connection.init_app(app)
    
    # accepts both /endpoint and /endpoint/ as valid URLs
    app.url_map.strict_slashes = False

    # register each active blueprint
    for url, blueprint in ACTIVE_ENDPOINTS:
        app.register_blueprint(blueprint, url_prefix=url)

    return app