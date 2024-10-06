#include <Wire.h>  
#include <SoftwareSerial.h> 
#include <LiquidCrystal.h> 

// Definición de pines
#define NITROGEN_PIN A0 
#define PHOSPHORUS_PIN A1 
#define POTASSIUM_PIN A2

// Variables globales
float nitrogenValue = 0.0; 
float phosphorusValue = 0.0; 
float potassiumValue = 0.0;      

// Función para inicializar el código
void setup() {
  Serial.begin(9600); // Iniciar comunicación serial
}

// Función para ejecutar de manera continua
void loop() {
  // Leer el valor del sensor de nitrógeno
  nitrogenValue = analogRead(NITROGEN_PIN);
  // Leer el valor del sensor de fósforo
  phosphorusValue = analogRead(PHOSPHORUS_PIN);
  // Leer el valor del sensor de potasio
  potassiumValue = analogRead(POTASSIUM_PIN);


  // Mostrar los valores en el monitor serial
  Serial.print("Valor de Nitrógeno: ");
  Serial.println(nitrogenValue);
  Serial.print("Valor de Fósforo: ");
  Serial.println(phosphorusValue);
  Serial.print("Valor de Potasio: ");
  Serial.println(potassiumValue);

  // tiempo antes de tomar otra lectura
  delay(5000); 
}
