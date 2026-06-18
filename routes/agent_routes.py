from fastapi import APIRouter, HTTPException
from database.agent_db import AgentDB
import logging



class RankError(Exception):
    pass
class IDNotFoundError(Exception):
    pass


logger = logging.getLogger()
db_agent = AgentDB()

router = APIRouter(prefix= "/agents", tags= ["Agents"])

@router.post("")
def create_agent(name: str, specialty: str, agent_rank: str):
    logger.info("")
    data = {"name": name, "specialty": specialty, "agent_rank": agent_rank}
    try:
        chack_data_for_create_agent(data)
    except ValueError:
        logger.error("")
        raise HTTPException(status_code=422)
    except KeyError:
        logger.error("")
        raise HTTPException(status_code=422)
    except RankError:
        logger.error("")
        raise HTTPException(status_code=400)

    logger.info("")
    new_agent = db_agent.create_agent(data)
    logger.info("")
    return new_agent

@router.get("")
def get_all_agents():
    logger.info("")
    all_agents = db_agent.get_all_agents()
    logger.info("")
    return all_agents

@router.get("/{id}")
def get_agent_by_id(id: int):
    logger.info("")
    try:
        check_id_if_exists(id)
    except IDNotFoundError:
        logger.error("")
        raise HTTPException(status_code=404)
    logger.info("")
    agent = db_agent.get_agent_by_id(id)
    logger.info("")
    return agent

@router.get("/{id}/performance")
def get_agent_performance(id: int):
    logger.info("")
    try:
        check_id_if_exists(id)
    except IDNotFoundError:
        logger.error("")
        raise HTTPException(status_code=404)
    logger.info("")
    agent_performance = db_agent.get_agent_performance(id)
    logger.info("")
    return agent_performance

@router.put("/{id}")
def update_agent(id: int, name: str, specialty: str, agent_rank: str):
    logger.info("")
    data = {"name": name, "specialty": specialty, "agent_rank": agent_rank}
    try:
        check_id_if_exists(id)
    except IDNotFoundError:
        logger.error("")
        raise HTTPException(status_code=404)
    try:
        chack_data_for_create_agent(data)
    except ValueError:
        logger.error("")
        raise HTTPException(status_code=400)
    except KeyError:
        logger.error("")
        raise HTTPException(status_code=401)
    except RankError:
        logger.error("")
        raise HTTPException(status_code=402)
    logger.info("")
    new_agent = db_agent.update_agent(id, data)
    logger.info("")
    return new_agent

@router.put("/{id}/deactivate")
def deactivate_agent(id: int):
    logger.info("")
    try:
        check_id_if_exists(id)
    except IDNotFoundError:
        logger.error("")
        raise HTTPException(status_code=404)
    logger.info("")
    deactivate = db_agent.deactivate_agent(id)
    logger.info("")
    return deactivate






































def chack_data_for_create_agent(data: dict) -> bool:
    keys = {"name", "specialty", "agent_rank"}
    input_keys = set(data.keys())
    missing_keys = keys - input_keys
    extra_keys = input_keys - keys
    if missing_keys:
        raise ValueError
    if extra_keys:
        raise KeyError
    values_of_agent_rank = ["Commander", "Senior", "Junior"]
    rank = data["agent_rank"].capitalize()
    if rank not in values_of_agent_rank:
        raise RankError
    return True

def check_id_if_exists(id: int) -> bool:
    conn = db_agent.connection.get_connection()
    cursor = conn.cursor()
    try:
        sql = """
              SELECT id \
              FROM agents;
              """
        cursor.execute(sql)
        ids = [i[0] for i in cursor.fetchall()]
        if id not in ids:
            raise IDNotFoundError
        return True
    finally:
        cursor.close()
        conn.close()

# s = check_id_if_exists(1)