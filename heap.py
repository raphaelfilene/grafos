# -*- coding: utf-8 -*-

class BHeap:

	def __init(self):
		self.heapList = [0]
		self.currentSize = 0

	def remove(self):

		menor_valor = self.heapList[1]
		self.heapList[1] = self.heapList[self.currentSize]
		self.currentSize -= 1
		self.heapList.pop()
		self.percDown(1)
		return menor_valor

	def update(self, elemento, elemento_atualizado):
		pass

	def add(self, elemento):
		self.heapList.append(elemento)
		self.currentSize += 1
		self.percUp(self.currentSize)

	def percDown(self,i):

		while (i * 2) <= self.currentSize:
			mc = self.minChild(i)

			if self.heapList[i] > self.heapList[mc]:
				tmp = self.heapList[i]
				self.heapList[i] = self.heapList[mc]
				self.heapList[mc] = tmp

			i = mc

	def percUp(self, i):

		while i // 2 > 0:
			if self.heapList[i] < self.heapList[i // 2]:
				tmp = self.heapList[i //2]
				self.heapList[i //2] = self.heapList[i]
				self.heapList[i] = tmp

			i = i // 2

	def minChild(self, i):

		if i * 2 + 1 > self.currentSize:
			return i * 2

		else:
			if self.heapList[i*2] < self.heapList[i*2+1]:
				return i * 2
			else:
				return i * 2 + 1

	def buildHeap(self, lista):

		i = len(lista) // 2
		self.currentSize = len(lista)
		self.heapList = [0] + lista[:]
		while (i > 0):
			self.percDown(i)
			i -= 1

if __name__ == '__main__':
	bh = BHeap()
	bh.buildHeap([9,5,6,2,3])

	print(bh.remove())
	print(bh.remove())
	print(bh.remove())
	print(bh.remove())
	print(bh.remove())