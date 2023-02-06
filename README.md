
## IGMA-CLIENT-REGISTER

  

### Descrição:

Minha solução para o teste técnico da IGMA: Construindo um cadastro de clientes com validação de CPF
  
* * *
### Como instalar:
Antes de mais nada caso deseja testar a aplicação em seu ambiente local é necessário que você tenha o interpretador python instalado, link para download:
https://www.python.org/downloads/

Após isso, faça um clone do projeto:
```
git clone https://github.com/f3rn4nd0000/igma-client-register
```
Entre no diretório em que foi clonado, crie e ative um ambiente virtual e instale as dependências:
```
cd igma-client-register
python -m venv venv

Linux/MacOS
source venv/bin/activate

Windows
venv/Scripts/activate
```
* Observação: Caso você tenha acabado de instalar o interpretador python em sua máquina pode ser que o virtualenv não esteja instalado, para corrigir esse erro digite esse comando em seu terminal:
`pip install virtualenv`

* * *
## Como testar a aplicação:
Para testar a aplicação é recomendado usar REST Clients como [Insomnia](https://insomnia.rest/download/)  ou [Postman](https://www.postman.com/)


### Endpoints:
Lembrando que a base-url pode variar conforme o tipo de teste que fizer, mas se for rodar testes localmente será http://localhost:8000
1. Consultar clientes:
* Endpoint (GET): <base-url>/api
* Resposta:
```

```
2. Cadastrar clientes:
* Endpoint (POST): <base-url>/api/createperson
* Exemplo de corpo da requisição:
```
{
	"person_name": "mariana silva",
	"person_cpf": "123.413.123-55",
	"person_birthdate": "12/04/1990"
}
```
O CPF acima é inválido, gerando uma resposta inválida:

```
{
	"error": "422, o CPF é inválido, tente novamente"
}
```
Porém ao enviar um CPF válido, usando um CPF gerado por um [gerador](https://www.4devs.com.br/gerador_de_cpf)
```
{
	"person_name": "mariana silva",
	"person_cpf": "517.179.680-74",
	"person_birthdate": "12/04/1990"
}
```
A resposta será uma lista com todos os clientes cadastrados, inclusive a mais recente:
```
{
	"people": [
		{
			"id": "63e11622308fd8452923b67c",
			"name": "asdrubal bastos",
			"cpf": "123.000.123-91",
			"birthdate": "11/10/1901"
		},
		{
			"id": "63e13695f65c18e0a595072a",
			"name": "mariana silva",
			"cpf": "517.179.680-74",
			"birthdate": "12/04/1990"
		}
	]
}
```
Caso o CPF já esteja cadastrado no banco a resposta será:
```
{
	"error": "Já existe esse cadastro no banco, tente novamente com outro CPF!"
}
```



4. Buscar clientes por CNPJ
* Endpoint (GET): <base-url>/api/person/<person_cpf>
Exemplo de requisição e resposta:
Requisição para URL: <base-url>/api/person/48149032002
```
{
	"people": {
		"id": "63e139e35d2eb2cd66acef73",
		"name": "mario Luigi",
		"cpf": "481.490.320-02",
		"birthdate": "12/04/1990"
	}
}
```

Onde person_cpf é uma string que pode ser com ou sem pontuação
  
### Stack usada:

Django (Backend)

PyMongo (ORM Para MongoDB) (Banco de dados)
  
* * *

### Como executar testes unitários?

Os testes unitários estão em:
`diretorio_base/core/tests.py`
E para executá-los basta digitar em seu terminal:
```
cd diretorio_base/core/tests.py
python tests.py
```  
* * * 
### Versão Online:
A aplicação foi desenvolvida em ambiente Linux e não foram feitos testes em amb. Windows, por isso hospedei uma versão online usando [fly.io](https://fly.io) com a seguinte URL:
[igma-client-register.fly.dev](https://igma-client-register.fly.dev)
que pode servir como <base-url> para os endpoints citados acima.

* * * 
### Dúvidas?
Entre em contato comigo !


