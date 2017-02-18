import numpy as np
from sklearn.cluster import KMeans
import scipy
import modelCliente as cli


def toMatrix(idToCliente):
	matriz = list()
	#cria matriz(narray) contendo a quantidade de pedidos e a soma dos valores dos pedidos dos clientes
	for clienteId in idToCliente:
		cliente = idToCliente[clienteId]
		linha = list()
		linha.append(cliente.quantPedidos)
		linha.append(cliente.somaPedidos)
		matriz.append(linha)

	matriz = np.array(matriz)
	return matriz

def clusterizar(matriz,idToCliente,limiteClusters=10,limiar=0.01):
	classes = {}
	k_range = range(1,limiteClusters+1)

	#clusteriza com k clusters para todo 0<k<=limiteClusters
	kmeans = [KMeans(init='k-means++',n_clusters=k).fit(matriz) for k in k_range]

	#recupera centroides para calcular o numero adequado de clusters
	centroids = [x.cluster_centers_ for x in kmeans]

	k_eclid = [scipy.spatial.distance.cdist(matriz,cent,'euclidean') for cent in centroids]
	distancia = [np.min(ke,axis=1) for ke in k_eclid]

	somaQuadrados = [sum(d**2) for d in distancia]

	#normaliza soma dos quadrados das distancias dos membros para os centroids
	delta = (somaQuadrados - min(somaQuadrados)) / (max(somaQuadrados)-min(somaQuadrados))

	#escolhe o numero de clusters que atendem ao limiar solicitado
	clusters = 0
	for x in range(0,limiteClusters):
		if(abs(delta[x] - delta[x-1]) < limiar):
			break
		clusters+=1
	if clusters >= limiteClusters:
		clusters = limiteClusters - 1


	classificados = kmeans[clusters].labels_
	centroid = centroids[clusters]
	cont = 0
	#relaciona clientes com suas classes
	for clienteId in idToCliente:
		cliente = idToCliente[clienteId]
		cliente.setClasse(classificados[cont])
		classe = classes.get(classificados[cont],False)
		if not classe: #classe nova
			classe = list()
			classes[classificados[cont]] = classe
		classe.append(cliente)
		cont+= 1
	return classes
	

def classificar(clustersMax,limiar):
	idToCliente = cli.readClientes("static/input/input.csv")
	matriz = toMatrix(idToCliente)
	classes = clusterizar(matriz,idToCliente,limiteClusters = clustersMax,limiar=limiar)
	return {'clientes' : idToCliente,'classes' : classes}