import csv


def crear_lista_gastos():
    with open('lista_gastos.csv', 'w') as lista_gastos:
        writer = csv.writer(lista_gastos)
        writer.writerow(['monto', 'autor', 'motivo', 'fecha_de_creacion'])


if __name__ == '__main__':

    crear_lista_gastos()
