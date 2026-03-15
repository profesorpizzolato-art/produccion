import numpy as np

class MotorSimulacion:

    def __init__(self):

        self.presion = 1000
        self.permeabilidad = 150
        self.viscosidad = 2

    def calcular_produccion(self):

        q = (self.presion * self.permeabilidad) / self.viscosidad

        return q

    def evolucion_produccion(self, pasos=100):

        datos = []

        for i in range(pasos):

            variacion = np.random.normal(0,20)

            produccion = self.calcular_produccion() + variacion

            datos.append(produccion)

        return datos
