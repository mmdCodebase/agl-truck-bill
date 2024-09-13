from fastapi import FastAPI
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.router import triage, health, email, file, data
from agl_python_helpers.agl_email_helpers import email_attachment_helpers as em 
# import app.agl.agl_python_helpers.agl_email_helpers.email_attachment_helpers as em
from fastapi_utils.tasks import repeat_every
from app.db.database import TruckBillDB
from app.db.model import Base


# Create the table
def create_table():
    engine = TruckBillDB.get_engine()
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

# if settings.FASTAPI_ENVIRONMENT == 'test':
#     create_table()


middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS + [settings.API_URL],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
        expose_headers=["Content-Disposition"],
    ),
]
app = FastAPI(title=settings.PROJECT_NAME, middleware=middleware)
app.include_router(health.router)
app.include_router(triage.router, prefix="/V1")
app.include_router(email.router, prefix="/V1")
app.include_router(file.router, prefix="/V1")
app.include_router(data.router, prefix="/V1")

def create_truck_bill_inbox():
    return em.EmailAttachmentHelpers(email_account='agl-email-test', shared_resource='truckbills@aglsupplychain.com')

def get_truck_bill_inbox():
    return app.state.truck_bill_inbox

@app.on_event("startup")
@repeat_every(seconds=60 * 10)  # 1 hour
async def startup_event():
    try:
        del app.state.truck_bill_inbox
        print('remove old api token')
    except Exception as e:
        print(e)

    app.state.truck_bill_inbox = create_truck_bill_inbox()
    print('Refresh API token')

# @app.on_event("startup")        
# @repeat_every(seconds=60 * 60)  # 1 hour
# def cleanup_old_mails():
#     from app.service.ms_graph import get_truck_bill_emails
#     from app.db.crud import email_crud
#     from app.main import create_truck_bill_inbox
#     import requests

#     data = email_crud.get_all_email_status(email_status_id=4)
#     inbox = create_truck_bill_inbox()

#     for email in data:
#         response = requests.get(
#                     inbox.GRAPH_API_ENDPOINT + '/messages/{0}'.format(email.email_id),
#                     headers=inbox.headers
#                 )
#         if response.status_code == 404:
#             print("not found")
#             email_crud.update_entry(email_id=email.email_id, email_status_id=6)