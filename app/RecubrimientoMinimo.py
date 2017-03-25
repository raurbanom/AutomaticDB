import json
import re, string

class RecubrimientoMinimo(object):

    def __init__(self, path):
        """
        :type path: string
        """
        self.path = path
        self.file_text = self.get_file_text()
        self.diccionario = dict(json.loads(self.file_text))
        self.listaL0X = []
        self.listaL0Y = []


    def get_file_text(self):
        file_io = open(self.path, "r")
        text = file_io.read()
        file_io.close()
        return text

    def descomponer(self):

        abc = self.diccionario.values()

        cantidad = abc[1].__len__()

        for i in range(cantidad):
            diccFD =  dict(json.loads(str(json.dumps(abc[1][i]))))
            listaX = [diccFD['x'].split(',')]
            listaY = [diccFD["y"].split(',')]
            print(str(listaX).replace('u','') + '  ->  ' + str(listaY).replace('u',''))
            cantImplicado = listaY[0].__len__()
            if cantImplicado > 1:
                for j in range(cantImplicado):
                    self.listaL0X.append(listaX[0])
                    self.listaL0Y.append(listaY[0][j])
            else:
                self.listaL0X.append(listaX[0])
                self.listaL0Y.append(listaY[0][0])

        return self.listaL0X, self.listaL0Y

    def imprimirDescomposicion(self):
        resultDescomposicion = ""
        cantl0 = self.listaL0X.__len__()
        for z in range(cantl0):
             resultDescomposicion = resultDescomposicion + str(self.listaL0X[z]).replace('u', '') + ' -> ' + str(self.listaL0Y[z] + "\n" )
        return resultDescomposicion
