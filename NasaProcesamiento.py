# -*- coding: utf-8 -*-
"""
Created on Sun Oct  6 06:36:49 2024

@author: cs940
"""

import cv2
import numpy as np
from matplotlib import pyplot as plt

# Cargar las imágenes (la imagen de NASA y tu imagen)
imagen_nasa = cv2.imread('C:/Users/cs940/OneDrive/Documentos/Hackatones/SpaceAppHackaton/Satelite.jpeg')
imagen_local = cv2.imread('C:/Users/cs940/OneDrive/Documentos/Hackatones/SpaceAppHackaton/Local.jpeg')

# Convertir las imágenes a espacio de color HSV para analizar la diferencia de color
imagen_nasa_hsv = cv2.cvtColor(imagen_nasa, cv2.COLOR_BGR2HSV)
imagen_local_hsv = cv2.cvtColor(imagen_local, cv2.COLOR_BGR2HSV)

# Calcular el histograma para cada canal de la imagen en HSV (Hue, Saturation, Value)
hist_nasa_hue = cv2.calcHist([imagen_nasa_hsv], [0], None, [256], [0, 256])
hist_local_hue = cv2.calcHist([imagen_local_hsv], [0], None, [256], [0, 256])

# Normalizar los histogramas para compararlos
hist_nasa_hue = cv2.normalize(hist_nasa_hue, hist_nasa_hue).flatten()
hist_local_hue = cv2.normalize(hist_local_hue, hist_local_hue).flatten()

# Comparar los histogramas utilizando la correlación
similarity = cv2.compareHist(hist_nasa_hue, hist_local_hue, cv2.HISTCMP_CORREL)

# Mostrar los histogramas para visualización
plt.figure()
plt.title("Histogram Comparison - Hue Channel")
plt.xlabel("Bin")
plt.ylabel("Frequency")
plt.plot(hist_nasa_hue, color='r', label="NASA Image")
plt.plot(hist_local_hue, color='g', label="Local Image")
plt.legend()
plt.grid(True)
plt.show()

# Imprimir la similitud entre las imágenes
print(f"Similitud entre las imágenes (correlación): {similarity}")

# Mostrar las imágenes originales para referencia
cv2.imshow('Imagen NASA', imagen_nasa)
cv2.imshow('Imagen Local', imagen_local)
cv2.waitKey(0)
cv2.destroyAllWindows()
