import agl_python_helpers.agl_email_helpers.email_attachment_helpers as em
from app.core.config import settings
import shortuuid
import logging
import requests
import base64
import requests
import shortuuid
import os
from io import BytesIO
import pdfplumber

logger = logging.getLogger(__name__)
logging.basicConfig(filename='truck_bill_processor.log', level=logging.INFO)

def get_truck_bill_emails():
    truck_bill_inbox = em.EmailAttachmentHelpers(email_account='agl-email-test',shared_resource='truckbills@aglsupplychain.com')
    #truck_bill_inbox.find_emails_all()
    if settings.FASTAPI_ENVIRONMENT == 'prod':
        folder_name ='inbox'
    else:
        folder_name ='test'

    folder_id = truck_bill_inbox.get_folder_id_by_name(folder_name=folder_name)

    params = {
        '$top': 1000,
        # '$filter': "ReceivedDateTime ge 2024-05-01" 
    }
    truck_bill_inbox.find_email_by_folder_id(folder_id=folder_id, params=params)
    return truck_bill_inbox.emails

def download_truck_bill_files(email):
    truck_bill_inbox = em.EmailAttachmentHelpers(email_account='agl-email-test',shared_resource='truckbills@aglsupplychain.com')
    file_names = truck_bill_inbox.download_email_attachments(email, save_folder='/tmp', file_prefix =shortuuid.uuid())
    return file_names

def move_truck_bill_emails(email_id, folder_name):
    try:
        truck_bill_inbox = em.EmailAttachmentHelpers(email_account='agl-email-test',shared_resource='truckbills@aglsupplychain.com')
        if settings.FASTAPI_ENVIRONMENT == 'prod':
            folder_id = 'AAMkADRkNTVkNTkyLTk1MmUtNDNhYy05NDdjLWUzNmM5YmI5ZTYwNgAuAAAAAACWy4VRFSR5TZt-OanExLefAQA-QFC3mEJiTYdtSoFJKBb1AAb90DKOAAA='
        else:
            folder_id = truck_bill_inbox.get_folder_id_by_name(folder_name)
        truck_bill_inbox.move_email_to_folder_id(email_id, folder_id)
    except Exception as e:
        print(e)
        raise
    return True

def move_emails_back_to_test():
    try:
        truck_bill_inbox = em.EmailAttachmentHelpers(email_account='agl-email-test', shared_resource='truckbills@aglsupplychain.com')
        source_folder_id = truck_bill_inbox.get_folder_id_by_name(folder_name='test_cargowise_tb')
        destination_folder_id = truck_bill_inbox.get_folder_id_by_name(folder_name='test')

        truck_bill_inbox.find_email_by_folder_id(folder_id=source_folder_id)

        emails = truck_bill_inbox.emails
        
        if emails is None:
            logger.warning("No emails found in the test_cargowise_tb folder to move back.")
            print("No emails found in the test_cargowise_tb folder to move back.")
            return
        
        for email in emails:
            truck_bill_inbox.move_email_to_folder_id(email['id'], destination_folder_id)
        
        logger.info(f"Moved {len(emails)} emails back to the test folder.")
    except Exception as e:
        logger.error(f"Error moving emails back to test folder: {str(e)}")
        raise


def get_file_bytes(email_id, truck_bill_inbox):
    #truck_bill_inbox = em.EmailAttachmentHelpers(email_account='agl-email-test',shared_resource='truckbills@aglsupplychain.com')
    folder_id = truck_bill_inbox.get_folder_id_by_name(folder_name='inbox')
    params = {
        '$top': 1000,
        '$filter': "ReceivedDateTime ge 2024-05-01" 
    }
    email = {"id": email_id}
    #truck_bill_inbox.find_email_by_folder_id(folder_id=folder_id, params=params)
    attachments = truck_bill_inbox.fetch_email_attachments(email)
    try:
        bytes = attachments[0]['contentBytes']
    except Exception as e:
        print(e)
        bytes = ''
        raise e
    return bytes

def extract_text_from_attachment(email):
    extracted_texts = []

    try:
        # Fetch attachments from the email
        truck_bill_inbox = em.EmailAttachmentHelpers(email_account='agl-email-test',shared_resource='truckbills@aglsupplychain.com')
        attachments = truck_bill_inbox.fetch_email_attachments(email)

        if not attachments:
            print("No attachments found.")
            return []

        print(f"Found {len(attachments)} attachments.")

        for attachment in attachments:
            bytes = attachment['contentBytes']
            decoded_bytes = base64.b64decode(bytes)
            pdf_file = BytesIO(decoded_bytes)
            text = ''
            with pdfplumber.open(pdf_file) as pdf:
                for page in pdf.pages:
                    text += page.extract_text()

            extracted_texts.append(text)

    except Exception as e:
        print(f"Error downloading attachments: {e}")
        return []

    return extracted_texts

def update_email(email_id, subject, body):
    truck_bill_inbox = em.EmailAttachmentHelpers(email_account='agl-email-test',shared_resource='truckbills@aglsupplychain.com')
    url = f"https://graph.microsoft.com/v1.0/users/truckbills@aglsupplychain.com/messages/{email_id}"
    body = {
        "subject" : subject,
        "body": body,
        "inferenceClassification": "other"
    }
    try:
        response = requests.patch(url =url, headers=truck_bill_inbox.headers, json=body)
        response.raise_for_status()
    except Exception as e:
        logger.error(f"Error Updating email: {str(e)}")
        raise

def get_attachments(id):
    truck_bill_inbox = em.EmailAttachmentHelpers(email_account='agl-email-test',shared_resource='truckbills@aglsupplychain.com')
    url= truck_bill_inbox.GRAPH_API_ENDPOINT + f"/messages/{id}/attachments"

    try:
        response = requests.get(url=url, headers=truck_bill_inbox.headers)
        response.raise_for_status()
    except Exception as e:
        logger.error(f"Getting Attachments: {str(e)}")
        raise

    return response.json()["value"]

def get_attachment_by_id(email_id, attachment_id):
    truck_bill_inbox = em.EmailAttachmentHelpers(email_account='agl-email-test',shared_resource='truckbills@aglsupplychain.com')
    url= truck_bill_inbox.GRAPH_API_ENDPOINT + f"/messages/{email_id}/attachments/{attachment_id}"

    try:
        response = requests.get(url=url, headers=truck_bill_inbox.headers)
        response.raise_for_status()
    except Exception as e:
        logger.error(f"Getting Attachments: {str(e)}")
        raise
    return response.json()
    
