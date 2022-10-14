from flask import Flask, jsonify, request
from math import sqrt
app = Flask (__name__)

@app.route('/')
def cumprimentar():
    return 'Olá, Mundo!'

# @app.route('/testes/1')
# def teste_GET_implicito():
#     return jsonify({"resp": "Teste 1: método GET implicito."})

# @app.route('/testes/2', methods=['GET'])
# def teste_GET_explicito():
#     return jsonify({"resp": "Teste 2: método GET explicito."})

# @app.route('/testes/3', methods=['POST'])
# def teste_POST():
#     return jsonify({"resp": "Teste 3: método POST."})

@app.route('/testes/4', methods=['GET', 'POST'])
def teste_GET_POST():
    return jsonify({"resp": "Teste 4: método GET ou POST."})

# http://127.0.0.1:5000/testes/1?linguagem=Python
@app.route('/testes/1')
def teste_query_string_1_agurmento_get():
    lang = request.args.get('linguagem')
    return '''<h1> Linguagem informada {}</h1>'''.format(lang)

# http://127.0.0.1:5000/testes/2?linguagem=Python&framework=Flask
@app.route('/testes/2')
def teste_query_string_2_agurmentos_get():
    lang = request.args.get('linguagem')
    frame = request.args.get('framework')
    return '''<h1> Linguagem informada {}</h1>
              <h1> Framework informado {}</h1>'''.format(lang, frame)

# http://127.0.0.1:5000/testes/3?linguagem=Python&framework=Flask
@app.route('/testes/3')
def teste_query_string_2_agurmentos_vetor():
    lang = request.args['linguagem']
    frame = request.args['framework']
    return '''<h1> Linguagem informada {}</h1>
              <h1> Framework informado {}</h1>'''.format(lang, frame)

# http://127.0.0.1:5000/calcula/temperatura?celsius=27
@app.route('/calcula/temperatura')
def calcula_temperatura_celsius_para_fahrenheit():
    celsius = float(request.args['celsius'])
    fahrenheit = (celsius * 1.8) + 32
    return '''<h1> A temperatura informada em Celsisus de {} °
    equivale a {} ° Fahrenheit'''.format(celsius, fahrenheit)

# http://127.0.0.1:5000/calcula/media?nota1=8&nota2=3&nota3=10
@app.route('/calcula/media')
def calcula_media_das_notas():
    nota1 = float(request.args['nota1'])
    nota2 = float(request.args['nota2'])
    nota3 = float(request.args['nota3'])
    media = (nota1 + nota2 + nota3) / 3
    if media >= 0 and  media <= 3: mensagem = 'REPROVADO'
    if media >= 3 and media < 7: mensagem = 'EXAME'
    if media >= 7 and media <= 10: mensagem = 'APROVADO'
    return '''<h1> As notas {}, {} e {}, tem média de {}</h1>
    <h2> O resultado do aluno ficou como {}.</h2>'''.format(nota1, nota2, nota3, media, mensagem)

# http://127.0.0.1:5000/formulario/1
@app.route('/formulario/1', methods=['GET', 'POST'])
def teste_dados_formulario_html():
    #testa se o metodo é POST
    if request.method == 'POST':    
        lang = request.form['linguagem']
        frame = request.form['framework']
        return '''<h1> Linguagem informada {}</h1>
                <h1> Framework informado {}</h1>'''.format(lang, frame)
    return '''
    <form method="POST">
        <div>
            <label>Linguagem: <input type="text" name="linguagem"></label>
        </div>
        <div>
            <label>Framework: <input type="text" name="framework"></label>
        </div>
        <input type="submit" value="Enviar">
    </form>
    '''

# http://127.0.0.1:5000/formulario/2
@app.route('/formulario/2', methods=['GET', 'POST'])
def teste_dados_formulario_html_numeros():
    #testa se o metodo é POST
    if request.method == 'POST':    
        num1 = float(request.form['num1'])
        num2 = float(request.form['num2'])
        num3 = float(request.form['num3'])
        minimo = min([num1, num2, num3])
        maximo = max([num1, num2, num3])
        media = (num1 + num2 + num3) / 3
        return '''<h1> Os numeros {}, {} e {} tem média {}</h1>
                <h1>O menor valor foi {} e o maior foi {}</h1>'''.format(num1, num2, num3, media, minimo, maximo)
    return '''
    <form method="POST">
        <div>
            <label>Numero 1: <input type="number" name="num1"></label>
        </div>
        <div>
            <label>Numero 2: <input type="number" name="num2"></label>
        </div>
        <div>
            <label>Numero 3: <input type="number" name="num3"></label>
        </div>
        <input type="submit" value="Enviar">
    </form>
    '''

