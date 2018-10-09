# -*- coding: utf-8 -*-
#Esta biblioteca foi feita para a versão 2.7 do Python, não sendo compatível com as versões 3.x do mesmo.

import time
import psutil
from heap import *

class Grafo:
	nome_output='output.txt'
	def __init__(self,entrada_txt=False,formato_lista=False,formato_matriz=False):
		u'''
		entrada_txt pode ser 'False' ou uma string contendo o endereço de um arquivo .txt com um grafo. Se for 'False', então significa que o arquivo com o grafo possui outro formato (.sql por exemplo, algo que ficará em aberto para possíveis evoluções do código). Mas caso seja uma string, então, o arquivo de texto com o grafo possui o seguinte formato:
			
			N #número de vértices
			V1 V2 #aresta ligando V1 a V2
			...
			Vi Vj #aresta ligando Vi a Vj

		*IMPORTANTE: para facilitar o entendimento do código, usarei o exemplo abaixo nos comentários subsequentes.
		4
		1 2
		1 3
		2 3
		2 4
		'''
		if entrada_txt:
			try:
				arquivo=open(entrada_txt,'r').read()
				self.lista_geral=arquivo.splitlines() #no exemplo: self.lista_geral=["4","1 2","1 3","2 3","2 4"]
				self.qtd_vertices=int(self.lista_geral[0])
				self.grafo_com_pesos = False
				self.criar_lista_grafo_a_partir_de_entrada_txt(formato_lista)
				self.criar_matriz_grafo_a_partir_de_entrada_txt(formato_matriz)
			except Exception,e:
				print u'Houve algum erro na criação do grafo oriundo do arquivo txt indicado. Veja:\n\n'
				print e

		open(self.nome_output,'wb') #abrindo no formato 'write byte' apenas pra criar um arquivo em branco com tal nome (ou apagar os dados de algum com o mesmo nome)
		self.output=open(self.nome_output,'ab') #abrindo no formato 'append byte'
	
	def criar_lista_grafo_a_partir_de_entrada_txt(self,formato_lista):
		u'''Se "formato_lista==True", então será criada uma lista a partir de um grafo oriundo de um arquivo txt'''
		if formato_lista:
			self.grafo_lista=[[] for i in xrange(self.qtd_vertices)]

			partition_format = ' '

			try:
				v1,espaco,v2 = self.lista_geral[1].partition(partition_format)
				teste1 = int(v1) #testa se a separação é feita por ' '

				try:
					v2,espaco,peso = v2.partition(partition_format)
					teste2 = int(v2)
					teste3 = float(peso)

					self.grafo_com_pesos = True

				except:
					pass
			
			except:

				try:
					partition_format = '\t'
					v1,espaco,v2 = self.lista_geral[1].partition(partition_format)
					teste1 = int(v1)

					try:
						v2,espaco,peso = v2.partition(partition_format)
						teste2 = int(v2)
						teste3 = float(peso)

						self.grafo_com_pesos = True

					except:
						pass

				except:
					pass

			for i in self.lista_geral[1:]: #ex: i="1 2"

				v1,espaco,v2=i.partition(partition_format) #ex: v1="1", espaco=" " ou espaco="\t", v2="2"

				if self.grafo_com_pesos:
					v2,espaco,peso = v2.partition(partition_format)

				#checando se o vértice é nulo ou negativo
				if int(v1) <= 0 or int(v2) <= 0:
				#	print "Linha não considerada pois possui vértice nulo ou negativo"
					continue

				#checando se os vértices possuem identificador superior ao máximo permitido
				elif int(v1) > self.qtd_vertices or int(v2) > self.qtd_vertices:
				#	print "Linha não considerada pois referencia vértices que ultrapassam a quantidade indicada"
					continue

				else:

					#adicionando a aresta(v1,v2) na lista de arestas de v1:
					lista1=self.grafo_lista[int(v1)-1]
					valor1=int(v2)-1
					if len(lista1)>0:
						indice1=self.indice_pra_insercao_binaria(lista1,valor1,0,len(lista1)-1)
					else:
						indice1=0

					if self.grafo_com_pesos:
						lista1.insert(indice1,[valor1,float(peso)])
					else:
						lista1.insert(indice1,valor1)

					#adicionando a aresta(v1,v2) na lista de arestas de v2:
					lista2=self.grafo_lista[int(v2)-1]
					valor2=int(v1)-1
					if len(lista2)>0:
						indice2=self.indice_pra_insercao_binaria(lista2,valor2,0,len(lista2)-1)
					else:
						indice2=0
					
					if self.grafo_com_pesos:
						lista2.insert(indice2,[valor2,float(peso)])
					else:
						lista2.insert(indice2,valor2)
				
			self.list_view=True #variável que me informará que o formato lista foi criado com sucesso

			#print psutil.virtual_memory() #Usado para cálculo de consumo de memória

		else:
			self.list_view=False

	def calcular_memoria_necessaria(self):
		qtd_memoria_necessaria=self.qtd_vertices*(20+4*self.qtd_vertices) #pois no python, uma lista vazia custa 20bytes, e uma lista com N inteiros custa 20+4*N bytes.
		if qtd_memoria_necessaria>=1024**3: #valor em Gbs
			return '%s Gbs'%str(qtd_memoria_necessaria/(1024.0**3))[:6]
		elif qtd_memoria_necessaria>=1024**2: #valor em Mbs
			return '%s Mbs'%str(qtd_memoria_necessaria/(1024.0**2))[:6]
		elif qtd_memoria_necessaria>=1024: #valor em Kbs
			return '%s Kbs'%str(qtd_memoria_necessaria/(1024.0**1))[:6]
		else: #valor em Bts
			return '%s Bytes'%qtd_memoria_necessaria

	def criar_matriz_grafo_a_partir_de_entrada_txt(self,formato_matriz):
		u'''Se "formato_matriz==True", então será criada uma matriz a partir de um grafo oriundo de um arquivo txt'''
		if formato_matriz:
			pergunta='A representação matricial do grafo pedido requer um total de %s de memória. Tem certeza que deseja criar esta representação? (S/N)\n'%self.calcular_memoria_necessaria()
			resposta=''
			while resposta not in ['S','N']:
				resposta=raw_input(pergunta)
				resposta=resposta.upper()
				if resposta not in ['S','N']:
					print u'\nErro: a resposta deve ser apenas S ou N.\n\n'
			if resposta=='S':
				self.grafo_matriz=[]
				linha=[0]*self.qtd_vertices
				for i in xrange(self.qtd_vertices):
					self.grafo_matriz.append(linha[:]) #ao fazer linha[:] em vez de apenas linha, eu obrigo o python a criar matrizes iguais a linha porém sem utilizar o mesmo endereço de memória (o que seria errado)
				if self.list_view:
					for v1 in xrange(self.qtd_vertices):
						for v2 in self.grafo_lista[v1]:
							self.grafo_matriz[v1][v2]=1
				else:

					partition_format = ' '
					try:
						v1,espaco,v2 = self.lista_geral[1].partition(partition_format)
						teste = int(v1) #testa se a separação é feita por ' '
					except:
						try:
							self.lista_geral[1].partition('\t')
							partition_format = '\t'
						except:
							pass

					for i in self.lista_geral[1:]: #ex: i="1 2"
						v1,espaco,v2=i.partition(partition_format) #ex: v1="1", espaco=" ", v2="2"

						if int(v1) <= 0 or int(v2) <= 0:
							print "Linha não considerada pois possui vértice nulo ou negativo"
							continue

						#checando se os vértices possuem identificador superior ao máximo permitido
						elif int(v1) > self.qtd_vertices or int(v2) > self.qtd_vertices:
							print "Linha não considerada pois referencia vértices que ultrapassam a quantidade indicada"
							continue

						else:
							self.grafo_matriz[int(v1)-1][int(v2)-1]=1 #ex: para i="1 2", o "1" representará o índice 0 e o "2" representará o índice 1, logo, uma aresta(0,1)
							self.grafo_matriz[int(v2)-1][int(v1)-1]=1

				self.matrix_view=True #variável que me informará que o formato matriz foi criado com sucesso

				#print psutil.virtual_memory() #Usado para cálculo de consumo de memória

			else:
				self.matrix_view=False
		else:
			self.matrix_view=False

	def calcular_numero_arestas(self):
		qtd=0
		if self.list_view:
			for i in self.grafo_lista:
				qtd=qtd+len(i)
		elif self.matrix_view:
			for v1 in xrange(self.qtd_vertices):
				for v2 in xrange(v1+1,self.qtd_vertices): #desse jeito eu evito recontagem de arestas e otimizo de forma que só olharei para a parte acima da diagonal secundária
					if self.grafo_matriz[v1][v2]:
						qtd=qtd+1
		else:
			return False
		self.qtd_arestas=qtd/2
		return True

	def criar_lista_de_graus(self):
		lista_graus=[0]*self.qtd_vertices
		if self.list_view:
			for v1 in xrange(self.qtd_vertices):
				for v2 in self.grafo_lista[v1]:
					lista_graus[v1]=lista_graus[v1]+1
		elif self.matrix_view:
			for v1 in xrange(self.qtd_vertices):
				for v2 in xrange(v1+1,self.qtd_vertices): #desse jeito eu evito recontagem de arestas e otimizo de forma que só olharei para a parte acima da diagonal secundária
					if self.grafo_matriz[v1][v2]:
						lista_graus[v1]=lista_graus[v1]+1
						lista_graus[v2]=lista_graus[v2]+1
		else:
			return False
		self.lista_graus=lista_graus
		return True

	def indice_pra_insercao_binaria(self,lista_ordenada,alvo,inicio,fim):
		u'''É um método para inserção binária de elementos. Criei esse método para que, quando eu for utilizar a visualização dos grafos por listas, para cada vértice vi, seus adjacentes vj estejam ordenados, de modo a otimizar futuras operações com esta lista.'''
		if fim<=inicio:
			if self.grafo_com_pesos:
				return inicio+1 if alvo>lista_ordenada[fim][0] else inicio
			else:
				return inicio+1 if alvo>lista_ordenada[fim] else inicio

		meio=int((inicio+fim)/2)

		if self.grafo_com_pesos:
			encontrada=lista_ordenada[meio][0]
		else:
			encontrada=lista_ordenada[meio]

		if alvo>encontrada:
			return self.indice_pra_insercao_binaria(lista_ordenada,alvo,meio+1,fim)
		else:
			if alvo<encontrada:
				return self.indice_pra_insercao_binaria(lista_ordenada,alvo,inicio,meio-1)
			return meio+1

	def imprimir_propriedades(self,componentes_conexas=False):
		self.output.write('número de vértices: %s\n'%self.qtd_vertices)
		if self.calcular_numero_arestas():
			self.output.write('número de arestas: %s\n'%self.qtd_arestas)
		
		if self.criar_lista_de_graus():
			grau_min=min(self.lista_graus)
			grau_max=max(self.lista_graus)
			grau_medio=sum(self.lista_graus)/float(self.qtd_vertices)
			lista_graus_ordenadas=self.lista_graus[:]
			lista_graus_ordenadas.sort()
			if self.qtd_vertices%2: #qtd ímpar de vértices
				mediana_graus=lista_graus_ordenadas[self.qtd_vertices/2]
			else:
				mediana_graus=(lista_graus_ordenadas[self.qtd_vertices/2]+lista_graus_ordenadas[(self.qtd_vertices/2)-1])/2.0
			self.output.write('''\
grau mínimo: %s
grau máximo: %s
grau médio: %s
mediana de grau: %s\
'''%(grau_min,grau_max,grau_medio,mediana_graus))

		if componentes_conexas == True:
			cc = self.componentes_conexas()

			self.output.write('''\
\nO número de componentes conexas deste grafo é igual a: %s
A maior componente conexa tem tamanho: %s
A menor componente conexa tem tamanho: %s\
				'''%(cc[0],cc[1],cc[2]))

	def ver_vizinhos(self,indice_vertice):
		u'''Esta função retornará os vizinhos de um determinado vértice, seja o grafo uma lista ou seja ele uma matriz.'''
		if self.list_view:
			return self.grafo_lista[indice_vertice]
		elif self.matrix_view:
			return [i for i,v in enumerate(self.grafo_matriz[indice_vertice]) if v==1]
		return []

	def gerar_arvore_da_bfs(self,vertice_inicial,output=True): #BFS(busca em largura)
		u'''Algoritmo:
		1.Desmarcar todos os vértices
		2.Definir fila "descobertos" inicialmente como vazia
		3.Marcar o "indice_inicial" e inserí-lo na fila "descobertos"
		4.Enquanto "descobertos" não estiver vazia:
			5.Retirar o vértice "v_descoberto" de "descobertos"
			6.Para todo vértice vizinho "v_vizinho" de v_descoberto faça
				7.Se v_vizinho não estiver marcado
					8.marcar v_vizinho
					9.inserir v_vizinho em "descobertos"
		
		#complexidades
		passo 1: O(n)
		passos de 4 a 9: O(m), onde m=qtd de vértices.
		
		resultado: O(n+m)
		'''
		indice_inicial=vertice_inicial-1

		marcados = set()
		marcados.add(indice_inicial)

		descobertos=[indice_inicial]
		caminho=[]
		arvore_bfs=[-2]*self.qtd_vertices #-2=não foi analisado; -1=sem pai; i=index do vértice do pai
		arvore_bfs[indice_inicial]=-1
		camadas=[-1]*self.qtd_vertices #-1 significa que a camada daquele vértice ainda não foi analisada.
		camadas[indice_inicial]=0
		camada_atual=0

		indice_descobertos = 0

		while(len(descobertos) > indice_descobertos):
			v_descoberto = descobertos[indice_descobertos]
			for v_vizinho in self.ver_vizinhos(v_descoberto):
				if v_vizinho not in marcados:
					marcados.add(v_vizinho)
					descobertos.append(v_vizinho)
					arvore_bfs[v_vizinho]=v_descoberto+1
					camadas[v_vizinho]=camadas[v_descoberto]+1
			caminho.append(descobertos[indice_descobertos]+1)
			indice_descobertos += 1

		if output == True:
			texto_output='\n\nTomando o vértice "%s" como ponto de partida, o caminho percorrido pelo algoritmo da BFS foi:\n%s'%(vertice_inicial,str(caminho)[1:-1])
			texto_output+='\n\nOs pais de cada vértice são:\n%s'%(str(arvore_bfs)[1:-1])
			texto_output+='\n\nAs camadas de cada vértice são:\n%s'%(str(camadas)[1:-1])
			self.output.write(texto_output)

		return caminho, arvore_bfs, camadas

	def gerar_arvore_da_dfs(self,vertice_inicial,output=True): #DFS(busca em profundidade)
		u'''Algoritmo:
		1.Desmarcar todos os vérticecs -- O(n)
		2.Definir pilha P com um elemento s
		3.Enquanto P não estiver vazia --------- passos 3 a 8 geram uma ordem igual a O(m), onde m=qtd de vértices.
			4.Remover v_descoberto de P // no topo da pilha
			5.Se v_descoberto não estiver marcado
				6.Marcar v_descoberto como descoberto
				7.Para cada aresta (v_descoberto,v_vizinho) incidente a v_descoberto
					8.Adicionar v_vizinho em P // no topo

		resultado: O(n+m)
		'''
		indice_inicial = vertice_inicial-1

		marcados=set() 
		P=[indice_inicial]
		caminho=[]
		arvore_dfs=[-2]*self.qtd_vertices
		arvore_dfs[indice_inicial]=-1
		camadas=[-1]*self.qtd_vertices
		camadas[indice_inicial] = 0
		camada_atual = 0

		while P != []:
			
			v_descoberto = P.pop()

			if v_descoberto not in marcados:
				marcados.add(v_descoberto)
				camada_atual += 1

				for v_vizinho in self.ver_vizinhos(v_descoberto):

					if v_vizinho not in marcados:
						P.append(v_vizinho)
						arvore_dfs[v_vizinho] = v_descoberto+1
						camadas[v_vizinho] = camada_atual

				caminho.append(v_descoberto+1)

		if output == True:
			texto_output='\n\nTomando o vértice "%s" como ponto de partida, o caminho percorrido pelo algoritmo da DFS foi:\n%s'%(vertice_inicial,str(caminho)[1:-1])
			texto_output+='\n\nOs pais de cada vértice são:\n%s'%(str(arvore_dfs)[1:-1])
			texto_output+='\n\nAs camadas de cada vértice são:\n%s'%(str(camadas)[1:-1])
			self.output.write(texto_output)

		return caminho, arvore_dfs, camadas

	def pai(self,vertice_inicial,vertice_desejado,modelo_arvore="BFS"):

		if modelo_arvore == "BFS":
			pais = self.gerar_arvore_da_bfs(vertice_inicial)[1]
			return pais[vertice_desejado-1]

		elif modelo_arvore == "DFS":
			pais = self.gerar_arvore_da_dfs(vertice_inicial)[1]
			return pais[vertice_desejado-1]

		else:
			print "Escolha uma árvore de busca válida"

	def nivel(self,vertice_inicial,vertice_desejado,modelo_arvore="BFS"):

		if modelo_arvore == "BFS":
			niveis = self.gerar_arvore_da_bfs(vertice_inicial)[2]
			return niveis[vertice_desejado-1]

		elif modelo_arvore == "DFS":
			niveis = self.gerar_arvore_da_dfs(vertice_inicial)[2]
			return niveis[vertice_desejado-1]

		else:
			print "Escolha uma árvore de busca válida"

	def componentes_conexas(self):
		vertices_conexos = set()
		num_cc=0
		lista_cc=[]
		lista_tamanhos_cc=[]
		tamanho_maior_cc=0
		tamanho_menor_cc=self.qtd_vertices

		#Examina cada vértice do grafo
		for i in xrange(self.qtd_vertices):
			vizinhos=self.ver_vizinhos(i-1)
			#Examina se o grau do vértice é maior que 0
			if len(vizinhos):
				#Examina cada vizinho do vértice escolhido
				for indice in vizinhos:
					vertice=indice+1
					#Caso o vizinho não seja parte de nenhuma componente conexa, é feita uma dfs partindo dele
					if vertice not in vertices_conexos:
						cc=self.gerar_arvore_da_dfs(vertice,output=False)[0]
						#Determina a posição da componente conexa criada na lista de componentes conexas, em ordem decrescente por número de vértices
						if len(lista_tamanhos_cc):
							indice_ordenacao=self.indice_pra_insercao_binaria(lista_tamanhos_cc,len(cc),0,len(lista_tamanhos_cc)-1)
						else:
							indice_ordenacao=0
						#Insere a componente conexa na lista de componentes conexas 
						lista_cc.insert(len(lista_tamanhos_cc)-indice_ordenacao,cc)
						lista_tamanhos_cc.insert(indice_ordenacao,len(cc))
						num_cc+=1

						#Adiciona cada vértice da componente em um set que contém todos os vértices que são parte de alguma componente
						for elemento in cc:
							vertices_conexos.add(elemento)
			#Caso o vértice tenha grau 0, ele é adicionado à lista de componentes conexas sem que seja realizada uma dfs
			else:	
				tamanho_menor_cc=1
				num_cc+=1
				vertices_conexos.add(i)
				lista_cc.append([i])
		
		#Examina o tamanho de cada elemento na lista de componentes conexas, caso esta não seja vazia, e determina o maior e menor valor
		if lista_cc != []:
			for cc in lista_cc:

				if len(cc) > tamanho_maior_cc:
					tamanho_maior_cc = len(cc)

				if tamanho_menor_cc != 1:
					if len(cc) < tamanho_menor_cc:
						tamanho_menor_cc = len(cc)

		else:
			print "Favor implementar o grafo em algum formato (matriz ou lista) antes de calcular as componentes conexas"
			return

		return num_cc, tamanho_maior_cc, tamanho_menor_cc, lista_cc

	def diametro(self):

		diametro = 0

		#Checa se existe algum par de vértices que não esteja conectado; caso exista, o diâmetro é infinito
		if self.componentes_conexas()[0] != 1:
			print "O diâmetro é infinito"
			return

		else:

			#Faz uma bfs para cada vértice do grafo
			for i in xrange(self.qtd_vertices):
				temp_camadas = self.gerar_arvore_da_bfs(i+1,output=False)[2]

				#Checa o valor da maior camada, e o atribui como maior menor distância do vértice
				maior_distancia = max(temp_camadas)

				#Se a maior menor distâcia deste vértice for maior que o diâmtro, este recebe o novo valor
				if maior_distancia > diametro:
					diametro = maior_distancia

		return diametro

	def dijkstra(self, vertice_inicial):

		for i in xrange(self.qtd_vertices):
			for peso in self.ver_vizinhos(i):
				if peso[1] < 0:
					print "Djikstra não pode ser realizado, pois o grafo possui pesos negativos"
					return

		indice_inicial = vertice_inicial-1

		dist = BHeap()
		dist.buildHeap(self.qtd_vertices)

		for vertice in xrange(self.qtd_vertices):
			dist.add([float('inf'),vertice])

		dist.add([0,indice_inicial])

		S = [float('inf')]*self.qtd_vertices #Lista de distâncias de cada vértice até o vértice inicial
		S[indice_inicial] = 0
		caminho = [[] for i in range(self.qtd_vertices)] #Lista de caminhos de cada vértice até o vértice inicial
		caminho[indice_inicial].append(indice_inicial)

		distancias = [float('inf')]*self.qtd_vertices
		distancias[indice_inicial] = 0

		explorados = set()

		while len(dist) > 0:

			u = dist.remove()

			if u[1] not in explorados:
				explorados.add(u[1])

				for v_vizinho in self.ver_vizinhos(u[1]):

					if distancias[v_vizinho[0]] > u[0] + v_vizinho[1]:
						distancias[v_vizinho[0]] = u[0] + v_vizinho[1]

						dist.add([distancias[v_vizinho[0]], v_vizinho[0]])
						S[v_vizinho[0]] = u[0] + v_vizinho[1]
						caminho[v_vizinho[0]] = caminho[u[1]] + [v_vizinho[0]]

		return S, caminho

	def dijkstra_caminho_minimo(self, vertice_inicial, vertice_desejado):

		caminhos = self.dijkstra(vertice_inicial)[1]
		return caminhos[vertice_desejado-1]

	def dijkstra_distancia(self, vertice_inicial, vertice_desejado):

		distancias = self.dijkstra(vertice_inicial)[0]
		return distancias[vertice_desejado-1]

	def prim(self, vertice_inicial):

		indice_inicial = vertice_inicial-1

		custo = BHeap()
		custo.buildHeap(self.qtd_vertices)

		for vertice in xrange(self.qtd_vertices):
			custo.add([float('inf'),vertice])

		custo.add([0,indice_inicial])

		caminho = [] #Caminho percorrido pela MST
		arvore_prim = [float('inf')]*self.qtd_vertices
		peso = 0

		distancias = [float('inf')]*self.qtd_vertices
		distancias[indice_inicial] = 0

		arvore_prim[indice_inicial] = -1

		explorados = set()

		while len(custo) > 0:

			u = custo.remove()

			if u[0] == float('inf'):
				break

			if u[1] not in explorados:
				explorados.add(u[1])
				caminho.append(u[1]+1)
				peso += u[0]

				for v_vizinho in self.ver_vizinhos(u[1]):

					if v_vizinho[0] not in explorados:

						if distancias[v_vizinho[0]] > v_vizinho[1]:
							distancias[v_vizinho[0]] = v_vizinho[1]
							custo.add([distancias[v_vizinho[0]], v_vizinho[0]])

							if u[0] < arvore_prim[v_vizinho[0]]:
								arvore_prim[v_vizinho[0]] = u[1]+1

		return peso, caminho, arvore_prim

	def excentricidade(self, vertice):

		excentricidades = self.dijkstra(vertice)[0]
		return max(excentricidades)

	def distancia_media(self):

		pares = 0
		distancia = 0

		for i in xrange(self.qtd_vertices):
			distancias_temp = self.dijkstra(i)[0]

			for i in distancias_temp:
				if i != float('inf'):
					distancia += i
					pares += 1

		if pares > 0:
			distancia = distancia / pares
			return distancia

		else:
			return "Nenhum par encontrado; verifique se o grafo foi introduzido corretamente."

	def maiores_graus_prim(self, vertice):

		arvore_prim = self.prim(vertice)[2]
		lista_graus = [1]*self.qtd_vertices
		lista_graus[vertice-1] = 0
		maiores_graus = []

		for i in xrange(len(arvore_prim)):

			if arvore_prim[i] != float('inf') and arvore_prim[i] > -1:

				lista_graus[arvore_prim[i]-1] += 1

		for i in xrange(3):
			indice = lista_graus.index(max(lista_graus))
			maiores_graus.append([indice+1,lista_graus[indice]])
			lista_graus[indice] = 0

		return maiores_graus

