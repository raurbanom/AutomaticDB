import json
from Utilidades import Utilidades


class RecubrimientoMinimo(object):
    def __init__(self, path):
        self.path = path

        self.listaL0X = []
        self.listaL0Y = []

        self.listaL1X = []
        self.listaL1Y = []

        self.listaL2X = []
        self.listaL2Y = []

        # read data file
        self.file_text = self.get_file_text(path)
        text_json = json.loads(self.file_text)
        self.diccionario = dict(text_json)

        self.result_operacionesXL0 = []
        self.result_operacionesYL0 = []
        self.result_operacionCierreL1 = []
        self.result_operacionCierreL2 = []
        self.utilidad = Utilidades()

    # ------------------------------------------------------------------------
    # FUNCIONES PRINCIPALES
    # ------------------------------------------------------------------------
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
                self.result_operacionesXL0.append(listaX[0][0])
                self.result_operacionesYL0.append(listaY[0])
                for index in range(cantImplicado):
                    self.listaL0X.append(listaX[0])
                    self.listaL0Y.append(listaY[0][index])
            else:
                self.listaL0X.append(listaX[0])
                self.listaL0Y.append(listaY[0][0])
        return self.listaL0X, self.listaL0Y

    def atributos_extranos(self):
        debug = 1
        i = 0
        listaL1X = []
        listaL1Y = []

        for listAux in self.listaL0X:
            j = 0
            list_resultado = []
            if debug == 1:
                # print(str(i) + ") (" + self.utilidad.LimpiarCadena(str(listAux)) + ')+')
                self.result_operacionCierreL1.append(str(i + 1) + ") (" + self.utilidad.LimpiarCadena(str(listAux)) + ')+')
            listCierre = []
            for value in listAux:
                listCierre.append(value)
                j = j + 1
            if j == 1:
                valida_lista_x = self.buscar_lista(listaL1X, self.listaL0X[i])
                if debug == 1:
                    # print("   Resultado: " + self.utilidad.LimpiarCadena(str(listAux)))
                    self.result_operacionCierreL1.append("   Resultado: " + self.utilidad.LimpiarCadena(str(listAux)) + '\n')
                    # print("")
                    # print("Paso " + str(i) + " Resultado X " + str(valida_lista_x).replace('u', '').replace(',', '').replace('[', '').replace(']', '').replace(' ', '').replace("'", ''))
                if valida_lista_x == -1 or (valida_lista_x != -1 and listaL1Y[valida_lista_x] != self.listaL0Y[i]):
                    listaL1X.append(self.listaL0X[i])
                    listaL1Y.append(self.listaL0Y[i])
            else:
                if debug == 1:
                    # print("    Calcular: (" + self.utilidad.LimpiarCadena(str(listCierre)) + ')+')
                    self.result_operacionCierreL1.append("   Calcular: (" + self.utilidad.LimpiarCadena(str(listCierre)) + ')+')
                list_resultado = self.armar_cierre(listCierre, self.listaL0Y[i], 0)
                if debug == 1:
                    # print("    Resultado: " + self.utilidad.LimpiarCadena(str(list_resultado)))
                    self.result_operacionCierreL1.append("    Resultado: " + self.utilidad.LimpiarCadena(str(list_resultado)) + '\n')
                valida_lista_x = self.buscar_lista(listaL1X, list_resultado)
                # if debug == 1:
                    # print("")
                    # print("Paso " + str(i) + " Resultado X " + str(valida_lista_x))
                if valida_lista_x == -1 or (valida_lista_x != -1 and listaL1Y[valida_lista_x] != self.listaL0Y[i]):
                    listaL1X.append(list_resultado)
                    listaL1Y.append(self.listaL0Y[i])
            i += 1

        self.listaL1X = listaL1X
        self.listaL1Y = listaL1Y

        return listaL1X, listaL1Y

    # dependencias redundantes.
    def dependencias_redundantes(self, debug = 1):
        i = 0
        listaAuxX = []
        listaAuxY = []
        listAux = []
        for listAux in self.listaL1X:
            listCierre = []
            for value in listAux:
                listCierre.append(value)
            if debug == 1:
                # print(str(i) + ") Calcular (" + self.utilidad.LimpiarCadena(str(listCierre)) + ')+')
                self.result_operacionCierreL2.append(str(i) + ") Calcular (" + self.utilidad.LimpiarCadena(str(listCierre)) + ')+')
            for z in range(self.listaL1X.__len__()):
                listaAuxX.insert(z, self.listaL1X[z])
                listaAuxY.insert(z, self.listaL1Y[z])
            listaAuxX.pop(i)
            listaAuxY.pop(i)
            # if debug == 1:
                # print("Paso lista_sin_AEX " + str(i) + " " + self.utilidad.LimpiarCadena(str(self.listaL1X)))
                # print("Paso lista_sin_AEY " + str(i) + " " + self.utilidad.LImpiarCadena(str(self.listaL1Y)))
                # print("Paso lista_sin_AEY[i] " + str(i) + " " + self.utilidad.LImpiarCadena(str(self.listaL1Y[i])))
                # print("Paso listaAuxX " + str(i) + " " + self.utilidad.LImpiarCadena(str(listaAuxX)))
                # print("-------Paso listaAuxY " + str(i) + " " + self.utilidad.LImpiarCadena(str(listaAuxY)))
            hay_redundancia = self.armar_cierre_redundantes(listCierre, self.listaL1Y[i], listaAuxX, listaAuxY, debug)
            if debug == 1:
                # print("   Redundancia en: " + self.utilidad.LimpiarCadena(str(listCierre)) + " = " + str(hay_redundancia) + '\n')
                self.result_operacionCierreL2.append("   Redundancia en: " + self.utilidad.LimpiarCadena(str(listCierre)) + " = " + str(hay_redundancia) + '\n')
            if not hay_redundancia:
                self.listaL2X.insert(i, self.listaL1X[i])
                self.listaL2Y.insert(i, self.listaL1Y[i])
            else:
                # if debug == 1:
                    # print("   Eliminacion en: " + str(i) + " " + self.utilidad.LimpiarCadena(str(self.listaL1X[i])) + " --> " + self.utilidad.LimpiarCadena(str(self.listaL1Y[i])) + '\n')
                self.result_operacionCierreL2.append("   Eliminacion en: " + str(i) + " " + self.utilidad.LimpiarCadena(str(self.listaL1X[i])) + " --> " + self.utilidad.LimpiarCadena(str(self.listaL1Y[i])) + '\n')
                self.listaL1X[i] = []
                self.listaL1Y[i] = []
                # i=i-1
            # Limpiamos la lista
            listaAuxX = []
            listaAuxY = []
            i = i + 1
        return self.listaL2X, self.listaL2Y

    # ------------------------------------------------------------------------
    # FUNCIONES AUXILIARES
    # ------------------------------------------------------------------------

    # Aplica el cierre
    def cierre(self, cadenaI, debug):
        cadenaF = str(cadenaI)
        if debug == 1:
            #print("   Calcular: " + " (" + cadenaF + ")+")
            self.result_operacionCierreL2.append("   Calcular: " + " (" + cadenaF + ")+")
            #print("Empezamos cierre" + " --> (" + cadenaF+ ')+')
        Suma_DF = True
        while Suma_DF:
            Suma_DF = False
            i = 0
            for listAux in self.listaL0X:
                cadena_aux = str("")
                for value in listAux:
                    cadena_aux = cadena_aux + str(value)
                #if debug == 1:
                    #print("Cadena aux" + " --> " + cadena_aux)
                    #print("Cadena final" + " --> " + cadenaF)
                if str(cadenaF).__len__() > 1:
                    if (str(cadenaF).__len__() == str(cadena_aux).__len__()) or (
                                str(cadena_aux).__len__() < str(cadenaF).__len__()):
                        if str(cadena_aux).__len__() > str(cadenaF).__len__():
                            cadena1 = str(cadena_aux)
                            cadena2 = str(cadenaF)
                        else:
                            cadena1 = str(cadenaF)
                            cadena2 = str(cadena_aux)
                        if self.buscar_cadena(str(cadena1), str(cadena2), debug) != False:
                            if str(cadenaF).find(str(self.listaL0Y[i])) == -1:
                                #if debug == 1:
                                    #print("i" + str(i))
                                cadenaF = str(cadenaF) + str(self.listaL0Y[i])
                                Suma_DF = True
                        #if debug == 1:
                            #print("cadena final" + "=>" + cadenaF)
                else:
                    #if debug == 1:
                        #print("cadena aux" + "=>" + cadena_aux)
                        #print("cadena final" + "=>" + cadenaF)
                    if cadenaF == cadena_aux:
                        cadenaF = cadenaF + str(self.listaL0Y[i])
                        Suma_DF = True
                    #if debug == 1:
                        #print("cadena final" + "=>" + cadenaF)
                i = i + 1
        return cadenaF

    # Aplica el cierre
    def cierre_redundante(self, cadenaI, listaX, listaY, debug):
        cadenaF = str(cadenaI)
        if debug == 1:
            #print("   Calcular: " + " (" + cadenaF + ')+')
            self.result_operacionCierreL2.append("   Calcular: " + " (" + cadenaF + ')+')
            #print("Empezamos cierre" + " --> (" + cadenaF + ')+')
        Suma_DF = True
        while Suma_DF:
            Suma_DF = False
            i = 0
            for listAux in listaX:
                cadena_aux = str("")
                for value in listAux:
                    cadena_aux = cadena_aux + str(value)
                # if debug == 1:
                    # print("Cadena aux" + " --> " + cadena_aux)
                    # print("Cadena final" + " --> " + cadenaF)
                if str(cadenaF).__len__() > 1:
                    if (str(cadenaF).__len__() == str(cadena_aux).__len__()) or (
                        str(cadena_aux).__len__() < str(cadenaF).__len__()):
                        if str(cadena_aux).__len__() > str(cadenaF).__len__():
                            cadena1 = str(cadena_aux)
                            cadena2 = str(cadenaF)
                        else:
                            cadena1 = str(cadenaF)
                            cadena2 = str(cadena_aux)
                        if self.buscar_cadena(str(cadena1), str(cadena2), debug) != False:
                            if str(cadenaF).find(str(listaY[i])) == -1:
                                #if debug == 1:
                                    #print("i" + str(i))
                                cadenaF = str(cadenaF) + str(listaY[i])
                                Suma_DF = True
                        #if debug == 1:
                            #print("cadena final" + " --> " + cadenaF)
                else:
                    #if debug == 1:
                        #print("Cadena aux" + " --> " + cadena_aux)
                        #print("Cadena final" + " --> " + cadenaF)
                    if cadenaF == cadena_aux:
                        cadenaF = cadenaF + str(listaY[i])
                        Suma_DF = True
                    #if debug == 1:
                        #print("Cadena final" + " --> " + cadenaF)
                i = i + 1
        return cadenaF

    # Arma el cierre y aplica tributos extrtanos
    def armar_cierre(self, list_a_cerrar, implicado, debug):
        global caracterExtrano
        if debug == 1:
            #print("    Validar: " + self.utilidad.LimpiarCadena(str(list_a_cerrar)) + ' --> ' + self.utilidad.LimpiarCadena(str(implicado)))
            self.result_operacionCierreL2.append("    Validar: " + self.utilidad.LimpiarCadena(str(list_a_cerrar)) + ' --> ' + self.utilidad.LimpiarCadena(str(implicado)))
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
                #if debug == 1:
                    #print("Caracter" + caracter)
                if j != i:
                    cadena = cadena + caracter
                else:
                    caracterExtrano = caracter
                j += 1
                #if debug == 1:
                    #print("Cadena armada" + cadena)
            lista.append(cadena)
            dic[str(cadena)] = False
            dicExrano[str(cadena)] = caracterExtrano
            i += 1
        #if debug == 1:
            #print("Cadena armada" + str(lista))
            #print("diccionario armada" + str(dic))
            #print("diccionario extrano" + str(dicExrano))
        for cadena in lista:
            cadena_cierre = self.cierre(str(cadena), debug)
            if debug == 1:
                #print("   Resultado cierre: " + str(cadena_cierre) + " --> " + str(implicado))
                self.result_operacionCierreL2.append("   Resultado cierre: " + str(cadena_cierre) + " --> " + str(implicado))
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

    # Arma el cierr y aplica tributos extrtanos
    def armar_cierre_redundantes(self, list_a_cerrar, implicado, listaX, listaY, debug):
        if debug == 1:
            #print('   Validar: ' + self.utilidad.LimpiarCadena(str(list_a_cerrar)) + ' --> ' + str(implicado))
            self.result_operacionCierreL2.append('   Validar: ' + self.utilidad.LimpiarCadena(str(list_a_cerrar)) + ' --> ' + str(implicado))
        i = 0
        validacion = False
        cadena = ''
        for caracter in list_a_cerrar:
            #if debug == 1:
                #print("")
                #print("Caracter " + caracter)
            cadena = cadena + caracter
            i = i + 1
        #if debug == 1:
            #print("")
            #print("Cadena armada " + cadena)
        cadena_cierre = self.cierre_redundante(str(cadena), listaX, listaY, debug)
        if debug == 1:
            #print("   Resultado cierre: " +  self.utilidad.LimpiarCadena(str(cadena_cierre)) + " --> " + self.utilidad.LimpiarCadena(str(implicado)))
            self.result_operacionCierreL2.append("   Resultado cierre: " +  self.utilidad.LimpiarCadena(str(cadena_cierre)) + " --> " + self.utilidad.LimpiarCadena(str(implicado)))
        if str(cadena_cierre).__len__() > str(implicado).__len__():
            cadena1 = str(cadena_cierre)
            cadena2 = str(implicado)
        else:
            cadena1 = str(implicado)
            cadena2 = str(cadena_cierre)
        if self.buscar_cadena(cadena1, cadena2, debug) != False:
            validacion = True
        return validacion

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

    # Busca la cadena 2 en la 1
    @staticmethod
    def buscar_cadena(cadena1, cadena2, debug):
        #if debug == 1:
            #print("Cadena 1" + "=>" + cadena1)
            #print("Cadena 2" + "=>" + cadena2)
        flag = True
        for caracter_cadena2 in cadena2:
            if cadena1.find(caracter_cadena2) != -1:
                continue
            else:
                flag = False
                break
        return flag

    # ------------------------------------------------------------------------
    # METODOS AUXILIARES
    # ------------------------------------------------------------------------

    def print_descomposicion(self):
        result = ""
        length = self.listaL0X.__len__()

        for index in range(length):
            result += self.utilidad.LimpiarCadena(str(self.listaL0X[index])) + '\t --> ' + \
                      str(self.listaL0Y[index]) + "\n"

        return result + '\n'

    def print_extranios(self):
        result = ""
        length = self.listaL1X.__len__()

        for z in range(length):
            result += self.utilidad.LimpiarCadena(str(self.listaL1X[z])) + "\t --> " + \
                      str(self.listaL1Y[z]).replace('u', '') + "\n"

        return result

    def print_resultado(self):
        result = ""
        length = self.listaL2X.__len__()

        for z in range(length):
            result += self.utilidad.LimpiarCadena(str(self.listaL2X[z])) + "\t --> " + \
                      str(self.listaL2Y[z]).replace('u', '') + "\n"

        return result

    def get_operaciones_L0(self):
        result2 = ""
        result3 = ""
        cant = self.result_operacionesXL0.__len__()
        for i in range(cant):
            cantImplicado = self.result_operacionesYL0[i].__len__()
            result1 = str(self.result_operacionesXL0[i]) + " --> " + self.utilidad.LimpiarCadena(
                str(self.result_operacionesYL0[i]))
            for j in range(cantImplicado):
                result2 = result2 + (
                    str(self.result_operacionesXL0[i]) + '\t --> ' + str(self.result_operacionesYL0[i][j])) + '\n'
            result3 += "Descomponer: " + result1 + "\n" + result2 + "\n"
            result2 = ""
        return result3

    def get_operaciones_L1(self):
        cant = self.result_operacionCierreL1.__len__()
        result = ""
        for i in range(cant):
            result = result + str(self.result_operacionCierreL1[i]) + "\n"
        return result

    def get_operaciones_L2(self):
        cant = self.result_operacionCierreL2.__len__()
        result = ""
        for i in range(cant):
            result = result + str(self.result_operacionCierreL2[i]) + "\n"
        return result
