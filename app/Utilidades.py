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

    @staticmethod
    def clearString(string):
        return re.sub('[^a-zA-Z0-9-_*.]', '', string)
