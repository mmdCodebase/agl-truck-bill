from fastapi import HTTPException
from app.service.langchain import extract_json_data as extract_json_data_langchain, extract_text_from_pdf as extract_text_from_pdf_langchain, extract_text_from_image
from app.service.ms_graph import get_truck_bill_emails, download_truck_bill_files, move_truck_bill_emails, move_emails_back_to_test, update_email, extract_text_from_attachment
from app.service.wiseman import WisemanClient
import re
import logging
import os
from bs4 import BeautifulSoup

client = WisemanClient()

logger = logging.getLogger(__name__)
logging.basicConfig(filename='truck_bill_processor.log', level=logging.INFO)

class TruckBillProcessor:
    #move_emails_back_to_test()

    def process_truck_bill(self):
        emails = get_truck_bill_emails()
        for email in emails:
            try:
                self._process_email(email)
            except Exception as e:
                logger.error(f"Error processing email {email['id']}: {str(e)}")
        print("finished processing")

    def _process_email(self, email):
        agl_shipment_number = self._extract_agl_shipment_number(email['subject'])

        if agl_shipment_number is None:
            logger.info(f"No reference number found in email {email['id']}, skipping.")
            return 
        
        files = download_truck_bill_files(email)
        file_upload_successful = True

        if len(files) == 1:
            try:
                self._process_file(files[0], agl_shipment_number)
            except Exception as e:
                file_upload_successful = False
        else:
            for file in files:
                try:
                    _, file_extension = os.path.splitext(f"/tmp/{file}")
                    file_extension = file_extension.lower()
                    print("fileextensioin", file_extension)
                    if file_extension == '.pdf':
                        text_pdf = extract_text_from_pdf_langchain(f"/tmp/{file}")
                        full_text = ''.join([doc.page_content for doc in text_pdf])
                        agl_shipment_number_pdf_attachment = self._extract_agl_shipment_number_from_attachment(full_text)
                        if agl_shipment_number_pdf_attachment is None:
                            return
                        self._process_file(file, agl_shipment_number_pdf_attachment)
                    elif file_extension in ['.jpg', '.jpeg', '.png', '.tif', '.tiff']:
                        try:
                            print("Processing image file...")
                            text_image = extract_text_from_image(f"/tmp/{file}")
                            if text_image is None:
                                print("Failed to extract text from image.")
                                return
                            print("Extracted text from image:", text_image)
                            agl_shipment_number_attachment = self._extract_agl_shipment_number_from_attachment(text_image)
                            print("Extracted AGL shipment number from image:", agl_shipment_number_attachment)

                            if agl_shipment_number_attachment is None:
                                print("No AGL shipment number found in the image.")
                                return

                            self._process_file(file, agl_shipment_number_attachment)

                        except Exception as e:
                            print(f"Error processing image file {file}: {e}")
                    else:
                        raise ValueError(f"Unsupported file type: {file_extension}")
                except Exception as e:
                    logger.error(f"Error processing file {file} for email {email['id']}: {str(e)}")
                    file_upload_successful = False
        
        if file_upload_successful:
            new_body = self._modify_email_body(email['body'], f"Processed by agl-truckbill service; system: CW, REF: {agl_shipment_number}, FILE UPLOAD SUCCESS\n")
            new_subject = "Processed by agl-truckbill: " + email["subject"]
            update_email(email['id'], new_subject, new_body)
            self._move_email(email['id'])
        else:
            logger.warning(f"Email {email['id']} not moved because file upload failed.")

    def _extract_agl_shipment_number(self, subject):
        pattern = r'S\d{11}'
        match = re.search(pattern, subject)
        
        if match:
            print("matchtrue")
            return match.group()
        else:
            logger.warning("No reference number found in the subject.")
            print("matchfalse")
            return None
        
    def _extract_agl_shipment_number_from_attachment(self, text):
        pattern = r'\bS\d{11}\b'
        match = re.search(pattern, text)
        
        if match:
            logger.info("AGL shipment number found in email attachment.")
            return match.group()
        else:
            logger.warning("No AGL shipment number found in email attachment.")
            return None

    def _process_file(self, file, agl_shipment_number):
        logger.info(f"Processing file: {file}")
        file_path = f"/tmp/{file}"
        
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return
        
        self._upload_attachments_to_cw(agl_shipment_number, file_path)

    def _upload_attachments_to_cw(self, agl_shipment_number, file_path):
        try:
            client.upload_to_wiseman(
                shipment_id=agl_shipment_number,
                event_type="DDI",
                doc_type="TRB",
                file_path=file_path
            )
            logger.info("CW upload file created successfully.")
            return True
        except Exception as e:
            logger.error(f"Failed to upload CW file: {str(e)}")
            return False
        

    def _move_email(self, email_id):
        try:
            move_truck_bill_emails(email_id, "test_cargowise_tb")
            logger.info(f"Email {email_id} moved to the test_cargowise_tb folder.")
        except Exception as e:
            logger.error(f"Error moving email {email_id} to test_cargowise_tb folder: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error moving email {email_id} to test_cargowise_tb folder: {str(e)}",
            )
    
    def _modify_email_body(self, body, new_text):
        new_content = new_text
        if body['contentType'] == 'html':
            soup = BeautifulSoup(body['content'], 'lxml')
            # Find the body tag and append the text
            body_tag = soup.body
            body_tag.insert(0, new_text)
            new_content = soup.get_text()

        if body['contentType'] == 'text':
            new_content = new_text + body['content']
        
        new_body = {
            "contentType": body['contentType'],
            "content": new_content
        }
        return new_body

# if __name__ == "__main__":
#     processor = TruckBillProcessor()
#     #processor.process_truck_bill()
