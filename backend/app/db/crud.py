from app.db.database import TruckBillDB
from app.db.model import TruckBillEmail, TruckBill, TruckBillCharges, TruckBillEmailAttachment
from app.model.truck_bill import TruckBill as TruckBillPyDantic
from sqlalchemy import select, func, case
from datetime import datetime, timezone
import logging

logger = logging.getLogger(__name__)

class TruckBillEmailCRUD:
    @staticmethod
    def create_entry(email_id, subject, email_status_id):
        SessionLocal = TruckBillDB.get_session_local()
        session = SessionLocal()
        try:
            new_entry = TruckBillEmail(
                email_id=email_id,
                subject=subject,
                email_status_id=email_status_id,
            )
            session.add(new_entry)
            session.commit()
            return new_entry
        finally:
            session.close()
    
    @staticmethod
    def create_attachment_entry(attachment_id, email_id, file_name, content_type, is_inline):
        SessionLocal = TruckBillDB.get_session_local()
        session = SessionLocal()
        try:
            new_entry = TruckBillEmailAttachment(
                attachment_id=attachment_id,
                email_id=email_id,
                file_name=file_name,
                content_type=content_type,
                is_inline=is_inline
            )
            session.add(new_entry)
            session.commit()
            return new_entry
        finally:
            session.close()


    @staticmethod
    def get_all_email_status(email_status_id):
        SessionLocal = TruckBillDB.get_session_local()
        session = SessionLocal()
        try:
            entry = (
                session.query(TruckBillEmail)
                .filter(TruckBillEmail.email_status_id == email_status_id)
                .all()
            )
            return entry
        finally:
            session.close()
    
    @staticmethod
    def get_all_attachment_by_status(email_status_id):
        SessionLocal = TruckBillDB.get_session_local()
        session = SessionLocal()
        try:
            entry = (
                session.query(TruckBillEmailAttachment)
                .join(TruckBillEmail, TruckBillEmailAttachment.email_id == TruckBillEmail.email_id)
                .filter(TruckBillEmail.email_status_id == email_status_id)
                .all()
            )
            return entry
        finally:
            session.close()

    @staticmethod
    def read_entry(entry_id):
        SessionLocal = TruckBillDB.get_session_local()
        session = SessionLocal()
        try:
            entry = (
                session.query(TruckBillEmail)
                .filter(TruckBillEmail.id == entry_id)
                .first()
            )
            return entry
        finally:
            session.close()

    @staticmethod
    def read_entry_by_status_id(status_id: int):
        SessionLocal = TruckBillDB.get_session_local()
        session = SessionLocal()
        try:
            entry = (
                session.query(TruckBillEmail)
                .filter(TruckBillEmail.email_status_id == status_id)
                .order_by(TruckBillEmail.created_at.desc())
                .all()
            )
            return entry
        finally:
            session.close()
    
    @staticmethod
    def read_entry_by_email_id(email_id: str):
        SessionLocal = TruckBillDB.get_session_local()
        session = SessionLocal()
        try:
            entry = (
                session.query(TruckBillEmail)
                .filter(TruckBillEmail.email_id == email_id)
                .order_by(TruckBillEmail.created_at.desc())
                .all()
            )
            return entry
        finally:
            session.close()

    @staticmethod
    def update_entry(email_id, subject=None, file_name=None, email_status_id=None):
        SessionLocal = TruckBillDB.get_session_local()
        session = SessionLocal()
        try:
            entry = (
                session.query(TruckBillEmail)
                .filter(TruckBillEmail.email_id == email_id)
                .first()
            )
            if entry:
                if subject:
                    entry.subject = subject
                if file_name:
                    entry.file_name = file_name
                if email_status_id:
                    entry.email_status_id = email_status_id
                entry.updated_at = datetime.now(timezone.utc)
                session.commit()
            return entry
        finally:
            session.close()

    @staticmethod
    def delete_entry(entry_id):
        SessionLocal = TruckBillDB.get_session_local()
        session = SessionLocal()
        try:
            entry = session.query(MyTable).filter(MyTable.id == entry_id).first()
            if entry:
                session.delete(entry)
                session.commit()
            return entry
        finally:
            session.close()
    
    @staticmethod
    def read_attachment_by_email_id(email_id: str):
        SessionLocal = TruckBillDB.get_session_local()
        session = SessionLocal()
        try:
            entry = (
                session.query(TruckBillEmailAttachment)
                .filter(TruckBillEmailAttachment.email_id == email_id)
                .all()
            )
            return entry
        finally:
            session.close()


