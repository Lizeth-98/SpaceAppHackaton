# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 13:28:28 2024

@author: Josue Villalobos
"""

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


potasio = ctrl.Antecedent(np.arange(0, 101, 1), 'potasio')
fosforo = ctrl.Antecedent(np.arange(0, 101, 1), 'fosforo')
nitrogeno = ctrl.Antecedent(np.arange(0, 101, 1), 'nitrogeno')

calidad = ctrl.Consequent(np.arange(0, 101, 1), 'calidad')


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


regla1 = ctrl.Rule(potasio['bajo'] | fosforo['bajo'] | nitrogeno['alto'], calidad['mala'])
regla2 = ctrl.Rule(potasio['medio'] & fosforo['medio'] & nitrogeno['medio'], calidad['buena'])
regla3 = ctrl.Rule(potasio['alto'] | fosforo['alto'] | nitrogeno['bajo'], calidad['regular'])


sistema_control = ctrl.ControlSystem([regla1, regla2, regla3])
simulador = ctrl.ControlSystemSimulation(sistema_control)


fig, axes = plt.subplots(3, 1, figsize=(10, 10))
axes = axes.flatten()
for i, variable in enumerate([potasio, fosforo, nitrogeno]):
    variable.view(ax=axes[i])


simulador.input['potasio'] = 783
simulador.input['fosforo'] = 777
simulador.input['nitrogeno'] = 752
simulador.compute()


print("Calidad del suelo:", simulador.output['calidad'])


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
x = np.array([60])
y = np.array([70])
z = np.array([40])
calidad.view(sim=simulador, ax=ax)
ax.scatter(x, y, z, color='r', s=100, label='Entrada')
ax.set_xlabel('Potasio')
ax.set_ylabel('Fósforo')
ax.set_zlabel('Nitrógeno')
plt.legend()
plt.show()