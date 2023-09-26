from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os
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