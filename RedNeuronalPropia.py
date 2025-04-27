# Importamos las librerías necesarias
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

# Datos de ejemplo: pesos mexicanos (MXN) y su equivalente en yenes japoneses (JPY)
pesos = np.array([1, 10, 50, 100, 500, 1000], dtype=float)  # Pesos mexicanos
yenes = np.array([7.5, 75, 375, 750, 3750, 7500], dtype=float)  # Yen japonés (tasa ficticia: 1 MXN = 7.5 JPY)

# Imprimimos los datos para verificar
print("Pesos mexicanos:", pesos)
print("Yenes japoneses:", yenes)

# Definimos el modelo de red neuronal
capa = tf.keras.layers.Dense(units=1, input_shape=[1])  # Una capa con una neurona
modelo = tf.keras.Sequential([capa])  # Modelo secuencial con una sola capa

# Compilamos el modelo
modelo.compile(
    optimizer=tf.keras.optimizers.Adam(0.1),  # Tasa de aprendizaje
    loss='mean_squared_error'  # Función de pérdida
)

# Entrenamos el modelo
print("Comenzando entrenamiento...")
historial = modelo.fit(pesos, yenes, epochs=1000, verbose=False)
print("Modelo entrenado!")

# Graficamos la función de pérdida
plt.xlabel("# Época")
plt.ylabel("Magnitud de pérdida")
plt.plot(historial.history["loss"])
plt.show()

# Realizamos una predicción
print("Hagamos una predicción!")
resultado = modelo.predict(np.array([200.0]))  # Convertimos 200 pesos mexicanos a yenes
print(f"El resultado es {resultado[0][0]:.2f} yenes!")

# Mostramos las variables internas del modelo
print("Variables internas del modelo (pesos y sesgos):")
print(capa.get_weights())