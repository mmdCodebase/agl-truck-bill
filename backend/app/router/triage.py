from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.model.truck_bill_processor import TruckBillProcessor
import logging

router = APIRouter(
    tags=["TriageEmails"],
    responses={404: {"description": "Not found"}},
)

logger = logging.getLogger(__name__)
logging.basicConfig(filename='truck_bill_action.log', level=logging.INFO)


@router.post("/TriageEmails")
async def generate_truck_bill_data(background_tasks: BackgroundTasks):
    try:
        processor = TruckBillProcessor()
        
        background_tasks.add_task(processor.process_truck_bill)
        
        logger.info("Added truck bill processing task to background.")
        
        return {"status": "success", "message": "Truck bill processing started."}
    except Exception as e:
        logger.error(f"Error starting truck bill processing: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    
