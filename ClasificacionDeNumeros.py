# Importamos las librerías necesarias
import tensorflow as tf
from keras import layers, models  # Importamos layers y models desde keras
import matplotlib.pyplot as plt

# Cargamos el dataset MNIST
mnist = tf.keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# Normalizamos los datos (escalamos los valores de píxeles entre 0 y 1)
x_train, x_test = x_train / 255.0, x_test / 255.0

# Mostramos un ejemplo del dataset
plt.imshow(x_train[0], cmap='gray')
plt.title(f"Etiqueta: {y_train[0]}")
plt.show()

# Definimos el modelo de red neuronal
modelo = tf.keras.Sequential([
    tf.keras.layers.Flatten(input_shape=(28, 28)),  # Aplanamos las imágenes de 28x28 píxeles
    tf.keras.layers.Dense(128, activation='relu'),  # Capa oculta con 128 neuronas y activación ReLU
    tf.keras.layers.Dropout(0.2),  # Dropout para evitar sobreajuste
    tf.keras.layers.Dense(10, activation='softmax')  # Capa de salida con 10 neuronas (una por cada dígito)
])

# Compilamos el modelo
modelo.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# Entrenamos el modelo
print("Comenzando entrenamiento...")
historial = modelo.fit(x_train, y_train, epochs=5, validation_data=(x_test, y_test))
print("Entrenamiento finalizado!")

# Evaluamos el modelo con los datos de prueba
test_loss, test_acc = modelo.evaluate(x_test, y_test, verbose=2)
print(f"Precisión en los datos de prueba: {test_acc:.2f}")

# Realizamos una predicción
print("Realizando una predicción...")
predicciones = modelo.predict(x_test)
print(f"Predicción para la primera imagen de prueba: {predicciones[0].argmax()} (Etiqueta real: {y_test[0]})")

# Mostramos la primera imagen de prueba y su predicción
plt.imshow(x_test[0], cmap='gray')
plt.title(f"Predicción: {predicciones[0].argmax()} (Etiqueta real: {y_test[0]})")
plt.show()