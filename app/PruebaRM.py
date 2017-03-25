import os

from AutomaticDB import settings
from RecubrimientoMinimo import RecubrimientoMinimo


filename = "file_test.json"
path = os.path.join(settings.MEDIA_ROOT, filename)

# path = "D:\\file.json"

recubrimiento = RecubrimientoMinimo(path)

print("*********Inicial*********")
listaL0X, listaL0Y = recubrimiento.get_descomposicion()


print("*********Algoritmo L0 Descomposicion*********")

print (recubrimiento.print_descomposicion())