class TruckBillCRUD:
    @staticmethod
    def insert_truck_bill(truck_bill: TruckBillPyDantic):
        SessionLocal = TruckBillDB.get_session_local()
        session = SessionLocal()
        try:
            truck_bill_dict = truck_bill.dict()
            del truck_bill_dict["charges"]
            del truck_bill_dict["balance_due"]
            new_truck_bill = TruckBill(**truck_bill_dict)
            session.add(new_truck_bill)
            session.commit()
            return new_truck_bill.id
        finally:
            session.close()

    @staticmethod
    def insert_truck_bill_charges(truck_bill_id, truck_bill: TruckBillPyDantic):
        SessionLocal = TruckBillDB.get_session_local()
        session = SessionLocal()
        try:
            new_truck_bill_charges = truck_bill.charges
            for new_truck_bill_charge in new_truck_bill_charges:
                new_truck_bill_charge = TruckBillCharges(
                    truck_bill_id=truck_bill_id, **new_truck_bill_charge.dict()
                )
                session.add(new_truck_bill_charge)
            session.commit()
            return len(new_truck_bill_charges)
        finally:
            session.close()
            
    @staticmethod
    def insert_truck_bill_charge(truck_bill_id, truck_bill_charge: TruckBillCharges):
        SessionLocal = TruckBillDB.get_session_local()
        session = SessionLocal()
        try:
            new_truck_bill_charge = TruckBillCharges(
                truck_bill_id=truck_bill_id, **truck_bill_charge.dict()
            )
            logger.info(new_truck_bill_charge)
            session.add(new_truck_bill_charge)
            session.commit()
            return True
        finally:
            session.close()

    @staticmethod
    def get_truck_bill_by_email_attachment_id(email_id: str, attachment_id: str):
        SessionLocal = TruckBillDB.get_session_local()
        session = SessionLocal()
        query = (
            session.query(
                TruckBill.agl_shipment_number,
                TruckBill.truck_bill_number.label("supplier_cost_ref"),
                TruckBill.invoice_date,
                TruckBill.creditor,
                TruckBill.id.label("truck_bill_id"),
                TruckBillEmail.subject,
                TruckBillEmail.email_id
            )
            .join(
                TruckBillEmail,
                TruckBill.email_id == TruckBillEmail.email_id,
                isouter=True,
            )
            .filter(TruckBillEmail.email_id == email_id, TruckBill.attachment_id == attachment_id)
        )
        return query.first()

    @staticmethod
    def get_charges_by_truck_bill_id(truck_bill_id: int):
        SessionLocal = TruckBillDB.get_session_local()
        session = SessionLocal()
        query = session.query(
            TruckBillCharges.id,
            TruckBillCharges.charge_code,
            TruckBillCharges.description,
            TruckBillCharges.charges_in_usd,
        ).filter(TruckBillCharges.truck_bill_id == truck_bill_id)
        return query.all()

    @staticmethod
    def update_truck_bill_by_id(truck_bill_id: int, update_data: dict):
        SessionLocal = TruckBillDB.get_session_local()
        session = SessionLocal()
        try:
            query = session.query(TruckBill).filter(TruckBill.id == truck_bill_id)
            query.update(update_data)
            session.commit()
        except Exception as e:
            session.rollback()
            raise
        finally:
            session.close()

    @staticmethod
    def update_charges_by_charge_id(charge_id: int, update_data: dict):
        SessionLocal = TruckBillDB.get_session_local()
        session = SessionLocal()
        try:
            query = session.query(TruckBillCharges).filter(
                TruckBillCharges.id == charge_id
            )
            query.update(update_data)
            session.commit()
        except Exception as e:
            session.rollback()
            raise
        finally:
            session.close()

    @staticmethod
    def get_charges_by_email_status_id_cw(email_status_id: int):
        SessionLocal = TruckBillDB.get_session_local()
        session = SessionLocal()
        try:
            query = (
                select(
                    TruckBill.email_id,
                    TruckBill.agl_shipment_number,
                    TruckBill.creditor,
                    TruckBill.invoice_num,
                    None,  # TruckBill.invoice_date,
                    TruckBill.truck_bill_number.label("supplier_cost_ref"),
                    TruckBill.ar_ap,
                    TruckBill.is_post,
                    TruckBillEmail.updated_at,
                    func.sum(
                        case(
                            (
                                TruckBillCharges.charge_code == "FRT",
                                TruckBillCharges.charges_in_usd,
                            ),
                            else_=0,
                        )
                    ).label("FRT"),
                    func.sum(
                        case(
                            (
                                TruckBillCharges.charge_code == "AGEN",
                                TruckBillCharges.charges_in_usd,
                            ),
                            else_=0,
                        )
                    ).label("AGEN"),
                    func.sum(
                        case(
                            (
                                TruckBillCharges.charge_code == "AMS",
                                TruckBillCharges.charges_in_usd,
                            ),
                            else_=0,
                        )
                    ).label("AMS"),
                    func.sum(
                        case(
                            (
                                TruckBillCharges.charge_code == "EQUIP",
                                TruckBillCharges.charges_in_usd,
                            ),
                            else_=0,
                        )
                    ).label("EQUIP"),
                    func.sum(
                        case(
                            (
                                TruckBillCharges.charge_code == "ORIGIN",
                                TruckBillCharges.charges_in_usd,
                            ),
                            else_=0,
                        )
                    ).label("ORIGIN"),
                    func.sum(
                        case(
                            (
                                TruckBillCharges.charge_code == "LOCAL",
                                TruckBillCharges.charges_in_usd,
                            ),
                            else_=0,
                        )
                    ).label("LOCAL"),
                    func.sum(
                        case(
                            (
                                TruckBillCharges.charge_code == "PP",
                                TruckBillCharges.charges_in_usd,
                            ),
                            else_=0,
                        )
                    ).label("PP"),
                    func.sum(
                        case(
                            (
                                TruckBillCharges.charge_code == "TERFEE",
                                TruckBillCharges.charges_in_usd,
                            ),
                            else_=0,
                        )
                    ).label("TERFEE"),
                    func.sum(
                        case(
                            (
                                TruckBillCharges.charge_code == "TELEX",
                                TruckBillCharges.charges_in_usd,
                            ),
                            else_=0,
                        )
                    ).label("TELEX"),
                    func.sum(
                        case(
                            (
                                TruckBillCharges.charge_code == "VGM",
                                TruckBillCharges.charges_in_usd,
                            ),
                            else_=0,
                        )
                    ).label("VGM"),
                    func.sum(
                        case(
                            (
                                TruckBillCharges.charge_code == "DCART",
                                TruckBillCharges.charges_in_usd,
                            ),
                            else_=0,
                        )
                    ).label("DCART"),
                    func.sum(
                        case(
                            (
                                TruckBillCharges.charge_code == "SEAL",
                                TruckBillCharges.charges_in_usd,
                            ),
                            else_=0,
                        )
                    ).label("SEAL"),
                    func.sum(
                        case(
                            (
                                TruckBillCharges.charge_code == "DOC",
                                TruckBillCharges.charges_in_usd,
                            ),
                            else_=0,
                        )
                    ).label("DOC"),
                    func.sum(
                        case(
                            (
                                TruckBillCharges.charge_code == "BOOK",
                                TruckBillCharges.charges_in_usd,
                            ),
                            else_=0,
                        )
                    ).label("BOOK"),
                    func.sum(
                        case(
                            (
                                TruckBillCharges.charge_code == "CCLR",
                                TruckBillCharges.charges_in_usd,
                            ),
                            else_=0,
                        )
                    ).label("CCLR"),
                    func.sum(
                        case(
                            (
                                TruckBillCharges.charge_code == "ALINE",
                                TruckBillCharges.charges_in_usd,
                            ),
                            else_=0,
                        )
                    ).label("ALINE"),
                    func.sum(
                        case(
                            (
                                TruckBillCharges.charge_code == "PSEC",
                                TruckBillCharges.charges_in_usd,
                            ),
                            else_=0,
                        )
                    ).label("PSEC"),
                    func.sum(
                        case(
                            (
                                TruckBillCharges.charge_code == "EGF",
                                TruckBillCharges.charges_in_usd,
                            ),
                            else_=0,
                        )
                    ).label("EGF"),
                    func.sum(
                        case(
                            (
                                TruckBillCharges.charge_code == "TRANS",
                                TruckBillCharges.charges_in_usd,
                            ),
                            else_=0,
                        )
                    ).label("TRANS"),
                    func.sum(
                        case(
                            (
                                TruckBillCharges.charge_code == "CHRENT",
                                TruckBillCharges.charges_in_usd,
                            ),
                            else_=0,
                        )
                    ).label("CHRENT"),
                )
                .select_from(TruckBillEmail)
                .join(TruckBill, TruckBillEmail.email_id == TruckBill.email_id)
                .outerjoin(
                    TruckBillCharges, TruckBill.id == TruckBillCharges.truck_bill_id
                )
                .where(TruckBillEmail.email_status_id == email_status_id)
                .group_by(
                    TruckBill.email_id,
                    TruckBill.agl_shipment_number,
                    TruckBill.creditor,
                    TruckBill.invoice_num,
                    TruckBill.invoice_date,
                    TruckBill.truck_bill_number,
                    TruckBill.ar_ap,
                    TruckBill.is_post,
                    TruckBillEmail.updated_at,
                )
            )
            result = session.execute(query)
            return result.all()
        except Exception as e:
            # Handle any exceptions that may occur during the query execution
            print(f"An error occurred: {str(e)}")
            return None
        finally:
            session.close()


email_crud = TruckBillEmailCRUD()
truck_bill_crud = TruckBillCRUD()
