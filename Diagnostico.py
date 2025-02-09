class Nodo:
    def __init__(self, nombre):
        self.nombre = nombre
        self.izquierdo = None
        self.derecho = None

class Arbol:
    def __init__(self):
        self.raiz = None

    def vacio(self):
        return self.raiz is None

    def insertar(self, nombre):
        if self.raiz is None:
            self.raiz = Nodo(nombre)
        else:
            self._insertar_recursivo(self.raiz, nombre)

    def _insertar_recursivo(self, nodo, nombre):
        if nombre < nodo.nombre:
            if nodo.izquierdo is None:
                nodo.izquierdo = Nodo(nombre)
            else:
                self._insertar_recursivo(nodo.izquierdo, nombre)
        else:
            if nodo.derecho is None:
                nodo.derecho = Nodo(nombre)
            else:
                self._insertar_recursivo(nodo.derecho, nombre)

    def buscarNodo(self, nombre):
        return self._buscar_recursivo(self.raiz, nombre)

    def _buscar_recursivo(self, nodo, nombre):
        if nodo is None or nodo.nombre == nombre:
            return nodo
        if nombre < nodo.nombre:
            return self._buscar_recursivo(nodo.izquierdo, nombre)
        return self._buscar_recursivo(nodo.derecho, nombre)

#Ejecución en consola
arbol = Arbol()

if(arbol.vacio()):
    print("El arbol Esta vacio")  
arbol.insertar("Juan")
arbol.insertar("Ana")
arbol.insertar("Pedro")

nodo = arbol.buscarNodo("Ana")
if nodo:
    print(f"Nodo encontrado: {nodo.nombre}")
else:
    print("Nodo no encontrado")