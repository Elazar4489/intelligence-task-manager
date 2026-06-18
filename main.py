from fastapi import FastAPI
from routes.agent_routes import router as agent_router
from routes.mission_routes import router as mission_router
import logging

#======================================================================================
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
file_handler = logging.FileHandler("logs/app.log", encoding = "utf-8")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
#=======================================================================================

app = FastAPI()

app.include_router(agent_router)
app.include_router(mission_router)

