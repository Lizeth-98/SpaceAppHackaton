# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 22:07:39 2024

@author: Josue Villalobos
"""

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Definición de los rangos para los parámetros de NPK
nitrogen = ctrl.Antecedent(np.arange(0, 101, 1), 'Nitrógeno')
phosphorus = ctrl.Antecedent(np.arange(0, 101, 1), 'Fósforo')
potassium = ctrl.Antecedent(np.arange(0, 101, 1), 'Potasio')

# Definición del rango para la calidad del suelo
quality = ctrl.Consequent(np.arange(0, 101, 1), 'Calidad del Suelo')

# Funciones de pertenencia para Nitrógeno (N)
nitrogen['bajo'] = fuzz.trapmf(nitrogen.universe, [0, 0, 20, 40])
nitrogen['medio'] = fuzz.trimf(nitrogen.universe, [30, 50, 70])
nitrogen['alto'] = fuzz.trapmf(nitrogen.universe, [60, 80, 100, 100])

# Funciones de pertenencia para Fósforo (P)
phosphorus['bajo'] = fuzz.trapmf(phosphorus.universe, [0, 0, 20, 40])
phosphorus['medio'] = fuzz.trimf(phosphorus.universe, [30, 50, 70])
phosphorus['alto'] = fuzz.trapmf(phosphorus.universe, [60, 80, 100, 100])

# Funciones de pertenencia para Potasio (K)
potassium['bajo'] = fuzz.trapmf(potassium.universe, [0, 0, 20, 40])
potassium['medio'] = fuzz.trimf(potassium.universe, [30, 50, 70])
potassium['alto'] = fuzz.trapmf(potassium.universe, [60, 80, 100, 100])

# Funciones de pertenencia para la calidad del suelo
quality['mala'] = fuzz.trapmf(quality.universe, [0, 0, 25, 50])
quality['regular'] = fuzz.trimf(quality.universe, [25, 50, 75])
quality['buena'] = fuzz.trapmf(quality.universe, [50, 75, 100, 100])

# Definición de las reglas difusas
rule1 = ctrl.Rule(nitrogen['bajo'] & phosphorus['bajo'] & potassium['bajo'], quality['mala'])
rule2 = ctrl.Rule(nitrogen['medio'] & phosphorus['medio'] & potassium['medio'], quality['regular'])
rule3 = ctrl.Rule(nitrogen['alto'] & phosphorus['alto'] & potassium['alto'], quality['buena'])
rule4 = ctrl.Rule(nitrogen['medio'] & phosphorus['medio'] & potassium['alto'], quality['buena'])
rule5 = ctrl.Rule(nitrogen['bajo'] & phosphorus['alto'] & potassium['medio'], quality['regular'])
rule6 = ctrl.Rule(nitrogen['alto'] & phosphorus['bajo'] & potassium['medio'], quality['regular'])
rule7 = ctrl.Rule(nitrogen['medio'] & phosphorus['alto'] & potassium['bajo'], quality['regular'])

# Controlador difuso
quality_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7])
quality_sim = ctrl.ControlSystemSimulation(quality_ctrl)

# Datos de ejemplo (puedes reemplazar estos datos con los datos reales de tus sensores)
nitrogen_values = np.array([50, 30, 80, 20, 70, 60, 40, 90, 50, 30])
phosphorus_values = np.array([60, 40, 90, 30, 70, 50, 30, 80, 60, 40])
potassium_values = np.array([70, 50, 100, 40, 80, 60, 40, 90, 70, 50])
quality_values = []

# Realizar la simulación para cada conjunto de datos
for n_value, p_value, k_value in zip(nitrogen_values, phosphorus_values, potassium_values):
    # Establecer entradas
    quality_sim.input['Nitrógeno'] = n_value
    quality_sim.input['Fósforo'] = p_value
    quality_sim.input['Potasio'] = k_value
    
    # Calcular salida
    quality_sim.compute()

    # Verificar si 'Calidad del Suelo' está disponible
    if 'Calidad del Suelo' in quality_sim.output:
        quality_values.append(quality_sim.output['Calidad del Suelo'])
    else:
        print(f"Error al calcular la salida para N={n_value}, P={p_value}, K={k_value}")
        quality_values.append(np.nan)  # Rellena con NaN si no hay valor calculado

quality_values = np.array(quality_values)

# El resto del código sigue igual para la regresión lineal
X = np.column_stack((nitrogen_values, phosphorus_values, potassium_values))
y = quality_values

# Manejar valores faltantes (NaN) si es necesario
X = X[~np.isnan(y)]
y = y[~np.isnan(y)]

regressor = LinearRegression()
regressor.fit(X, y)

# Predicciones del modelo de regresión
y_pred = regressor.predict(X)

# Imprimir los coeficientes de la regresión
print("Coeficientes de la regresión lineal múltiple:")
print(f"Intercepto: {regressor.intercept_}")
print(f"Coeficiente para Nitrógeno: {regressor.coef_[0]}")
print(f"Coeficiente para Fósforo: {regressor.coef_[1]}")
print(f"Coeficiente para Potasio: {regressor.coef_[2]}")

# Gráfica de resultados
plt.figure(figsize=(10, 6))

plt.subplot(2, 1, 1)
plt.plot(y, label='Valores calculados por Lógica Difusa', marker='o')
plt.plot(y_pred, label='Valores predichos por Regresión Lineal', linestyle='--', marker='x')
plt.title('Calidad del Suelo: Lógica Difusa vs. Regresión Lineal')
plt.xlabel('Índice de muestra')
plt.ylabel('Calidad del Suelo')
plt.legend()

plt.subplot(2, 1, 2)
plt.scatter(y, y_pred)
plt.plot([min(y), max(y)], [min(y), max(y)], color='red', linestyle='--')
plt.title('Valores Reales vs. Valores Predichos')
plt.xlabel('Valores calculados por Lógica Difusa')
plt.ylabel('Valores predichos por Regresión Lineal')

plt.tight_layout()
plt.show()

# Evaluación del modelo
mse = mean_squared_error(y, y_pred)
r2 = r2_score(y, y_pred)

print(f"Error Cuadrático Medio (MSE): {mse:.2f}")
print(f"Coeficiente de Determinación (R^2): {r2:.2f}")

# Predicción con nuevos valores
new_n_value = 60
new_p_value = 50
new_k_value = 70

new_quality_value = regressor.predict([[new_n_value, new_p_value, new_k_value]])
print(f"\nPredicción de la Calidad del Suelo con Regresión Lineal: {new_quality_value[0]:.2f}")
