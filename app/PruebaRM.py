import json
import re, string
from RecubrimientoMinimo import RecubrimientoMinimo

path = "D:\\file.json"

re = RecubrimientoMinimo(path)
print("")
print("*********Inicial*********")
listaL0X, listaL0Y = re.descomponer()

print("")
print("*********Algoritmo L0 Descomposicion*********")

print (re.imprimirDescomposicion())
