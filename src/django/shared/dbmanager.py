import mysql.connector as connector
import json

class DBManager:
    class __DBManager:

        def __init__(self):
            self.connections = {}
            with open("shared/connections.json") as conns:
                self.config = json.load(conns)

    instance = None
    

    def __init__(self):
        if not DBManager.instance:
            DBManager.instance = DBManager.__DBManager()


    def getconnection(self, dbname):
        if dbname not in self.instance.connections:
                if dbname not in self.instance.config:
                    raise Exception (f'Missing config for database: {dbname}')
                self.instance.connections[dbname] = connector.connect(**self.instance.config[dbname])
        return self.instance.connections[dbname]

            
