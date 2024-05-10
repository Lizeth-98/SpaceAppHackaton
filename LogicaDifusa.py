# -*- coding: utf-8 -*-
"""
Created on Fri May 10 12:56:46 2024

@author: cs940
"""

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

#Definir las variables de entrada y salida del sistema difuso
humedad = ctrl.Antecedent(np.arange(0, 101, 1), 'humedad')
ph = ctrl.Antecedent(np.arange(0, 15, 0.1), 'ph')
potasio = ctrl.Antecedent(np.arange(0, 101, 1), 'potasio')
fosforo = ctrl.Antecedent(np.arange(0, 101, 1), 'fosforo')
nitrogeno = ctrl.Antecedent(np.arange(0, 101, 1), 'nitrogeno')
calidad = ctrl.Consequent(np.arange(0, 101, 1), 'calidad')

#Definir las funciones de membresía para cada variable

humedad['baja'] = fuzz.trimf(humedad.universe, [0, 0, 50])
humedad['media'] = fuzz.trimf(humedad.universe, [25, 50, 75])
humedad['alta'] = fuzz.trimf(humedad.universe, [50, 100, 100])

ph['acido'] = fuzz.trimf(ph.universe, [0, 0, 7])
ph['neutro'] = fuzz.trimf(ph.universe, [6, 7, 8])
ph['basico'] = fuzz.trimf(ph.universe, [7, 14, 14])

potasio['bajo'] = fuzz.trimf(potasio.universe, [0, 0, 50])
potasio['medio'] = fuzz.trimf(potasio.universe, [25, 50, 75])
potasio['alto'] = fuzz.trimf(potasio.universe, [50, 100, 100])

fosforo['bajo'] = fuzz.trimf(fosforo.universe, [0, 0, 50])
fosforo['medio'] = fuzz.trimf(fosforo.universe, [25, 50, 75])
fosforo['alto'] = fuzz.trimf(fosforo.universe, [50, 100, 100])

nitrogeno['bajo'] = fuzz.trimf(nitrogeno.universe, [0, 0, 50])
nitrogeno['medio'] = fuzz.trimf(nitrogeno.universe, [25, 50, 75])
nitrogeno['alto'] = fuzz.trimf(nitrogeno.universe, [50, 100, 100])

calidad['mala'] = fuzz.trimf(calidad.universe, [0, 0, 50])
calidad['regular'] = fuzz.trimf(calidad.universe, [25, 50, 75])
calidad['buena'] = fuzz.trimf(calidad.universe, [50, 100, 100])

# Definir las reglas difusa
regla1 = ctrl.Rule(humedad['baja'] | ph['acido'] | potasio['bajo'] | fosforo['bajo'] | nitrogeno['alto'], calidad['mala'])
regla2 = ctrl.Rule(humedad['media'] & ph['neutro'] & potasio['medio'] & fosforo['medio'] & nitrogeno['medio'], calidad['buena'])
regla3 = ctrl.Rule(humedad['alta'] & ph['basico'] | potasio['alto'] | fosforo['alto'] | nitrogeno['bajo'], calidad['regular'])

# Crear el sistema de control difuso
sistema_control = ctrl.ControlSystem([regla1, regla2, regla3])

#Crear un simulador para el sistema de control difuso
simulador = ctrl.ControlSystemSimulation(sistema_control)

# Graficar las funciones de membresía de las variables de entrada
fig, axes = plt.subplots(3, 2, figsize=(10, 10))
axes = axes.flatten()
for i, variable in enumerate([humedad, ph, potasio, fosforo, nitrogeno]):
    variable.view(ax=axes[i])

#Evaluar el sistema de control difuso y graficar en 3D
simulador.input['humedad'] = 80
simulador.input['ph'] = 7
simulador.input['potasio'] = 60
simulador.input['fosforo'] = 40
simulador.input['nitrogeno'] = 30
simulador.compute()

# Obtener el valor de salida
print("Calidad del suelo:", simulador.output['calidad'])

# Graficar la salida en 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
x = np.array([80])
y = np.array([7])
z = np.array([60])
calidad.view(sim=simulador, ax=ax)
ax.scatter(x, y, z, color='r', s=100, label='Entrada')
ax.set_xlabel('Humedad')
ax.set_ylabel('pH')
ax.set_zlabel('Potasio')
plt.legend()
plt.show()