from pymongo import MongoClient
import os 
from dotenv import load_dotenv

# Inicializa variáveis de ambiente
load_dotenv()
CONNECTION_STRING = os.getenv("ATLAS_URI")
def create_connection():
    return MongoClient(CONNECTION_STRING)

def create_connection_and_return_person_collection():
    client = create_connection()
    db = client['person_db']
    person_collection = db['client_details']

    return person_collection