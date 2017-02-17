import numpy as np
from sklearn.cluster import KMeans
import scipy
import modelCliente as cli


def main():
	idToCliente = cli.readClientes("input/tabula-ACD.csv")
	matriz = toMatrix(idToCliente)
	classes = clusterizar(matriz,idToCliente)
	print("clusters: "+str(len(classes)))
	for classeId in classes:
		print("\n\n\nClasse: " + str(classeId))
		for cliente in classes[classeId]:
			print("q: "+ str(cliente.quantPedidos)+" s: "+str(cliente.somaPedidos))

def toMatrix(idToCliente):
	matriz = list()
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

	kmeans = [KMeans(init='k-means++',n_clusters=k).fit(matriz) for k in k_range]

	centroids = [x.cluster_centers_ for x in kmeans]

	k_eclid = [scipy.spatial.distance.cdist(matriz,cent,'euclidean') for cent in centroids]
	distancia = [np.min(ke,axis=1) for ke in k_eclid]

	somaQuadrados = [sum(d**2) for d in distancia]


	delta = (somaQuadrados - min(somaQuadrados)) / (max(somaQuadrados)-min(somaQuadrados))
	# print(delta)

	clusters = 0
	for x in range(0,limiteClusters):
		if(abs(delta[x] - delta[x-1]) < limiar):
			break
		clusters+=1


	# print("clusters: "+str(clusters)+" ----- "+str(delta[clusters]))
	classificados = kmeans[clusters].labels_
	cont = 0
	for clienteId in idToCliente:
		cliente = idToCliente[clienteId]
		cliente.setClasse(classificados[cont])
		classe = classes.get(classificados[cont],False)
		if not classe: #classe nova
			classe = list()
			classes[classificados[cont]] = classe
		classe.append(cliente)
		# print(cliente)
		cont+= 1
	return classes
	

if __name__ == "__main__":
	main()