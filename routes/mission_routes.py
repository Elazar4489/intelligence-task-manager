from fastapi import APIRouter, HTTPException
from database.agent_db import AgentDB
from database.mission_db import MissionDB
import routes.agent_routes
import logging


class OutAllowRange(Exception):
    pass
class IDNotFoundError(Exception):
    pass
class StatusError(Exception):
    pass
class AgentNotActiveError(Exception):
    pass


logger = logging.getLogger()
db_missions = MissionDB()
db_agent = AgentDB()

router = APIRouter(prefix= "/missions", tags= ["Missions"])

@router.post("")
def create_mission(title: str, description: str, location: str, difficulty: int, importance: int):
    logger.info("")
    data = {"title": title, "description": description, "location": location, "difficulty": difficulty, "importance": importance}
    try:
        chack_data_for_create_mission(data)
    except ValueError:
        logger.error("")
        raise HTTPException(status_code=422)
    except KeyError:
        logger.error("")
        raise HTTPException(status_code=422)
    except OutAllowRange:
        logger.error("")
        raise HTTPException(status_code=400)
    data["risk_level"] = calculating_risk_level(difficulty, importance)
    logger.info("")
    new_mission = db_missions.create_mission(data)
    logger.info("")
    return new_mission

@router.get("")
def get_all_missions():
    logger.info("")
    all_missions = db_missions.get_all_missions()
    logger.info("")
    return all_missions

@router.get("{id}")
def get_mission_by_id(id: int):
    logger.info("")
    try:
        check_id_if_exists(id)
    except IDNotFoundError:
        logger.error("")
        raise HTTPException(status_code=404)
    logger.info("")
    mission = db_missions.get_mission_by_id(id)
    logger.info("")
    return mission

@router.put("/{id}/assign/{agent_id}")
def assigned_mission(id: int, agent_id: int):
    logger.info("")
    try:
        check_id_if_exists(id)

    except IDNotFoundError:
        logger.error("")
        raise HTTPException(status_code=404)
    try:
        check_id_if_exists2(agent_id)
    except IDNotFoundError:
        logger.error("")
        raise HTTPException(status_code=404)
    try:
        check_other(agent_id, id)
    except AgentNotActiveError:
        logger.error("")
        raise HTTPException(status_code=400, detail="not active")
    except StatusError:
        logger.error("")
        raise HTTPException(status_code=400, detail="not NEW")
    except OutAllowRange:
        logger.error("")
        raise HTTPException(status_code=400, detail="too much missions")
    except ValueError:
        logger.error("")
        raise HTTPException(status_code=400, detail="not Commander")
    logger.info("")
    db_missions.assign_mission(id, agent_id)
    db_missions.update_mission_status(id, "ASSIGNED")
    logger.info("")
    return "done"

@router.put("/{id}/start")
def start_mission(id: int):
    logger.info("")
    try:
        check_id_if_exists(id)
    except IDNotFoundError:
        logger.error("")
        raise HTTPException(status_code=404)
    missions = db_missions.get_mission_by_id(id)
    try:
        check_status(missions["status"], 'IN_PROGRESS')
    except StatusError:
        logger.error("")
        raise HTTPException(status_code=400)
    logger.info("")
    db_missions.update_mission_status(id, 'IN_PROGRESS')
    logger.info("")
    return "done"


@router.put("/{id}/complete")
def complete_mission(id: int):
    logger.info("")
    try:
        check_id_if_exists(id)
    except IDNotFoundError:
        logger.error("")
        raise HTTPException(status_code=404)
    missions = db_missions.get_mission_by_id(id)
    try:
        check_status(missions["status"], 'COMPLETED')
    except StatusError:
        logger.error("")
        raise HTTPException(status_code=400)
    logger.info("")
    db_missions.update_mission_status(id, 'COMPLETED')
    id_agent=db_missions.get_mission_by_id(id)["assigned_agent_id"]
    db_agent.increment_completed(id_agent)
    logger.info("")
    return "done"

@router.put("/{id}/fail")
def fail_mission(id: int):
    logger.info("")
    try:
        check_id_if_exists(id)
    except IDNotFoundError:
        logger.error("")
        raise HTTPException(status_code=404)
    missions = db_missions.get_mission_by_id(id)
    try:
        check_status(missions["status"], 'FAILED')
    except StatusError:
        logger.error("")
        raise HTTPException(status_code=400)
    logger.info("")
    db_missions.update_mission_status(id, 'FAILED')
    id_agent = db_missions.get_mission_by_id(id)["assigned_agent_id"]
    db_agent.increment_failed(id_agent)
    logger.info("")
    return "done"

@router.put("/{id}/cancel")
def cancel_mission(id: int):
    logger.info("")
    try:
        check_id_if_exists(id)
    except IDNotFoundError:
        logger.error("")
        raise HTTPException(status_code=404)
    missions = db_missions.get_mission_by_id(id)
    try:
        check_status(missions["status"], 'CANCELLED')
    except StatusError:
        logger.error("")
        raise HTTPException(400)
    logger.info("")
    db_missions.update_mission_status(id, 'CANCELLED')
    logger.info("")
    return "done"













































def chack_data_for_create_mission(data: dict) -> bool:
    keys = {"title", "description", "location", "difficulty", "importance"}
    input_keys = set(data.keys())
    missing_keys = keys - input_keys
    extra_keys = input_keys - keys
    if missing_keys:
        raise ValueError
    if extra_keys:
        raise KeyError
    if not 1 <= data["difficulty"] <= 10 or not 1 <= data["importance"] <= 10:
        raise OutAllowRange
    return True

def check_id_if_exists(id: int) -> bool:
    conn = db_missions.connection.get_connection()
    cursor = conn.cursor()
    try:
        sql = """
              SELECT id FROM missions;
              """
        cursor.execute(sql)
        ids = [i[0] for i in cursor.fetchall()]
        if id not in ids:
            raise IDNotFoundError
        return True
    finally:
        cursor.close()
        conn.close()

def check_id_if_exists2(id: int) -> bool:
    conn = db_missions.connection.get_connection()
    cursor = conn.cursor()
    try:
        sql = """
              SELECT id FROM missions;
              """
        cursor.execute(sql)
        ids = [i[0] for i in cursor.fetchall()]
        if id not in ids:
            raise IDNotFoundError
        return True
    finally:
        cursor.close()
        conn.close()
def calculating_risk_level(difficulty, importance):
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

def check_status_valid(status):
    statuses = ["NEW", "ASSIGNED", "IN_PROGRESS", "COMPLETED", "FAILED", "CANCELLED"]
    if status not in statuses:
        raise StatusError
    return True


def check_other(agent_id, mission_id):
    agent = db_agent.get_agent_by_id(agent_id)
    mission = db_missions.get_mission_by_id(mission_id)
    if not agent["is_active"]:
        raise AgentNotActiveError
    if mission["status"] != "NEW":
        raise StatusError
    if db_missions.get_open_missions_by_agent(agent_id)["open"] > 2:
        raise OutAllowRange
    if agent["agent_rank"] != "Commander" and mission["risk_level"] == "CRITICAL":
        raise ValueError
    return True

def check_status(old_status, new_status):
    if new_status == "IN_PROGRESS" and old_status != "ASSIGNED":
        raise StatusError
    if (new_status == "COMPLETED" or new_status == "FAILED") and old_status != "IN_PROGRESS":
        raise StatusError
    if new_status == "CANCELLED" and (old_status != "ASSIGNED" and old_status != "NEW"):
        raise StatusError
    return True