from db_connection import DBConnection

class RankError(Exception):
    pass
class IDNotFoundError(Exception):
    pass

class AgentDB:
    def __init__(self):
        self.connection = DBConnection()

    def create_agent(self, data: dict) -> dict:
        try:
            self.chack_data_for_create_agent(data)
        except KeyError:
            raise KeyError
        except RankError:
            raise RankError
        conn = self.connection.get_connection()
        cursor = conn.cursor()
        try:
            sql = """
            INSERT INTO agents (`name`, `specialty`, `agent_rank`) VALUES (%s, %s, %s);
            """
            cursor.execute(sql, (data['name'], data['specialty'], data['agent_rank']))
            conn.commit()
            the_id = self.return_the_last_id()
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
        try:
            self.check_id_if_exists(id)
        except IDNotFoundError:
            return None
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
        try:
            self.chack_data_for_create_agent(data)
        except KeyError:
            raise KeyError
        except RankError:
            raise RankError

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
        try:
            self.check_id_if_exists(id)
        except IDNotFoundError:
            return None
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
        try:
            self.check_id_if_exists(id)
        except IDNotFoundError:
            return None
        conn = self.connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            sql = """
            UPDATE agents SET completed_missions = completed_missions+1
            """
            cursor.execute(sql)
            conn.commit()
            return "done"
        finally:
            cursor.close()
            conn.close()


    def increment_failed(self, id):
        try:
            self.check_id_if_exists(id)
        except IDNotFoundError:
            return None
        conn = self.connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            sql = """
                  UPDATE agents \
                  SET failed_missions = failed_missions + 1 \
                  """
            cursor.execute(sql)
            conn.commit()
            return "done"
        finally:
            cursor.close()
            conn.close()

    def get_agent_performance(self, id):
        try:
            self.check_id_if_exists(id)
        except IDNotFoundError:
            return None
        agent = self.get_agent_by_id(id)
        total = agent["completed_missions"] + agent["failed_missions"]
        success_rate = (agent["completed_missions"] / total) * 100
        agent_performance = {
            "completed" : agent["completed_missions"],
            "failed": agent["failed_missions"],
            "total": total,
            "success_rate": f"{success_rate} %"
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

    def chack_data_for_create_agent(self, data: dict) -> bool:
        keys = ["name", "specialty", "agent_rank"]
        for k in data:
            if k not in keys or k == "id":
                raise KeyError
        values_of_agent_rank = ["Commander", "Senior", "Junior"]
        rank = data["agent_rank"].capitalize()
        print(rank)
        if rank not in values_of_agent_rank:
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
                  FROM agents; \
                  """
            cursor.execute(sql)
            id = cursor.fetchone()[0]
            return id
        finally:
            cursor.close()
            conn.close()






sss=AgentDB()
# print(sss.get_agent_by_id(1))
print(sss.count_active_agents())
# print(sss.get_agent_by_id(1))
# print(sss.return_the_last_id())
# print(sss.update_agent(3,{"name": "donald ben fred", "specialty": "ciber", "agent_rank": 'Senior'}))
# print(sss.get_all_agents())

# print(sss.check_id_if_exists(4)

# print(chack_data_for_create_agent({"name": "eli", "specialty": "data", "agent_rank": 'junior'}))

# utils_agents.check_id_if_exists(1)