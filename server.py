import os
from flask import Flask,render_template,request, redirect, url_for
import controlCluster as cc
import modelCliente as mc

 

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "static/input"

@app.route('/')
def index():
	mensagem = ""
	if 'mensagem' in request.args:
		mensagem = request.args['mensagem']
	if os.path.isfile("static/input/input.csv"):#verifica se ja existe um arquivo upado para o servidor
		return redirect(url_for('list'))#clusteriza arquivo ja existente
	return render_template("index.html",mensagem=mensagem)#pagina para configuracao de nova culsterizacao

@app.route('/new')
def new():#apaga arquivo ja existe no servidor e redireciona para a pagina de configuracao de nova culsterizacao
	os.system("rm static/input/input.csv")
	return redirect(url_for('index'))


@app.route('/cluster',methods = ['POST'])
def cluster():
	#recupera valores de configuracao
	clustersMax = request.form['clusters']
	limiar = request.form['limiar']

	if 'arquivo' not in request.files:#verifica se o arquivo foi enviado
		return redirect(url_for("index",mensagem="E necessario enviar um arquivo"))
	file = request.files['arquivo']
	if file.filename == "":
		return redirect(url_for("index",mensagem="Arquivo invalido"))

	#remove possivel arquivo que ja possa existir no servidor
	os.system("rm static/input/input.csv")
	
	#salva novo arquivo
	nomeArquivo = "input.csv"
	file.save(os.path.join(app.config['UPLOAD_FOLDER'],nomeArquivo))
	return redirect(url_for('list',clustersMax = clustersMax,limiar = limiar))

@app.route('/list')
def list():
	#recupera valores de configuracao
	clustersMax = int(request.args['clustersMax'])
	limiar = float(request.args['limiar'])

	#classifica
	try:
		classificacao = cc.classificar(clustersMax,limiar)
		classes = classificacao['classes']
		clientes = classificacao['clientes']
		return render_template("lista.html",classes = classes,clientes = clientes)
	except Exception as erro:
		os.system("rm static/input/input.csv")
		return redirect(url_for('index',mensagem="Arquivo invalido"))
if __name__ == "__main__":
	app.run(host='0.0.0.0')