# http://127.0.0.1:5000/formulario/3
@app.route('/formulario/3', methods=['GET', 'POST'])
def teste_dados_formulario_html_imc():
    #testa se o metodo é POST
    if request.method == 'POST':    
        peso = float(request.form['peso'])
        altura = float(request.form['altura'])
        imc = peso / (altura ** 2)
        if imc <= 18.5: mensagem = 'Abaixo do peso'
        if imc >= 18.6 and imc <= 24.9: mensagem = 'Peso ideal (parabéns)'
        if imc >= 25.0 and imc <= 29.9: mensagem = 'Levemente acima do peso'
        if imc >= 30.0 and imc <= 34.9: mensagem = 'Obesidade grau I'
        if imc >= 35.0 and imc <= 39.9: mensagem = 'Obesidade grau II (severa)'
        if imc >= 40.0: mensagem = 'Obesidade grau III (mórbida)'
        return '''<h1> O indivisuo possui {}Kg e mede {}m</h1>
                <h1>O seu IMC foi de {} {}</h1>'''.format(peso, altura, imc, mensagem)
    return '''
    <form method="POST">
        <div>
            <label>Peso em Kg: <input type="text" name="peso"></label>
        </div>
        <div>
            <label>Altura em m: <input type="text" name="altura"></label>
        </div>
        <input type="submit" value="Enviar">
    </form>
    '''

#EXERCICIOS DA PARTE 18

# http://127.0.0.1:5000/triangulo
@app.route('/triangulo', methods=['GET', 'POST'])
def teste_do_triangulo():
    #testa se o metodo é POST
    if request.method == 'POST':    
        ladoA = float(request.form['ladoA'])
        ladoB = float(request.form['ladoB'])
        ladoC = float(request.form['ladoC'])

        if (ladoA > ladoB % ladoC and ladoA < ladoB + ladoC):
            mensagem = 'Pode formar um triangulo'
        if (ladoB > abs((ladoA % ladoC)) and ladoB < ladoA + ladoC):
            mensagem = 'Pode formar um triangulo'
        if (ladoC > abs((ladoA % ladoB)) and ladoC < ladoA + ladoB):
            mensagem = 'Pode formar um triangulo'
        else: 
            mensagem = 'Não pode formar um triangulo'

        return '''<p> Os valores informados: {}, {} e {} <br> {} </p>'''.format(ladoA, ladoB, ladoC, mensagem)

    return '''
    <form method="POST">
        <div>
            <label>Lado A: <input type="text" name="ladoA"></label>
        </div>
        <div>
            <label>Lado B: <input type="text" name="ladoB"></label>
        </div>
        <div>
            <label>Lado C: <input type="text" name="ladoC"></label>
        </div>
        <input type="submit" value="Enviar">
    </form>
    '''

# http://127.0.0.1:5000/produtos?id=1
# @app.route('/produtos')
# def get_produto_by_id():
#     produtos_id = [    
#         {'id': 1, 'produto': 'sapato', 'preco': 99.99}, 
#         {'id': 2, 'produto': 'bolsa', 'preco': 103.89}, 
#         {'id': 3, 'produto': 'camisa', 'preco': 49.98}, 
#         {'id': 4, 'produto': 'calça', 'preco': 89.72}, 
#         {'id': 5, 'produto': 'blusa', 'preco': 97.35}
#         ]
#     id = int(request.args['id']) - 1
   
#     # print(produtos_id[id])
#     return ''' O produto {} tem o preço de R${}'''.format(produtos_id[id]['produto'], produtos_id[id]['preco'])

#EXERCICIOS DA PARTE 18

#PARTE 19 TESTES
produtos = [
    {'nome': 'sapato', 'preco': 128.55},
    {'nome': 'camisa', 'preco': 49.89},
    {'nome': 'calça', 'preco': 89.99},
    {'nome': 'bermuda', 'preco': 78.63}
    ]

