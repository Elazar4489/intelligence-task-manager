from db_connection import DBConnection

class RankError(Exception):
    pass
class IDNotFoundError(Exception):
    pass

class MissionDB:
    def __init__(self):
        self.connection = DBConnection()

    def create_mission(self, data: dict) -> dict:
        try:
            self.chack_data_for_create_mission(data)
        except KeyError:
            raise KeyError
        except RankError:
            raise RankError
        risk_level = self.calculating_risk_level(data["difficulty"], data["importance"])
        conn = self.connection.get_connection()
        cursor = conn.cursor()
        try:
            sql = """
            INSERT INTO missions (`title`, `description`, `location`, `difficulty`, `importance`, `risk_level`) VALUES (%s, %s, %s, %s, %s, %s);
            """
            cursor.execute(sql, (data["title"], data["description"], data["location"], data["difficulty"], data["importance"], risk_level))
            conn.commit()
            the_id = self.return_the_last_id()
            mission = self.get_mission_by_id(the_id)
            return mission
        finally:
            cursor.close()
            conn.close()

    def get_all_missions(self):
        conn = self.connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            sql = """
                  SELECT * \
                  FROM missions; \
                  """
            cursor.execute(sql)
            all_missions = cursor.fetchall()
            return all_missions
        finally:
            cursor.close()
            conn.close()

    def get_mission_by_id(self, id):
        try:
            self.check_id_if_exists(id)
        except IDNotFoundError:
            return None
        conn = self.connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            sql = """
                  SELECT * \
                  FROM missions \
                  WHERE `id` = %s \
                  """
            cursor.execute(sql, (id,))
            mission = cursor.fetchone()
            return mission
        finally:
            cursor.close()
            conn.close()

    def update_mission(self, id: int, data: dict):
        try:
            self.chack_data_for_create_mission(data)
        except KeyError:
            raise KeyError
        except RankError:
            raise RankError
        risk_level = self.calculating_risk_level(data["difficulty"], data["importance"])
        conn = self.connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            sql = """
                  UPDATE missions \
                  SET `title` = %s, `description` = %s, `location` = %s, `difficulty` = %s, `importance` = %s, `risk_level` = %s
                  WHERE `id` = %s \
                  """
            cursor.execute(sql, (data["title"], data["description"], data["location"], data["difficulty"], data["importance"], risk_level, id))
            conn.commit()
            return "done"
        finally:
            cursor.close()
            conn.close()











#################################################################################################################################
    def chack_data_for_create_mission(self, data: dict) -> bool:
        keys = ["title", "description", "location", "difficulty", "importance"]
        for k in data:
            if k not in keys or k == "id":
                raise KeyError
        if not 1 <= data["difficulty"] <= 10 or not 1 <= data["importance"] <= 10:
            raise RankError
        return True

    def check_id_if_exists(self, id: int) -> bool:
        conn = self.connection.get_connection()
        cursor = conn.cursor()
        try:
            sql = """
                  SELECT id FROM agents;
                  """
            cursor.execute(sql)
            ids = [i[0] for i in cursor.fetchall()]
            if id not in ids:
                raise IDNotFoundError
            return True
        finally:
            cursor.close()
            conn.close()

    def return_the_last_id(self):
        conn = self.connection.get_connection()
        cursor = conn.cursor()
        try:
            sql = """
                  SELECT max(id) \
                  FROM missions; \
                  """
            cursor.execute(sql)
            id = cursor.fetchone()[0]
            return id
        finally:
            cursor.close()
            conn.close()

    def calculating_risk_level(self, difficulty, importance):
        num_level = difficulty * 2 + importance
        risk_level = ""
        if 1 <= num_level <= 9:
            risk_level = "LOM"
        elif 10 <= num_level <= 17:
            risk_level = "MEDIUM"
        elif 18 <= num_level <= 24:
            risk_level = "HIGH"
        elif num_level >= 25:
            risk_level = "CRITICAL"
        return risk_level


x = MissionDB()