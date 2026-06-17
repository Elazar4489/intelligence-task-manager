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

    def create_database(self):
        conn = mysql.connector.connect(
            host= DBConnection.host,
            user = DBConnection.user,
            password = DBConnection.password
        )
        cursor = conn.cursor()
        try:
            cursor.execute("""
            CREATE DATABASE IF NOT EXISTS Intelligence_db;
            """)
        finally:
            cursor.close()
            conn.close()

    def create_tables(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS agents (
                id INT PRIMARY KEY AUTO_INCREMENT,
                `name` VARCHAR(50) NOT NULL,
                specialty VARCHAR(50) NOT NULL,
                is_active BOOLEAN DEFAULT TRUE NOT NULL,
                completed_missions INT DEFAULT 0,
                failed_missions INT DEFAULT 0,
                agent_rank ENUM("Junior", "Senior", "Commander")
                );
            """)

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS missions (
                id INT PRIMARY KEY AUTO_INCREMENT,
                title VARCHAR(50) NOT NULL,
                description TEXT NOT NULL,
                location VARCHAR(50) NOT NULL,
                difficulty INT NOT NULL,
                importance INT NOT NULL,
                status VARCHAR(50) DEFAULT 'NEW' NOT NULL,
                risk_level VARCHAR(50) NOT NULL,
                assigned_agent_id INT DEFAULT NULL
                );
            """)
        finally:
            cursor.close()
            conn.close()
# a=DBConnection()
# a.create_tables()