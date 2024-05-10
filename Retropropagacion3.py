# -*- coding: utf-8 -*-
"""
Created on Fri May 10 09:29:40 2024

@author: cs940
"""

import numpy as np
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense

# Datos de entrenamiento
X = np.array([[0.7, 0.3, 0.4, 0.6],   # Humedad, Nitrógeno, Fósforo, Potasio
              [0.8, 0.6, 0.5, 0.7],   
              [0.5, 0.4, 0.3, 0.5],  
              [0.6, 0.5, 0.6, 0.8]]) 

# Etiquetas  calidad del suelo
y = np.array([0.8, 0.9, 0.7, 0.85])  

# Definir el modelo de la red neuronal
model = Sequential()
model.add(Dense(10, input_dim=4, activation='relu'))  # Capa oculta con 10 neuronas y función de activación ReLU
model.add(Dense(1, activation='linear'))  # Capa de salida con una neurona y función de activación lineal

# Compilar el modelo
model.compile(loss='mean_squared_error', optimizer='adam')

# Entrenar el modelo
history = model.fit(X, y, epochs=900, verbose=0)  # Entrenar durante 1000 épocas

# Evaluar el modelo
loss = model.evaluate(X, y)
print("Pérdida (error cuadrático medio):", loss)

# Predicccion
nuevo_dato = np.array([[0.5, 0.4, 0.3, 0.6]])  # Nuevos niveles de humedad, nitrógeno, fósforo y potasio
prediccion = model.predict(nuevo_dato)
print("Predicción de la calidad del suelo:", prediccion[0][0])

# Grafica
plt.plot(history.history['loss'])
plt.title('Pérdida durante el entrenamiento')
plt.xlabel('Época')
plt.ylabel('Pérdida')
plt.show()
