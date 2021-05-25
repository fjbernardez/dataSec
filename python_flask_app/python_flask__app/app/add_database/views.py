from flask import Blueprint, request, jsonify
from flask_restplus import Api, Resource

from app.config.mongodb_connection.database_connection import mongo_connection

from app.utils.encryptUtils import FernetCipher

add_database = Blueprint("add_database", __name__)

api = Api(add_database, title="Add database", description="Allow added connection")


@api.route("/", methods = ['POST'])
class InsertDatabase(Resource):
    def post(self):
        data = request.get_json()
        fernetCipher = FernetCipher() 

        host = fernetCipher.encrypt(data.get("host"))
        port = fernetCipher.encrypt(str(data.get("port")))
        username = fernetCipher.encrypt(data.get("username"))
        password = fernetCipher.encrypt(data.get("password"))

        id_connection = {}

        if host and port and username and password:
            try:
                id_connection = mongo_connection.db.databases_scan.sequences.find_one_and_update({'_id': 'posts'}, {'$inc': {'seq': 1}})
                mongo_connection.db.databases_scan.connection.insert({'id_connection': id_connection.get('seq') + 1,'host':host,'port':port,'username':username,'password':password})
            except Exception as e:
                message = "Exception occurred: " + str(e)
                response = jsonify({"message": message})
                response.status_code = 500
                return response
            response = jsonify({'id_connection': id_connection.get('seq') + 1})
            response.status_code = 201
            return response
        else:
            response = jsonify({"message":"host,port,user and password are requered"})
            response.status_code = 400
            return response