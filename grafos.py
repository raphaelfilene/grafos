# -*- coding: utf-8 -*-
#Esta biblioteca foi feita para a versão 2.7 do Python, não sendo compatível com as versões 3.x do mesmo.

class Grafo:
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
				self.criar_lista_grafo_a_partir_de_entrada_txt(formato_lista)
				self.criar_matriz_grafo_a_partir_de_entrada_txt(formato_matriz)
			except Exception,e:
				print u'Houve algum erro na criação do grafo oriundo do arquivo txt indicado. Veja:\n\n'
				print e
	
	def criar_lista_grafo_a_partir_de_entrada_txt(self,formato_lista):
		u'''Se "formato_lista==True", então será criada uma lista a partir de um grafo oriundo de um arquivo txt'''
		if formato_lista:
			self.grafo_lista=[[] for i in xrange(self.qtd_vertices)]
			for i in self.lista_geral[1:]: #ex: i="1 2"
				v1,espaco,v2=i.partition(' ') #ex: v1="1", espaco=" ", v2="2"
				
				#adicionando a aresta(v1,v2) na lista de arestas de v1:
				lista1=self.grafo_lista[int(v1)-1]
				valor1=int(v2)-1
				if len(lista1)>0:
					indice1=self.indice_pra_insercao_binaria(lista1,valor1,0,len(lista1)-1)
				else:
					indice1=0
				lista1.insert(indice1,valor1)

				#adicionando a aresta(v1,v2) na lista de arestas de v2:
				lista2=self.grafo_lista[int(v2)-1]
				valor2=int(v1)-1
				if len(lista2)>0:
					indice2=self.indice_pra_insercao_binaria(lista2,valor2,0,len(lista2)-1)
				else:
					indice2=0
				lista2.insert(indice2,valor2)
				
			self.list_view=True #variável que me informará que o formato lista foi criado com sucesso
		else:
			self.list_view=False

	def criar_matriz_grafo_a_partir_de_entrada_txt(self,formato_matriz):
		u'''Se "formato_matriz==True", então será criada uma matriz a partir de um grafo oriundo de um arquivo txt'''
		if formato_matriz:
			qtd_memoria_necessaria=(20+4*self.qtd_vertices)*(20+4*self.qtd_vertices) #pois no python, uma lista vazia custa 20bytes, e uma lista com N inteiros custa 20+4*N bytes.
			pergunta='A representação matricial do grafo pedido requer um total de %s Gbs de memória. Tem certeza que deseja criar esta representação? (S/N)\n'%str(qtd_memoria_necessaria/(1024.0**3))[:6]
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
					self.grafo_matriz.append(linha[:]) #ao fazer linha[:] em vez de apenas linha, eu obrigo o python a criar matrizes iguais a linha porém sem copiar utilizar o mesmo endereço de memória (o que seria errado)
				if self.list_view:
					for v1 in xrange(self.qtd_vertices):
						for v2 in self.grafo_lista[v1]:
							self.grafo_matriz[v1][v2]=1
				else:
					for i in self.lista_geral[1:]: #ex: i="1 2"
						v1,espaco,v2=i.partition(' ') #ex: v1="1", espaco=" ", v2="2"
						self.grafo_matriz[int(v1)-1][int(v2)-1]=1 #ex: para i="1 2", o "1" representará o índice 0 e o "2" representará o índice 1, logo, uma aresta(0,1)
						self.grafo_matriz[int(v2)-1][int(v1)-1]=1
				self.matrix_view=True #variável que me informará que o formato matriz foi criado com sucesso
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
		self.qtd_arestas=qtd
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
			return fim+1 if alvo>lista_ordenada[fim] else fim
		meio=int((inicio+fim)/2)
		encontrada=lista_ordenada[meio]
		if alvo>encontrada:
			return self.indice_pra_insercao_binaria(lista_ordenada,alvo,meio+1,fim)
		else:
			if alvo<encontrada:
				return self.indice_pra_insercao_binaria(lista_ordenada,alvo,inicio,meio-1)
			return meio+1

	def imprimir_propriedades(self):
		nome_arquivo='propriedades.txt'
		open(nome_arquivo,'wb') #abrindo no formato 'write byte' apenas pra criar um arquivo em branco com tal nome (ou apagar os dados de algum com o mesmo nome)
		arquivo_propriedades=open(nome_arquivo,'ab') #abrindo no formato 'append byte'
		arquivo_propriedades.write('número de vértices: %s\n'%self.qtd_vertices)
		if self.calcular_numero_arestas():
			arquivo_propriedades.write('número de arestas: %s\n'%self.qtd_arestas)
		
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
			arquivo_propriedades.write('''\
grau mínimo: %s
grau máximo: %s
grau médio: %s
mediana de grau: %s\
'''%(grau_min,grau_max,grau_medio,mediana_graus))

	def gerar_arvore_da_bfs(self,vertice_inicial): #BFS(busca em largura)
		u'''Algoritmo:
		1.Desmarcar todos os vértices -- O(n)
		2.Definir fila Q vazia
		3.Marcar s e inserir s na fila Q
		4.Enquanto Q não estiver vazia --------- passos de 4 a 9 geram uma ordem igual a O(m), onde m=qtd de vértices.
			5.Retirar v de Q
			6.Para todo vizinho w de v faça
				7.Se w não estiver marcado
					8.marcar w
					9.inserir w em Q

		resultado: O(n+m)
		'''
		indice_inicial=vertice_inicial-1

		desmarcados=[1]*self.qtd_vertices #1=desmarcado 0=marcado
		desmarcados[indice_inicial]=0
		Q=[indice_inicial]
		caminho=[]
		while len(Q)!=0:
			for v in Q[:]:
				for w in self.grafo_lista[v]:
					if desmarcados[w]:
						desmarcados[w]=0
						Q.append(w)
			caminho.append(Q[0]+1)
			del Q[0]
		print caminho
		#if self.qtd_vertices>=indice_inicial>=0:
		#	self.busca_em_largura(indice_vertice)
		#else:
		#	print u'Digite um vértice válido!'


grafo=Grafo(entrada_txt='teste.txt',formato_lista=True,formato_matriz=True)
#grafo=Grafo(entrada_txt='as_graph.txt',formato_lista=True,formato_matriz=False)
grafo.imprimir_propriedades()
grafo.gerar_arvore_da_bfs(1)