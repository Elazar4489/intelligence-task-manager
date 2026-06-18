from fastapi import APIRouter, HTTPException
from database.agent_db import AgentDB
from database.mission_db import MissionDB
import routes.agent_routes
import logging




logger = logging.getLogger()
db_missions = MissionDB()
db_agent = AgentDB()

router = APIRouter(prefix= "/reports", tags= ["Reports"])

@router.get("/summary")
def get_summary():
    logger.info("")
    summary = {
        "active_agents_count": db_agent.count_active_agents()["active_agents"],
        "total_missions": db_missions.count_all_missions()['o'],
        "open_missions": db_missions.count_open_missions()['o'],
        "completed_missions": db_missions.count_by_status("COMPLETED")['s'],
        "failed_missions": db_missions.count_by_status("FAILED")['s'],
        "critical_missions": db_missions.count_critical_missions()['c']
    }
    logger.info("")
    return summary

@router.get("/missions-by-status")
def missions_by_status():
    logger.info("")
    openes = db_missions.count_by_status("NEW")['s'] + db_missions.count_by_status("ASSIGNED")['s']
    by_status = {
        "open": openes,
        "in_progress": db_missions.count_by_status("IN_PROGRESS")['s'],
        "completed": db_missions.count_by_status("COMPLETED")['s'],
        "failed": db_missions.count_by_status("FAILED")['s'],
        "canceled": db_missions.count_by_status("CANCELED")['s']
    }
    logger.info("")
    return by_status

@router.get("/top-agent")
def get_top_agent():
    logger.info("")
    top_agent = db_missions.get_top_agent()
    logger.info("")
    return top_agent