if __name__ == "__main__":

	########## Trabalho 1 ########## 

	#print psutil.virtual_memory()
	#start = time.time()
	#grafo=Grafo(entrada_txt='teste.txt',formato_lista=True,formato_matriz=False)
	#grafo=Grafo(entrada_txt='as_graph.txt',formato_lista=True,formato_matriz=False)
	#grafo=Grafo(entrada_txt='dblp.txt',formato_lista=True,formato_matriz=False)
	#grafo=Grafo(entrada_txt='live_journal.txt',formato_lista=True,formato_matriz=False)
	#end = time.time()
	#print(end-start)

	#start = time.time()
	#grafo.imprimir_propriedades()
	#end = time.time()
	#print(end-start)

	#start = time.time()
	#print grafo.componentes_conexas()[2]
	#end = time.time()
	#print(end-start)

	#start = time.time()
	#print grafo.diametro()
	#end = time.time()
	#print(end-start)

	#start = time.time()
	#grafo.gerar_arvore_da_dfs(1)
	#end = time.time()
	#print(end-start)

	########## Trabalho 2 ##########

	grafo = Grafo(entrada_txt='teste.txt', formato_lista = True, formato_matriz = False)

	start = time.time()
	print grafo.maiores_graus_prim(1)
	end = time.time()
	print(end-start)