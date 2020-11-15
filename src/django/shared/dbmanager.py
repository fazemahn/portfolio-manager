import mysql.connector as connector
import json

class DBManager:
    class __DBManager:

        def __init__(self):
            with open("shared/connections.json") as config:
                data = json.load(config)
                db = data["monte_carlo"]
                self.connection = connector.connect(**db)

        def __str__(self):
            return repr(self)

    instance = None

    def __init__(self):
        if not DBManager.instance:
            DBManager.instance = DBManager.__DBManager()

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def getconnection(self):
        return self.instance.connection
