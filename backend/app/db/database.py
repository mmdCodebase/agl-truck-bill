import os
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.util import get_aws_secret
from app.core.config import settings

class TruckBillDB:
    _session_local = None

    @classmethod
    def _retrieve_connection_string(cls):
        secret_name = "agl-dwh-db-admin"
        secret_value = get_aws_secret(secret_name=secret_name)
        secret_data = json.loads(secret_value)

        # Adjusted connection string for PostgreSQL
        connection_string = f"postgresql+psycopg2://{secret_data['username']}:{secret_data['password']}@{secret_data['host']}:{secret_data['port']}/{settings.DB_NAME}"
        return connection_string
    
    @classmethod
    def get_engine(cls):
        connection_string = cls._retrieve_connection_string()
        engine = create_engine(connection_string)
        return engine

    @classmethod
    def get_session_local(cls):
        if cls._session_local is None:
            connection_string = cls._retrieve_connection_string()
            engine = create_engine(connection_string)
            cls._session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        return cls._session_local
