"""This module contains the API endpoints for displaying statistics graphs."""

import os
import tempfile
from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from starlette.background import BackgroundTasks
from auth import get_current_active_user
from models import User
from sessions import sessions


router = APIRouter(
    prefix="/statistics",
    tags=["statistics"],
    responses={404: {"description": "Not found"}}
)

stats_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","experimental_data","plots")


@router.get("/network")
def displayNetwork():
    """Returns a FileResponse object containing the network graph."""
    return FileResponse(stats_dir + "/network.png")


@router.get("/mtd_record")
def displayRecord():
    """Returns a FileResponse object containing the MTD record graph."""
    return FileResponse(stats_dir + "/mtd_record.png")


@router.get("/attack_record")
def displayAttackRecord():
    """Returns a FileResponse object containing the attack record graph."""
    return FileResponse(stats_dir + "/attack_record.png")


@router.get("/attack_action")
def displayAttackAction():
    """Returns a FileResponse object containing the attack action record graph."""
    return FileResponse(stats_dir + "/attack_action_record_group_by_host.png")


def delete_temp(path:str) -> None: 
    """Deletes a temporary file."""
    os.unlink(path)


@router.get("/{graph_num}/{graph_type}")
def getGraphType(    
    graph_num: str,
    graph_type: str,
    client: Annotated[User, Depends(get_current_active_user)],
    background_tasks: BackgroundTasks
): 
    """Returns a FileResponse object containing a user's evaluation graph.

    Args:
        graph_num (str): The evaluation graph number.
        graph_type (str): The evaluation graph type.
        client (User): The current active user.
        background_tasks (BackgroundTasks): The background tasks.

    Returns:
        FileResponse: The evaluation graph file.
    """
    fd, path = tempfile.mkstemp(suffix=".png") 
    usr_eval = sessions[client.uuid]["evaluation"][graph_num]
    usr_eval.save_to_temp(path,graph_type)
    background_tasks.add_task(delete_temp, path)
    return FileResponse(path=path)
