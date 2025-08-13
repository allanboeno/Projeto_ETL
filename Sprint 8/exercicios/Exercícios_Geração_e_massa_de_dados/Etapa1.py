import random

lista = []

for i in range(0,250):
    n = random.randint(1,1000)
    lista.append(n)

lista.reverse()
print(lista)

