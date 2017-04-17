import re


class Utilidades(object):
    def LimpiarCadena(self, cadena):
        nuevaCadena = cadena.replace('u', '') \
            .replace('[', '') \
            .replace(']', '') \
            .replace("'", '') \
            .replace(',', '') \
            .replace(' ', '')
        return nuevaCadena

    def printLists(self, listX, listY):
        length = listX.__len__()
        result = ""

        for z in range(length):
            result += "   " + self.LimpiarCadena(str(listX[z])) + "\t --> " + \
                      self.LimpiarCadena(str(listY[z])) + "\n"
        return result

    def printListClean(self, listX):
        length = listX.__len__()
        result = ""

        for z in range(length):
            result += "   " + self.LimpiarCadena(str(listX[z])) + "\n"
        return result

    def printList(self, listX):
        length = listX.__len__()
        result = ""

        for z in range(length):
            result += "   " + str(listX[z]) + "\n"
        return result



    @staticmethod
    def clearString(string):
        return re.sub('[^a-zA-Z0-9-_*.]', '', string)
