import mysql.connector

class DBConnection:
    host = "localhost"
    user = "root"
    password = "1234"
    database = "Intelligence_db"

    def get_connection(self):
        conn = mysql.connector.connect(
            host= DBConnection.host,
            user = DBConnection.user,
            password = DBConnection.password,
            database = DBConnection.database
        )
        return conn

