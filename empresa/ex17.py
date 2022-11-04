from flask import Flask
from flask_restx import reqparse, abort, Api, Resource, fields

app = Flask(__name__)
api = Api(
    app,
    version='1.0',
    title='API Funcionarios da Empresa',
    description='Permite consultar a folha de pagamentos dos funcionários da empresa',
    doc='/doc'
)
#-=-=-=-=-=-=-=-=-=-=-EXCERCICIO 01 DA ATIVIDADE 17 -=-=-=-=-=-=-=-=--=-=-=-=
FUNCIONARIOS = [
    {'cpf': 1, 'nome': 'Ana', 'horas_trabalhadas': 8, 'valor_da_hora_trabalhada': 45.78},
    {'cpf': 2, 'nome': 'Bruna', 'horas_trabalhadas': 2, 'valor_da_hora_trabalhada': 60.00},
    {'cpf': 3, 'nome': 'Carlos', 'horas_trabalhadas': 10, 'valor_da_hora_trabalhada': 38.99},
    {'cpf': 4, 'nome': 'Diogo', 'horas_trabalhadas': 4, 'valor_da_hora_trabalhada': 45.78},
    {'cpf': 5, 'nome': 'Ester', 'horas_trabalhadas': 5, 'valor_da_hora_trabalhada': 45.78}
    ]

# Parse dos dados enviados na requisição no formato JSON:
parser = reqparse.RequestParser()
parser.add_argument('cpf', type=int, help='cpf do funcionario')
parser.add_argument('nome', type=str, help='nome funcionario')
parser.add_argument('horas_trabalhadas', type=int, help='horas trabalhadas')    
parser.add_argument('valor_da_hora_trabalhada', type=float, help='valor das horas trabalhadas')    

def aborta_se_o_funcionario_nao_existe(cpf):
    encontrei = False
    for funcionario in FUNCIONARIOS:
        if funcionario['cpf'] == int(cpf):
            encontrei = True
            if encontrei == False:
                abort(404, mensagem="O funcionario com cpf = {} não existe".format(cpf)) #404:Not Found


campos_obrigatorios_para_atualizacao = api.model('Atualizaçao de hora do funcionario', {
    'cpf': fields.Integer(required=False, description='cpf do funcionario'),
    'nome': fields.String(required=False, description='nome funcionario'),
    'horas_trabalhadas': fields.Integer(required=False, description='horas trabalhadas'),
    'valor_da_hora_trabalhada': fields.Float(required=False, description='valor das horas trabalhadas')}
    )

campos_obrigatorios_para_insercao = api.model('Inserção de Funcionario', {
    'cpf': fields.Integer(required=False, readonly=True, description='identificador do produto'),
    'nome': fields.String(required=True, description='nome funcionario'),
    'horas_trabalhadas': fields.Integer(required=True, description='horas trabalhadas'),
    'valor_da_hora_trabalhada': fields.Float(required=True, description='valor das horas trabalhadas')}
)    

@api.route('/funcionarios')
class ListaFuncionarios(Resource):
    @api.doc(responses={200: 'funcionarios retornados'})
    def get(self):
        return FUNCIONARIOS
    
    @api.doc(responses={201: 'funcionario inserido'}) #201: Created
    @api.expect(campos_obrigatorios_para_insercao)
    def post(self):
        args = parser.parse_args()
        cpf = -1
        for funcionario in FUNCIONARIOS:
            if int(funcionario['cpf']) > cpf:
                cpf = int(funcionario['cpf'])
        cpf = cpf + 1
        funcionario = {'cpf': cpf, 'nome': args['nome'], 'horas_trabalhadas': args['horas_trabalhadas'], 'valor_da_hora_trabalhada': args['valor_da_hora_trabalhada']}
        FUNCIONARIOS.append(funcionario)
        return funcionario, 201, #201: Created    


