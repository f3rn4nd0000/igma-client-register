from pymongo import MongoClient
from utils import create_connection, create_connection_and_return_person_collection
from django.http import HttpResponse, JsonResponse
from core.models import PersonModel
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.exceptions import ValidationError
from core.cpf_validator import CPF
from datetime import datetime
from bson.json_util import loads, dumps, default
import json

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
        person_collection = create_connection_and_return_person_collection()
        
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
        request_body = json.loads(request.body)
        print(request_body)

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
        if(valid_cpf == cpf):
            correct_cpf_format = valid_cpf[:3]+'.'+valid_cpf[3:6]+'.'+valid_cpf[6:9]+'-'+valid_cpf[9:11]

            # Converte data para o formato pt-BR dd/mm/yyyy
            try:
                datetime.strptime(birthdate, "%Y-%m-%d")
                date_object = datetime.strptime(birthdate, "%Y-%m-%d")
                correct_date_string = date_object.strftime("%d-%m-%Y")
            except ValueError:
                correct_date_string = birthdate
                pass

            new_object_person = {
                "name": name,
                "cpf": correct_cpf_format,
                "birthdate": correct_date_string
            }

            print("new_object_person")
            print(new_object_person)

            person_collection = create_connection_and_return_person_collection()
            if person_collection.count_documents({ 'cpf': correct_cpf_format }):
                print("**Error: You're already in the database**")
                return JsonResponse({"error": "Já existe esse cadastro no banco, tente novamente com outro CPF!"})
            print(person_collection)
            return_value = person_collection.insert_one(new_object_person)
            print("return_value")
            print(loads(return_value))
            print("Cadastro de pessoa concluído com sucesso!")

            return redirect('index')
        else:
            return JsonResponse({"error": "422, o CPF é inválido, tente novamente"} )

def return_person_by_cpf(request, person_cpf):
    """
        Importante lembrar que todo cpf passado para a URL deve 
        ter somente numeros, uma vez que pontos fariam a aplicação 
        possivelmente quebrar, já que são parametros de uma URL '.com', '.io' ...
    """
    if request.method == 'GET':
        print(">>>>"+str(person_cpf))
        person_collection = create_connection_and_return_person_collection()
        # parsed_cpf_value = CPF.parse_cpf(cpf_value)
        cursor_retrieve_desired_person = person_collection.find_one({"cpf": person_cpf})
        print(cursor_retrieve_desired_person)
        if cursor_retrieve_desired_person:
            util_service = UtilService()
            parsed_cursor = util_service.parse_cursor(cursor_retrieve_desired_person)
            return JsonResponse({"people": parsed_cursor}, safe = False)
        else:
            return JsonResponse({"error": "404 Not Found"})

