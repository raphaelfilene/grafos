# -*- coding: utf-8 -*-

import time
import psutil
from grafos import *

print "Escolha o Estudo de Caso para ser testado:"
caso = input("Escolha o Estudo de Caso para ser executado (inteiro de 1 a 7):")

if caso in [4,5,6,7]:

	grafo1=Grafo(entrada_txt='as_graph.txt',formato_lista=True,formato_matriz=False)
	grafo2=Grafo(entrada_txt='dblp.txt',formato_lista=True,formato_matriz=False)
	grafo3=Grafo(entrada_txt='live_journal.txt',formato_lista=True,formato_matriz=False)

elif caso in [2,3]:

	confirmacao = raw_input("Esta operação consumirá mais de 15GB de memória e demorará mais de 24 horas para concluir. Tem certeza que deseja continuar? (s/n) ")

	if confirmacao == "s":
		grafo1v=Grafo(entrada_txt='as_graph.txt',formato_lista=True,formato_matriz=False)
		grafo1m=Grafo(entrada_txt='as_graph.txt',formato_lista=False,formato_matriz=True)
		grafo2=Grafo(entrada_txt='dblp.txt',formato_lista=True,formato_matriz=False)
		grafo3=Grafo(entrada_txt='live_journal.txt',formato_lista=True,formato_matriz=False)

	else:
		caso = 0

elif caso == 1:
	pass

else:
	print "Insira um Estudo de Caso válido"
	caso = 0

##Estudo de Caso 1 - Memória

if caso == 1:

	print "\nConsumo de memória do Grafo 1 - Vetor: Comparar os valores de 'used' antes e depois de criar o grafo"
	print psutil.virtual_memory()
	grafo1v=Grafo(entrada_txt='as_graph.txt',formato_lista=True,formato_matriz=False)
	print psutil.virtual_memory()

	print "\nConsumo de memória do Grafo 1 - Matriz: Comparar os valores de 'used' antes e depois de criar o grafo"
	print psutil.virtual_memory()
	grafo1m=Grafo(entrada_txt='as_graph.txt',formato_lista=False,formato_matriz=True)
	print psutil.virtual_memory()

	print "\nConsumo de memória do Grafo 2 - Vetor: Comparar os valores de 'used' antes e depois de criar o grafo"
	print psutil.virtual_memory()
	grafo2=Grafo(entrada_txt='dblp.txt',formato_lista=True,formato_matriz=False)
	print psutil.virtual_memory()

	print "\nConsumo de memória do Grafo 3 - Vetor: Comparar os valores de 'used' antes e depois de criar o grafo"
	print psutil.virtual_memory()
	grafo3=Grafo(entrada_txt='live_journal.txt',formato_lista=True,formato_matriz=False)
	print psutil.virtual_memory()

##Estudo de Caso 2 - Tempo de Execução (BFS)

elif caso == 2:

	lista_tempos = []

	for i in range(10):

		start = time.time()
		grafo1v.gerar_arvore_da_bfs(i)
		end = time.time()
		tempo = end-start

		lista_tempos.append(tempo)

	tempo_medio = sum(lista_tempos)/10.0
	print "Tempo médio do grafo 1 com vetor:", tempo_medio

	lista_tempos = []

	for i in range(1000):

		start = time.time()
		grafo1m.gerar_arvore_da_bfs(i)
		end = time.time()
		tempo = end-start

		lista_tempos.append(tempo)

	tempo_medio = sum(lista_tempos)/1000.0
	print "Tempo médio do grafo 1 com matriz:", tempo_medio

	lista_tempos = []

	for i in range(1000):

		start = time.time()
		grafo2.gerar_arvore_da_bfs(i)
		end = time.time()
		tempo = end-start

		lista_tempos.append(tempo)

	tempo_medio = sum(lista_tempos)/1000.0
	print "Tempo médio do grafo 2 com vetor:", tempo_medio

	lista_tempos = []

	for i in range(1000):

		start = time.time()
		grafo3.gerar_arvore_da_bfs(i)
		end = time.time()
		tempo = end-start

		lista_tempos.append(tempo)

	tempo_medio = sum(lista_tempos)/1000.0
	print "Tempo médio do grafo 3 com vetor:", tempo_medio

##Estudo de Caso 3 - Tempo de Execução (DFS)

