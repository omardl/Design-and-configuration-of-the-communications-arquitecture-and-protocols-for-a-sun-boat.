# Diseño y configuración de las comunicaciones de un barco solar pilotado de forma remota

## Objetivo
Con la finalidad de lograr establecer un protocolo de comunicaciones para un barco solar pilotado remotamente, se ha llevado a cabo un estudio de diferentes protocolos y tecnologías de telecomunicación y se han seleccionado y configurado aquellos considerados más adecuados.

En el barco se dispondrá de una Raspberry Pi, un Arduino y una serie de sensores (Ultrasonidos, Pitch-Roll y GPS) que permitirán localizar el barco y variar su trayectoria y velocidad en función de las medidas obtenidas.

El barco también dispondrá de una webcam para la transmisión en directo.

A su vez, una interfaz web permitirá observar los datos recibidos y el streaming, y permitirá enviar una señal sonora y visual activando una serie de buzzers y leds en el barco.

## Tecnologías
- Wi-Fi
- NB-IoT
- LTE

Se ha usado Wi-Fi como tecnología inicial para estudiar adecuadamente el uso de diferentes protocolos en un entorno más cómodo. En base al alcance requerido y la necesidad de una tasa mínima que permita la retransmisión de la webcam, se ha seleccionado LTE como tecnología.

## Protocolos
- TCP
- AMQP
- DDS
- CoAP
- MQTT

Dado que era un protocolo conocido y usado anteriormente, se ha utilizado TCP inicialmente para configurar y comprobar el funcionamiento de los sensores. Se han estudiado diversos protocolos IoT y, en base a su complejidad, su eficiencia y las necesidades del proyecto, se ha optado por elegir MQTT.

También se implementó en cada protocolo la sincronización del NTP para coordinar la Raspberry y el equipo servidor y evitar fallas en el cálculo de los retardos mediante sellos temporales.

## Arquitectura final
![Scheme](https://github.com/omardl/Sun-boat--RSFM-GETT-UVigo/assets/105445540/131c9f32-931f-4949-ac52-2e14f6f581c6)


## Interfaz

La interfaz principal recoge la información de los sensores mencionados, permitiendo ver el último valor recibido y una gráfica de su variación temporal.

![Dashboard](https://github.com/omardl/Sun-boat--RSFM-GETT-UVigo/assets/105445540/ff5b6057-d3dd-4c42-a6fe-fb14ad8389b5)


Para una visualización más cómoda del Pitch-Roll, se usan dos imágenes que representan la visión lateral y frontal del barco y que rotarán en función de los valores del sensor.

![Dashboard Pitch](https://github.com/omardl/Sun-boat--RSFM-GETT-UVigo/assets/105445540/47e057a3-c9b1-428e-a30e-e0c4c48d94c6)

![Dashboard Roll](https://github.com/omardl/Sun-boat--RSFM-GETT-UVigo/assets/105445540/82cadf60-548e-42df-b894-72d77c1cf59a)




También puede verse su locazación en tiempo real a través de un mapa. 

![Dashboard Location](https://github.com/omardl/Sun-boat--RSFM-GETT-UVigo/assets/105445540/3efd3739-a6c3-4c10-bb37-5f7a8bc5b20e)


La información de los sensores, salvo la del GPS, se guarda en un archivo que podrá ser consultado posteriormente en la pestaña Histórico seleccionando la fecha deseada.

![Dashboard Historic](https://github.com/omardl/Sun-boat--RSFM-GETT-UVigo/assets/105445540/e2bce654-adf2-4829-b22b-a37fb5970296)


---------
### Proyecto desarrollado para la asignatura "Redes inalámbricas y móviles" del grado en Ingeniería de Tecnologías de Telecomunicación de la UVigo

### Autores
- Omar Delgado
- Jorge Estévez
- Iago Estévez
- Alba Ferreira
