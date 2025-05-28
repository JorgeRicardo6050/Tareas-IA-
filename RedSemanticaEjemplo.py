# Definición de la clase Nodo para representar conceptos en la red semántica
class Nodo:
    def __init__(self, nombre):
        self.nombre = nombre
        self.relaciones = {}

    def agregar_relacion(self, tipo, nodo):
        if tipo not in self.relaciones:
            self.relaciones[tipo] = []
        self.relaciones[tipo].append(nodo)

    def obtener_relaciones(self, tipo):
        return self.relaciones.get(tipo, [])

# Creación de nodos/conceptos principales
animal = Nodo("Animal")
mamifero = Nodo("Mamífero")
ave = Nodo("Ave")
perro = Nodo("Perro")
gato = Nodo("Gato")
canario = Nodo("Canario")
pez = Nodo("Pez")

# Definición de relaciones entre los nodos
animal.agregar_relacion("es_un", mamifero)
animal.agregar_relacion("es_un", ave)
animal.agregar_relacion("es_un", pez)
mamifero.agregar_relacion("ejemplo", perro)
mamifero.agregar_relacion("ejemplo", gato)
ave.agregar_relacion("ejemplo", canario)

# Función para mostrar la red semántica de manera simple
def mostrar_red(nodo, nivel=0):
    print("  " * nivel + f"- {nodo.nombre}")
    for tipo, nodos_rel in nodo.relaciones.items():
        for n in nodos_rel:
            print("  " * (nivel + 1) + f"[{tipo}]")
            mostrar_red(n, nivel + 2)

# Ejecución: mostrar la red semántica desde el nodo principal
if __name__ == "__main__":
    mostrar_red(animal)