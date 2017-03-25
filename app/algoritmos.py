import json
import re, string

def get_file_text(path):
    file_io = open(path, "r")
    text = file_io.read()
    file_io.close()
    return text

path = "D:\\file.json"
file_text = get_file_text(path)
diccionario = dict(json.loads(file_text))
abc = diccionario.values()

print("")
print("*********Inicial*********")
cantidad = abc[1].__len__()
listaL0X = []
listaL0Y = []
for i in range(cantidad):
    diccFD =  dict(json.loads(str(json.dumps(abc[1][i]))))
    listaX = [diccFD['x'].split(',')]
    listaY = [diccFD["y"].split(',')]
    print(str(listaX).replace('u','') + '  ->  ' + str(listaY).replace('u',''))
    cantImplicado = listaY[0].__len__()
    if cantImplicado > 1:
        for j in range(cantImplicado):
            listaL0X.append(listaX[0])
            listaL0Y.append(listaY[0][j])
    else:
        listaL0X.append(listaX[0])
        listaL0Y.append(listaY[0][0])

#descomposicion
print("")
print("*********Algoritmo L0 Descomposicion*********")
cantl0 = listaL0X.__len__()
for z in range(cantl0):
    print(str(listaL0X[z]).replace('u', '') + ' -> ' + str(listaL0Y[z]))
