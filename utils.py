from pymongo import MongoClient
import os 
from dotenv import load_dotenv

# Inicializa variáveis de ambiente
load_dotenv()
CONNECTION_STRING = os.getenv("ATLAS_URI")
def create_connection():
    return MongoClient(CONNECTION_STRING)