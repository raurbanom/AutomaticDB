import json


class RecubrimientoMinimo(object):

    def __init__(self, path):
        self.path = path

        self.listaL0X = []
        self.listaL0Y = []

        self.file_text = self.get_file_text(path)
        text_json = json.loads(self.file_text)
        self.diccionario = dict(text_json)

    @staticmethod
    def get_file_text(path):
        file_io = open(path, 'r')
        text = file_io.read()
        file_io.close()

        return text

    def get_descomposicion(self):
        abc = self.diccionario.values()
        cantidad = abc[1].__len__()

        for i in range(cantidad):
            dicStr = str(json.dumps(abc[1][i]))
            diccFD = dict(json.loads(dicStr))

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

    def print_descomposicion(self):

        resultDescomposicion = ""
        length = self.listaL0X.__len__()

        for index in range(length):
            resultDescomposicion = resultDescomposicion + \
                                   str(self.listaL0X[index]).replace('u', '') + ' -> ' + \
                                   str(self.listaL0Y[index] + "\n")
        return resultDescomposicion
