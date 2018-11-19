# -*- coding: utf-8 -*-
#Esta biblioteca foi feita para a versão 2.7 do Python, não sendo compatível com as versões 3.x do mesmo.

import time
import psutil
from heap import *
from math import sqrt

class Grafo:
	nome_output='output.txt'
	def __init__(self,entrada_txt=False,formato_lista=False,formato_matriz=False,diretorio_grafo_distancias=None,qtd_vertices_pra_analisar=None):
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
		if diretorio_grafo_distancias:
			assert(isinstance(qtd_vertices_pra_analisar,int))
			self.qtd_vertices_pra_analisar=qtd_vertices_pra_analisar
			lista=[]
			with open(diretorio_grafo_distancias) as f:
				for linha in f:
					lista.append(linha[:-1].split(' '))
			self.qtd_vertices=int(lista[0][0])
			lista=[[int(i[0]),int(i[1])] for i in lista[1:]]
			dist=lambda xo,yo,x,y:sqrt(((x-xo)**2)+((y-yo)**2))
			self.grafo_matriz=[]
			for xo,yo in lista:
				vertice=[]
				for x,y in lista:
					vertice.append(dist(xo,yo,x,y))
				self.grafo_matriz.append(vertice)
			self.matrix_view=True
			self.list_view=False
			self.grafo_com_pesos=True
			self.coordenadas=lista

		else:
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
			#pergunta='A representação matricial do grafo pedido requer um total de %s de memória. Tem certeza que deseja criar esta representação? (S/N)\n'%self.calcular_memoria_necessaria()
			#resposta=''
			#while resposta not in ['S','N']:
			#	resposta=raw_input(pergunta)
			#	resposta=resposta.upper()
			#	if resposta not in ['S','N']:
			#		print u'\nErro: a resposta deve ser apenas S ou N.\n\n'
			resposta = 'S'
			if resposta=='S':
				self.grafo_matriz=[]
				linha=[0]*self.qtd_vertices
				for i in xrange(self.qtd_vertices):
					self.grafo_matriz.append(linha[:]) #ao fazer linha[:] em vez de apenas linha, eu obrigo o python a criar matrizes iguais a linha porém sem utilizar o mesmo endereço de memória (o que seria errado)
				#if self.list_view:
				#	for v1 in xrange(self.qtd_vertices):
				#		for v2 in self.grafo_lista[v1]:
				#			self.grafo_matriz[v1][v2]=1
				if False:
					pass

				else:

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
						v1,espaco,v2=i.partition(partition_format) #ex: v1="1", espaco=" ", v2="2"

						if self.grafo_com_pesos:
							v2,espaco,peso = v2.partition(partition_format)

						if int(v1) <= 0 or int(v2) <= 0:
							print "Linha não considerada pois possui vértice nulo ou negativo"
							continue

						#checando se os vértices possuem identificador superior ao máximo permitido
						elif int(v1) > self.qtd_vertices or int(v2) > self.qtd_vertices:
							print "Linha não considerada pois referencia vértices que ultrapassam a quantidade indicada"
							continue

						else:

							valor = 1
							if self.grafo_com_pesos:
								valor = float(peso)

							self.grafo_matriz[int(v1)-1][int(v2)-1]=valor #ex: para i="1 2", o "1" representará o índice 0 e o "2" representará o índice 1, logo, uma aresta(0,1)
							self.grafo_matriz[int(v2)-1][int(v1)-1]=valor

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
			if self.grafo_com_pesos:
				return [[i,v] for i,v in enumerate(self.grafo_matriz[indice_vertice]) if v!=0]
			else:
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

				if self.grafo_com_pesos:
					v_vizinho = v_vizinho[0]

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

					if self.grafo_com_pesos:
						v_vizinho = v_vizinho[0]

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

					if self.grafo_com_pesos:
						indice = indice[0]

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

		# Criação e inicialização do heap que será utilizado
		dist = BHeap()
		dist.buildHeap()

		#Preenche o heap com peso infinito para cada vértice do grafo; elementos do heap tem formato [peso,vertice]
		for vertice in xrange(self.qtd_vertices):
			dist.add([float('inf'),vertice])

		#Adiciona o indice inicial com peso 0 ao heap
		dist.add([0,indice_inicial])

		S = [float('inf')]*self.qtd_vertices #Lista de distâncias de cada vértice até o vértice inicial
		S[indice_inicial] = 0 #Distância do vértice até ele próprio definida como 0
		caminho = [[] for i in range(self.qtd_vertices)] #Lista de caminhos de cada vértice até o vértice inicial
		caminho[indice_inicial].append(indice_inicial+1) #Vértice inicial adicionado como primeiro elemento do caminho percorrido

		explorados = set() #Set que contém todos os vértices já explorados

		while len(dist) > 0:

			u = dist.remove() #Remove elemento de menor peso do heap

			#Checa se o elemento já foi explorado; caso não tenha sido, adiciona-se ele ao set explorados
			if u[1] not in explorados:
				explorados.add(u[1])

				#Para cada vizinho não explorado de u
				for v_vizinho in self.ver_vizinhos(u[1]):
					if v_vizinho[0] not in explorados:

						#Verifica se o peso atual do vizinho é maior que a soma do peso para chegar até o vértice u e ir deste até o vizinho;
						#em caso positivo, atualiza-se o peso atual do vizinho, adiciona-se o valor atualizado de sua distância ao heap
						#e seu caminho até o vértice inicial é atualizado com o caminho ao vértice u adicionado do vizinho
						if S[v_vizinho[0]] > u[0] + v_vizinho[1]:
							S[v_vizinho[0]] = u[0] + v_vizinho[1]
							dist.add([S[v_vizinho[0]], v_vizinho[0]])
							caminho[v_vizinho[0]] = caminho[u[1]] + [v_vizinho[0]+1]

		return S, caminho

	def dijkstra_caminho_minimo_distancia(self, vertice_inicial, vertice_desejado):

		valores = self.dijkstra(vertice_inicial)
		return valores[1][vertice_desejado-1], valores[0][vertice_desejado-1]

	def prim(self, vertice_inicial):

		indice_inicial = vertice_inicial-1

		# Criação e inicialização do heap que será utilizado
		custo = BHeap()
		custo.buildHeap()

		#Preenche o heap com custo infinito para cada vértice do grafo; elementos do heap tem formato [custo,vertice]
		for vertice in xrange(self.qtd_vertices):
			custo.add([float('inf'),vertice])

		#Adiciona o indice inicial com custo 0 ao heap
		custo.add([0,indice_inicial])

		caminho = [] #Caminho percorrido pela MST
		arvore_prim = [float('inf')]*self.qtd_vertices #Lista contendo o pai de cada vértice na MST
		peso = 0 #Peso total da MST

		distancias = [float('inf')]*self.qtd_vertices #Lista contendo as menores distâncias necessárias para chegar a cada vértice
		distancias[indice_inicial] = 0

		arvore_prim[indice_inicial] = -1
		explorados = set() #Set que contém todos os vértices já explorados

		while len(custo) > 0:
			u = custo.remove() #Remove do heap o elemento de menor custo

			#Caso o custo seja infinito, todos os elementos restando no heap possuem custo infinito; logo, quebra-se o loop
			if u[0] == float('inf'):
				break

			#Caso u não tenha sido explorado, adiciona-se ele aos explorados, ao caminho percorrido pela MST e seu peso ao peso total
			if u[1] not in explorados:
				explorados.add(u[1])
				caminho.append(u[1]+1)
				peso += u[0]

				for v_vizinho in self.ver_vizinhos(u[1]):
					if v_vizinho[0] not in explorados:

						#Verifica se a distância atual para chegar ao vértice é maior que a distância para chegar a este vértice partindo de u;
						#caso ela seja, sua distância é atualizada em distancias e no heap
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

		pares = 0 #Número de pares válidos
		distancia = 0 #Distância total

		#Para cada vértice no grafo, faz-se Dijkstra e retorna-se a lista contendo a distância do vértice a todos os outros
		for i in xrange(self.qtd_vertices):
			distancias_temp = self.dijkstra(i)[0]

			#Para as distâncias recebidas, caso ela não seja infinita ela é somada a distância total e o número de pares válidos incrementado por 1
			for i in distancias_temp:
				if i != float('inf'):
					distancia += i
					pares += 1

		if pares > 0:
			#Divide a distância total pelo número de pares para se obter a distância média
			distancia = distancia / pares
			return distancia

		else:
			print "Nenhum par encontrado; verifique se o grafo foi introduzido corretamente."
			return

	def maiores_graus_prim(self, vertice):

		arvore_prim = self.prim(vertice)[2] #Lista de pais de cada vértice da MST obtida por Prim
		lista_graus = [1]*self.qtd_vertices #Lista contendo o grau de cada vértice da MST; todos começam com grau 1 pois a função assume que todo vértice exceto a raiz da MST possui um pai
		lista_graus[vertice-1] = 0 #Reduz-se o grau da raiz por 1, dado que ela não possui pai na MST
		maiores_graus = [] #Lista contendo os maiores graus e seus respectivos vértices encontrados, no formato [vértice, grau]

		for i in xrange(len(arvore_prim)):

			#Cada vez que um vértice é considerado como pai na lista de vértices, soma-se 1 à seu grau total
			if arvore_prim[i] != float('inf') and arvore_prim[i] > -1:
				lista_graus[arvore_prim[i]-1] += 1

		#Encontra-se o vértice de maior grau da lista, que é então adicioná-lo a lista maiores_graus; seu valor em lista_graus é atualizado para 0
		#O processo se repete 3 vezes, coletando assim os 3 maiores graus
		for i in xrange(3):
			indice = lista_graus.index(max(lista_graus))
			maiores_graus.append([indice+1,lista_graus[indice]])
			lista_graus[indice] = 0

		return maiores_graus

	def comprimento_caminho(self,caminho):
		comprimento=0
		for i in xrange(1,len(caminho)):
			comprimento+=self.grafo_matriz[caminho[i-1]][caminho[i]]
		return comprimento

	def vizinho_mais_proximo(self,vertice,vizinhos):
		distancia=float('inf')
		vizinho=None
		for v in vizinhos:
			if self.grafo_matriz[vertice][v]<distancia:
				distancia=self.grafo_matriz[vertice][v]
				vizinho=v
		return vizinho,distancia

	def menor_caminho(self,vertices):
		melhor_caminho=[]
		comprimento_melhor_caminho=float('inf')
		for i,v in enumerate(vertices):
			caminho=[v]
			comprimento=0
			resto=vertices[:]
			del resto[i]
			while len(resto):
				novo_vizinho,distancia=self.vizinho_mais_proximo(caminho[-1],resto)
				caminho.append(novo_vizinho)
				comprimento+=distancia
				resto.remove(novo_vizinho)
			if comprimento<comprimento_melhor_caminho:
				melhor_caminho=caminho
				comprimento_melhor_caminho=comprimento
		return melhor_caminho,comprimento_melhor_caminho

	def caixeiro_viajante(self,vertices=None):
		u'''
		Separo o conjunto de pontos em 4 regiões: Nordeste(NO), Noroeste(NE), Sudeste(SE) e Sudoeste(SO).
		Se alguma dessas regiões possuir uma quantidade de vértices menor ou igual a self.qtd_vertices_pra_analisar, então eu calculo o menor caminho dentro dessa região utilizando a força bruta. Caso contrário eu pego essa região e uso recurssão para separá-la em novas 4 partes (NO, NE, SE e SO) e vou fazendo assim até ter o caminho de todas as regiões.
		Considero ciclos horários e anti-horários como sendo "... > NO > NE > SE > SO > NO > ..." e " ... > NE > NO > SO > SE > NE > ... ".
		Sendo assim, para cada uma das quatro regiões eu tento criar caminhos utilizando vértices que vão percorrer toda a sua região e em seguida migrar para o clico seguinte utilizando uma das duas direções (horária ou anti-horária). No final, com os 8 caminhos que eu encontrar, verifico o mais curto e 
		'''
		if vertices==None:
			vertices=range(self.qtd_vertices)
		coordenadas=[self.coordenadas[i] for i in vertices]

		intervalo_x=[coordenadas[0][0],coordenadas[0][0]]
		intervalo_y=[coordenadas[0][1],coordenadas[0][1]]
		for x,y in coordenadas:
			if x<intervalo_x[0]:
				intervalo_x[0]=x
			elif x>intervalo_x[1]:
				intervalo_x[1]=x
			
			if y<intervalo_y[0]:
				intervalo_y[0]=y
			elif y>intervalo_y[1]:
				intervalo_y[1]=y
		x_centro=sum(intervalo_x)/2
		y_centro=sum(intervalo_y)/2

		#dividindo em regiões 0=Noroeste, 1=Nordeste, 2=Sudeste, 3=Sudoeste
		regioes=[]
		vertices_por_regioes=[[],[],[],[]]
		for i,v in enumerate(coordenadas):
			if v[0]>x_centro: #leste
				if v[1]>y_centro: #norte
					r=1
				else: #sul
					r=2
			else: #oeste
				if v[1]>y_centro: #norte
					r=0
				else: #sul
					r=3
			regioes.append(r)
			vertices_por_regioes[r].append(vertices[i])

		caminhos=[]
		comprimentos=[]
		for regiao in vertices_por_regioes:
			if len(regiao)<=self.qtd_vertices_pra_analisar:
				caminho,comprimento=self.menor_caminho(regiao)
			else:
				caminho,comprimento=self.caixeiro_viajante(regiao)
			caminhos.append(caminho)
			comprimentos.append(comprimento)

		lista_caminhos=[]
		lista_comprimentos=[]
		for sentido in [1,-1]:
			for regiao in xrange(4):
				if len(caminhos[regiao]):
					caminho=list(caminhos[regiao])
					comprimento=comprimentos[regiao]
					for i in xrange(1,4):
						proxima_regiao=(regiao+i*sentido)%4
						if len(caminhos[proxima_regiao]):
							comprimento+=comprimentos[proxima_regiao]+self.grafo_matriz[caminho[-1]][caminhos[proxima_regiao][0]]
							caminho.extend(caminhos[proxima_regiao])
					lista_caminhos.append(caminho)
					lista_comprimentos.append(comprimento)
		menor_comprimento=min(lista_comprimentos)
		melhor_caminho=lista_caminhos[lista_comprimentos.index(menor_comprimento)]
		return melhor_caminho,menor_comprimento

	def caixeiro_viajante_com_volta(self):
		caminho,comprimento=self.caixeiro_viajante()
		comprimento+=self.grafo_matriz[caminho[0]][caminho[-1]]
		caminho=[i+1 for i in caminho]
		return caminho,comprimento


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

	#grafo = Grafo(entrada_txt='teste2.txt', formato_lista = True, formato_matriz = False)
	#grafo.gerar_arvore_da_bfs(2,output=False)
	#print ""
	#grafo2 = Grafo(entrada_txt='teste.txt', formato_lista = False, formato_matriz = True)
	#print grafo2.prim(2)
	#print grafo.distancia_media()

	######### Trabalho 3 ###########
	texto=''
	for i in [5,10,20,50,100,200,500,1000,2000,5000,7500,10000]:
		arquivo='points-%s.txt'%i
		grafo=Grafo(diretorio_grafo_distancias=arquivo,qtd_vertices_pra_analisar=10)
		t0=time.time()
		caminho,comprimento=grafo.caixeiro_viajante_com_volta()
		dt=time.time()-t0
		texto+='''
arquivo: %s
caminho: %s
comprimento: %s
tempo: %.6f segundos
		'''%(arquivo,str(caminho)[1:-1],comprimento,dt)
		open('resultado caixeiro viajante.txt','wb').write(texto)
		print arquivo
