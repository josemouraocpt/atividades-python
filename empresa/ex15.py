from flask import Flask, jsonify, request
from flask_restful import reqparse, abort, Api, Resource

app = Flask (__name__)
api = Api(app)

#EXERCICIO 20
produtos = [
    {'nome': 'sapato', 'preco': 128.55},
    {'nome': 'camisa', 'preco': 49.89},
    {'nome': 'calça', 'preco': 89.99},
    {'nome': 'bermuda', 'preco': 78.63}
    ]

@app.route('/produtos', methods=['GET'])
def retorna_todos_produtos():
    resp = produtos

    if 'X-nome-produto' in request.headers:
        nome = request.headers['X-nome-produto']
        for produto in produtos:
            if produto['nome'] == nome:
                resp = produto

    return jsonify(resp)            

#EXERCICIO 1

camisetas = [
    {'tamanho': 'pequeno', 'preco': '10'},
    {'tamanho': 'media', 'preco': '12'},
    {'tamanho': 'grande', 'preco': '15'}
]

@app.route('/camisetas', methods=['GET'])
def retorna_valor_total_das_camisetas():
    pequena = int(request.args['pequena'])
    media = int(request.args['media'])
    grande = int(request.args['grande'])
    total = pequena * 10 + media * 12 + grande * 15
    return '''<p>O total da vendas de camisetas pequenas {}, medias {} e grandes {} foi de R${}</p>
    '''.format(pequena, media, grande, total)

#EXERCICIO 2

@app.route('/salario/horas', methods=['GET'])
def retorna_salario_liquido_e_bruto():
    horas_normal = int(request.args['normal'])
    horas_extra = int(request.args['extra'])
    salario_bruto = float(horas_normal * 40 + horas_extra * 50)
    salario_liquido = float(salario_bruto - (salario_bruto * 0.10))
    return jsonify({
        "Horas normais tarbalhadas": horas_normal,
        "Horas extras trabalhadas": horas_extra,
        "Salário bruto": "R${:.2f}".format(salario_bruto),
        "Salário liquido": "R${:.2f}".format(salario_liquido)
    })


#EXERCICIOS 21

PRODUTOS = [
    {'id': 0, 'nome': 'sapato', 'preco': 128.55},
    {'id': 1, 'nome': 'camisa', 'preco': 49.89},
    {'id': 2, 'nome': 'calça', 'preco': 89.99},
    {'id': 3, 'nome': 'bermuda', 'preco': 78.63}
    ]

def aborta_se_o_produto_nao_existe(id):
    encontrei = False
    for produto in PRODUTOS:
        if produto['id'] == int(id):
            encontrei = True
    if encontrei == False:
        abort(404, mensagem="O produto com id = {} não existe".format(id))

# parser = reqparse.RequestParser()
# parser.add_argument('id', type=int, help='identificador do produto')
# parser.add_argument('nome', type=str, help='nome do produto')
# parser.add_argument('preco', type=float, help='preço do produto')        

class Produto(Resource):
    def get(self, id):
        aborta_se_o_produto_nao_existe(id)
        return PRODUTOS[int(id)]

    def delete(self, id):
        aborta_se_o_produto_nao_existe(id)
        del PRODUTOS[int(id)]
        return '', 204

    def put(self, id):
        aborta_se_o_produto_nao_existe(id)
        args = parser.parse_args()
        for produto in PRODUTOS:
            if produto['id'] == int(id):
                produto['id'] = args['id']
                produto['nome'] = args['nome']
                produto['preco'] = args['preco']
                break
        return produto, 200

class ListaProduto(Resource):
    def get(self):
        return PRODUTOS

    def post(self):
        args = parser.parse_args()
        id = -1
        for produto in PRODUTOS:
            if int(produto['id']) > id:
                id = int(produto['id'])
        id = id + 1
        produto = {'id': id, 'nome': args['nome'], 'preco': args['preco']}
        PRODUTOS.append(produto)
        return produto, 201 

api.add_resource(Produto, '/produtos/<id>')
api.add_resource(ListaProduto, '/produtos')

#EXERCICIO 01

alunos = [
    {"matricula": 1, "nome": "ana", "nota": 72.00},
    {"matricula": 2, "nome": "bruna", "nota": 71.50},
    {"matricula": 3, "nome": "carlos", "nota": 68.50},
    {"matricula": 4, "nome": "diogo", "nota": 70.00},
    {"matricula": 5, "nome": "ester", "nota": 69.00},
]

parser = reqparse.RequestParser()
parser.add_argument('matricula', type=int, help='matricula do aluno')
parser.add_argument('nome', type=str, help='nome do aluno')
parser.add_argument('nota', type=float, help='nota do aluno')        

def aborta_se_o_aluno_nao_existe(matricula):
    encontrei = False
    for aluno in alunos:
        if aluno['matricula'] == int(matricula):
            encontrei = True
    if encontrei == False:
        abort(404, mensagem="O aluno com a matricula = {} não existe".format(matricula))


class Aluno(Resource):
    def get(self, matricula):
        aborta_se_o_aluno_nao_existe(matricula)
        return alunos[int(matricula)] 

    def put(self, matricula):
        aborta_se_o_aluno_nao_existe(matricula)
        args = parser.parse_args()
        for aluno in alunos:
            if aluno['matricula'] == int(matricula):
                aluno['matricula'] = args['matricula']
                aluno['nome'] = args['nome']
                aluno['nota'] = args['nota']
                break
        return aluno, 200

    def patch(self, matricula):
        aborta_se_o_aluno_nao_existe(matricula)
        args = parser.parse_args()
        for aluno in alunos:
            if aluno['matricula'] == int(matricula):
                aluno['matricula'] = args['matricula'] if args['matricula'] != None else  aluno['matricula']
                aluno['nome'] = args['nome'] if args['nome'] != None else aluno['nome']
                aluno['nota'] = args['nota'] if args['nota'] != None else aluno['nota']
                break
        return aluno, 200

    def delete(self, matricula):
        aborta_se_o_aluno_nao_existe(matricula)
        del alunos[int(matricula)]
        return '', 204

class ListaAlunos(Resource):
    def get(self):
        return alunos

    def post(self):
        args = parser.parse_args()
        matricula = -1
        for aluno in alunos:
            if int(aluno['matricula']) > matricula:
                matricula = int(aluno['matricula'])
        matricula = matricula + 1
        aluno = {'matricula': matricula, 'nome': args['nome'], 'nota': args['nota']}
        alunos.append(aluno)
        return aluno, 201 


api.add_resource(Aluno, '/alunos/<matricula>')
api.add_resource(ListaAlunos, '/alunos')

if __name__ == "__main__":
    app.run(debug=True)