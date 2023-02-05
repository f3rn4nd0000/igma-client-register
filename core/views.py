from pymongo import MongoClient
from utils import CONNECTION_STRING
from utils import create_connection
from django.http import HttpResponse
from core.models import PersonModel
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.exceptions import ValidationError

# Create your views here.

def index(request):
    if request.method == 'GET':
        client = create_connection()

        db = client['person_db']
        person_collection = db['client_details']
        # count = collection_name.count_documents(filter={})
        # print(count)
        med_details = person_collection.find({})
        return render(request, 'core/showpeople.html', {"pessoas": med_details})
    
    # if request.method == 'POST':

    #     db = client['person_db']
    #     person_collection = db['client_details']

    #     person_name = request.POST[""]

    #     person = PersonModel()

        # person = {
        #     "name": "fernando",
        #     "cpf": "123456789-00",
        #     "birthdate": "04/10/1994"
        # }
        # person_collection.insert_one(person_1)

@csrf_exempt
def createperson(request):
    if request.method == 'GET':
        return render(request,'core/createperson.html')

    if request.method == 'POST':
        
        new_person = PersonModel()
        new_person.name = request.POST.get("person_name")
        new_person.cpf = request.POST.get("person_cpf")
        new_person.birthdate = request.POST.get("person_birthdate")

        print(new_person.name)
        print(new_person.cpf)
        print(new_person.birthdate)

        return HttpResponse({'message': 'Cliente cadastrado com sucesso'})

