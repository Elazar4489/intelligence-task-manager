import database.db_connection
class OutAllowRange(Exception):
    pass
class IDNotFoundError(Exception):
    pass
class StatusError(Exception):
    pass

class MissionDB:
    def __init__(self):
        self.connection = database.db_connection.DBConnection()

    def create_mission(self, data: dict) -> dict:
        conn = self.connection.get_connection()
        cursor = conn.cursor()
        try:
            sql = """
            INSERT INTO missions (`title`, `description`, `location`, `difficulty`, `importance`, `risk_level`) VALUES (%s, %s, %s, %s, %s, %s);
            """
            cursor.execute(sql, (data["title"], data["description"], data["location"], data["difficulty"], data["importance"], data["risk_level"]))
            the_id = cursor.lastrowid
            conn.commit()
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
        # try:
        #     self.check_id_if_exists(id)
        # except IDNotFoundError:
        #     return None
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


    def assign_mission(self, m_id, a_id):
        pass


    def count_all_missions(self):
        conn = self.connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            sql = """
            SELECT COUNT(*) FROM missions;
            """
            cursor.execute(sql)
            all_missions = cursor.fetchone()
            return all_missions
        finally:
            cursor.close()
            conn.close()

    def count_by_status(self, status):
        if not self.check_status_valid(status):
            raise StatusError

        conn = self.connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            sql = """
                  SELECT COUNT(*) FROM missions WHERE `status` = %s;
                  """
            cursor.execute(sql, (status,))
            by_status = cursor.fetchone()
            return by_status
        finally:
            cursor.close()
            conn.close()

    def count_open_missions(self):
        conn = self.connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            sql = """
                  SELECT COUNT(*) \
                  FROM missions \
                  WHERE `status` = %s OR %s; \
                  """
            cursor.execute(sql, ("ASSIGNED", "IN_PROGRESS"))
            open_missions = cursor.fetchone()
            return open_missions
        finally:
            cursor.close()
            conn.close()

    def count_critical_missions(self):
        conn = self.connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            sql = """
                  SELECT COUNT(*) \
                  FROM missions \
                  WHERE `risk_level` = %s;
                  """
            cursor.execute(sql, ("CRITICAL",))
            critical_missions = cursor.fetchone()
            return critical_missions
        finally:
            cursor.close()
            conn.close()


    def get_top_agent(self):
        conn = self.connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            sql = """
                  SELECT * FROM agents ORDER BY `completed_missions` DESC LIMIT 1;
                  """
            # sql1 = """
            # SELECT `assigned_agent_id` FROM missions GROUP BY `assigned_agent_id`;
            # """
            cursor.execute(sql)
            critical_missions = cursor.fetchone()
            return critical_missions
        finally:
            cursor.close()
            conn.close()

