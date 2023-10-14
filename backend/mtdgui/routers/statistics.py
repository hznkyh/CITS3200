from fastapi import APIRouter
from fastapi.responses import FileResponse
import os
from typing import Annotated
from sessions import sessions
from fastapi import APIRouter, Depends
from starlette.background import BackgroundTasks
from auth import get_current_active_user
from models import User

import tempfile
router = APIRouter(
    prefix="/statistics",
    tags=["statistics"],
    responses={404: {"description": "Not found"}}
)

stats_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","experimental_data","plots")

@router.get("/network")
def displayNetwork():
    return FileResponse(stats_dir + "/network.png")

@router.get("/mtd_record")
def displayRecord():
    return FileResponse(stats_dir + "/mtd_record.png")

@router.get("/attack_record")
def displayAttackRecord():
    return FileResponse(stats_dir + "/attack_record.png")

@router.get("/attack_action")
def displayAttackAction():
    return FileResponse(stats_dir + "/attack_action_record_group_by_host.png")

def delete_temp(path:str) -> None: 
    os.unlink(path)

@router.get("/{graph_name}/{graph_type}")
def getGraphType(    
    graph_name: str,
    graph_type: str,
    client: Annotated[User, Depends(get_current_active_user)],
    background_tasks: BackgroundTasks
): 
    print("Getting ", graph_name)
    fd, path = tempfile.mkstemp(suffix=".png") 
    # print(sessions)
    usr_eval = sessions[client.uuid]["evaluation"][graph_name]
    # print("RETURNED")
    # print(usr_eval)
    usr_eval.save_to_temp(path,graph_type)
    background_tasks.add_task(delete_temp, path)
    return FileResponse(path)
