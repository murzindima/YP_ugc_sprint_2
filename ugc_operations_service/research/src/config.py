import os

from dotenv import load_dotenv

from managers.data_manager import DataManager
from services.mongo_service import MongoService
from services.postgres_service import PostgresService

load_dotenv()

pg_service = PostgresService(dsn=os.getenv("POSTGRES_DSN"))
mongo_service = MongoService(
    uri=os.getenv("MONGO_URI"), database_name=os.getenv("MONGO_DATABASE")
)
data_manager = DataManager()
