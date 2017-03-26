import json


class RecubrimientoMinimo(object):
    def __init__(self, path):
        self.path = path

        self.listaL0X = []
        self.listaL0Y = []

        self.listaL1X = []
        self.listaL1Y = []

        # read data file
        self.file_text = self.get_file_text(path)
        text_json = json.loads(self.file_text)
        self.diccionario = dict(text_json)

    def get_descomposicion(self):
        dictionary_data = self.diccionario.values()
        length = dictionary_data[1].__len__()

        for i in range(length):
            dictionaryStr = str(json.dumps(dictionary_data[1][i]))
            diccFD = dict(json.loads(dictionaryStr))

            listaX = [diccFD['x'].split(',')]
            listaY = [diccFD["y"].split(',')]

            # print(str(listaX).replace('u', '') + '  ->  ' + str(listaY).replace('u', ''))
            cantImplicado = listaY[0].__len__()

            if cantImplicado > 1:
                for index in range(cantImplicado):
                    self.listaL0X.append(listaX[0])
                    self.listaL0Y.append(listaY[0][index])
            else:
                self.listaL0X.append(listaX[0])
                self.listaL0Y.append(listaY[0][0])

        return self.listaL0X, self.listaL0Y

    def atributos_extranos(self, debug):
        i = 0
        listaL1X = []
        listaL1Y = []

        for listAux in self.listaL0X:
            j = 0
            list_resultado = []
            if debug == 1:
                print("Paso " + str(i) + " " + str(listAux))
            listCierre = []
            for value in listAux:
                listCierre.append(value)
                j = j + 1
            if j == 1:
                valida_lista_x = self.buscar_lista(listaL1X, self.listaL0X[i])
                if debug == 1:
                    print("Paso " + str(i) + " Resultado X " + str(valida_lista_x))
                if valida_lista_x == -1 or (valida_lista_x != -1 and listaL1Y[valida_lista_x] != self.listaL0Y[i]):
                    listaL1X.append(self.listaL0X[i])
                    listaL1Y.append(self.listaL0Y[i])
            else:
                if debug == 1:
                    print("Lista a cerrar: " + str(listCierre))
                list_resultado = self.armar_cierre(listCierre, self.listaL0Y[i], 0)
                if debug == 1:
                    print("Paso " + str(i) + " Resultado " + str(list_resultado))
                valida_lista_x = self.buscar_lista(listaL1X, list_resultado)
                if debug == 1:
                    print("Paso " + str(i) + " Resultado X " + str(valida_lista_x))
                if valida_lista_x == -1 or (valida_lista_x != -1 and listaL1Y[valida_lista_x] != self.listaL0Y[i]):
                    listaL1X.append(list_resultado)
                    listaL1Y.append(self.listaL0Y[i])
            i += 1

        self.listaL1X = listaL1X
        self.listaL1Y = listaL1Y

        return listaL1X, listaL1Y

    # Busca la cadena 2 en la 1
    def buscar_cadena(self, cadena1, cadena2, debug):
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

    # Aplica el cierre
    def cierre(self, cadenaI, debug):
        cadenaF = str(cadenaI)

        if debug == 1:
            print("Empezamos cierre" + "=>" + cadenaF)
        i = 0
        for listAux in self.listaL0X:
            cadena_aux = str("")
            for value in listAux:
                cadena_aux += str(value)
            if debug == 1:
                print(cadenaF + " Leng " + str(str(cadenaF).__len__()))
            if str(cadenaF).__len__() > 1:
                if debug == 1:
                    print("cadena aux" + "=>" + cadena_aux)
                    print("cadena final" + "=>" + cadenaF)
                if (str(cadenaF).__len__() == str(cadena_aux).__len__()) or (
                            str(cadena_aux).__len__() < str(cadenaF).__len__()):
                    if str(cadena_aux).__len__() > str(cadenaF).__len__():
                        cadena1 = str(cadena_aux)
                        cadena2 = str(cadenaF)
                    else:
                        cadena1 = str(cadenaF)
                        cadena2 = str(cadena_aux)
                    if self.buscar_cadena(str(cadena1), str(cadena2), debug):
                        if str(cadenaF).find(str(self.listaL0Y[i])) == -1:
                            cadenaF = str(cadenaF) + str(self.listaL0Y[i])
                    if debug == 1:
                        print("cadena final" + "=>" + cadenaF)
            else:
                if debug == 1:
                    print("cadena aux" + "=>" + cadena_aux)
                    print("cadena final" + "=>" + cadenaF)
                if cadenaF == cadena_aux:
                    cadenaF += str(self.listaL0Y[i])
                if debug == 1:
                    print("cadena final" + "=>" + cadenaF)
            i += 1
        return cadenaF

    # Arma el cierre y aplica tributos extrtanos
    def armar_cierre(self, list_a_cerrar, implicado, debug):
        global caracterExtrano
        if debug == 1:
            print("Entro validar_cierre", str(list_a_cerrar) + "=>" + str(implicado))
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
                j += 1
                if debug == 1:
                    print("Cadena armada" + cadena)
            lista.append(cadena)
            dic[str(cadena)] = False
            dicExrano[str(cadena)] = caracterExtrano
            i += 1
        if debug == 1:
            print("Cadena armada" + str(lista))
            print("diccionario armada" + str(dic))
            print("diccionario extrano" + str(dicExrano))
        for cadena in lista:
            cadena_cierre = self.cierre(str(cadena), debug)
            if debug == 1:
                print("despues de cierre " + str(cadena_cierre), "Implicado " + str(implicado))
            if str(cadena_cierre).__len__() > str(implicado).__len__():
                cadena1 = str(cadena_cierre)
                cadena2 = str(implicado)
            else:
                cadena1 = str(implicado)
                cadena2 = str(cadena_cierre)
            if self.buscar_cadena(cadena1, cadena2, debug):
                dic[str(str(cadena))] = True
                hay_extrano = True
                break
            else:
                dic[str(str(cadena))] = False
            if debug == 1:
                print("cierre parcial " + str(dic))
        if debug == 1:
            print("cierre difinitivo " + str(dic))
        # validamos elementos extranos
        if hay_extrano:
            for llave, valor in dic.items():
                if debug == 1:
                    print ("Llave: ", llave)
                    print ("Valor: ", valor)
                '''Armamos el nuevo cierre'''
                if valor:
                    valor_a_remover = dicExrano[str(llave)]
                    if debug == 1:
                        print("Valor a remover: " + str(valor_a_remover))
                        print("Lista a cerrar Antes: " + str(list_a_cerrar))
                    list_a_cerrar.remove(str(valor_a_remover))
                    if debug == 1:
                        print("Lista a cerrar Despues: " + str(list_a_cerrar))
                        print("Lista a cerrar Despues: " + str(list_a_cerrar.__len__()))

                    # recursion
                    if list_a_cerrar.__len__() > 1:
                        self.armar_cierre(list_a_cerrar, implicado, debug)
                else:
                    pass
        return list_a_cerrar

    @staticmethod
    def buscar_lista(lista1, lista2):
        for i in range(0, len(lista1)):
            if lista1[i] == lista2:
                return i
        return -1

    @staticmethod
    def get_file_text(path):
        file_io = open(path, 'r')
        text = file_io.read()
        file_io.close()

        return text

    # Metodos Auxiliares

    def print_descomposicion(self):

        resultDescomposicion = ""
        length = self.listaL0X.__len__()

        for index in range(length):
            resultDescomposicion = resultDescomposicion + \
                                   str(self.listaL0X[index]).replace('u', '').replace('[', '').replace(']', '').replace("'", '').replace(',', '').replace(' ', '') + ' --> ' + \
                                   str(self.listaL0Y[index]) + "\n"
        return resultDescomposicion

    def print_extranios(self):
        resultExtranios = ""
        length = self.listaL1X.__len__()

        for z in range(length):
            resultExtranios = resultExtranios + \
                                   str(self.listaL1X[z]).replace('u', '').replace('[', '').replace(']', '').replace("'", "").replace(',', '').replace(' ', '') + " --> " + \
                                   str(self.listaL1Y[z]).replace('u', '') + "\n"

        return resultExtranios