elif caso == 3:

	lista_tempos = []

	for i in range(1000):

		start = time.time()
		grafo1v.gerar_arvore_da_dfs(i)
		end = time.time()
		tempo = end-start

		lista_tempos.append(tempo)

	tempo_medio = sum(lista_tempos)/1000.0
	print "Tempo médio do grafo 1 com vetor:", tempo_medio

	lista_tempos = []

	for i in range(1000):

		start = time.time()
		grafo1m.gerar_arvore_da_dfs(i)
		end = time.time()
		tempo = end-start

		lista_tempos.append(tempo)

	tempo_medio = sum(lista_tempos)/1000.0
	print "Tempo médio do grafo 1 com matriz:", tempo_medio

	lista_tempos = []

	for i in range(1000):

		start = time.time()
		grafo2.gerar_arvore_da_dfs(i)
		end = time.time()
		tempo = end-start

		lista_tempos.append(tempo)

	tempo_medio = sum(lista_tempos)/1000.0
	print "Tempo médio do grafo 2 com vetor:", tempo_medio

	lista_tempos = []

	for i in range(1000):

		start = time.time()
		grafo3.gerar_arvore_da_dfs(i)
		end = time.time()
		tempo = end-start

		lista_tempos.append(tempo)

	tempo_medio = sum(lista_tempos)/1000.0
	print "Tempo médio do grafo 3 com vetor:", tempo_medio

##Estudo de Caso 4 - Pais

elif caso == 4:

	print "\nBFS - Grafo 1"

	print grafo1.pai(1,10)
	print grafo1.pai(2,20)
	print grafo1.pai(3,30)
	print grafo1.pai(4,40)
	print grafo1.pai(5,50)

	print "\nDFS - Grafo 1"

	print grafo1.pai(1,10,modelo_arvore="DFS")
	print grafo1.pai(2,20,modelo_arvore="DFS")
	print grafo1.pai(3,30,modelo_arvore="DFS")
	print grafo1.pai(4,40,modelo_arvore="DFS")
	print grafo1.pai(5,50,modelo_arvore="DFS")

	print "\nBFS - Grafo 2"

	print grafo2.pai(1,10)
	print grafo2.pai(2,20)
	print grafo2.pai(3,30)
	print grafo2.pai(4,40)
	print grafo2.pai(5,50)

	print "\nDFS - Grafo 2"

	print grafo2.pai(1,10,modelo_arvore="DFS")
	print grafo2.pai(2,20,modelo_arvore="DFS")
	print grafo2.pai(3,30,modelo_arvore="DFS")
	print grafo2.pai(4,40,modelo_arvore="DFS")
	print grafo2.pai(5,50,modelo_arvore="DFS")

	print "\nBFS - Grafo 3"

	print grafo3.pai(1,10)
	print grafo3.pai(2,20)
	print grafo3.pai(3,30)
	print grafo3.pai(4,40)
	print grafo3.pai(5,50)

	print "\nDFS - Grafo 3"

	print grafo3.pai(1,10,modelo_arvore="DFS")
	print grafo3.pai(2,20,modelo_arvore="DFS")
	print grafo3.pai(3,30,modelo_arvore="DFS")
	print grafo3.pai(4,40,modelo_arvore="DFS")
	print grafo3.pai(5,50,modelo_arvore="DFS")

##Estudo de Caso 5 - Componentes Conexas

elif caso == 5:

	print "\nGrafo 1:"

	cc1 = grafo1.componentes_conexas()
	print "Número de componentes conexas:", cc1[0]
	print "A maior componente conexa tem tamanho:", cc1[1]
	print "A menor componente conexa tem tamanho:", cc1[2]
	
	print "\nGrafo 2"

	cc2 = grafo2.componentes_conexas()
	print "Número de componentes conexas:", cc2[0]
	print "A maior componente conexa tem tamanho:", cc2[1]
	print "A menor componente conexa tem tamanho:", cc2[2]

	print "\nGrafo 3"

	cc3 = grafo3.componentes_conexas()
	print "Número de componentes conexas:", cc3[0]
	print "A maior componente conexa tem tamanho:", cc3[1]
	print "A menor componente conexa tem tamanho:", cc3[2]

##Estudo de Caso 6 - Grau

elif caso == 6:

	grafo1.imprimir_propriedades()

	a = raw_input("Verificar resultado do Grafo 1 em output.txt; Aperte Enter para examinar o próximo grafo")

	grafo2.imprimir_propriedades()

	b = raw_input("Verificar resultado do Grafo 2 em output.txt; Aperte Enter para examinar o próximo grafo")

	grafo3.imprimir_propriedades()

	print "Verificar resultado do Grafo 3 em output.txt"

##Estudo de Caso 7 - Diâmetro

elif caso == 7:

	print "\nGrafo 1:"
	print "O diâmetro é igual a:", grafo1.diametro()

	print "\nGrafo 2:"
	print "O diâmetro é igual a:", grafo2.diametro()

	print "\nGrafo 3:"
	print "O diâmetro é igual a:", grafo3.diametro()