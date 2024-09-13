from fastapi import APIRouter, Depends, HTTPException, Request, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Union
from app.model.email import TruckBillEmail
from app.db.crud import TruckBillEmailCRUD

router = APIRouter(
    tags=["Emails"],
    responses={404: {"description": "Not found"}},
)

@router.get("/Emails", response_model=List[TruckBillEmail])
async def get_emails(email_status_id: int = Query(...)):
    try:    
        crud = TruckBillEmailCRUD()
        data = crud.read_entry_by_status_id(status_id=email_status_id)
        for email in data:
            attachments = crud.read_attachment_by_email_id(email.email_id)
            print(attachments)
            email.attachments = attachments
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Failed to get emails {str(e)}')