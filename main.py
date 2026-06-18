from fastapi import FastAPI
from routes.agent_routes import router as agent_router
from routes.mission_routes import router as mission_router
from routes.report_routes import router as report_router
import logging
import database.db_connection
#======================================================================================
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
file_handler = logging.FileHandler("logs/app.log", encoding = "utf-8")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
#=======================================================================================

app = FastAPI()
conn = database.db_connection.DBConnection()
conn.create_database()
conn.create_tables()

app.include_router(agent_router)
app.include_router(mission_router)

app.include_router(report_router)