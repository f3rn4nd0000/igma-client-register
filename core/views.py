from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from utils import create_connection_and_return_person_collection, punctuated_cpf
from core.cpf_validator import CPF
from core.util_service import UtilService
from datetime import datetime
import json


def index(request):
    if request.method == 'GET':
        person_collection = create_connection_and_return_person_collection()
        
        cursor_retrieve_all_people = person_collection.find({})
        util_service = UtilService()
        parsed_cursor = util_service.convertDocumentsToJson(cursor_retrieve_all_people)
        
        return JsonResponse({"people": parsed_cursor}, safe = False)
    

@csrf_exempt
def createperson(request):
    """
        Rota responsável pela criação de novos usuários
    """
    if request.method == 'GET':
        return JsonResponse({"message":"Sem corpo especificado"})

    if request.method == 'POST':
        
        request_body = json.loads(request.body)
        name = str(request_body.get("person_name"))
        cpf = str(request_body.get("person_cpf"))
        birthdate = str(request_body.get("person_birthdate"))

        """
            Invoca classe validadora e retorna o cpf válido com a devida pontuação para comparação com
            o valor fornecido pelo usuário
        """
        cpf_validator = CPF(number = cpf)
        valid_cpf = cpf_validator.get_valid_cpf()
        correct_cpf_format = punctuated_cpf(valid_cpf)

        if(correct_cpf_format == cpf):

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

            person_collection = create_connection_and_return_person_collection()
            if person_collection.count_documents({ 'cpf': correct_cpf_format }):
                return JsonResponse({"error": "Já existe esse cadastro no banco, tente novamente com outro CPF!"})
            
            person_collection.insert_one(new_object_person)
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
        print(punctuated_cpf(person_cpf))
        cursor_retrieve_desired_person = person_collection.find_one({"cpf": punctuated_cpf(person_cpf)})
        print(cursor_retrieve_desired_person)
        if cursor_retrieve_desired_person:
            util_service = UtilService()
            parsed_cursor = util_service.parse_cursor(cursor_retrieve_desired_person)
            return JsonResponse({"people": parsed_cursor}, safe = False)
        else:
            return JsonResponse({"error": "404 Não encontrado"})

