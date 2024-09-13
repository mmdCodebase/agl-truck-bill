from fastapi import APIRouter, Depends, HTTPException, Request, Query, BackgroundTasks
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Union
from app.model.truck_bill import TruckBillData, TruckBillCharges, TruckBillCWUpload
from app.model.truck_bill_email_status import TruckBillEmailStatusEnum
from app.db.crud import TruckBillCRUD, truck_bill_crud
from app.model.truck_bill_processor import TruckBillProcessor
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    tags=["Data"],
    responses={404: {"description": "Not found"}},
)

@router.get("/data", response_model=TruckBillData)
async def get_truck_bill_data(attachment_id: str = Query(...), email_id: str = Query(...)):
    try:
        truck_bill = truck_bill_crud.get_truck_bill_by_email_attachment_id(email_id, attachment_id)
        
        if truck_bill is None:
            logger.error(f"No truck bill found for email_id: {email_id} and attachment_id: {attachment_id}")
            raise HTTPException(status_code=404, detail=f'Truck bill not found for email_id: {email_id} and attachment_id: {attachment_id}')
        
        charges = truck_bill_crud.get_charges_by_truck_bill_id(truck_bill_id=truck_bill.truck_bill_id)
        charges = [
            TruckBillCharges(id=charge[0], charge_code=charge[1], description=charge[2], charges_in_usd=charge[3]) 
            for charge in charges
        ]
        
        truck_bill_data = TruckBillData( 
            email_id=truck_bill.email_id,
            truck_bill_id=truck_bill.truck_bill_id,
            invoice_date=truck_bill.invoice_date,
            agl_shipment_number=truck_bill.agl_shipment_number,
            supplier_cost_ref=truck_bill.supplier_cost_ref,
            creditor=truck_bill.creditor,
            charges=charges,
            subject=truck_bill.subject
        )
        
        return truck_bill_data
    
    except Exception as e:
        logger.exception("An error occurred while loading invoice data")
        raise HTTPException(status_code=500, detail=f'Failed to load invoice data for file {attachment_id}, {str(e)}')

@router.get("/data/CWUpload", response_model=List[TruckBillCWUpload]
            )
async def get_cw_upload_template_data(action_type: TruckBillEmailStatusEnum = Query(...)):
    try:
        email_status_id = {
            TruckBillEmailStatusEnum.CREATED: 1, 
            TruckBillEmailStatusEnum.PENDING_DATA_EXTRACTION: 2, 
            TruckBillEmailStatusEnum.FAILED: 3, 
            TruckBillEmailStatusEnum.READY_FOR_REVIEW: 4, 
            TruckBillEmailStatusEnum.PENDING_CW_UPLOAD: 5, 
            TruckBillEmailStatusEnum.SKIPPED: 6,
            TruckBillEmailStatusEnum.DOWNLOADED: 7,
        }.get(action_type, None)
        
        if email_status_id is None:
            return []

        truck_bills = []
        data = truck_bill_crud.get_charges_by_email_status_id_cw(email_status_id=email_status_id)
        for row in data:
            row_dict = dict(row._mapping)
            truck_bill = TruckBillCWUpload(**row_dict)
            truck_bills.append(truck_bill)
        
        return truck_bills
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Failed to get data for {action_type}, {str(e)}')
    
@router.post("/data")
async def generate_truck_bill_data(background_tasks: BackgroundTasks):
    try:
        processor = TruckBillProcessor()
        background_tasks.add_task(processor.process_truck_bills)
        return True
    except Exception as e:
        print(e)