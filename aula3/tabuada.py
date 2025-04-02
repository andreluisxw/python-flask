from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def raiz():
    return render_template('index.html')

@app.route('/calcule_tabuada', methods=['POST'])
def calcula():
    if 'txt_numero' in request.form and request.form['txt_numero'].isdigit():
        numero = int(request.form['txt_numero'])
        result = {"tabuada_do": numero, "valores": []}
        for i in range(0, 11):
            r = numero * i
            result['valores'].append(r)
        return render_template('index.html', resultado=result)
    else:
        return render_template('index.html', erro="Por favor, insira um número válido.")

if __name__ == '__main__':
    app.run(debug=True)