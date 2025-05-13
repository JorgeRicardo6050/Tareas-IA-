# Importamos las librerías necesarias
import tensorflow as tf
from tensorflow.keras import layers, models
import matplotlib.pyplot as plt

# Cargamos el dataset CIFAR-10
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.cifar10.load_data()

# Normalizamos los datos (escalamos los valores de píxeles entre 0 y 1)
x_train, x_test = x_train / 255.0, x_test / 255.0

# Convertimos las etiquetas a formato categórico
y_train = tf.keras.utils.to_categorical(y_train, 10)
y_test = tf.keras.utils.to_categorical(y_test, 10)

# Mostramos un ejemplo del dataset
class_names = ['Avión', 'Automóvil', 'Pájaro', 'Gato', 'Ciervo', 'Perro', 'Rana', 'Caballo', 'Barco', 'Camión']
plt.imshow(x_train[0])
plt.title(f"Etiqueta: {class_names[y_train[0].argmax()]}")
plt.show()

# Mostramos 10 ejemplos del dataset con sus etiquetas
plt.figure(figsize=(10, 5))  # Ajustamos el tamaño de la figura
for i in range(10):
    plt.subplot(2, 5, i + 1)  # Creamos una cuadrícula de 2 filas y 5 columnas
    plt.imshow(x_train[i])
    plt.title(class_names[y_train[i].argmax()])
    plt.axis('off')  # Ocultamos los ejes
plt.tight_layout()
plt.show()

# Definimos el modelo de red neuronal convolucional
modelo = models.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 3)),  # Primera capa convolucional
    layers.MaxPooling2D((2, 2)),  # Primera capa de pooling
    layers.Conv2D(64, (3, 3), activation='relu'),  # Segunda capa convolucional
    layers.MaxPooling2D((2, 2)),  # Segunda capa de pooling
    layers.Conv2D(128, (3, 3), activation='relu'),  # Tercera capa convolucional
    layers.MaxPooling2D((2, 2)),  # Tercera capa de pooling
    layers.Flatten(),  # Aplanamos las características
    layers.Dense(128, activation='relu'),  # Capa completamente conectada
    layers.Dense(10, activation='softmax')  # Capa de salida con 10 clases
])

# Compilamos el modelo
modelo.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# Entrenamos el modelo
print("Comenzando entrenamiento...")
historial = modelo.fit(
    x_train, y_train,
    epochs=10,
    validation_data=(x_test, y_test)
)
print("Entrenamiento finalizado!")

# Evaluamos el modelo con los datos de prueba
test_loss, test_acc = modelo.evaluate(x_test, y_test, verbose=2)
print(f"Precisión en los datos de prueba: {test_acc:.2f}")

# Graficamos la precisión y la pérdida
plt.plot(historial.history['accuracy'], label='Precisión de entrenamiento')
plt.plot(historial.history['val_accuracy'], label='Precisión de validación')
plt.xlabel('Épocas')
plt.ylabel('Precisión')
plt.legend()
plt.show()

plt.plot(historial.history['loss'], label='Pérdida de entrenamiento')
plt.plot(historial.history['val_loss'], label='Pérdida de validación')
plt.xlabel('Épocas')
plt.ylabel('Pérdida')
plt.legend()
plt.show()