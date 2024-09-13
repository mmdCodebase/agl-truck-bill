import os
from dotenv import load_dotenv
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain.pydantic_v1 import BaseModel, Field, validator
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader
from app.model.truck_bill import TruckBill, TruckBillCharges
from itertools import groupby
from typing import List
from PIL import Image
import pytesseract


def extract_text_from_pdf(file_path):
    loader = PyPDFLoader(file_path, extract_images=True)
    pages = loader.load_and_split()
    return pages

def extract_json_data(pdf_data):
    load_dotenv()

    model_name = "gpt-3.5-turbo-0125"
    temperature = 0.0
    model = ChatOpenAI(
        model_name=model_name,
        temperature=temperature,
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    parser = PydanticOutputParser(pydantic_object=TruckBill)
    prompt = PromptTemplate(
        template="""
        Extract data from this PDF file.\n Return dates as yyyy-mm-dd format
        Dates are usually displayed in dd-MMM-yy format
        charge_code DCART is for Delivery Charges
        charge_code EQUIP is for Equipment Fee
        charge_code LOCAL is for Local Charge Difference
        charge_code PP is for Pier Pass
        charge_code DCART is for Delivery Cartage
        charge_code SEAL is for Seal Fee
        charge_code DOC is for Documentation Fee
        charge_code ALINE is for Additional HTS Lines
        charge_code PSEC is for Port Security
        charge_code EGF is for Extended Gate Fee
        charge_code CHRENT is for Chassis Rental
        charge_code PREPULL is for Prepull charges
        charge_code FSC is for Fuel Surcharge or FSC
        charge_code BOB is for Bobtail 
        charge_code LINE is for Linehaul
        LIGHTNING TRANSPORTATION (LTNG) maps to LIGHTNING
        EVANS DELIVERY COMPANY INC maps to EVANS
        SEI ACQUISITION LLC DBA SKYLINE EXPRESS LLC maps to SKYLINE
        NEWHAWK XPRESS maps to NEWHAWK
        KCH TRANSPORTATION, INC. maps to KCH
        MARIN TRUCKING INC maps to MARIN
        FLEET INTEGRATED SERVICES maps to FMQR
        BLACK STAR TRUCKING maps to BLACKSTAR
        MOON GLOBAL GROUP maps to MOON
        WALLPORT TRANSIT XPRESS INC maps to WALLPORT
        PRIME LOGIX maps to PRIME
        D. HAUSER, INC maps to DHAUSER
        NGL TRANSPORTATION LLC maps to NGL
        GOLDS GLOBAL LOGISTICS maps to GOLDS
        KNIGHT TRANSPORTATION SERVICES INC maps to KNIG
        D2 LOGISTICS INC maps to DTDI
        INTUIT LOGISTICS INC maps to INTUIT
        ARC TRANSIT maps to ARC
        UNITED INTERMODAL CARRIERS INC maps to UICR
        IMEX LOGISTICS, LLC maps to IMEX
        MANTORIA INC. maps to MANT
        CLASSIC TRANSPORTATION maps to CLASSIC
        HALE INTERMODAL TRUCKING maps to HALE
        AMH ENTERPRISES LLC maps to AMHS
        CONTAINER PORT GROUP maps to CPG
        OHIO INTERMODAL SERVICES, LLC *DO NOT USE* SEE CODE INTERCART maps to OHIOINTER
        SAVANNAH LOGISTICS GROUP LLC maps to SSLF
        THE TRANSPORTER INC maps to TRANSPORTER
        SHIPPERS TRANSPORT EXPRESS maps to SHIPPERS
        CANADIAN NATIONAL RAILWAY maps to CNRAIL
        NATIONAL DRAYAGE SERVICES maps to NATIONAL
        ACW LOGISTICS LLC maps to ACUK
        TRUMP TRANSPORT INC. maps to TRUMP
        HORIZON MIDWEST INC maps to HORIZON
        TRINITY LOGISTICS INC maps to TTFD
        HARRINGTON TRUCKING, INC. maps to HARRINGTON
        PACIFIC COAST EXPRESS maps to PACIFIC
        AMC TRANSPORTATION INC. maps to AMC
        TAMPA CONTAINER TRANSPORT maps to TAMPACONT
        PRO TRANSPORT SAVANNAH INC maps to PORS
        GS TRANSPORT maps to GSTRANSPORT
        OMEGA LOGISTICS maps to OMEGA
        PFS TRANSPORTATION INC maps to PFXC
        STOCKMYER TRUCKING INC maps to STOCKMYER
        FORWARD AIR INC maps to FORWARDAIR
        BIG BLUE BOXES maps to BIGBLUE
        TAX AIRFREIGHT, INC. maps to TAXAIRFREIGH
        IMC LOGISTICS LLC maps to INTERCART
        BARR FREIGHT SYSTEM INC (K737) maps to K737
        LIPSEY LOGISTICS WORLDWIDE LLC maps to LLWL
        VANGUARD LOGISTICS SERVICES maps to VANGUARD
        DENVER INTERMODAL EXPRESS INC. maps to DENVER
        DAYLIGHT LOGISTICS maps to DAYLIGHT
        ULTIMATE BROKERAGE, INC. maps to ULTIMATE
        SSA MARINE maps to OICT
        EXPRESS FREIGHT INC maps to EXPRESS
        ROADONE INTERMODAL LOGISTICS maps to RDKA
        RI - TIME LOGISTICS maps to RITIME
        CALHOUN TRUCK LINES maps to CALHOUN
        HTS LOGISTICS LLC maps to HTSS
        C.L. SERVICES INC. maps to CLSERVICES
        SHIPCO TRANSPORT INC maps to SHIPCO
        FIRST COAST LOGISTICS maps to FIRSTCOAST
        DNJ INTERMODAL SERVICES maps to DNJINTCHH
        AMERICAN MARINE EXPRESS, INC. maps to AMX
        HHM INTL INC maps to HHMM
        3 M & D ENTERPRISES maps to 3MD
        QFS TRANSPORTATION maps to QFS
        FORWARD INTERMODAL (CENTRAL STATES) maps to FORWARDI
        GLOBAL INTERMODAL TRANSPORT maps to GLOBAL
        HERNANDEZ SERVICE CORPORATION maps to HZSP
        ROADONE LOGISTIC SOLUTIONS LLC maps to RINO
        PROMISING TRANSPORTATION LTD. maps to PROTRARCH
        {format_instructions}
        {query}
        """,
        input_variables=["query"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    _input = prompt.format_prompt(query=pdf_data)
    output = model.invoke(_input.to_string())
    # The parsed_output variable now contains the structured data as a Pydantic model instance.
    try:
        parsed_output = parser.invoke(output)
        parsed_output.group_charges_by_code()
        return parsed_output
    except Exception as e:
        print(e)
        return TruckBill()
    
def extract_text_from_image(file_path):
    try:
        # Attempt to open the image and perform OCR
        with Image.open(file_path) as img:
            text = pytesseract.image_to_string(img)
        return text
    except Exception as e:
        print(f"Error extracting text from image {file_path}: {e}")
        return None
