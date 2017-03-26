class Utilidades(object):
    def LImpiarCadena(self, cadena):
        nuevaCadena = cadena.replace('u', '').replace('[', '').replace(']', '').replace("'", '').replace(',', '').replace(' ', '')
        return nuevaCadena
