from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from flask_mail import Mail, Message

from app import app

import smtplib, ssl

import Projeto as proj # Importa

global classif_lista_pontos
classif_lista_pontos = [[],[],[],[]]



@app.route('/')

# Exemplo do Flask
@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    return render_template('index.html', title='Home', user=user)

# Exemplo do Flask
@app.route('/student')
def student():
   return render_template('student.html')

# Exemplo do Flask
@app.route('/result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      result = request.form
      return render_template("result.html",result = result)

# Rota para envio dos pontos obtidos
@app.route('/upload')
def upload_file():
   return render_template('upload.html')

# Rota para abrir o site com Webgazer, para captação dos pontos
@app.route('/captacao')
def captacao():
   return render_template('captacao.html')

# Rota usada pelo /upload, para envio de e-mail, e apresentação de resultados
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file_final():
    Correcao = proj.Classe_Correcao()

    if request.method == 'POST':
        f = request.files['file']
        predicao = Correcao.acao_botao(f)

      #f.save(secure_filename(f.filename))
      #return str(predicao)
        return render_template("uploader.html",predicao = predicao)

# Rota usada depois que é realiza a captação pelo Webgazer
@app.route("/function_route", methods=["GET", "POST"])
def my_function():
    Correcao = proj.Classe_Correcao()
    #request.headers['Content-Type'] == 'application/json'
    #request.headers.get('application/json')
    request.get_json(force=True)

    
    if request.method == "POST":
        #a = request.json()

        a = request.get_json()
        file = open("pontos.txt", "w")
        for linha in a:
            file.write("%s" % linha)
        file.close()

        predicao = Correcao.acao_botao("./pontos.txt")

        file_2 = open("resultado.txt", "w")
        for linha_2 in predicao:
            file_2.write("%s" % linha_2)
        file_2.close()#

        print("Fim da Predição")

    return "Ok"
    #return render_template("uploader.html",predicao = predicao)
