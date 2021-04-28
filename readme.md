# Cashtrol

Já imaginou viajar com amigos, e se livrar daquela dor de cabeça no final, quando chega a hora de dividir as despesas?

**O Cashtrol chegou pra acabar com esse problema!**

## Proposta

   A função principal do **Cashtrol** é facilitar a divisão de despesas para qualquer situação: compras, gasolina, aluguel, o que quiser.

   Quando todos os planos e gastos forem finalizados, o app automaticamente gerará o quanto cada um precisa receber, o quanto precisa pagar e para qual pessoa irá pagar. Acabou toda aquela confusão de fazer contas e lembrar de todos os gastos.

## Tecnologias

- **Linguagem utilizada**: Python
- **Framework para criação de API**: Flask
- **Banco de dados**: PostgreSQL
- V**alidação de login/token**: Flask_JWT_Extended, Flask-Login
- **ORM utilizado:** SQLAlchemy
- **Testes**: Pytest
- **Criptografia de senha**: Werkzeug

## Features MVP

- Cadastro

É necessário ter uma conta no aplicativo para poder utilizar todas as suas funcionalidades

- Login

Após efetuar o cadastro, você já pode logar na sua conta, utilizando o seu e-mail e senha. Após logar, vc receberá um token de acesso ( esse token é necessário para acessar outras features )

- Descrição do usuário

Com essa feature, após a validação do token, é possível saber todos os dados do usuário, como seu id, nome, email, todos os grupos os quais ele está participando, seus débitos, créditos, e também o saldo total.

- Histórico de transações

Aqui, após a validação do token, é possível ver todas as transações do usuário, com relação a sua conta ou seja, aqui será mostrado os dados de todos os grupos que o usuário está interagindo.

- Atualização de Cadastro

Caso seja de interesse do usuário modificar algum dado da sua conta, como nome e email, ele pode efeutar essas mudanças tranquilamente.

- Deletar usuário

Caso o usuário nao deseja mais ter essa conta no aplicativo, é possível fazer a deleção da mesma.

- Criar Grupo

Através dessa feature, informando a API o nome do grupo, ele vai automaticamente ser criado para o usuário que fez o request

- Listar Grupos

Após a validação do token e verificação de qual usuário está tentando acessar a rota, ele devolverá a listagem de todos os grupos os quais o usuário esta participando

- Procurar grupo específico

Fornecendo o ID do grupo pela rota,após a validação do token, vc consegue obter todas as informações sobre o mesmo, caso o usuário que está tentando acessar essas informações tem autorização para acessá-lo.

- Adicionar um membro a um grupo

Aqui, o usuário que está tentando ingressar em um grupo, ao fornecer o código de convite ( invite_code ) certo a rota, automaticamente será ingressado àquele grupo.

- Listar membros do grupo

Ao fornecer o ID do grupo pela rota, e passando pela validação do token, o usuário receberá como resposta o id, nome do grupo, e todos os membros que já fazem parte dele.

- Balanço geral de um grupo

Através dessa feature, após fornecer o ID do grupo na rota, e passar pela validação do token, o usuário receberá o nome do grupo como resposta, e o balanço do saldo de cada usuário que existe dentro dele.

- Histórico de transações de um grupo

Após a validação do token, e recebendo o ID do grupo pela rota, é possível receber todo o histórico de transações de todos que que participam do grupo.

- Balanço de todos os grupos

Após passar pela validação do token, o usuário receberá como resposta os dados e o saldo de **todos** os grupos existentes no aplicativo.

- Realizando um pagamento para outro membro do grupo

Com essa rota, após validação do token, e recebendo o ID do grupo, o usuário informa a rota a quantidade que está pagando, e para qual membro do grupo será o pagamento.

- Histórico de pagamentos do grupo

Nessa rota, conseguimos obter o histórico de pagamento de todos os membros do grupo.

- Registrando uma despesa

Aqui, um usuário pode registrar o quanto gastou em uma despesa, adicionando um título e também uma descrição.

- Obtendo informações de **uma** despesa

Através dessa rota, é possível obter todas as informações pertinentes a uma despesa específica, como nome, o quanto foi gasto, em quais categorias ela se encaixa, descrição etc.

