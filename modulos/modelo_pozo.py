class Pozo:

    def __init__(self, nombre, presion, permeabilidad):

        self.nombre = nombre
        self.presion = presion
        self.permeabilidad = permeabilidad

    def produccion(self):

        q = self.presion * self.permeabilidad / 10

        return q
