# Análisis de Palabras Discriminatorias en Twitter entre ususarios de la CDMX

## Problema
COPRED tiene 7 categorías de discriminación identificadas en sus catálogos:
+ apariencia
+ discapacidad
+ edad
+ género
+ ideología
+ orientación
+ religión

Cada categoría engloba palabras y frases específicas con las que COPRED ha identificado actos discriminatorios en la CDMX. A continuación las palabras por categoría. La lista no pretende ser exhaustiva ni limitativa, y solo refleja un ejercicio que se realizó desde COPRED para identificar las palabras de acuerdo a la experiencia de sus funcionarios.

![Tabla motivos de discriminación COPRED](https://i.imgur.com/e5sdQaP.png)

Se desea conocer los patrones de discriminación en la red social Twitter particulares de la CDMX. Preguntas relevantes para este propósito son:

+ ¿Qué palabras discriminatorias aparecen juntas siempre?
+ ¿Es posible detectar discriminación emergente en grupos sociales?
+ ¿Qué tipo de discriminación es más frecuente en el medio de interés?

### Modelo de clasificación y su intuición

Se creará un modelo de clasificación de texto que "aprenda" los patrones de un universo de tuits recolectados. Estos patrones identificarán las palabras y textos específicos definidos por COPRED aunadas a métricas de relevancia de dichos textos dentro de todo el conjunto de mensajes para tratar de identificar el contexto correctamente.

La intuición del algoritmo utilizado para identificar las palabras y su relevancia para formar contextos correctamente es el siguiente:

1. Contar las ocurrencias de cada palabra dentro de cada uno de los mensajes.
2. Dividir esta frecuencia de ocurrencias entre el total de palabras en todos los documentos.
3. Si una palabra de interés se encuentra en la mayoría de los mensajes, es de poca relevancia.
4. Si una palabra de interés se encuentra en pocos mensajes, es de mayor relevancia.
5. Si una palabra de interés se encuentra en MUY pocos mensajes, es de poca relevancia.

Ejemplo:

1. Digamos que en un discurso político sobre seguridad pública predominan las palabras "policía", "vulnerabilidad", "protección" y "fuerza".
2. Nosotros determinamos, desde antes, que la palabra "narcotráfico", es palabra de interés.
3. Si domina en la conversación, significa que todo el discurso fue de narcotráfico, por lo cual no es relevante porque no aporta información.
4. Si solo se menciona una vez, igual no es relevante, porque no aporta información.
5. Si se menciona una cantidad media de veces, entonces si será de relevancia porque podemos deducir que hubo una parte del discurso dedicado al tema.

Esta métrica de relevancia de ocurrencia de palabras entre palabras totales lo establece el algoritmo automáticamente, tomando como base la longitud de los mensajes, y su cantidad.

La idea clave sobre la aportación de información es la variabilidad. Si tenemos un texto con 10,000 palabras, y todas las palabras son iguales, entonces no hay información discernible. Si todas las palabras son diferentes, tampoco habrá información ni patrón que podamos seguir. Si por el contrario, hay cierta cantidad de información, entonces podemos tratar de identificar el patrón y seguirlo.

![Intuición del algoritmo](https://i.imgur.com/SohEw9A.png?1)

## Datos
Utilizando la API gratuita de Twitter, se recolectaron tweets acotados a la CDMX durante 45 días, buscando las palabras o frases específicas mostradas arriba que COPRED detectó en su ejercicio empírico.

El API gratuito de Twitter tiene limitantes en cuanto al número de mensajes que pueden descargarse, así que se tuvo que realizar esta tarea de manera programática, separando los queries a la API por palabra o frase, y a razón de 300 mensajes por día.

En total, se cuenta con una base de 12,000 tuits de la CDMX entre los meses de Abril, Mayo y Junio.

Este repositorio contiene todos los datos recolectados en `discriminating-words/data/tweets/` y `discriminating-words/data2/tweets/`.

Aunque se han eliminado retuits y replies, algunas plataformas de consulta de Twitter más antiguas no distinguen entre la nueva y la vieja estructura de tuits, y un RT dado con una plataforma nueva puede no ser identificado por una vieja.

### Disclaimer importante sobre la densidad de mensajes

1. Es importante mencionar que la razón de tuits discriminatorios contra la cantidad de tuits totales nunca será representativa. Aún cuando hemos encontrado que la discriminación es muy virulenta, no tiene el potencial de convertirse en epidemia. En este caso de 10 mensajes, menos de 0.012 son discriminatorios. Esto es un problema común en cualquier esfuerzo de Artificial Intelligence, donde frecuentemente la señal es demasiado tenue para ser identificada entre el ruido, y generar las ecuaciones y modelos que puedan extraerla.

2. También es importante considerar las coyunturas, y el momento en el que recogimos los tuits fue en medio del mundial de fútbol. Las coyunturas agregan ruido focalizado a las conversaciones. El efecto es que surge argot y jerga que puede ser relevante, solo en el contexto de la coyuntura, tal que, por ejemplo, la palabra "puto", dirigido a algún equipo, puede no ser detectado por este modelo.

3. Finalmente, es importante declarar que los datos recabados son generados desde procesos humanos de comunicación, y como todo proceso humano, es falible, y esta falibilidad se reflejará en sesgos. La manera de suavizar el ruido que introducen los sesgos es recabando mayor número de observaciones y de más tipos, tal que las variaciones que existan en algunas, sean canceladas por las variaciones en otras.

### DEBILIDADES DEL PRODUCTO
1. Tiene datos muy viejos
2. Tiene datos solo de TW
3. Tiene datos taggeados de CDMX
4. Solo busca palabras, cuando debe buscar frases y con contexto

Dadas las debilidades arriba mencionadas, SocialTIC y la Sociedad Mexicana de Ciencia de Datos ha decidido iterar una 2a vez sobre este proyecto, con las siguiente especificación.

# DISCRIMINAMÓMETRO

## Siguientes Pasos - Summer of Data
El *Summer of Data* propone que este proyecto evolucione a su 2a iteración.

Lo que se propone es un **"discriminamómetro"**, un producto de datos que esté tomando diariamente una muestra de tuits y tome *la temperatura del uso de lenguaje discriminatorio*, concentrándose en eventos o coyunturas que traigan al spotlight este lenguaje (i.e. #blacklivesmatter, #mexicoracista, etc).

Los elementos del tablero son:
1. Discriminamómetro (semáforo con 3 niveles: rojo - evento o coyuntura de discriminación presente o en las últimas 48h, amarillo - discriminación elevada, verde: discriminación a niveles normales (acoso por afición deportiva, etc). Ojo que los semáforos no son inmediatos, sino sensan *acumulación* del fenómeno.
2. Top 5 motivos de discriminación en el TW actual de MX de acuerdo al diccionario de CONAPRED
3. De esos motivos de discriminación, hacer el desglose del hashtag asociado y las top 5 words o phrases asociadas al fenómeno discriminatorio actual.
4. Ventana para capturar un tuit (280 chars) y correrle el modelo de clasificación para ubicarlo en la categoría de discriminación.

### Vista sugerida
https://www.clicdata.com/wp-content/uploads/2019/06/example-dashboard-014-1.png

### Mejoras sugeridas VS debilidades actuales
1. Ampliar la BD de tuits a todo el territorio nacional - esto implicará desarrollar un *descargador de tuits*.
2. Agregar a la BD de mensajes lo obtenido por Crowd Tangle de FB - otorgado por SocialTIC
3. Desarrollar un modelo probabilístico basado en Latent Dirichlet Allocation para detección de tópicos y temas discriminatorios
4. Una vez obtenidos los temas, desarrollar un modelo supervisado de clasificación
5. Desarrollo de un pipeline de adquisición y refresh de datos muestra para el semáforo

## Fases y Calendario tentativo
1. Kickoff & Inducción - 9 de Junio
2. Desarrollo de tuit downloader y Crowd Tangle downloader-  10 Junio - 17 de Junio
3. EDA de tuits y desarrollo de diccionario - 17 de Junio - 27 de Junio
4. Modelo LDA - 27 de Junio - 10 de Julio
5. Sanity check - 10 Julio - 17 Julio
5. Desarrollo de discriminamómetro - 17 Julio - 31 de Julio
5. Desarrollo de producto de datos / editorial - 1 Agosto - 14 de Agosto

### Organización sugerida
1. Líder de Proyecto: Jesús Ramos
2. Científico de Datos: Paco Paz
3. Ingeniero de Datos: Marco Julio Monroy Ayala
4. Desarrollo de infraestructura y scripts para almacenamiento de tuits desde TW, sin firehose, por el momento.
5. Desarrollo de pipeline de adquisición desde Crowd Tangle de FB (revisar si hay API)
6. CRÍTICO: saber, entender, y manipular efectivamente el algoritmo de Latent Dirichlet Allocation.
