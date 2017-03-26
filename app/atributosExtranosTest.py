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

print ("")
print("*********Segundo paso Atributos extranos*********")

def buscar_cadena(cadena1, cadena2, debug):
    if debug == 1:
        print("Cadena 1" + "=>" + cadena1)
        print("Cadena 2" + "=>" + cadena2)
    flag = True
    for caracter_cadena2 in cadena2:
        if cadena1.find(caracter_cadena2) != -1:
            continue
        else:
            flag = False
            break
    return flag

def cierre(cadenaI, debug):
    cadenaF = str(cadenaI)
    if debug == 1:
        print("Empezamos cierre" + "=>" + cadenaF)
    i=0
    for listAux in listaL0X:
        cadena_aux = str("")
        for value in listAux:
            cadena_aux = cadena_aux + str(value)
        if debug == 1:
            print(cadenaF + " Leng " + str(str(cadenaF).__len__()))
        if str(cadenaF).__len__() > 1:
            if debug == 1:
                print("cadena aux" + "=>" + cadena_aux)
                print("cadena final" + "=>" + cadenaF)

            if (str(cadenaF).__len__() == str(cadena_aux).__len__() ) or (str(cadena_aux).__len__() < str(cadenaF).__len__()):
                if str(cadena_aux).__len__() > str(cadenaF).__len__():
                    cadena1 = str(cadena_aux)
                    cadena2 = str(cadenaF)
                else:
                    cadena1 = str(cadenaF)
                    cadena2 = str(cadena_aux)

                if buscar_cadena(str(cadena1), str(cadena2), debug) != False:
                    if str(cadenaF).find(str(listaL0Y[i])) == -1:
                       cadenaF = str(cadenaF) + str(listaL0Y[i])
                if debug == 1:
                    print("cadena final" + "=>" + cadenaF)
        else:
            if debug == 1:
                print("cadena aux" + "=>" + cadena_aux)
                print("cadena final" + "=>" + cadenaF)
            if cadenaF == cadena_aux:
                cadenaF = cadenaF + str(listaL0Y[i])
            if debug == 1:
                print("cadena final" + "=>" + cadenaF)
        i = i + 1
    return cadenaF



def armar_cierre(list_a_cerrar, implicado, debug):
    if debug == 1:
        print("Entro validar_cierre", str(list_a_cerrar) + "=>" + str(implicado) )
    lista = []
    dic = {}
    dicExrano = {}
    i = 0
    hay_extrano = False
    for i in range(list_a_cerrar.__len__()):
        if debug == 1:
            print (str(i))
        j = 0
        cadena = ''
        for caracter in list_a_cerrar:
            if debug == 1:
                print("Caracter" + caracter)
            if j != i:
                cadena = cadena + caracter
            else:
                caracterExtrano = caracter
            j=j+1
            if debug == 1:
                print("Cadena armada" + cadena)
        lista.append(cadena)
        dic[str(cadena)] = False
        dicExrano[str(cadena)] = caracterExtrano
        i=i+1
    if debug == 1:
        print("Cadena armada" + str(lista))
        print("diccionario armada" + str(dic))
        print("diccionario extrano" + str(dicExrano))
    for cadena in lista:
        cadena_cierre = cierre(str(cadena), debug)
        if debug == 1:
            print("despues de cierre " + str(cadena_cierre), "Implicado " + str(implicado) )
        if str(cadena_cierre).__len__() > str(implicado).__len__():
            cadena1 = str(cadena_cierre)
            cadena2 = str(implicado)
        else:
            cadena1 = str(implicado)
            cadena2 = str(cadena_cierre)
        if buscar_cadena(cadena1, cadena2, debug) != False:
            dic[str(str(cadena))] = True
            hay_extrano = True
        else:
            dic[str(str(cadena))] = False
        if debug == 1:
            print("cierre parcial " + str(dic))
    if debug == 1:
        print("cierre difinitivo " + str(dic))
    #validamos elementos extranos
    if hay_extrano != False:
       for llave, valor in dic.items():
           if debug == 1:
               print ("Llave: ", llave)
               print ("Valor: ", valor)
           '''Armamos el nuevo cierre'''
           if valor == True:
                valor_a_remover = dicExrano[str(llave)]
                if debug == 1:
                    print("Valor a remover: " + str(valor_a_remover))
                    print("Lista a cerrar Antes: " + str(list_a_cerrar))
                list_a_cerrar.remove(str(valor_a_remover))
                if debug == 1:
                    print("Lista a cerrar Despues: " + str(list_a_cerrar))
                    print("Lista a cerrar Despues: " + str(list_a_cerrar.__len__()))
                #recursion
                if list_a_cerrar.__len__() > 1:
                    armar_cierre(list_a_cerrar, implicado, debug)
           else:
                pass
    return list_a_cerrar

def buscarLista(lista1, lista2):
    for i in range(0,len(lista1)):
        if(lista1[i] == lista2):
            return i
    return  -1

#Pasamo de la lista L0 a la L1 los que esten 1 a 1



def atributos_extranos(listaL0X, listaL0Y, debug):
    i= 0
    listaL1X = []
    listaL1Y = []
    for listAux in listaL0X:
        j = 0
        list_resultado = []
        if debug == 1:
            print("Paso " + str(i) + " " + str(listAux))
        listCierre = []
        for value in listAux:
            listCierre.append(value)
            j=j+1
        if j == 1:
            valida_lista_x = buscarLista(listaL1X,listaL0X[i])
            if debug == 1:
                print("Paso " + str(i) + " Resultado X " + str(valida_lista_x))
            if valida_lista_x == -1 or (valida_lista_x != -1 and listaL1Y[valida_lista_x] != listaL0Y[i]):
                listaL1X.append(listaL0X[i])
                listaL1Y.append(listaL0Y[i])
        else:
            if debug == 1:
                print("Lista a cerrar: " + str(listCierre))
            list_resultado = armar_cierre(listCierre, listaL0Y[i], 0)
            if debug == 1:
                print("Paso " + str(i) + " Resultado " + str(list_resultado))
            valida_lista_x = buscarLista(listaL1X,list_resultado)
            if debug == 1:
                print("Paso " + str(i) + " Resultado X " + str(valida_lista_x))
            if valida_lista_x == -1 or (valida_lista_x != -1 and listaL1Y[valida_lista_x] != listaL0Y[i]):
                listaL1X.append(list_resultado)
                listaL1Y.append(listaL0Y[i])
        i=i+1
    return listaL1X, listaL1Y

lista_sin_AEX, lista_sin_AEY = atributos_extranos(listaL0X, listaL0Y, 0)

for z in range(lista_sin_AEX.__len__()):
    print("Resultado " + str(lista_sin_AEX[z]) + "=>" + str(lista_sin_AEY[z]) )







