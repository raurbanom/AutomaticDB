class Utilidades(object):
    def LimpiarCadena(self, cadena):
        nuevaCadena = cadena.replace('u', '').replace('[', '').replace(']', '').replace("'", '').replace(',', '').replace(' ', '')
        return nuevaCadena
