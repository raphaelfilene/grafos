# -*- coding: utf-8 -*-

import time
from grafos import *

grafo=Grafo(entrada_txt='as_graph.txt',formato_lista=True,formato_matriz=False)

lista_tempos = []

for i in range(1000):

	start = time.time()
	grafo.gerar_arvore_da_bfs(i)
	end = time.time()
	tempo = end-start

	lista_tempos.append(tempo)

tempo_medio = sum(lista_tempos)/1000.0
print tempo_medio