- Histórico de despesas

Nessa rota, conseguimos obter o histórico de despesas de todos os membros do grupo.

## Criação de Usuário

# POST: {URL}api/users/signup

        Body:
        {
        	“name” : “Fulano Rodrigues”,
        	“email” : “fulano@email.com”,
        	“password” : “EuSouFulano123”
        }

        #------------------------------------

        Return:
        CREATED 201
        {
        	“id” : 23034,
        	“email” : “fulano@email.com”,
        }

## Login de Usuário

        #POST: {URL}api/users/login
        Body:
        {
        	“email” : “fulano@email.com”,
        	“password” : “EuSouFulano123”
        }

        #-------------------------------------

        Return:
        SUCCESS 200
        {
        	“access_token” : “erfweu39gvgrw3vniv5aael1rvakbe2r234uigeiate32r
        	atveityvbaer258v2”
        }

## Ler Dados de Usuário

        #GET: {URL}/users
        #Token : True
        Return 200
        {“id” : 23034
        “name” : “Fulano Rodrigues”,
        “email” : “fulano@email.com”,
        “groups” : [{ “group_name” : “República”, “group_id” : 20} ,
        { “group_name” :  “Eu e a Mina”, “group_id” : 23}],
        “payables” : 50,
        “receivables”: 20,
        “saldo” : 30
        }

