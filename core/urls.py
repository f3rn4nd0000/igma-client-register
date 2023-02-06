from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('createperson', views.createperson, name='createperson'),
    path('person/<str:person_cpf>/', views.return_person_by_cpf, name='return_person_by_cpf')
]