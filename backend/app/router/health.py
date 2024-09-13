from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Union

router = APIRouter(
    tags=["Health"],
    responses={404: {"description": "Not found"}},
)


@router.get("/Health")
async def get_health():
    return True
