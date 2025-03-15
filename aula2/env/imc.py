from flask import Flask, render_template, request

app = Flask(__name__)
 
@app.route('/')
def index():
    return render_template('imc_calc.html')

@app.route('/calcular_imc_post', methods=['POST'])
def calcIMC():
    altura = float(request.form['txt_altura'])
    peso = float(request.form['txt_peso'])
    imc = peso / (altura * altura)
    return render_template('imc_calc.html', res_imc = imc)

app.run()