from pymongo import MongoClient
from utils import create_connection
from django.http import HttpResponse, JsonResponse
from core.models import PersonModel
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.exceptions import ValidationError
from core.cpf_validator import CPF
from datetime import datetime
from bson.json_util import loads, dumps, default
import json

# Create your views here.

class UtilService:
    def __init__(self):
        pass

    @staticmethod
    def pinCodeParser(path):
        location = {}
        f = open(path)
        for line in f:
            words = line.split()
            location[words[1]] = (words[-3],words[-2])
        return location

    @staticmethod
    def listHelper(str):
        s = []
        str = str.split(',')
        for e in str:
            s.append(e.replace("[","").replace("]",""))
        return s

    @staticmethod
    def parseList(str):
        if ',' in str:
            return UtilService.listHelper(str)
        return str

    @staticmethod
    def trimStr(str):
        return str.replace('"','')

    @staticmethod
    def parse_cursor(cursor):
        """
            Converte o cursor retornado pela consulta ao banco mongo em um dicionario,
            que é então retornado.
        """
        cursor = eval(dumps(cursor))
        parsed_cursor = {}
        for key, value in cursor.items():
            if "_id" in key:
                parsed_cursor["id"] = str(value["$oid"])
                print("if parsed_cursor")
            else:
                parsed_cursor[ UtilService.trimStr(key) ] = UtilService.parseList( value )
                print("else parsed_cursor")
                print(parsed_cursor)
        
        return parsed_cursor

    @staticmethod
    def convertDocumentsToJson(documents):
        result = []
        for document in documents:
            result.append(UtilService.parse_cursor(document))
        return result

def index(request):
    if request.method == 'GET':
        client = create_connection()
        db = client['person_db']
        person_collection = db['client_details']
        
        cursor_retrieve_all_people = person_collection.find({})
        util_service = UtilService()
        parsed_cursor = util_service.convertDocumentsToJson(cursor_retrieve_all_people)
        
        return JsonResponse({"people": parsed_cursor}, safe = False)
    

@csrf_exempt
def createperson(request):
    if request.method == 'GET':
        return JsonResponse({"message":"No body specified"})

    if request.method == 'POST':
        print("request.get_json()")
        print(json.loads(request.body))
        request_body = json.loads(request.body)

        name = str(request_body.get("person_name"))
        cpf = str(request_body.get("person_cpf"))
        birthdate = str(request_body.get("person_birthdate"))

        print(name)
        print(cpf)
        print(birthdate)

        cpf_validator = CPF(number = cpf)
        valid_cpf = cpf_validator.get_valid_cpf()

        print('O CPF válido para o número digitado é')
        print(valid_cpf)
        correct_cpf_format = valid_cpf[:3]+'.'+valid_cpf[3:6]+'.'+valid_cpf[6:9]+'-'+valid_cpf[9:11]

        # Converte data para o formato pt-BR dd/mm/yyyy
        date_object = datetime.strptime(birthdate, "%Y-%m-%d")
        correct_date_string = date_object.strftime("%d-%m-%Y")

        new_object_person = {
            "name": name,
            "cpf": correct_cpf_format,
            "birthdate": correct_date_string
        }
        
        client = create_connection()
        db = client['person_db']
        person_collection = db['client_details']
        person_collection.insert_one(new_object_person)
        print("Cadastro de pessoa concluído com sucesso!")

        return redirect('index')
