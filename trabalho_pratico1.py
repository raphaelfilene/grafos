# -*- coding: utf-8 -*-
#Esta biblioteca foi feita para a versão 2.7 do Python, não sendo compatível com as versões 3.x do mesmo.

import time
from grafos import *

grafo=Grafo(entrada_txt='as_graph.txt',formato_lista=False,formato_matriz=True)

lista_tempos = []

for i in range(1000):

	start = time.time()
	grafo.gerar_arvore_da_dfs(i)
	end = time.time()
	tempo = end-start

	lista_tempos.append(tempo)

tempo_medio = sum(lista_tempos)/1000.0
print tempo_medio