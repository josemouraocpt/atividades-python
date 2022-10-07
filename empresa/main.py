from flask import Flask, jsonify, request
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

if __name__ == "__main__":
    app.run ()