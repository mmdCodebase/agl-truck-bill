from sqlalchemy import Column, Integer, String, DateTime, Enum, Boolean, Date, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import json
from datetime import datetime
from app.db.database import TruckBillDB
from app.model.truck_bill_email_status import TruckBillEmailStatusEnum
from app.core.config import settings

db = TruckBillDB()
engine = db.get_engine()

Base = declarative_base()

# Define the ORM class/table
class TruckBillCharges(Base):
    __tablename__ = 'truck_bill_charges'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String, nullable=True)
    charge_code = Column(String, nullable=True)
    charges_in_usd = Column(Float, nullable=True)
    truck_bill_id = Column(Integer, ForeignKey('truck_bill.id'), nullable=False)

class TruckBill(Base):
    __tablename__ = 'truck_bill'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    email_id = Column(String, nullable=True)
    attachment_id = Column(String, nullable=True)
    truck_bill_number = Column(String, nullable=True)
    agl_shipment_number = Column(String, nullable=True)
    invoice_date = Column(Date, nullable=True)
    due_date = Column(Date, nullable=True)
    shipper = Column(String, nullable=True)
    consignee = Column(String, nullable=True)
    weight = Column(String, nullable=True)
    chargeable_packages = Column(String, nullable=True)
    master_bill_of_lading = Column(String, nullable=True)
    house_bill_of_lading = Column(String, nullable=True)
    container_number = Column(String, nullable=True)
    container_size = Column(String, nullable=True)
    payment_method = Column(String, nullable=True)
    payment_due_date = Column(Date, nullable=True)
    creditor = Column(String, nullable=True)
    invoice_num = Column(String, nullable=True)
    ar_ap = Column(String, nullable=True)
    is_post = Column(String, nullable=True)

    # Relationships
    # charges = relationship('TruckBillCharges', backref='truck_bill', cascade='all, delete-orphan')
    # invoiced_amount = relationship('TruckBillAmount', foreign_keys='TruckBillAmount.truck_bill_id', uselist=False, cascade='all, delete-orphan')
    # balance_due = relationship('TruckBillAmount', foreign_keys='TruckBillAmount.truck_bill_id', uselist=False, cascade='all, delete-orphan')

class TruckBillEmail(Base):
    __tablename__ = 'truck_bill_email'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email_id = Column(String, nullable=False, unique=True)
    subject = Column(String, nullable=False)
    email_status_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            'id': self.email_id,
            'subject': self.subject,
            'file_name': self.file_name,
            'email_status_id': self.email_status_id,
            'created_at': self.created_at.isoformat(),  # Convert datetime to string
            'updated_at': self.created_at.isoformat()  # Convert datetime to string
        }

    def to_json(self):
        return json.dumps(self.to_dict(), default=str)  # Convert dictionary to JSON string
    
class TruckBillEmailAttachment(Base):
    __tablename__ = 'truck_bill_email_attachment'

    id = Column(Integer, primary_key=True, autoincrement=True)
    attachment_id = Column(String, nullable=False, unique=True)
    email_id = Column(String, nullable=False, unique=False)
    file_name = Column(String, nullable=False, unique=False)
    content_type = Column(String, nullable=False, unique=False)
    is_inline = Column(Boolean, nullable=False, unique=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            'id': self.email_id,
            'subject': self.subject,
            'file_name': self.file_name,
            'email_status_id': self.email_status_id,
            'created_at': self.created_at.isoformat(),  # Convert datetime to string
            'updated_at': self.created_at.isoformat()  # Convert datetime to string
        }

    def to_json(self):
        return json.dumps(self.to_dict(), default=str)  # Convert dictionary to JSON string
    

class TruckBillEmailStatus(Base):
    __tablename__ = 'truck_bill_email_status'

    id = Column(Integer, primary_key=True, autoincrement=True)
    status_name = Column(Enum(TruckBillEmailStatusEnum), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

# # Function to insert sample statuses
def insert_email_status():
    SessionLocal = TruckBillDB.get_session_local()
    session = SessionLocal()
    try:
        statuses = [
            TruckBillEmailStatus(id=1, status_name=TruckBillEmailStatusEnum.CREATED, is_active=True),
            TruckBillEmailStatus(id=2, status_name=TruckBillEmailStatusEnum.PENDING_DATA_EXTRACTION, is_active=True),
            TruckBillEmailStatus(id=3, status_name=TruckBillEmailStatusEnum.FAILED, is_active=True),
            TruckBillEmailStatus(id=4, status_name=TruckBillEmailStatusEnum.READY_FOR_REVIEW, is_active=True),
            TruckBillEmailStatus(id=5, status_name=TruckBillEmailStatusEnum.PENDING_CW_UPLOAD, is_active=True),
            TruckBillEmailStatus(id=6, status_name=TruckBillEmailStatusEnum.SKIPPED, is_active=True),
            TruckBillEmailStatus(id=7, status_name=TruckBillEmailStatusEnum.DOWNLOADED, is_active=True),
        ]
        session.add_all(statuses)
        session.commit()
    finally:
        session.close()


# # Create the table
def create_table():
    print("testcreatetable")
    engine = TruckBillDB.get_engine()
    Base.metadata.reflect(bind=engine)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    create_table()
    insert_email_status()
