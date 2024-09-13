import requests

class WisemanClient:
    def __init__(self):
        # Base URL for Wiseman service
        self.base_url = "https://agl-wiseman.terraportation.com/V1/UniversalXML/UniversalEvent"

    def upload_to_wiseman(self, shipment_id: str, event_type: str, doc_type: str, file_path: str):

        url = f"{self.base_url}/{shipment_id}/Events/{event_type}"
        params = {'doc_type': doc_type}
        files = {'file': open(file_path, 'rb')}
                
        response = requests.post(url, params=params, files=files)

        if response.status_code == 200:
            print('Success:', response.json())
        else:
            print('Error:', response.status_code, response.text)



