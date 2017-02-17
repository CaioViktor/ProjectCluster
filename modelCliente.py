import pandas as pd
class Cliente:
	def __init__(self,codigo,nome,regiao):
		self.codigo = codigo
		self.nome = str(nome)
		self.regiao = str(regiao)
		self.pedidos = list()
		self.quantPedidos = 0
		self.somaPedidos = 0
		self.classe = -1

	def __str__(self):
		return "("+str(self.codigo)+")"+self.nome+" -- "+self.regiao +"\tquantidade compras: "+str(self.quantPedidos)+"\tsoma total: "+str(self.somaPedidos)+"\tclasse: "+str(self.classe)


	def addPedido(self,data,codigo,comissao,valorPedido,valorComissao):
		comissaoFloat = float(str(comissao).replace(".","").replace(",","."))
		valorFloat = float(str(valorPedido).replace(".","").replace(",","."))
		valorComissaoFloat = float(str(valorComissao).replace(".","").replace(",","."))
		pedido = Pedido(data,codigo,comissaoFloat,valorFloat,valorComissaoFloat)
		self.pedidos.append(pedido)
		self.quantPedidos+= 1
		self.somaPedidos+= valorFloat
	
	def setClasse(self,classe):
		self.classe = classe


class Pedido:
	def __init__(self,data,codigo,comissao,valorPedido,valorComissao):
		self.data = data
		self.codigo = codigo
		self.comissao = comissao
		self.valorPedido = valorPedido
		self.valorComissao = valorComissao

def readClientes(path,delimiters=","):
	idToCliente = {}
	data_full = pd.read_csv(path,delimiter = delimiters)
	for linha in data_full.values:
		codigoCliente = str(linha[2])
		cliente = idToCliente.get(codigoCliente,False)
		if not cliente:# eh um cliente novo
			cliente = Cliente(codigoCliente,linha[3],linha[4])
			idToCliente[codigoCliente] = cliente
		cliente.addPedido(linha[0],linha[1],linha[5],linha[6],linha[7])
	return idToCliente