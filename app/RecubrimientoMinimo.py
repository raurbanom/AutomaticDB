# coding=utf-8
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
        self.listaResultResta = []
        self.T = []
        self.Z = []
        self.Yi = []
        self.W = []
        self.Xi = []
        self.V = []
        self.M1 = []
        self.M2 = []
        self.lista_claves = []
        self.utilidad = Utilidades()

        self.cierreZ = ''
        self.listaElementosCierreZ = []
        self.listaOpePosibleCombinacion = []

    # ------------------------------------------------------------------------
    # FUNCION EJECUTAR
    # ------------------------------------------------------------------------

    def get_resultado(self):

        self.get_descomposicion()
        data = "1. Dependencias Elementales\n"
        data += self.get_operaciones_L0()
        data += "1.1 Resultado L0 \n"
        data += self.print_descomposicion()

        self.atributos_extranos()
        data += "\n2. Atributos Extraños\n"
        data += self.get_operaciones_L1()
        data += "2.1 Resultado L1\n"
        data += self.print_extranios()

        self.dependencias_redundantes()
        data += "\n3. Dependencias Funcionales Redundantes\n"
        data += self.get_operaciones_L2()
        data += "3.1 Resultado L2\n"

        result1 = "Recubrimiento Minimo\n"
        result1 += self.print_resultado()

        data += result1

        self.calculo_de_llaves()
        data += "\n4. Algoritmo Rapido\n"
        resultAux1, resultAux2 = self.get_operacionCalculoLlaves()
        data += resultAux1
        data += resultAux2
        data += "\n4.1 resultado M2\n"

        result2 = "\nCalculo de Llaves\n"
        result2 += self.print_calculo_de_llaves()

        data += result2

        result = result1 + result2

        return result, data

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
        i = 0
        listaL1X = []
        listaL1Y = []

        for listAux in self.listaL0X:
            j = 0

            # Debug
            self.result_operacionCierreL1.append(str(i + 1) + ") (" + self.utilidad.LimpiarCadena(str(listAux)) + ')+')

            listCierre = []
            for value in listAux:
                listCierre.append(value)
                j = j + 1
            if j == 1:
                valida_lista_x = self.buscar_lista(listaL1X, self.listaL0X[i])
                # Debug
                self.result_operacionCierreL1.append("   Resultado: " + self.utilidad.LimpiarCadena(str(listAux)) + '\n')

                if valida_lista_x == -1 or (valida_lista_x != -1 and listaL1Y[valida_lista_x] != self.listaL0Y[i]):
                    listaL1X.append(self.listaL0X[i])
                    listaL1Y.append(self.listaL0Y[i])
            else:
                # Debug
                self.result_operacionCierreL1.append("   Calcular: (" + self.utilidad.LimpiarCadena(str(listCierre)) + ')+')

                list_resultado = self.armar_cierre(listCierre, self.listaL0Y[i])

                # Debug
                self.result_operacionCierreL1.append("   Resultado: " + self.utilidad.LimpiarCadena(str(list_resultado)) + '\n')

                valida_lista_x = self.buscar_lista(listaL1X, list_resultado)
                if valida_lista_x == -1 or (valida_lista_x != -1 and listaL1Y[valida_lista_x] != self.listaL0Y[i]):
                    listaL1X.append(list_resultado)
                    listaL1Y.append(self.listaL0Y[i])
            i += 1

        self.listaL1X = listaL1X
        self.listaL1Y = listaL1Y

        return listaL1X, listaL1Y

    # Dependencias redundantes.
    def dependencias_redundantes(self):
        i = 0
        listaAuxX = []
        listaAuxY = []

        # Debug
        self.result_operacionCierreL2.append("\n")

        for listAux in self.listaL1X:
            listCierre = []
            for value in listAux:
                listCierre.append(value)

            # Debug
            self.result_operacionCierreL2.append(str(i) + ") Calcular (" + self.utilidad.LimpiarCadena(str(listCierre)) + ')+')

            for z in range(self.listaL1X.__len__()):
                listaAuxX.insert(z, self.listaL1X[z])
                listaAuxY.insert(z, self.listaL1Y[z])

            listaAuxX.pop(i)
            listaAuxY.pop(i)
            hay_redundancia = self.armar_cierre_redundantes(listCierre, self.listaL1Y[i], listaAuxX, listaAuxY)

            # Debug
            self.result_operacionCierreL2.append("   Redundancia en: " + self.utilidad.LimpiarCadena(str(listCierre)) + " = " + str(hay_redundancia) + '\n')

            if not hay_redundancia:
                self.listaL2X.insert(i, self.listaL1X[i])
                self.listaL2Y.insert(i, self.listaL1Y[i])
            else:
                # Debug
                self.result_operacionCierreL2.append("   Eliminacion en: " + str(i) + " " + self.utilidad.LimpiarCadena(str(self.listaL1X[i])) + " --> " + self.utilidad.LimpiarCadena(str(self.listaL1Y[i])) + '\n')

                self.listaL1X[i] = []
                self.listaL1Y[i] = []

            listaAuxX = []
            listaAuxY = []
            i = i + 1

        return self.listaL2X, self.listaL2Y

    # ------------------------------------------------------------------------
    # FUNCIONES AUXILIARES
    # ------------------------------------------------------------------------

    # Aplica el cierre
    def cierre(self, cadenaI):
        cadenaF = str(cadenaI)

        # Debug
        self.result_operacionCierreL2.append("   Calcular: " + "(" + cadenaF + ")+")

        Suma_DF = True

        while Suma_DF:
            Suma_DF = False
            i = 0

            for listAux in self.listaL0X:
                cadena_aux = str("")
                for value in listAux:
                    cadena_aux = cadena_aux + str(value)
                if str(cadenaF).__len__() > 1:
                    if (str(cadenaF).__len__() == str(cadena_aux).__len__()) or (str(cadena_aux).__len__() < str(cadenaF).__len__()):
                        if str(cadena_aux).__len__() > str(cadenaF).__len__():
                            cadena1 = str(cadena_aux)
                            cadena2 = str(cadenaF)
                        else:
                            cadena1 = str(cadenaF)
                            cadena2 = str(cadena_aux)
                        if self.buscar_cadena(str(cadena1), str(cadena2)):
                            if str(cadenaF).find(str(self.listaL0Y[i])) == -1:
                                cadenaF = str(cadenaF) + str(self.listaL0Y[i])
                                Suma_DF = True
                else:
                    if cadenaF == cadena_aux:
                        cadenaF = cadenaF + str(self.listaL0Y[i])
                        Suma_DF = True
                i = i + 1
        return cadenaF

    # Aplica el cierre
    def cierre_redundante(self, cadenaI, listaX, listaY):
        cadenaF = str(cadenaI)
        # Debug
        self.result_operacionCierreL2.append("   Calcular: " + "(" + cadenaF + ')+')

        Suma_DF = True
        while Suma_DF:
            Suma_DF = False
            i = 0
            for listAux in listaX:
                cadena_aux = str("")
                for value in listAux:
                    cadena_aux = cadena_aux + str(value)
                if str(cadenaF).__len__() > 1:
                    if (str(cadenaF).__len__() == str(cadena_aux).__len__()) or (
                                str(cadena_aux).__len__() < str(cadenaF).__len__()):
                        if str(cadena_aux).__len__() > str(cadenaF).__len__():
                            cadena1 = str(cadena_aux)
                            cadena2 = str(cadenaF)
                        else:
                            cadena1 = str(cadenaF)
                            cadena2 = str(cadena_aux)
                        if self.buscar_cadena(str(cadena1), str(cadena2)):
                            if str(cadenaF).find(str(listaY[i])) == -1:
                                cadenaF = str(cadenaF) + str(listaY[i])
                                Suma_DF = True
                else:
                    if cadenaF == cadena_aux:
                        cadenaF = cadenaF + str(listaY[i])
                        Suma_DF = True
                i = i + 1
        return cadenaF

    # Aplica el cierre
    def cierre_claves(self, cadenaI):
        cadenaF = str(cadenaI)
        # Debug
        self.result_operacionCierreL2.append("   Calcular: " + "(" + cadenaF + ")+")

        Suma_DF = True
        while Suma_DF:
            Suma_DF = False
            i = 0
            for listAux in self.listaL2X:
                cadena_aux = str("")
                for value in listAux:
                    cadena_aux = cadena_aux + str(value)
                if str(cadenaF).__len__() > 1:
                    if (str(cadenaF).__len__() == str(cadena_aux).__len__()) or (
                                str(cadena_aux).__len__() < str(cadenaF).__len__()):
                        if str(cadena_aux).__len__() > str(cadenaF).__len__():
                            cadena1 = str(cadena_aux)
                            cadena2 = str(cadenaF)
                        else:
                            cadena1 = str(cadenaF)
                            cadena2 = str(cadena_aux)
                        if self.buscar_cadena(str(cadena1), str(cadena2)):
                            if str(cadenaF).find(str(self.listaL2Y[i])) == -1:
                                cadenaF = str(cadenaF) + str(self.listaL2Y[i])
                                Suma_DF = True
                else:
                    if cadenaF == cadena_aux:
                        cadenaF = cadenaF + str(self.listaL2Y[i])
                        Suma_DF = True
                i = i + 1
        return cadenaF

    # Arma el cierre y aplica tributos extranos
    def armar_cierre(self, list_a_cerrar, implicado):
        global caracterExtrano

        # Debug
        self.result_operacionCierreL2.append("\n   Validar: " + self.utilidad.LimpiarCadena(str(list_a_cerrar)) + ' --> ' + self.utilidad.LimpiarCadena(str(implicado)))

        lista = []
        dic = {}
        dicExrano = {}
        i = 0
        hay_extrano = False
        for i in range(list_a_cerrar.__len__()):

            j = 0
            cadena = ''
            for caracter in list_a_cerrar:
                if j != i:
                    cadena = cadena + caracter
                else:
                    caracterExtrano = caracter
                j += 1
            lista.append(cadena)
            dic[str(cadena)] = False
            dicExrano[str(cadena)] = caracterExtrano
            i += 1
        for cadena in lista:
            cadena_cierre = self.cierre(str(cadena))

            # Debug
            self.result_operacionCierreL2.append("   Resultado cierre: " + str(cadena_cierre) + " --> " + str(implicado))

            if str(cadena_cierre).__len__() > str(implicado).__len__():
                cadena1 = str(cadena_cierre)
                cadena2 = str(implicado)
            else:
                cadena1 = str(implicado)
                cadena2 = str(cadena_cierre)
            if self.buscar_cadena(cadena1, cadena2):
                dic[str(str(cadena))] = True
                hay_extrano = True
                break
            else:
                dic[str(str(cadena))] = False

        # validamos elementos extranos
        if hay_extrano:
            for llave, valor in dic.items():

                '''Armamos el nuevo cierre'''
                if valor:
                    valor_a_remover = dicExrano[str(llave)]
                    list_a_cerrar.remove(str(valor_a_remover))

                    # recursion
                    if list_a_cerrar.__len__() > 1:
                        self.armar_cierre(list_a_cerrar, implicado)
                else:
                    pass
        return list_a_cerrar

    # Arma el cierr y aplica tributos extrtanos
    def armar_cierre_redundantes(self, list_a_cerrar, implicado, listaX, listaY):
        # Debug
        self.result_operacionCierreL2.append('   Validar: ' + self.utilidad.LimpiarCadena(str(list_a_cerrar)) + ' --> ' + str(implicado))

        i = 0
        validacion = False
        cadena = ''
        for caracter in list_a_cerrar:
            cadena = cadena + caracter
            i = i + 1
        cadena_cierre = self.cierre_redundante(str(cadena), listaX, listaY)

        # Debug
        self.result_operacionCierreL2.append("   Resultado cierre: " + self.utilidad.LimpiarCadena(str(cadena_cierre)) + " --> " + self.utilidad.LimpiarCadena(str(implicado)))

        if str(cadena_cierre).__len__() > str(implicado).__len__():
            cadena1 = str(cadena_cierre)
            cadena2 = str(implicado)
        else:
            cadena1 = str(implicado)
            cadena2 = str(cadena_cierre)
        if self.buscar_cadena(cadena1, cadena2):
            validacion = True
        return validacion

    # Calculo de llaves
    def calculo_de_llaves(self):
        self.cierreZ = ''
        caracteresT = ''
        caracteresZ = ''
        cadena1 = ''
        cadena2 = ''
        seguimos = True
        lista_z_cierre = []
        lista_z_u_w = []
        # Armo Conjunto T
        self.T = self.diccionario['attributes']
        self.T.sort()
        # Armo Conjunto Yi
        length = self.listaL2Y.__len__()
        for z in range(length):
            result = self.buscar_cadena_en_lista(str(self.listaL2Y[z]), self.Yi)
            if result == -1 or z == 0:
                self.Yi += self.listaL2Y[z]
        self.Yi.sort()
        # Calculamos Z
        self.Z = self.restar_listas(self.T, self.Yi)
        self.Z.sort()
        # Calculamos Z y validamos
        if self.Z.__len__() > 0:
            for caracter in self.Z:
                caracteresZ = caracteresZ + caracter
            self.cierreZ = self.cierre_claves(caracteresZ)
            self.listaElementosCierreZ.append(self.cierre_claves(caracteresZ))
            # obtenemos caracteres de T
            for c in self.T:
                caracteresT = caracteresT + c
            if str(caracteresT).__len__() == str(self.cierreZ).__len__():
                if self.buscar_cadena(caracteresT, self.cierreZ):
                    self.lista_claves.append(caracteresZ)
                    seguimos = False
                else:
                    pass
            else:
                pass
        else:
            # obtenemos caracteres de T
            for c in self.T:
                caracteresT = caracteresT + c
        if seguimos:
            # calculamos W
            # Armo Conjunto Xi
            length = 0
            length = self.listaL2X.__len__()
            for z in range(length):
                if self.listaL2X[z].__len__() > 0:
                    for d in self.listaL2X[z]:
                        result = self.buscar_cadena_en_lista(str(d), self.Xi)
                        if result == -1 or z == 0:
                            self.Xi.append(d)
                else:
                    result = self.buscar_cadena_en_lista(str(self.listaL2X[z]), self.Xi)
                    if result == -1 or z == 0:
                        self.Xi.append(d)
            self.Xi.sort()
            self.W = self.restar_listas(self.T, self.Xi)
            self.W.sort()
            # calculamos V
            # armamos la lista del cierre de Z
            for c in self.cierreZ:
                lista_z_cierre.append(c)
            lista_z_cierre.extend([element for element in self.W if element not in lista_z_cierre])
            lista_z_u_w = lista_z_cierre
            lista_z_u_w.sort()
            self.V = self.restar_listas(self.T, lista_z_u_w)
            self.V.sort()
            if self.V.__len__() > 0:
                self.buscando_llaves(caracteresZ, caracteresT)
        self.lista_claves.sort()
        return self.lista_claves

    def buscando_llaves(self, caracteresZ, caracteresT):
        primera = True
        cierre_aux = ''
        indice = 0
        # inicializamos M1
        if caracteresZ.__len__() > 0:
            for char in self.V:
                self.M1.append(str(caracteresZ) + str(char))
        else:
            for char in self.V:
                self.M1.append(str(char))
        while self.M1.__len__() > 0:
            self.M1.sort()
            if not primera:
                self.inserto_sig_nivel()
            indice = 0
            for cadena in self.M1:
                if not self.es_subConjunto(cadena):
                    cierre_aux = self.cierre_claves(cadena)
                    if str(caracteresT).__len__() == str(cierre_aux).__len__():
                        if self.buscar_cadena(caracteresT, cierre_aux):
                            self.lista_claves.append(cadena)
                            self.M1[indice] = []
                else:
                    self.M1[indice] = []
                indice = indice + 1
                primera = False
                self.listaOpePosibleCombinacion.append('(' + cadena + ')+ = ' + cierre_aux)

    def es_subConjunto(self, cadena):
        self.lista_claves.sort()
        cadena1 = ''
        cadena2 = ''
        validacion = False
        for subConjunto in self.lista_claves:
            if len(subConjunto) <= cadena:
                cadena1 = cadena
                cadena2 = subConjunto
                if self.buscar_cadena(cadena1, cadena2):
                    validacion = True
        return validacion

    def inserto_sig_nivel(self):
        i = 0
        longitud = 0
        pos_v = 0
        nueva_cadena = ''
        M1_aux = []
        for cadena in self.M1:
            if cadena != []:
                self.M1[i] = []
                longitud = len(cadena)
                ultima = cadena[longitud - 1]
                pos_v = self.posicion_en_V(ultima)
                if pos_v != -1:
                    pos_v = pos_v + 1
                    while pos_v < self.V.__len__():
                        nueva_cadena = cadena + self.V[pos_v]
                        M1_aux.append(nueva_cadena)
                        pos_v = pos_v + 1
                i = i + 1
        self.M1 = []
        self.M1 = M1_aux

    def posicion_en_V(self, ultima):
        indice = 0
        for c in self.V:
            if c == ultima:
                return indice
            indice = indice + 1
        return -1

    def restar_listas(self, listaA, listaB):
        listaR = []
        for c in listaA:
            result = self.buscar_cadena_en_lista(str(c), listaB)
            if result == -1:
                listaR.append(c)
        return listaR

    @staticmethod
    def buscar_lista(lista1, lista2):
        for i in range(0, len(lista1)):
            if lista1[i] == lista2:
                return i
        return -1

    @staticmethod
    def buscar_cadena_en_lista(cadena, lista):
        for i in range(0, len(lista)):
            if lista[i] == cadena:
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
    def buscar_cadena(cadena1, cadena2):
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
        return self.utilidad.printLists(self.listaL0X, self.listaL0Y)

    def print_extranios(self):
        return self.utilidad.printLists(self.listaL1X, self.listaL1Y)

    def print_resultado(self):
        return self.utilidad.printLists(self.listaL2X, self.listaL2Y)

    def print_calculo_de_llaves(self):
        return self.utilidad.printList(self.lista_claves)

    def get_operacionCalculoLlaves(self):
        dictionary_data = self.diccionario.values()
        diccionario = dictionary_data[0]

        self.listaResultResta.append("Z = T - Yi")

        if self.Z != []:
            self.listaResultResta.append("Z = " + self.utilidad.LimpiarCadena(str(self.Z)))
            self.listaResultResta.append("(Z)+ = " + self.utilidad.LimpiarCadena(str(self.listaElementosCierreZ)))
            self.listaResultResta.append("")
        else:
            self.listaResultResta.append("Z = 0")
            self.listaResultResta.append("")

            if self.listaElementosCierreZ.__len__() != diccionario.__len__():
                self.listaResultResta.append("W = T - Xi")
                if self.W != []:
                    self.listaResultResta.append("W = " + self.utilidad.LimpiarCadena(str(self.W)))
                    self.listaResultResta.append("")
                else:
                    self.listaResultResta.append("W = 0")
                    self.listaResultResta.append("")
                self.listaResultResta.append("V = T - { (A)+ U W }")
                self.listaResultResta.append("V = " + self.utilidad.LimpiarCadena(str(self.V)))
                self.listaResultResta.append("")

        result1 = self.utilidad.printList(self.listaResultResta)
        result2 = self.utilidad.printList(self.listaOpePosibleCombinacion)

        return result1, result2

    def get_operaciones_L0(self):
        result2 = ""
        result3 = ""
        cant = self.result_operacionesXL0.__len__()
        for i in range(cant):
            cantImplicado = self.result_operacionesYL0[i].__len__()
            result1 = str(self.result_operacionesXL0[i]) + " --> " + \
                      self.utilidad.LimpiarCadena(str(self.result_operacionesYL0[i]))
            for j in range(cantImplicado):
                result2 += str(self.result_operacionesXL0[i]) + '\t --> ' + str(self.result_operacionesYL0[i][j]) + '\n'
            result3 += "Descomponer: " + result1 + "\n" + result2 + "\n"
            result2 = ""
        return result3

    def get_operaciones_L1(self):
        return self.utilidad.printList(self.result_operacionCierreL1)

    def get_operaciones_L2(self):
        return self.utilidad.printList(self.result_operacionCierreL2)
