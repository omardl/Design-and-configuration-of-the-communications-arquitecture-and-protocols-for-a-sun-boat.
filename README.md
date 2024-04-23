# Diseño y configuración de las comunicaciones de un barco solar pilotado de forma remota

## Objetivo
Con la finalidad de lograr establecer un protocolo de comunicaciones para un barco solar pilotado remotamente, se ha llevado a cabo un estudio de diferentes protocolos y tecnologías de telecomunicación y se han seleccionado y configurado aquellos considerados más adecuados.

En el barco se dispondrá de una Raspberry Pi, un Arduino y una serie de sensores (Ultrasonidos, Pitch-Roll y GPS) que permitirán localizar el barco y variar su trayectoria y velocidad en función de las medidas obtenidas.

El barco también dispondrá de una webcam para la transmisión en directo.

A su vez, una interfaz web permitirá observar los datos recibidos y el streaming, y permitirá enviar una señal sonora y visual activando una serie de buzzers y leds en el barco.

El proyecto fue realizado en equipo utilizando metodología Scrum y usando las herramientas Jira y Confluence.

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

![Scheme](https://github.com/omardl/Design-and-configuration-of-the-communications-arquitecture-and-protocols-for-a-sun-boat./assets/105445540/08537133-a793-41ba-82cf-e5fadc285f47)


## Interfaz

La interfaz principal recoge la información de los sensores mencionados, permitiendo ver el último valor recibido y una gráfica de su variación temporal.

![Dashboard](https://github.com/omardl/Design-and-configuration-of-the-communications-arquitecture-and-protocols-for-a-sun-boat./assets/105445540/039ff6ea-65b2-4e5f-9903-0a558485f97d)


Para una visualización más cómoda del Pitch-Roll, se usan dos imágenes que representan la visión lateral y frontal del barco y que rotarán en función de los valores del sensor.

![DashboardPitch](https://github.com/omardl/Design-and-configuration-of-the-communications-arquitecture-and-protocols-for-a-sun-boat./assets/105445540/fc19df9e-cd9b-4afd-ab67-dc45c383500a)

![DashboardRoll](https://github.com/omardl/Design-and-configuration-of-the-communications-arquitecture-and-protocols-for-a-sun-boat./assets/105445540/58f82195-073b-4b6b-879c-320f9e92e8eb)


También puede verse su locazación en tiempo real a través de un mapa. 

![DashboardLocation](https://github.com/omardl/Design-and-configuration-of-the-communications-arquitecture-and-protocols-for-a-sun-boat./assets/105445540/72115fec-c98d-453e-8df3-20b17cebd110)


La información de los sensores, salvo la del GPS, se guarda en un archivo que podrá ser consultado posteriormente en la pestaña Histórico seleccionando la fecha deseada.

![DashboardLog](https://github.com/omardl/Design-and-configuration-of-the-communications-arquitecture-and-protocols-for-a-sun-boat./assets/105445540/8a268a3b-12d0-4b98-9cd8-c40cef875d4e)

---------

### Proyecto desarrollado para la asignatura "Redes inalámbricas y móviles" del grado en Ingeniería de Tecnologías de Telecomunicación de la UVigo

### Autores
- Omar Delgado
- Jorge Estévez
- Iago Estévez
- Alba Ferreira
