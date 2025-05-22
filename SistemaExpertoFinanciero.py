class Nodo:
    def __init__(self, nombre):
        self.nombre = nombre
        self.relaciones = {}

    def agregar_relacion(self, tipo, nodo):
        self.relaciones[tipo] = nodo

    def obtener_relacion(self, tipo):
        return self.relaciones.get(tipo, None)

#nodos principales
deuda = Nodo("Deuda")
ahorro = Nodo("Ahorro")
compra = Nodo("Compra")
inversion = Nodo("Inversion")
ingreso = Nodo("Ingreso")
gasto = Nodo("Gasto")
imprevisto = Nodo("Imprevisto")

# Definimos relaciones
deuda.agregar_relacion("afecta", compra)
ahorro.agregar_relacion("permite", compra)
ahorro.agregar_relacion("permite", inversion)
ingreso.agregar_relacion("aumenta", ahorro)
gasto.agregar_relacion("reduce", ahorro)
imprevisto.agregar_relacion("reduce", ahorro)
deuda.agregar_relacion("reduce", ahorro)

def preguntar_tres_opciones(pregunta, opciones):
    while True:
        respuesta = input(f"{pregunta} ({'/'.join(opciones)}): ").strip().lower()
        if respuesta in opciones:
            return respuesta
        print(f"Por favor responde con una de las siguientes opciones: {', '.join(opciones)}.")

def sistema_experto_financiero():
    print("Sistema Experto Financiero (Red Semántica)")
    tiene_deuda = input("¿Tienes deudas? (si/no): ").strip().lower() == "si"
    deuda_grande = input("¿Son grandes tus deudas? (si/no): ").strip().lower() == "si" if tiene_deuda else False
    tiene_ahorro = input("¿Tienes ahorros? (si/no): ").strip().lower() == "si"
    ahorro_suficiente = input("¿Tus ahorros son suficientes para emergencias? (si/no): ").strip().lower() == "si" if tiene_ahorro else False
    planea_compra = input("¿Tienes planeado hacer una compra? (si/no): ").strip().lower() == "si"
    compra_grande = input("¿La compra representa un gran gasto? (si/no): ").strip().lower() == "si" if planea_compra else False
    planea_inversion = input("¿Estás pensando en invertir? (si/no): ").strip().lower() == "si"
    inversion_riesgo = input("¿La inversión es de alto riesgo? (si/no): ").strip().lower() == "si" if planea_inversion else False
    ingreso_fijo = input("¿Tienes un ingreso fijo mensual? (si/no): ").strip().lower() == "si"
    gastos_nivel = preguntar_tres_opciones("¿Cómo calificarías tus gastos mensuales?", ["altos", "medios", "pequeños"])
    imprevistos = input("¿Has tenido imprevistos financieros recientemente? (si/no): ").strip().lower() == "si"

    # Reglas del sistema experto
    if tiene_deuda and deuda_grande and planea_compra and compra_grande:
        print("No es recomendable realizar grandes compras mientras tengas deudas importantes.")
    elif tiene_deuda and not deuda_grande and planea_compra and not compra_grande:
        print("Deberías esperar a que termines de pagar la mayor parte de tu deuda para permitirte gastos medianos o pequeños.")
    elif not tiene_ahorro and planea_compra:
        print("Evita hacer compras si no tienes ahorros para emergencias.")
    elif tiene_ahorro and not ahorro_suficiente and planea_compra:
        print("Tus ahorros no son suficientes para emergencias, considera ahorrar más antes de comprar.")
    elif planea_inversion and inversion_riesgo and tiene_deuda:
        print("No inviertas en opciones de alto riesgo si tienes deudas pendientes.")
    elif planea_inversion and not inversion_riesgo and tiene_ahorro:
        print("Puedes considerar invertir una parte de tus ahorros en opciones de bajo riesgo.")
    elif not ingreso_fijo and gastos_nivel == "altos":
        print("Reduce tus gastos mensuales hasta tener un ingreso fijo.")
    elif not ingreso_fijo and gastos_nivel == "medios":
        print("Intenta reducir aún más tus gastos y busca estabilizar tus ingresos.")
    elif not ingreso_fijo and gastos_nivel == "pequeños":
        print("Tus gastos son bajos, pero prioriza conseguir un ingreso fijo.")
    elif imprevistos and not tiene_ahorro:
        print("Prioriza crear un fondo de emergencia antes de cualquier otro gasto.")
    elif not tiene_deuda and tiene_ahorro and planea_compra and not compra_grande:
        print("Puedes permitirte compras pequeñas o medianas si tienes ahorros y no tienes deudas.")
    elif not tiene_deuda and tiene_ahorro and planea_inversion and not inversion_riesgo:
        print("Es un buen momento para considerar inversiones de bajo riesgo.")
    else:
        print("Revisa tu situación financiera con calma y prioriza el ahorro y la reducción de deudas.")

if __name__ == "__main__":
    sistema_experto_financiero()