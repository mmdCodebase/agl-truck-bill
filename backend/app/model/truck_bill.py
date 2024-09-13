from pydantic import BaseModel, field_validator
from datetime import date, datetime
from typing import List, Optional, Dict, Union
from itertools import groupby
from enum import Enum


class ChargeCode(str, Enum):
    FRT = "FRT"
    AGEN = "AGEN"
    AMS = "AMS"
    EQUIP = "EQUIP"
    ORIGIN = "ORIGIN"
    LOCAL = "LOCAL"
    PP = "PP"
    TERFEE = "TERFEE"
    TELEX = "TELEX"
    VGM = "VGM"
    DCART = "DCART"
    SEAL = "SEAL"
    DOC = "DOC"
    BOOK = "BOOK"
    CCLR = "CCLR"
    ALINE = "ALINE"
    PSEC = "PSEC"
    EGF = "EGF"
    TRANS = "TRANS"
    CHRENT = "CHRENT"
    FSC = "FSC"
    BOB = "BOB"
    LINE = "LINE"
    PREPULL = "PREPULL"

class OrgCode(str, Enum):
    LIGHTNING="LIGHTNING"
    EVANS="EVANS"
    SKYLINE="SKYLINE"
    NEWHAWK="NEWHAWK"
    KCH="KCH"
    MARIN="MARIN"
    FMQR="FMQR"
    BLACKSTAR="BLACKSTAR"
    MOON="MOON"
    WALLPORT="WALLPORT"
    PRIME="PRIME"
    DHAUSER="DHAUSER"
    NGL="NGL"
    GOLDS="GOLDS"
    KNIG="KNIG"
    DTDI="DTDI"
    INTUIT="INTUIT"
    ARC="ARC"
    UICR="UICR"
    IMEX="IMEX"
    MANT="MANT"
    CLASSIC="CLASSIC"
    HALE="HALE"
    AMHS="AMHS"
    CPG="CPG"
    OHIOINTER="OHIOINTER"
    SSLF="SSLF"
    TRANSPORTER="TRANSPORTER"
    SHIPPERS="SHIPPERS"
    CNRAIL="CNRAIL"
    NATIONAL="NATIONAL"
    ACUK="ACUK"
    TRUMP="TRUMP"
    HORIZON="HORIZON"
    TTFD="TTFD"
    HARRINGTON="HARRINGTON"
    PACIFIC="PACIFIC"
    AMC="AMC"
    TAMPACONT="TAMPACONT"
    PORS="PORS"
    GSTRANSPORT="GSTRANSPORT"
    OMEGA="OMEGA"
    PFXC="PFXC"
    STOCKMYER="STOCKMYER"
    FORWARDAIR="FORWARDAIR"
    BIGBLUE="BIGBLUE"
    TAXAIRFREIGH="TAXAIRFREIGH"
    INTERCART="INTERCART"
    K737="K737"
    LLWL="LLWL"
    VANGUARD="VANGUARD"
    DENVER="DENVER"
    DAYLIGHT="DAYLIGHT"
    ULTIMATE="ULTIMATE"
    OICT="OICT"
    EXPRESS="EXPRESS"
    RDKA="RDKA"
    RITIME="RITIME"
    CALHOUN="CALHOUN"
    HTSS="HTSS"
    CLSERVICES="CLSERVICES"
    SHIPCO="SHIPCO"
    FIRSTCOAST="FIRSTCOAST"
    DNJINTCHH="DNJINTCHH"
    AMX="AMX"
    HHMM="HHMM"
    QFS="QFS"
    FORWARDI="FORWARDI"
    GLOBAL="GLOBAL"
    HZSP="HZSP"
    RINO="RINO"
    PROTRARCH="PROTRARCH"

class TruckBillCharges(BaseModel):
    id: Optional[int] = None
    charge_code: ChargeCode = ChargeCode.ORIGIN
    description: Optional[str] = None
    charges_in_usd: Optional[Union[float, str]] = None

    @field_validator("charges_in_usd")
    def validate_charges_in_usd(cls, v):
        if v == "":
            return 0
        return v


class TruckBillAmount(BaseModel):
    currency: Optional[str] = None
    amount: Optional[float] = None


class TruckBillData(BaseModel):
    email_id: Optional[str] = None
    truck_bill_id: Optional[int] = None
    agl_shipment_number: Optional[str] = None
    creditor: Optional[str] = None
    invoice_num: Optional[str] = None
    invoice_date: Optional[date] = date.today()
    supplier_cost_ref: Optional[str] = None
    ar_ap: Optional[str] = "AP"
    is_post: Optional[str] = None
    charges: Optional[List[TruckBillCharges]] = None
    subject: Optional[str] = None
    


class TruckBill(BaseModel):
    truck_bill_number: Optional[str] = None
    email_id: Optional[str] = None
    attachment_id: Optional[str] = None
    agl_shipment_number: Optional[str] = None
    invoice_date: Optional[date] = None
    due_date: Optional[date] = None
    shipper: Optional[str] = None
    consignee: Optional[str] = None
    weight: Optional[str] = None
    chargeable_packages: Optional[str] = None
    master_bill_of_lading: Optional[str] = None
    house_bill_of_lading: Optional[str] = None
    container_number: Optional[List[str]] = None
    container_size: Optional[List[str]] = None
    charges: Optional[List[TruckBillCharges]] = None
    balance_due: Optional[str] = None
    payment_method: Optional[str] = None
    payment_due_date: Optional[date] = None
    creditor: Optional[OrgCode] = None

    def group_charges_by_code(self):
        if not self.charges:
            return

        combined_charges: Dict[ChargeCode, TruckBillCharges] = {}

        for charge in self.charges:
            if charge.charge_code in combined_charges:
                existing_charge = combined_charges[charge.charge_code]
                existing_charge.charges_in_usd += charge.charges_in_usd or 0
                if charge.description:
                    if existing_charge.description:
                        existing_charge.description += f", {charge.description}"
                    else:
                        existing_charge.description = charge.description
            else:
                combined_charges[charge.charge_code] = TruckBillCharges(
                    charge_code=charge.charge_code,
                    description=charge.description,
                    charges_in_usd=charge.charges_in_usd,
                )
        self.charges = list(combined_charges.values())

    def set_grouped_charges(
        self, grouped_charges: Dict[ChargeCode, List[TruckBillCharges]]
    ):
        self.charges = [
            charge for charges in grouped_charges.values() for charge in charges
        ]


class TruckBillCWUpload(BaseModel):
    email_id: Optional[str] = None
    agl_shipment_number: Optional[str] = None
    creditor: Optional[str] = None
    invoice_num: Optional[str] = None
    invoice_date: Optional[date] = None
    supplier_cost_ref: Optional[str] = None
    ar_ap: Optional[str] = None
    is_post: Optional[str] = None
    updated_at: Optional[datetime] = None
    FRT: Optional[float] = None
    AGEN: Optional[float] = None
    AMS: Optional[float] = None
    EQUIP: Optional[float] = None
    ORIGIN: Optional[float] = None
    LOCAL: Optional[float] = None
    PP: Optional[float] = None
    TERFEE: Optional[float] = None
    TELEX: Optional[float] = None
    VGM: Optional[float] = None
    DCART: Optional[float] = None
    SEAL: Optional[float] = None
    DOC: Optional[float] = None
    BOOK: Optional[float] = None
    CCLR: Optional[float] = None
    ALINE: Optional[float] = None
    PSEC: Optional[float] = None
    EGF: Optional[float] = None
    TRANS: Optional[float] = None
    CHRENT: Optional[float] = None
