import os

from AutomaticDB import settings
from RecubrimientoMinimo import RecubrimientoMinimo

filename = "file_test.json"
path = os.path.join(settings.MEDIA_ROOT, filename)

recubrimiento = RecubrimientoMinimo(path)

print(" ------------------------------------------------------------------------")
print(" Algoritmo L0 Descomposicion")
print(" ------------------------------------------------------------------------")

listaL0X, listaL0Y = recubrimiento.get_descomposicion()
print (recubrimiento.print_descomposicion())
print (recubrimiento.get_operaciones_L0())

print(" ------------------------------------------------------------------------")
print(" Algoritmo L1 Atributos Extranios")
print(" ------------------------------------------------------------------------")

lista_sin_AEX, lista_sin_AEY = recubrimiento.atributos_extranos()
print (recubrimiento.print_extranios())
print (recubrimiento.get_operaciones_L1())

print(" ------------------------------------------------------------------------")
print(" Algoritmo L2 Dependencias Redundantes")
print(" ------------------------------------------------------------------------")

lista_Rta_X, lista_Rta_Y = recubrimiento.dependencias_redundantes()
print (recubrimiento.print_resultado())
print (recubrimiento.get_operaciones_L2())

print(" ------------------------------------------------------------------------")
print(" Algoritmo Calculo de llaves")
print(" ------------------------------------------------------------------------")
lista_Rta_Y1 = recubrimiento.calculo_de_llaves()
result1, result2 = recubrimiento.get_operacionCalculoLlaves()

print(result1)
print(result2)

print (recubrimiento.print_calculo_de_llaves())