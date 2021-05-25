import json

from flask import Blueprint, request, Response, jsonify, make_response, Flask
from flask_restplus import Api, Resource

from app.utils.enum import EnumUtils

from app.config.mongodb_connection.database_connection import mongo_connection
from app.config.mySql_connection.mySql_connection import mysqlbase

from app.dto.DataBaseScanned import DataBaseScanned
from app.dto.Schema import Schema
from app.dto.Table import Table
from app.dto.Column import Column

from app.utils.regexUtils import RegexUtils

from app.utils.encryptUtils import FernetCipher

scan_database = Blueprint("scan_database", __name__)

api = Api(scan_database, title="Scan database", description="Scan or obtain database according to indicated id")

@api.route("/<id>")
class GetDataBaseScan(Resource):
    def get(self, id):

        if id:
            print("id recibido: " + str(id))
            try:
                scan = mongo_connection.db.databases_scan.scans.find_one_or_404({"id_connection": int(id)})
                print("scan: " + str(scan))
                response = Response( json.dumps({"id_connection":int(id), "schema_list":scan.get('schema_list')}), 200)
                response.headers["Content-Type"] = "application/json"
                return response

            except Exception as e:
                message = "Exception occurred: " + str(e)
                response = jsonify({"message": message})
                response.status_code = 404
                return response


@api.route("/<id>", methods = ['POST'])
class ScanDataBase(Resource):
    def post(self, id):

        regexUtils = RegexUtils()

        if id:
            
            print("id recibido: " + str(id)) 
            try:
                connection = mongo_connection.db.databases_scan.connection.find_one_or_404({"id_connection": int(id)})
                print("conexion encontrada: " + str(connection))
            except Exception as e:
                message = "Exception occurred: " + str(e)
                response = jsonify({"message": message})
                response.status_code = 404
                return response
            
            try:
                fernetCipher = FernetCipher()

                # tomar los datos de la connection encontrada
                connection_host = fernetCipher.decrypt(connection.get('host')).decode()
                connection_username = fernetCipher.decrypt(connection.get('username')).decode()
                connection_password = fernetCipher.decrypt(connection.get('password')).decode()
                connection_port = int(fernetCipher.decrypt(connection.get('port')).decode())

                mysqlbase.Connect(self, connection_host, connection_username, connection_password, "", connection_port)
                _, result = mysqlbase.Exec(self, EnumUtils.query.value)
                mysqlbase.Close(self)
                
                schema_list = []
                schema = str
                tables = []
                columns = []
                count = 0

                if result:
                    for row in result:
                        if count == 0:
                            schema = row[0]
                            tables.append(Table(row[1]))
                            columns.append(Column(row[2],regexUtils.get_information_type(row[2])))
                            count+=1
                        else:
                            if schema == row[0]: # coincide el schema
                                if tables[-1].table_name == row[1]: # coincide la table
                                    columns.append(Column(row[2],regexUtils.get_information_type(row[2])))
                                    count+=1
                                else: # no coincide la tabla
                                    tables[-1].add_columns(columns)                    

                                    tables.append(Table(row[1])) # añado nueva tabla a la lista
                                    columns = [] # reinicio lista de columnas
                                    columns.append(Column(row[2],regexUtils.get_information_type(row[2])))
                                    count+=1
                            else: # no coincide el schema, entonces tampoco la tabla

                                tables[-1].add_columns(columns)  # añado las columnas a la ultima tabla

                                schema_to_add = Schema(schema)  # creo schema a añadir

                                schema_to_add.add_tables(tables)
                                schema_list.append(schema_to_add)  # añado a lista de schemas clasificados

                                # reinicio tables y columns buffer
                                tables = []
                                columns = []
                                
                                # añado primer elemento de nuevo schema
                                schema = row[0]
                                tables.append(Table(row[1]))
                                columns.append(Column(row[2],regexUtils.get_information_type(row[2])))
                                count+=1
                    
                    # añado ultimas columnas
                    tables[-1].add_columns(columns)

                    # añado ultimo schema
                    schema_to_add = Schema(schema)
                    schema_to_add.add_tables(tables)
                    schema_list.append(schema_to_add)

                # creo scanner y añado los shcemas analizados
                scanner = DataBaseScanned()
                scanner.add_schemas(schema_list)

                # delete if it exist
                mongo_connection.db.databases_scan.scans.delete_one({"id_connection": int(id)})

                # add scan
                mongo_connection.db.databases_scan.scans.insert({"id_connection": int(id), "schema_list": scanner.__dict__})

                response = Response( json.dumps({"message":"successful scanning"}), 201)
                response.headers["Content-Type"] = "application/json"
                return response

            except Exception as e:
                message = "Exception occurred: " + str(e)
                response = jsonify({"message": message})
                response.status_code = 500
                return response