# Para poder meter caracteres especiales
# encoding=utf8

"""
@ author = Aitor Gorrotxategi
@ desc = Este programa lee los datos Temp, humedad y presión
el protocolo HTTP
"""

# importamos las libreria que queremos usar
import httplib
import urllib
import json
import time
from Adafruit_BMP085 import BMP085

#Inicializar el sensor BMP180
bmp = BMP085(0x77)

USER_API_KEY = 'Q9X8CPMPFPWCAUQJ' # USER_API_KEY de la cuenta de ThingSpeak
server = 'api.thingspeak.com'     # Sevidor al que se quieren subir los datos

#Se establece la conexión
#conn es el objeto que hace referencia a la conexion TCP
connTCP = httplib.HTTPSConnection(server)
print("Estableciendo conexion TCP..."),
connTCP.connect()#establecer conexion
print("Conexion TCP establecida!")

# Crear primer canal de ThingSpeak
method = "POST"
relative_uri = "/channels.json"
# la llave se llama diccionario, las cabeceras se definen mediante dicccionarios
headers = {'HOST': server,
           'Content-Type': 'application/x-www-form-urlencoded'}

payload = {'api_key': USER_API_KEY,
           'name': 'Datos enviados por Raspberry Pi,Canal 1.',
           'field1': 'Temperarura',
           'field2': 'Presión',
           'field3': 'Altitud'}
# La libreria urllib nos permite poner los datos en formato form, para poder enviarlos
payload_encoded = urllib.urlencode(payload)
headers['Content-Length'] = len(payload_encoded)
print("Enviando peticion..."),
connTCP.request(method, relative_uri, body=payload_encoded, headers=headers)
print("Peticion enviada!")
print ("Esperando respuesta HTTP...")
respuesta = connTCP.getresponse()

# Estado de la respuesta para saber si el envio ha sido satisfactorio
status = respuesta.status
print(str(status))

# Tenemos que sacar variables de la url de la respuesta, usaremos otra libreria
contenido = respuesta.read()
#print contenido
# Copiamos contenido en formato json a un diccionario
contenido_json = json.loads(contenido)
CHANNEL_ID_1 = contenido_json['id']
WRITE_API_KEY_1 = contenido_json['api_keys'][0]['api_key']

# Crear nuevo canal
method = "POST"
relative_uri = "/channels.json"
# la llave se llama diccionario, las cabeceras se definen mediante dicccionarios
headers = {'HOST': server,
           'Content-Type': 'application/x-www-form-urlencoded'}

payload = {'api_key': USER_API_KEY,
           'name': 'Datos enviados por Raspberry Pi, Canal 2.',
           'field1': 'Temperarura',
           'field2': 'Presión',
           'field3': 'Altitud'}
# La libreria urllib nos permite poner los datos en formato form, para poder enviarlos
payload_encoded = urllib.urlencode(payload)
headers['Content-Length'] = len(payload_encoded)
print("Enviando peticion..."),
connTCP.request(method, relative_uri, body=payload_encoded, headers=headers)
print("Peticion enviada!")
print ("Esperando respuesta HTTP...")
respuesta = connTCP.getresponse()
# Estado de la respuesta para saber si el envio ha sido satisfactorio
status = respuesta.status
print(str(status))

# Tenemos que sacar variables de la url de la respuesta, usaremos otra libreria
contenido = respuesta.read()
# Copiamos contenido en formato json a un diccionario
contenido_json = json.loads(contenido)
CHANNEL_ID_2 = contenido_json['id']
WRITE_API_KEY_2 = contenido_json['api_keys'][0]['api_key']

WRITE_API_KEY = WRITE_API_KEY_1 # Metemos la WRITE_API_KEY del primer canal, para empezar
                                # metiendo los datos en el primer canal

try:

    while(True):
        
        #Lectura de la temperatura actual
        temp = bmp.readTemperature()
        #Lectura de la presión barométrica
        pressure = bmp.readPressure()
        #Calculo de la altitud, no es nada preciso
        altitude = bmp.readAltitude()
        #Convertir presion a hPa
        presbar = pressure/100

        #Crear la petición HTTP que sube datos a mi canal de thingspeak
        #https://es.mathworks.com/help/thingspeak/writedata.html
        method = "POST"
        relative_uri = "/update.json"
        # la llave se llama diccionario, las cabeceras se definen mediante dicccionarios
        headers = {'HOST': server,
                   'Content-Type': 'application/x-www-form-urlencoded'}
        payload = {'api_key': WRITE_API_KEY,
                   'field1': temp,
                   'field2': presbar,
                   'field3': altitude}
        # LA libreria urllib nos permite poner los datos en formato form, para poder enviarlos
        payload_encoded = urllib.urlencode(payload)
        headers ['Content-Length'] = len(payload_encoded)

        print("Enviando peticion..."),
        connTCP.request(method, relative_uri, body=payload_encoded, headers=headers)
        print("Peticion enviada!")
        print ("Esperando respuesta HTTP...")
        respuesta = connTCP.getresponse()
        # Estado de la respuesta para saber si el envio ha sido satisfactorio
        status = respuesta.status
        respuesta.read()
        print(str(status))
        
        time.sleep(10.00)

        # Cambiamos el "WRITE_API_KEY" para subir los datos al otro canal
        # y así poder subir los datos a ThingSpeak cada 10 s, actualizando cada canal
        # con una frecuencia de 20 segundos.
        if WRITE_API_KEY == WRITE_API_KEY_1:
          WRITE_API_KEY = WRITE_API_KEY_2
        else:
          WRITE_API_KEY = WRITE_API_KEY_1

# Se define la condición para interrumpir el programa
# En este caso, se sale del programa pulsando "CRT+C"
except KeyboardInterrupt:
  connTCP.close()
  print("se ha pulsado CRT+C. Saliendo del programa...")