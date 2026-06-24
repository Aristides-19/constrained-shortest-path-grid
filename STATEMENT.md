# Enunciado del Proyecto

Bogotá es una hermosa ciudad ubicada sobre un inmenso altiplano que está más de 8000 pies encima del nivel del mar. Con algunas excepciones, sus vías de comunicación constituyen una cuadrícula en la que:
* Las carreras van de norte a sur y vice-versa.
* Las calles las intersectan a 90º y van sentido oeste-este y vice-versa.

Cuando una carrera o una calle es muy importante, se le antepone el prefijo “Avenida”, como por ejemplo la Avenida Carrera 68 o la Avenida Calle 134. *En algunas zonas hay vías que no son norte-sur ni oeste-este… Se llaman diagonales y transversales, pero para los efectos de este proyecto supondremos que no existen.*

En la zona norte de la ciudad, los números de las carreras crecen desde el este hacia el oeste, mientras que las calles crecen a medida que se avanza hacia el norte. *A diferencia de Caracas, en la que el Parque Nacional El Ávila delimita el confín norte de la ciudad, la interrupción del altiplano en Bogotá se produce al este de la ciudad, debido a los llamados Cerros Orientales.*

Javier y Andreína son novios y viven en Bogotá… Lamentablemente la familia de ella no aprueba la relación, por lo que tienen que verse en secreto. Javier vive en la intersección de la Calle 54 con la Carrera 14, en tanto que Andreína vive en la intersección de la Calle 52 con la Carrera 13; o sea, a tres cuadras de su novio. 

Los establecimientos nocturnos que visitan para encontrarse (sin perjuicio de que el día de la defensa del proyecto se agreguen otros) son:
* **Discoteca The Darkness:** Carrera 14 con Calle 50.
* **Bar La Pasión:** Calle 54 con Carrera 11.
* **Cervecería Mi Rolita** *(“rolo” es un término coloquial de “bogotano” aplicable a quienes, habiendo nacido en la capital, descienden de colombianos de otra parte del país)*: Calle 50 con Carrera 12.

Estos establecimientos son solo para parejas, por lo que los porteros exigen que los dos miembros de la pareja lleguen simultáneamente. 

La zona de la ciudad delimitada entre la Calle 50 por el Sur, la Calle 55 por el norte, la Carrera 10 por el este y la Carrera 15 por el oeste constituyen una cuadrícula perfecta de 25 cuadras, cada una de las cuales tarda 5 minutos en caminar, con excepción de:
* Las Carreras 11, 12 y 13, cuyas aceras están en mal estado y se tarda 7 minutos recorrer cada cuadra.
* La Calle 51, cuya extensa actividad comercial hace que uno se tarde 10 minutos en recorrer cada cuadra.

Como se indicó antes, Javier y Andreína deben llegar al mismo momento a la entrada del establecimiento que desean visitar, pero no pueden ser vistos caminando juntos. Escriba un programa en Python que, a partir del dato del establecimiento destino, indique la trayectoria que debe seguir cada uno y que minimice el tiempo total de caminata de la pareja. 

En caso de que el tiempo de caminata de cada uno sea distinto, se debe indicar cuál de los dos debe salir antes de su domicilio y cuánto tiempo antes, a fin de llegar a la puerta del establecimiento simultáneamente.

## Defensa

Defensa presencial el martes 30 de junio a la hora de clase en el salón de clase. Deben acudir todos los miembros del grupo. El domingo previo 28/6 durante el día deben subir al Aula Virtual un archivo con todos los programas fuente en Python y otro (tipo PDF) describiendo el algoritmo y debe incluir pantallazos de las funcionalidades más relevantes.

Todo se debe programar en Python. Deben representar el grafo usando alguna de las 5 representaciones usadas en clase (es lícito usar más de una si mejora la velocidad del programa). Se tiene que utilizar el método de Dijkstra, adaptándolo a las restricciones del caso. Con la excepción de alguna "librería" para dibujar el grafo, no se puede utilizar ningún software de terceros… Todo deberá ser elaborado por los miembros del equipo. 

En la defensa oral se podrá pedir a los desarrolladores que justifiquen las técnicas de programación utilizadas. Recuerden que se puede agregar un sitio de encuentro adicional en el momento de la defensa y ningún dato puede estar "hard coded".