# http://127.0.0.1:5000/produtos
@app.route('/produtos', methods=['GET'])
def retornar_todos_os_produtos():
    return jsonify({'produtos': produtos})

# http://127.0.0.1:5000/produtos/camisa
@app.route('/produtos/<string:nome>', methods=['GET'])
def retornar_dados_do_produto_informado(nome):
    resp = {'produto': '', 'preco': None}
    for produto in produtos:
        if produto['nome'] == nome:
            resp = produto
    return jsonify(resp)

# http://127.0.0.1:5000/produtos/cinto/45.67
@app.route('/produtos/<string:nome>/<float:preco>', methods=['POST'])
def inserir_produto(nome, preco):
    produtos.append({'produto': nome, 'preco': preco})
    return jsonify({'produto': nome, 'preco': preco})

# http://127.0.0.1:5000/produtos/camisa/10.00
# http://127.0.0.1:5000/produtos/camisa/-10.00
@app.route('/produtos/<string:nome>/<float(signed=True):preco>', methods=['PATCH'])
def alterar_preco_do_produto(nome, preco):
    resp = {'produto': '', 'preco': None}
    for produto in produtos:
        if produto['nome'] == nome:
            produto['preco'] += preco
            resp = produto
    return jsonify(resp)

# http://127.0.0.1:5000/produtos/camisa
@app.route('/produtos/<string:nome>', methods=['DELETE'])
def remover_produto(nome):
    for i, produto in enumerate(produtos):
        if produto['nome'] == nome:
            del produtos[i]
    return jsonify({'produtos': produtos})    
#PARTE 19 TESTES

#EXERCICIOS DA PARTE 19

# http://127.0.0.1:5000/abscissas/12/2/5/8
@app.route('/abscissas/<int:x1>/<int:y1>/<int:x2>/<int:y2>', methods=['PATCH'])
def distancia_entres_abscissas(x1, y1, x2, y2):
    d = sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return '''<p>A distância entre os pontos A({},{}) e B({},{}) é de {:.2}</p>'''.format(x1, y1, x2, y2, d)

cardapio = [
    {'nome': 'cachorro quente', 'preço': 12.00},
    {'nome': 'sanduiche', 'preço': 23.89},
    {'nome': 'pastel', 'preço': 3.98},
    {'nome': 'refrigerante', 'preço': 5.72},
    {'nome': 'suco', 'preço': 4.35}
    ]

# http://127.0.0.1:5000/cardapio
@app.route('/cardapio', methods=['GET'])
def retornar_itens_do_cardapio():
    return jsonify(cardapio)

# http://127.0.0.1:5000/cardapio/suco
@app.route('/cardapio/<string:nome>', methods=['GET'])
def retornar_item_do_cardapio_informado(nome):
    resp = {'nome': '', 'preco': None}
    for produto in cardapio:
        if produto['nome'] == nome:
            resp = produto
    return jsonify(resp)    

# http://127.0.0.1:5000/cardapio/coxinha/3.50
@app.route('/cardapio/<string:nome>/<float:preco>', methods=['POST'])
def inserir_produto_no_cardapio(nome, preco):
    cardapio.append({'produto': nome, 'preco': preco})
    return jsonify({'produto': nome, 'preco': preco})

# http://127.0.0.1:5000/cardapio/suco/4.35/empadinha/2.50
@app.route('/cardapio/<string:nome>/<float(signed=True):preco>/<string:newnome>/<float(signed=True):newpreco>', methods=['PUT'])
def altera_produto_do_cardapio(nome, preco, newnome, newpreco):
    resp = {'produto': '', 'preco': None}
    for produto in cardapio:
        if produto['nome'] == nome:
            produto['nome'] = newnome
            produto['preço'] = newpreco
            resp = produto
    return jsonify(resp)

# http://127.0.0.1:5000/cardapio/suco
@app.route('/cardapio/<string:nome>', methods=['DELETE'])
def remover_item_cardapio(nome):
    for i, produto in enumerate(cardapio):
        if produto['nome'] == nome:
            del cardapio[i]
    return jsonify({'produtos': cardapio})    

if __name__ == "__main__":
    app.run ()