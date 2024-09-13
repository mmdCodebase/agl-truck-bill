from fastapi import APIRouter, Depends, HTTPException, Request, Query, Body, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List, Union, Optional
from app.service.s3 import s3_download_file
from io import BytesIO
from app.model.truck_bill import TruckBillCWUpload
from datetime import datetime
from app.service.cw_upload import create_cw_upload_file
from app.db.crud import email_crud
from app.service.ms_graph import get_file_bytes, get_attachment_by_id
import agl_python_helpers.agl_email_helpers.email_attachment_helpers as em
import base64
import time

router = APIRouter(
    tags=["File"],
    responses={404: {"description": "Not found"}},
)

def get_truck_bill_inbox():
    from main import app  # Local import to avoid circular dependency
    return app.state.truck_bill_inbox


@router.get("/file")
async def get_file(
                attachment_id: Optional[str] = Query(None),
                file_name: Optional[str] = Query(None, description="Key of the file to download from S3"),
                email_id: Optional[str] = Query(None),
                truck_bill_inbox = Depends(get_truck_bill_inbox)
                ):
    try:
        media_type = 'application/octet-stream'
        if attachment_id is not None and email_id is not None:
            print('here')
            file_content=get_attachment_by_id(email_id=email_id, attachment_id=attachment_id)
            print('here')
            
            media_type=file_content['contentType']
            file_name=file_content['name']
            file_content=base64.b64decode(file_content['contentBytes'])
            
            
        if email_id and attachment_id is None:
            file_content=get_file_bytes(email_id, truck_bill_inbox)
            file_content=base64.b64decode(file_content)

        if email_id is None and attachment_id is None:
            file_content = s3_download_file(file_name, 'agl-debit-notes', file_name)

        response = StreamingResponse(BytesIO(file_content), media_type=media_type)
        response.headers['Content-Disposition'] = f'attachment; filename={file_name}'
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/file")
async def create_file(request: List[TruckBillCWUpload]):
    file_name = f'CW1_NewChargeRate_UpSert_{datetime.now()}.xlsx'
    file_stream = create_cw_upload_file(request)
    response = StreamingResponse(file_stream, media_type='application/octet-stream')
    response.headers['Content-Disposition'] = f'attachment; filename={file_name}'
    for row in request:
        if row.email_id:
            email_crud.update_entry(email_id=row.email_id, email_status_id=7)
    return response