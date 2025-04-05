from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

def tipo_triangulo(a, b, c):
    """
    Determina o tipo de triângulo com base nos lados fornecidos.
    """
    if a + b > c and a + c > b and b + c > a:
        if a == b == c:
            return "equilátero", "equilatero.png"
        elif a == b or a == c or b == c:
            return "isósceles", "isoceles.png"
        else:
            return "escaleno", "escaleno.png"
    else:
        return "não é um triângulo", "nao_triangulo.png"

@app.route('/')
def index():
    """Rota para renderizar o arquivo index.html."""
    return render_template('index.html')

@app.route('/triangulo', methods=['POST'])
def verificar_triangulo():
    """
    Rota Flask para receber os lados do triângulo e retornar o tipo.
    """
    dados = request.get_json()
    a = dados['lado_a']
    b = dados['lado_b']
    c = dados['lado_c']

    tipo, imagem = tipo_triangulo(a, b, c)
    return jsonify({'tipo': tipo, 'imagem': imagem})

if __name__ == '__main__':
    app.run(debug=True)