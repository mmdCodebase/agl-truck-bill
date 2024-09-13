from io import BytesIO
import base64
from app.service.ms_graph import get_truck_bill_emails, get_attachments, get_attachment_by_id
from app.db.crud import email_crud, truck_bill_crud
from app.model.email import TruckBillEmailAttachment
from app.service.langchain import extract_json_data, extract_text_from_pdf
# read email from test folder
# create entry into email table
# create entry into attachment table

class TruckBillBot():
    def __init__(self):
        self.import_email_attachment()
        self.extract_truckbill_data()

    def import_email_attachment(self):
        emails = get_truck_bill_emails()
        for email in emails[0:30]:
            try:
                email_crud.create_entry(email['id'], email['subject'], 1)
            except Exception as e:
                print(e)
            for attachment in get_attachments(email["id"]):
                try:
                    email_crud.create_attachment_entry(attachment['id'], email['id'], attachment['name'], attachment['contentType'], attachment['isInline'])
                except Exception as e:
                    print(e)

    def extract_truckbill_data(self):
        # get attachments from table
        attachments = email_crud.get_all_attachment_by_status(email_status_id=1)
        for attachment in attachments:
            attachment = TruckBillEmailAttachment.from_orm(attachment)
            # get bytes

            response = get_attachment_by_id(email_id=attachment.email_id, attachment_id=attachment.attachment_id)
            if attachment.content_type == 'application/pdf' or "pdf" in attachment.file_name.lower():
                with open(f'/tmp/{attachment.file_name}', 'wb') as file:
                    pdf_bytes = base64.b64decode(response['contentBytes'])
                    file.write(pdf_bytes)
                    # send to openai/langchain
                    text = extract_text_from_pdf(f'/tmp/{attachment.file_name}')
                    truckbill = extract_json_data(text)
                    truckbill.email_id = attachment.email_id
                    truckbill.attachment_id= attachment.attachment_id
                    #insert truckbill data
                    try:
                        truckbill_id = truck_bill_crud.insert_truck_bill(truck_bill=truckbill)
                    except Exception as e:
                        print(f'{attachment.attachment_id}: {e}')
                    
                    email_crud.update_entry(email_id=attachment.email_id, email_status_id=4)

                    try:
                        truck_bill_crud.insert_truck_bill_charges(truck_bill_id=truckbill_id, truck_bill=truckbill)
                    except Exception as e:
                        print(f'{attachment.attachment_id}: {e}')
        

TruckBillBot()