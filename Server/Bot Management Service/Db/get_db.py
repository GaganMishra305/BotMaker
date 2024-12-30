from astrapy import DataAPIClient
import os
from dotenv import load_dotenv

load_dotenv('.env')

# Create a global database instance
db_instance = None

def connect_db():
    global db_instance
    if db_instance is None:
        try:
            client = DataAPIClient(os.getenv("ASTRA_DB_TOKEN"))
            db_instance = client.get_database_by_api_endpoint(
                "https://97880d6f-5499-419c-aba5-ededb51d4d23-us-east-2.apps.astra.datastax.com"
            )
            print(f"Connected to Astra DB: {db_instance.list_collection_names()}")
        except Exception as e:
            raise RuntimeError(f"Cannot connect to database: {str(e)}")
    return db_instance

# Dependency to provide the database instance
def get_db():
    if db_instance is None:
        raise RuntimeError("Database not initialized.")
    return db_instance
