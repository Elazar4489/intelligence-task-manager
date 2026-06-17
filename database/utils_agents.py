from agent_db import RankError
from db_connection import DBConnection

def chack_data_for_create_agent(data: dict) -> bool:
    keys = ["name", "specialty", "agent_rank"]
    for k in data:
        if k not in keys:
            raise KeyError
    values_of_agent_rank = ["Commander", "Senior", "Junior"]
    rank = data["agent_rank"].capitalize()
    print(rank)
    if rank not in values_of_agent_rank:
        raise RankError
    return True

def check_id_if_exists(id: int) -> bool:
    connection = DBConnection()
    conn = connection.get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        sql = """
        SELECT id FROM agents
        """
        cursor.execute(sql)
        ids = cursor.fetchall()
        print(ids)
    finally:
        cursor.close()
        conn.close()