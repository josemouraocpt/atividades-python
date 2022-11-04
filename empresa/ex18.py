from flask import Flask
from flask_restx import reqparse, abort, Api, Resource, fields

app = Flask(__name__)
api = Api(
    app,
    version='1.0',
    title='API Estoque da Empresa',
    description='Permite consultar o estoque da empresa',
    doc='/doc'
)
#-=-=-=-=-=-=-=-=-=-=-EXCERCICIO 02 DA ATIVIDADE 17 -=-=-=-=-=-=-=-=--=-=-=-=
PRODUTO = [
    {'id': 1, 'nome': 'Calça', 'quantidade': 12, 'preco': 89.94},
    {'id': 2, 'nome': 'Camisa', 'quantidade': 54, 'preco': 49.99},
    {'id': 3, 'nome': 'Saia', 'quantidade': 33, 'preco': 72.14},
    {'id': 4, 'nome': 'Sapato', 'quantidade': 12, 'preco': 99.11},
    {'id': 5, 'nome': 'Vestido', 'quantidade': 47, 'preco': 78.32}
    ]

# Parse dos dados enviados na requisição no formato JSON:
parser = reqparse.RequestParser()
parser.add_argument('id', type=int, help='id do produto')
parser.add_argument('nome', type=str, help='nome do produto')
parser.add_argument('quantidade', type=int, help='quantidade de produtos')    
parser.add_argument('preco', type=float, help='preço dos produtos')    

def aborta_se_o_produto_nao_existe(id):
    encontrei = False
    for produto in PRODUTO:
        if produto['id'] == int(id):
            encontrei = True
            if encontrei == False:
                abort(404, mensagem="O produto com id = {} não existe".format(id)) #404:Not Found


campos_obrigatorios_para_atualizacao = api.model('Atualizaçao de produto', {
    'id': fields.Integer(required=False, description='id do produto'),
    'nome': fields.String(required=False, description='nome do produto'),
    'quantidade': fields.Integer(required=False, description='quantidade do produto'),
    'preco': fields.Float(required=False, description='preço do produto')}
    )

campos_obrigatorios_para_insercao = api.model('Inserção de Produtos', {
    'id': fields.Integer(required=False, readonly=True, description='id do produto'),
    'nome': fields.String(required=True, description='nome do produto'),
    'quantidade': fields.Integer(required=True, description='quantidade do produto'),
    'preco': fields.Float(required=True, description='preço do produto')}
)    

campos_obrigatorios_para_venda = api.model('Venda de produto', {
    'id': fields.Integer(required=True, description='id do produto'),
    'quantidade': fields.Integer(required=True, description='quantidade do produto')}
    )


@api.route('/produtos')
class ListaProdutos(Resource):
    @api.doc(responses={200: 'produtos retornados'})
    def get(self):
        return PRODUTO
    
    @api.doc(responses={201: 'produto inserido'}) #201: Created
    @api.expect(campos_obrigatorios_para_insercao)
    def post(self):
        args = parser.parse_args()
        id = -1
        for produto in PRODUTO:
            if int(produto['id']) > id:
                id = int(produto['id'])
        id = id + 1
        produto = {'id': id, 'nome': args['nome'], 'quantidade': args['quantidade'], 'preco': args['preco']}
        PRODUTO.append(produto)
        return produto, 201, #201: Created    


@api.route('/produto/<id>')
@api.doc(params={'id': 'id do produto'})
class Produto(Resource):
    @api.doc(responses={200: 'produto retornado'})
    def get(self, id):
        aborta_se_o_produto_nao_existe(id)
        return PRODUTO[int(id)]
    
    @api.doc(responses={200: 'produto atualizado'}) #200: OK
    @api.expect(campos_obrigatorios_para_atualizacao)
    def put(self, id):
        aborta_se_o_produto_nao_existe(id)
        args = parser.parse_args()
        for produto in PRODUTO:
            if produto['id'] == int(id):
                produto['id'] = args['id']
                produto['nome'] = args['nome']
                produto['quantidade'] = args['quantidade']
                produto['preco'] = args['preco']
                break
        return produto, 200, #200: OK   

    @api.doc(responses={200: 'produto atualizado'}) #200: OK
    @api.expect(campos_obrigatorios_para_atualizacao)
    def patch(self, id):
        aborta_se_o_produto_nao_existe(id)
        args = parser.parse_args()
        for produto in PRODUTO:
            if produto['id'] == int(id):
                produto['id'] = args['id'] if args['id'] != None else  produto['id']

                produto['nome'] = args['nome'] if args['nome'] != None else produto['nome']

                produto['quantidade'] = args['quantidade'] if args['quantidade'] != None else produto['quantidade']

                produto['preco'] = args['preco'] if args['preco'] != None else produto['preco']
                break
        return produto, 200   #200: OK 

    @api.doc(responses={204: 'produto removido'}) #204: No Content
    def delete(self, id):
        aborta_se_o_produto_nao_existe(id)
        del PRODUTO[int(id)]
        return '', 204, #204: No Content


@api.route('/produtos/estoque')
class TotalEstoque(Resource):
    @api.doc(responses={200: 'estoque retornado'})
    def get(self):
        total_em_estoque = 0;
        for produto in PRODUTO:
            total_em_estoque += produto['quantidade']
        return {'total estoque': total_em_estoque} 


@api.route('/produto/estoque/<id>')
@api.doc(params={'id': 'id do produto'})
class EstoqueIndividual(Resource):
    @api.doc(responses={200: 'estoque do produto retornado'})
    def get(self, id):
        aborta_se_o_produto_nao_existe(id)
        produto = PRODUTO[int(id)]
        estoque = produto['quantidade']
        return {'id': produto, 'salario': estoque }


@api.route('/produtos/estoque/menor')
class MenorProdutoEmEstoque(Resource):
    @api.doc(responses={200: 'menor produto em estoque retornado'})
    def get(self):
        estoque = []
        for produto in PRODUTO:
            estoque.append(produto['quantidade'])
        return {'estoque': min(estoque)}


@api.route('/produtos/estoque/maior')
class MaiorProdutoEmEstoque(Resource):
    @api.doc(responses={200: 'maior produto em estoque retornado'})
    def get(self):
        estoque = []
        for produto in PRODUTO:
            estoque.append(produto['quantidade'])
        return {'estoque': max(estoque)}

            

@api.route('/produtos/estoque/total')
class TotalPagamentos(Resource):
    @api.doc(responses={200: 'total dos pagamentos retornados'})
    def get(self):
        total = 0
        for produto in PRODUTO:
            total += produto['preco']
        return {"total":total}  


@api.route('/produtos/venda/<id>')       
class Venda(Resource):
    @api.expect(campos_obrigatorios_para_venda)
    def put(self, id):
        aborta_se_o_produto_nao_existe(id)
        args = parser.parse_args()
        for produto in PRODUTO:
            if produto['id'] == args['id']:
                produto['quantidade'] = produto['quantidade'] - args['quantidade']
                return produto, 201

@api.route('/produtos/compra/<id>')       
class Compra(Resource):
    @api.expect(campos_obrigatorios_para_venda)
    def put(self, id):
        aborta_se_o_produto_nao_existe(id)
        args = parser.parse_args()
        for produto in PRODUTO:
            if produto['id'] == args['id']:
                produto['quantidade'] = produto['quantidade'] + args['quantidade']
                return produto, 201
      

#*************************************FIM DA PRATICA 23 **************************************************


if __name__ == '__main__':
    app.run(debug=True)