@api.route('/funcionarios/<cpf>')
@api.doc(params={'cpf': 'CPF do funcionario'})
class Funcionario(Resource):
    @api.doc(responses={200: 'funcionario retornado'})
    def get(self, cpf):
        aborta_se_o_funcionario_nao_existe(cpf)
        return FUNCIONARIOS[int(cpf)]
    
    @api.doc(responses={200: 'funcionario atualizado'}) #200: OK
    @api.expect(campos_obrigatorios_para_atualizacao)
    def put(self, cpf):
        aborta_se_o_funcionario_nao_existe(cpf)
        args = parser.parse_args()
        for funcionario in FUNCIONARIOS:
            if funcionario['cpf'] == int(cpf):
                funcionario['cpf'] = args['cpf']
                funcionario['nome'] = args['nome']
                funcionario['horas_trabalhadas'] = args['horas_trabalhadas']
                funcionario['valor_da_hora_trabalhada'] = args['valor_da_hora_trabalhada']
                break
        return funcionario, 200, #200: OK   

    @api.doc(responses={200: 'funcionario atualizado'}) #200: OK
    @api.expect(campos_obrigatorios_para_atualizacao)
    def patch(self, cpf):
        aborta_se_o_funcionario_nao_existe(cpf)
        args = parser.parse_args()
        for funcionario in FUNCIONARIOS:
            if funcionario['cpf'] == int(cpf):
                funcionario['cpf'] = args['cpf'] if args['cpf'] != None else  funcionario['cpf']

                funcionario['nome'] = args['nome'] if args['nome'] != None else funcionario['nome']

                funcionario['horas_trabalhadas'] = args['horas_trabalhadas'] if args['horas_trabalhadas'] != None else funcionario['horas_trabalhadas']

                funcionario['valor_da_hora_trabalhada'] = args['valor_da_hora_trabalhada'] if args['valor_da_hora_trabalhada'] != None else funcionario['valor_da_hora_trabalhada']
                break
        return funcionario, 200   #200: OK 

    @api.doc(responses={204: 'funcionario removido'}) #204: No Content
    def delete(self, cpf):
        aborta_se_o_funcionario_nao_existe(cpf)
        del FUNCIONARIOS[int(cpf)]
        return '', 204, #204: No Content


@api.route('/funcionarios/pagamentos')
class Pagamentos(Resource):
    @api.doc(responses={200: 'pagamentos retornados'})
    def get(self):
        pagamentos = []
        for funcionario in FUNCIONARIOS:
            salario = funcionario['horas_trabalhadas'] * funcionario['valor_da_hora_trabalhada']
            pagamentos.append({'cpf': funcionario['cpf'], 'salario': salario})
        return pagamentos    


@api.route('/funcionarios/pagamentos/<cpf>')
@api.doc(params={'cpf': 'CPF do funcionario'})
class Pagamento(Resource):
    @api.doc(responses={200: 'pagamento do funcionario retornado'})
    def get(self, cpf):
        aborta_se_o_funcionario_nao_existe(cpf)
        funcionario = FUNCIONARIOS[int(cpf)]
        salario = funcionario['horas_trabalhadas'] * funcionario['valor_da_hora_trabalhada']
        return {'cpf': funcionario, 'salario': salario }


@api.route('/funcionarios/pagamentos/menor')
class MenorPagamento(Resource):
    @api.doc(responses={200: 'menor pagamento retornado'})
    def get(self):
        salarios = []
        for funcionario in FUNCIONARIOS:
            salario = funcionario['horas_trabalhadas'] * funcionario['valor_da_hora_trabalhada']
            salarios.append(salario)
        return {"salario":min(salarios)}


@api.route('/funcionarios/pagamentos/maior')
class MaiorPagamento(Resource):
    @api.doc(responses={200: 'maior pagamento retornado'})
    def get(self):
        salarios = []
        for funcionario in FUNCIONARIOS:
            salario = funcionario['horas_trabalhadas'] * funcionario['valor_da_hora_trabalhada']
            salarios.append(salario)
        return {"salario":max(salarios)}  
            

@api.route('/funcionarios/pagamentos/total')
class TotalPagamentos(Resource):
    @api.doc(responses={200: 'total dos pagamentos retornados'})
    def get(self):
        total = 0
        for funcionario in FUNCIONARIOS:
            salario = funcionario['horas_trabalhadas'] * funcionario['valor_da_hora_trabalhada']
            total += salario
        return {"total":total}  

#*************************************FIM DA PRATICA 22 **************************************************


if __name__ == '__main__':
    app.run(debug=True)