## Histórico de Transações

        #GET {URL}/users/transactions
        #Token : True
        #Param: True

        Return Success 200

        { “data” : [{“id” : 3402,
        “entry: {“entry_name”:”Energia”, “entry_id”: 203},
        “type”: “DEBIT”,
        “created_at”:” 11/11/2011”,
        “amount”:” 20.00”,
        “description”: “conta de luz”
        “category”: {“category_id”  : 1,“category_name”  : “Moradia”},
        “group”: {“group_id: 79, “group_name” : “Fraternidade”}
        },
        {“id” : 3241,
        “entry” : {"entry_name":”Pizza para lucas”, “entry_id” : 324}
        “type”: “CREDIT”,
        “created_at”:” 10/11/2011”,
        “amount”:” 50.00”,
        “description”: “dinheiro pro lucas comprar pizza”
        “category”: {“category_id”  : 2, “category_name”  : “Lanches”}
        “group_id” : {“group_id: 79, “group_name” : “Fraternidade”}
        },
        …]

## Atualizar Dados de Usuário

        #PATCH: {URL}/users
        #TOKEN: True

        body {
        	“email” : “fulano2@email”
        }
        #-----------------------------------------
        Return 201

        {
        “Id”: 2,
        “Name” : “fulano”,
        “Email”: “fulano2@email.com”
        }

## Deletar Usuário

        #DELETE:  {URL}/users

        Return 204

## Criar um Grupo

        #POST {URL}/groups
        #Token: True

        Body {
        	“name”: “AP da galera”
        }
        # --------------------------------------------
        Return: Created 204
        {
        	“Id” : 2352,
        “name”:”AP da galera”,
        “Invite_code”: “Y35ER0”
        }

## Listar Grupos com relação ao Usuário

        #GET {URL}/groups
        #Token : True

        Return:
        Success 200
        [
        {“id”:1,
        “name”:”apartamento dos guri”,
        “members”: [1,3,6,7,15],
        “Categories” : [4,23,5,7],
        “Invite_code”: “Y35TP0”
        },
        {“id”:3,
        “Name”:”cerveja da firma”,
        “members”: [1,37,57,19,27],
        “Invite_code”: “Y35TP0”
        }
        ]

## Dados de um Grupo Específico

        #GET {URL}/groups/{group_id}
        #Token : True

        Return:
        Success 200

        “Data” : {“id”:1,
        “name”:”apartamento dos guri”,
        “members”: [1,3,6,7,15],
        “Categories” : [4,23,5,7],
        “Invite_code”: “Y35TP0”
        },

## Adicionando um membro ao grupo por convite

        #POST {URL}/groups/members
        #Token: True

        Body {
        	“invite_code”: “Y35ER0”
        }
        # ----------------------------------------------------------
        Return: CREATED 204
        {
        	“Id” : 2352,
        “name”:”AP da galera”,
        “Invite_code”: “Y35ER0”,
        “members”: [1,3,4],
        }

## Listar membros do grupo

        #GET {URL}/groups/{group_id}/members
        #Token : True

        Return:
        Success 200
        data: {“id”:1,
        “name”:”apartamento dos guri”,
        “Members”: [ {“member_id” : 3, “member_name” : “Fulano”},
        		{“member_id” : 4, “member_name” : “Ciclano”}]
        }

## Balanço de um grupo

        #GET {URL}/groups/{group_id}/balance
        #Token: True

        Return: CREATED 204
        “Data” :  {“group_name”:”AP da Galera”,
        “balance” : [ {“user_id” : 1, “user_saldo” : 30”},
        		   {“user_id” : 24, “user_saldo” : -20},
        ]

## Transações de um Grupo Específico

        #GET {URL}/groups/{group_id}/transactions
        #Token: True
        Return:
        Success 200
        “Data” : [
        	{“Id”: 30,
        “name” : “Pagamento”,
        “amount” : 100.00,
        “group” : “Galera do AP”,
        “created_at” : “05/04/2020”,
        “Splitted” : {
        		“payers” : [{“payer_id” : 1, “paid_amount” : 100}],
        “Benefited” : [{“benefited_id: 2, “benefited_amount” : 100}]
        }
        },
         { “id” : 31,
        “name” : “Pizza da Sexta”,
        “amount” : 80.00,
        		“group” : “Galera do AP”,
        “created_at” : “05/08/2020”,
        "splitted": {“payers” :  [{ “payer_id” : 1, “paid_amount”  : 100}],
        “benefited” : [{“benefited_id” : 1, “benefited_amount” : 40} ,
                                    {“benefited_id” : 2, “benefited_amount” : 30},
                                    {“benefited_id” : 3, “benefited_amount” : 30} ]
                             }
        ]

## Balanço de todos os grupos

        #GET {URL}/groups/balance
        #Token : True
        Return:
        Success 200
        [
        {“group_Id”:1,
        “users_saldo” : [ {“user_id” : 1, “user_saldo” : 30”},
        		   {“user_id” : 24, “user_saldo” : -20},
        ]
        },
        {“group_id”:3,
        “users_saldo” : [ {“user_id” : 1, “user_saldo” : 30”},
        		   	{“user_id” : 24, “user_saldo” : -20},
        }
        ]

## Criação de um pagamento para um usuário

        #POST {URL}/groups/{group_id}/payments
        #Token:true
        Body:{
        “amount” : 100.00,
        “paid_to” : 2
        }
        # --------------------------------
        Return
        Data:
        {
        	“Id”: 30,
        “name” : “Pagamento”,
        “amount” : 100.00,
        “group” : “Galera do AP”,
        “created_at” : “05/04/2020”,
        }

## Histórico de Pagamentos de um Grupo

        #GET {URL}/groups/{groups_id}/payments
        #Token: true

        SUCCESS 200
        Return {
        “Data”:[
        {“Id”: 30,
        “name” : “Pagamento”,
        “amount” : 100.00,
        “group” : “Galera do AP”,
        “created_at” : “05/04/2020”,
        “Splitted” : {
        		“payers” : [{“payer_id” : 1, “paid_amount” : 100}],
        “Benefited” : [{“benefited_id: 2, “benefited_amount” : 100}]
        }
        		},
        		{“Id”: 35,
        “name” : “Pagamento”,
        “amount” : 100.00,
        “group” : “Galera do AP”,
        “created_at” : “09/04/2020”,
        “Splitted” : {
        		“payers” : [{“payer_id” : 1, “paid_amount” : 100}],
        “Benefited” : [{“benefited_id: 2, “benefited_amount” : 100}]
        }
        		},

        ...]
        }

## Criação de uma Despesa

        #POST: {URL}/groups/{group_id}/expenses

        #TOKEN = TRUE
        Body:{
        “name” : “Conta Luz”,
        “amount” : 100.00,
        “category” : 1,
        “status”: “PAID”,
        “paid_at” : “06/04/2020”,
        “description” :”Veio mais alta por causa da secadora”,
        }

        # ----------------------------------------------------

        SUCCESS 200
        Return {
        “Data”: [
            { “id” : 41254322,
        “name” : “Conta Luz”,
        “amount” : 100.00,
        “category” : {“category_name” : “Moradia”, “category_id”: 2},
        “status”: “PAID”,
        “created_at” : “05/04/2020”,
        “paid_at” : “06/04/2020”,
        “description” : “Veio mais alta por causa da secadora”,
        “Splitted” : {
        “payers” :  [
        { “payer_id” : 34, “paid_amount”  : 100}
        ],
        “benefited” : [
        {“benefited_id” : 2, “benefited_amount” : 33.33} ,
        {“benefited_id” : 34, “benefited_amount” : 33.33},
        {“benefited_id” : 40, “benefited_amount” : 33.33}
        ]
        }
        }
        { “id” : 51254322,
        “name” : “Pizza da Sexta”,
        “value” : 80.00,
        “category” : {“Category_id” : 1, “category_name” : “Lanches”} ,
        “status”: “PAID”,
        “created_at” : “05/08/2020”,
        “paid_at” : “05/08/2020”,
        “description” : “Fulano pediu pepperoni e Ciclano Frango com Cheddar”,
        “Splitted” : {
        “payers” :  [{ “payer_id” : 34, “paid_amount”  : 80}],
        “benefited” : [{“benefited_id” : 2, “benefited_amount” : 20} ,
        {“benefited_id” : 34, “benefited_amount” : 30},
        {“benefited_id” : 40, “benefited_amount” : 30} ]
        }
        } ] }

## Histórico de uma Despesa Específica

        #GET {URL}groups/{group_id}/expenses/{expense_id}
        #Token: true

        SUCCESS 200
        Return {
        “Data”:{ “id” : 51254322,

        “name” : “Pizza da Sexta”,
        “amount” : 80.00,
        “category” : {“Category_id” : 1, “category_name” : “Lanches”} ,
        “status”: “PAID”,
        “created_at” : “05/08/2020”,
        “paid_at” : “05/08/2020”,
        “description” : “Fulano pediu pepperoni e Ciclano Frango com Cheddar”,
        “Splitted” : {
        “payers” :  [{ “payer_id” : 34, “paid_amount”  : 80}],
        “benefited” : [{“benefited_id” : 2, “benefited_amount” : 20} ,
        {“benefited_id” : 34, “benefited_amount” : 30},
        {“benefited_id” : 40, “benefited_amount” : 30}]
        }
        }
        }

## Histórico de Despesas de um Grupo Específico

        #GET {URL}/groups/{groups_id}/expenses
        #Token: true

        SUCCESS 200
        Return {
        “Data”:[
        { “id” : 51254322,
        “name” : “Pizza da Sexta”,
        “amount” : 80.00,
        “category” : {“Category_id” : 1, “category_name” : “Lanches”} ,
        “status”: “PAID”,
        “created_at” : “05/08/2020”,
        “paid_at” : “05/08/2020”,
        “description” : “Fulano pediu pepperoni e Ciclano Frango com Cheddar”,
        “Splitted” : {
        “payers” :  [{ “payer_id” : 34, “paid_amount”  : 80}],
        “benefited” : [{“benefited_id” : 2, “benefited_amount” : 20} ,
        {“benefited_id” : 34, “benefited_amount” : 30},
        {“benefited_id” : 40, “benefited_amount” : 30}]
        }
        } ,
        { “id” : 51254322,
        “name” : “Pizza da Sexta”,
        “amount” : 80.00,
        “category” : {“Category_id” : 1, “category_name” : “Lanches”} ,
        “status”: “PAID”,
        “created_at” : “05/08/2020”,
        “paid_at” : “05/08/2020”,
        “description” : “Fulano pediu pepperoni e Ciclano Frango com Cheddar”,
        “Splitted” : {
        “payers” :  [{ “payer_id” : 34, “paid_amount”  : 80}],
        “benefited” : [{“benefited_id” : 2, “benefited_amount” : 20} ,
        {“benefited_id” : 34, “benefited_amount” : 30},
        {“benefited_id” : 40, “benefited_amount” : 30}]
        }
        } ,
        ...]
        }
