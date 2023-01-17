#   importamos las siguientes librerias
import csv  # Importa la librería csv para leer archivos CSV.
import math # Importa la librería math para tener acceso a funciones matemáticas.
import numpy as np
from procesar import procesamiento_de_datos

""""
la clase importacion_de_datos se encarga de importar los datos de un archivo de texto 
especificado. Utiliza la librería csv para leer el archivo y guarda los datos en una array.
"""
class importacion_de_datos:
    def __init__(self, file_path):
        self.file_path = file_path

    def import_data(self):
        data = []
        with open(self.file_path, 'r') as file:
            csv_reader = csv.reader(file, delimiter=',')
            next(csv_reader)
            for row in csv_reader:
                t = float(row[0])
                theta = float(row[1])
                v = float(row[2])
                w = float(row[3])
                data.append((t, theta, v, w))
        return data

"""
exportacion_de_datos : exporta los datos procesados a un archivo de texto con el formato especificado
"""
class exportacion_de_datos:
    def __init__(self, procesar_datos, file_path):
        self.procesar_datos = procesar_datos
        self.file_path = file_path

    def export_data(self):
        with open(self.file_path, 'w') as file:
            for t, right_angular_velocity, left_angular_velocity in self.procesar_datos:
                file.write(f"{t}, {right_angular_velocity}, {left_angular_velocity}\n")


# En el hilo principal

# Crear una instancia de importacion_de_datos
importacion_de_dato_txt = importacion_de_datos("datos.txt")
# Importar los datos
data = importacion_de_dato_txt.import_data()

# Crear una instancia de procesamiento_de_datos
procesamiento_datos = procesamiento_de_datos(data)

# Procesar los datos
procesar_datos = procesamiento_datos.process_data()

# Crear una instancia de exportacion_de_datos
exportar_datos = exportacion_de_datos(procesar_datos, "resultado.txt")

# Exportar los datos
exportar_datos.export_data()
