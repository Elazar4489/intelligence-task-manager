import database.db_connection

class RankError(Exception):
    pass
class IDNotFoundError(Exception):
    pass

class AgentDB:
    def __init__(self):
        self.connection = database.db_connection.DBConnection()

    def create_agent(self, data: dict) -> dict:
        conn = self.connection.get_connection()
        cursor = conn.cursor()
        try:
            sql = """
            INSERT INTO agents (`name`, `specialty`, `agent_rank`) VALUES (%s, %s, %s);
            """
            cursor.execute(sql, (data['name'], data['specialty'], data['agent_rank']))
            the_id = cursor.lastrowid
            conn.commit()
            agent = self.get_agent_by_id(the_id)
            return agent
        finally:
            cursor.close()
            conn.close()




    def get_all_agents(self):
        conn = self.connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            sql = """
            SELECT * FROM agents;
            """
            cursor.execute(sql)
            all_agents = cursor.fetchall()
            return all_agents
        finally:
            cursor.close()
            conn.close()





    def get_agent_by_id(self, id):
        conn = self.connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            sql = """
            SELECT * FROM agents WHERE `id` = %s
            """
            cursor.execute(sql, (id,))
            agent = cursor.fetchone()
            return agent
        finally:
            cursor.close()
            conn.close()


    def update_agent(self, id: int, data: dict):
        conn = self.connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            sql = """
            UPDATE agents SET `name` = %s, `specialty` = %s, `agent_rank` = %s WHERE `id` = %s
            """
            cursor.execute(sql,(data["name"], data["specialty"], data["agent_rank"], id))
            conn.commit()
            return "done"
        finally:
            cursor.close()
            conn.close()


    def deactivate_agent(self, id):
        conn = self.connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            sql = """
            UPDATE agents SET `is_active` = FALSE WHERE `id` = %s
            """
            cursor.execute(sql, (id,))
            conn.commit()
            return "done"
        finally:
            cursor.close()
            conn.close()

    def increment_completed(self, id):
        # try:
        #     self.check_id_if_exists(id)
        # except IDNotFoundError:
        #     return None
        conn = self.connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            sql = """
            UPDATE agents SET completed_missions = completed_missions+1 WHERE `id` = %s;
            """
            cursor.execute(sql, (id,))
            conn.commit()
            return "done"
        finally:
            cursor.close()
            conn.close()


    def increment_failed(self, id):
        # try:
        #     self.check_id_if_exists(id)
        # except IDNotFoundError:
        #     return None
        conn = self.connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            sql = """
                  UPDATE agents \
                  SET failed_missions = failed_missions + 1 WHERE `id` = %s;
                  """
            cursor.execute(sql, (id,))
            conn.commit()
            return "done"
        finally:
            cursor.close()
            conn.close()

    def get_agent_performance(self, id):
        agent = self.get_agent_by_id(id)
        total = agent["completed_missions"] + agent["failed_missions"]
        try:
            success_rate = (agent["completed_missions"] / total) * 100
            agent_performance = {
                "completed" : agent["completed_missions"],
                "failed": agent["failed_missions"],
                "total": total,
                "success_rate": success_rate
            }
            return agent_performance
        except ZeroDivisionError:
            agent_performance = {
                "completed": agent["completed_missions"],
                "failed": agent["failed_missions"],
                "total": total,
                "success_rate": 0
            }
            return agent_performance



    def count_active_agents(self):
        conn = self.connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            sql = """
            SELECT COUNT(*) AS `active_agents` FROM agents WHERE is_active = TRUE
            """
            cursor.execute(sql)
            active_agents = cursor.fetchone()
            return active_agents
        finally:
            cursor.close()
            conn.close()










#######################################################################################################################

# sss=AgentDB()
# sss.increment_completed(4)
