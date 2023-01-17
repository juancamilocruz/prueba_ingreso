import numpy as np
import math

"""
La clase procesamiento_de_datos se encarga de procesar los datos importados por importacion_de_datos. 
Utiliza los métodos que realizan las transformaciones matemáticas para convertir las 
velocidades lineales en velocidades angulares de las ruedas del robot. 
Los datos procesados se guardan en una lista.
"""

class procesamiento_de_datos:
    def __init__(self, data):
        self.data = data

        # Declare las variables necesarias
        self.alfaIz = (math.pi)/2
        self.betaIz = math.pi
        self.alfaDe = -(math.pi)/2
        self.betaDe = 0
        
        self.r_iz = 35 #mm radio llanta izquierda
        self.r_de = 35 #mm radio llanta derecha
        self.l = 80 #mm longitud al centro

        self.J1 = [[math.sin(self.alfaIz+self.betaIz), -math.cos(self.alfaIz+self.betaIz), -self.l*math.cos(self.betaIz)], [math.sin(self.alfaDe+self.betaDe), -math.cos(self.alfaDe+self.betaDe), -self.l*math.cos(self.betaDe)]]
        self.J2_inv = [[1/self.r_iz, 0],[0, 1/self.r_de]]

    """
    El método velocidad_linear_a_cartesiana() : convierte las velocidades 
    lineales (v, w) y el ángulo (theta) en velocidades cartesianas (x_dot, y_dot, theta_dot)
    """
    def velocidad_linear_a_cartesiana(self, v, w, theta):
        # En este método se calculan las velocidades x_dot, y_dot y theta_dot utilizando las funciones matemáticas de coseno y seno.
        x_dot = v * math.cos(theta) + w * math.sin(theta)
        y_dot = w * math.cos(theta) - v * math.sin(theta)
        theta_dot = w
        return x_dot, y_dot, theta_dot

    """
    El método velocidad_global_a_relativa() : convierte las velocidades cartesianas en 
    velocidades locales utilizando una matriz de rotación (R_matrix)
    """
    def velocidad_global_a_relativa(self, v_cartesian, theta):
        #En este método se calcula la matriz R que representa la transformación de velocidades del marco global
        # al marco local y se multiplica por las velocidades cartesianas para obtener las velocidades locales.
        R_matrix = np.array([[math.cos(theta), -math.sin(theta), 0],
                        [-math.sin(theta), math.cos(theta), 0],
                        [0, 0, 1]])
        v_local = np.dot(R_matrix, v_cartesian)
        return v_local

    """
    velocidad_angular_a_local() : convierte las velocidades locales en 
    velocidades angulares de las ruedas (r_iz_dot, r_de_dot)
    """
    def velocidad_angular_a_local(self, v_local):
        #En este método se calculan las velocidades angulares de las llantas izquierda y derecha a
        # partir de las velocidades locales.
        matriz_vel_motor = np.dot(np.dot(self.J1, v_local),  self.J2_inv)
        r_iz_dot = matriz_vel_motor[0]
        r_de_dot = matriz_vel_motor[1]        
        return r_iz_dot, r_de_dot

    def process_data(self):
        procesar_datos = []
        for t, theta, v, w in self.data:
            v_cartesian = self.velocidad_linear_a_cartesiana(v, w, theta)
            v_local = self.velocidad_global_a_relativa(v_cartesian, theta)
            right_angular_velocity, left_angular_velocity = self.velocidad_angular_a_local(v_local)
            procesar_datos.append((t, right_angular_velocity, left_angular_velocity))
        return procesar_datos