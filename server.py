import os
from flask import Flask,render_template,request, redirect, url_for
import controlCluster as cc
import modelCliente as mc

 

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "static/input"

@app.route('/')
def index(mensagem=""):
	if os.path.isfile("static/input/input.csv"):
		return redirect(url_for('list'))
	return render_template("index.html",mensagem=mensagem)

@app.route('/new')
def new():
	os.system("rm static/input/input.csv")
	return redirect(url_for('index'))


@app.route('/cluster',methods = ['POST'])
def cluster():
	clustersMax = request.form['clusters']
	limiar = request.form['limiar']
	if 'arquivo' not in request.files:
		return redirect(url_for("index"),mensagem="E necessario enviar um arquivo")
	file = request.files['arquivo']
	if file.filename == "":
		return redirect(url_for("index"),mensagem="Arquivo invalido")
	os.system("rm static/input/input.csv")
	nomeArquivo = "input.csv"
	file.save(os.path.join(app.config['UPLOAD_FOLDER'],nomeArquivo))
	return redirect(url_for('list',clustersMax = clustersMax,limiar = limiar))

@app.route('/list')
def list():
	clustersMax = int(request.args['clustersMax'])
	limiar = float(request.args['limiar'])
	classificacao = cc.classificar(clustersMax,limiar)
	classes = classificacao['classes']
	# for classeID in classes:
	# 	for cliente in classes[classeID]:
	# 		print(cliente) 
	clientes = classificacao['clientes']
	return render_template("lista.html",classes = classes,clientes = clientes)

if __name__ == "__main__":
	app.run(host='0.0.0.0')