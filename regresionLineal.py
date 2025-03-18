import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# 1. Generar datos de ejemplo
np.random.seed(0)
X = 2 * np.random.rand(100, 1)  # Característica (variable independiente)
y = 4 + 3 * X + np.random.randn(100, 1)  # Variable objetivo (variable dependiente)

# 2. Dividir los datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Crear y entrenar el modelo de regresión lineal
model = LinearRegression()
model.fit(X_train, y_train)

# 4. Hacer predicciones en el conjunto de prueba
y_pred = model.predict(X_test)

# 5. Evaluar el modelo
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Error cuadrático medio (MSE): {mse}")
print(f"Coeficiente de determinación (R²): {r2}")

# 6. Visualizar los resultados
plt.scatter(X_test, y_test, color='blue')
plt.plot(X_test, y_pred, color='red')
plt.xlabel('Característica X')
plt.ylabel('Variable objetivo y')
plt.title('Regresión Lineal Simple')
plt.show()

# 7. Imprimir los coeficientes del modelo
print(f"Coeficiente (pendiente): {model.coef_[0][0]}")
print(f"Intercepción (ordenada al origen): {model.intercept_[0]}")