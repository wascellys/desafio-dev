# Desafio Bycoders

- [Instalação](#instalação)
- [Como executar](#como-executar)
- [Requisições HTTP](#requisições-http)
- [Códigos de respostas HTTP](#códigos-de-respostas-http)
- [Endpoints](#endpoints)
  - [Endpoints abetos](#endpoints-abetos)
    - [Autenticação](#authentications)
  - [Endpoints fechados](#endpoints-fechados)
    - [Tipos de transações](#categorias-de-quarto)
    - [Transações](#transactions)
    - [Lojas](#stores)

## Instalação

### Repositório
```
git clone https://github.com/wascellys/desafio-dev.git
```
### Se for usar Docker
```
docker-compose up --build -d

ALTER USER postgres CREATEDB;

exit
```
### Se for usar env
#### Terminal Linux
```
sudo apt install python3-pip python3-dev libpq-dev virtualenv postgresql postgresql-contrib
```
#### Usando postgres
```
psql -h localhost -U postgres
```

#### Criar banco de dados
```
CREATE DATABASE financial_db;

GRANT ALL ON DATABASE financial_db TO postgres;
```

#### Criando virtualenv
```
virtualenv env_bycoders --python=python3
```

#### Ativação da  virtualenv
```
source env_bycoders/bin/activate
```
#### Instalação das dependencias
```
pip install -r requirements.txt
```

## Como executar

#### Criar migrações para o banco de dados
```
python manage.py makemigrations api
```

#### Aplicar migrações
```
python manage.py migrate
```
#### Criar um superuser para testes
```
python manage.py createsuperuser
```
#### Carregando dados de teste
```
python manage.py loaddata api/fixtures/type_transactions.json
```
#### Executar teste unitário
```
python manage.py test api.tests
```

#### Rodar aplicação
```
python manage.py runserver
```

Se estiver usando Docker

```
docker-compose up --build -d
```

## Requisições HTTP
Toda requisição para a API são feitas por uma requisição HTTP usando para um dos seguintes métodos:

* `POST` Criar um recurso
* `PUT` Atualizar um recurso
* `GET` Buscar um ou uma lista de recursos
* `DELETE` Excluir um recurso

## Códigos de respostas HTTP
Cada resposta será retornada com um dos seguintes códigos de status HTTP:

* `201` `CREATED` A criação foi bem sucedida
* `200` `OK` A requisição foi bem sucedida
* `400` `Bad Request` Houve um problema com a solicitação (segurança, malformado, validação de dados, etc.)
* `401` `Unauthorized` As credenciais fornecidas à API são inválidas
* `403` `Forbidden` As credenciais fornecidas não têm permissão para acessar o recurso solicitado
* `404` `Not found` Foi feita uma tentativa de acessar um recurso que não existe
* `500` `Server Error` Ocorreu um erro no servidor

## Endpoints

### Endpoints abetos
Os endpoints abertos não precisam de autenticação :

- *[Login]() : `POST` `/api/login`*
- *[Register]() : `POST` `/api/register`*

#### Login e Register
- Campos:
  | Campo     | Descição        | Tipo    | Obrigatório             |
  | :----     | :------         | :------ | :---------------------: |
  | username  | Nome de usuario | String  | :ballot_box_with_check: |
  | email     | Email do usuário | String  | :ballot_box_with_check: |
  | password  | Senha do usuário | String  | :ballot_box_with_check: |

- Rotas
  - *Cadastrar usuário: `POST` `/api/register/`*
  - *Obter token de autenticação: `POST` `/api/api-token-auth/`*
  - *Autenticar usando Google-oauht2: `GET` `/oauth/login/google-oauth2/`*
  

### Endpoints fechados
Os endpoints fechados precisam de autenticação via token:
passar no cabeçalho da requisição: "Authorization": Token <token>

#### Tipo de Transações (TransactionType)


- Campos:
  | Campo       | Descição                       | Tipo     | Obrigatório             |
  | :----       | :------                        | :------  | :---------------------: |
  | t_type      | indice de representação        | Integer  | :ballot_box_with_check: |
  | description | Descrição da transação         | String   | :ballot_box_with_check: |
  | nature      | Natureza da transação          | String   | :ballot_box_with_check: |
  | sign        | Sinal de representação do tipo | String   | :ballot_box_with_check: |

- Rotas
  - *Listar tipos transações: `GET` `/api/type-transactions/`*
  - *Cadastrar um tipo transação: `POST` `/api/type-transactions/`*
  - *Atualizar um tipo transação: `PUT` `/api/type-transactions/{id}`*
  - *Deletar um tipo transação: `DELETE` `/api/type-transactions/{id}/`*


#### Lojas (Stores)


- Campos:
  | Campo       | Descição                       | Tipo     | Obrigatório             |
  | :----       | :------                        | :------  | :---------------------: |
  | name      | Nome da Loja        | String  | :ballot_box_with_check: |
  | owner | Proprietário da Loja         | String   | :ballot_box_with_check: |

- Rotas
  - *Listar lojas: `GET` `/api/stores/`*
  - *Cadastrar uma loja: `POST` `/api/stores/`*
  - *Atualizar uma loja: `PUT` `/api/stores/{id}`*
  - *Deletar uma loja: `DELETE` `/api/stores/{id}/`*

#### Transações (Transactions)


- Campos:
  | Campo       | Descição                       | Tipo     | Obrigatório             |
  | :----       | :------                        | :------  | :---------------------: |
  | store      | Loja responsavel pela transação        | String  | :ballot_box_with_check: |
  | t_type | Tipo de Transação         | String   | :ballot_box_with_check: |
  | date | Data da transação         | Date   | :ballot_box_with_check: |
  | amount | Valor da transação         | String   | :ballot_box_with_check: |
  | cpf | CPF do beneficiado        | String   | :ballot_box_with_check: |
  | card | Cartão de crédito         | String   | :ballot_box_with_check: |
  | time | Tempo da transação         | Time   | :ballot_box_with_check: |


- Rotas
  - *Listar transações: `GET` `/api/transactions`*
  - *Filtrar transações de uma Loja: `GET` `/api/transactions/?store_id=<id>`*
  - *Cadastrar uma transação: `POST` `/api/transactions/`*
  - *Cadastrar usando arquivo CNAB.txt: `POST` `/api/upload/file`*
    - *Passando os dados :*
    ```
    'file' : arquivo.txt
    ```
  - *Atualizar uma transação: `PUT` `/api/transactions/{id}/`*
  - *Deletar uma transação: `DELETE` `/api/transactions/{id}/`*