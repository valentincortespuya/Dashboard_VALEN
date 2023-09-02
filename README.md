# Dashboard de movimiento usando los datos de google recopilados por tu teléfono.
En este trabajo vas a encontrar un Dashboard para anlizar los datos extraidos desde google sobre los movimientos que se han realizado. 

Google utiliza varias técnicas y fuentes de datos para recopilar información de movilidad a través de los teléfonos móviles. Estas son algunas de las formas en las que Google obtiene datos de movilidad:

Servicios de ubicación: Google recopila datos de ubicación a través de servicios de ubicación en dispositivos móviles, como el GPS, las redes móviles y Wi-Fi. Cuando un dispositivo Android tiene la función de ubicación habilitada, Google puede rastrear su ubicación en tiempo real.

Aplicaciones y servicios de Google: Muchas aplicaciones y servicios de Google, como Google Maps, recopilan datos de ubicación de forma activa para proporcionar servicios basados en la ubicación, como mapas, direcciones y recomendaciones locales.

Historial de ubicaciones: Si has habilitado la función "Historial de ubicaciones" en tu cuenta de Google, la compañía puede rastrear y almacenar un historial detallado de tus movimientos a lo largo del tiempo. Esto se utiliza para ofrecer información sobre el tráfico en tiempo real y recomendaciones personalizadas.

Sensores del dispositivo: Los teléfonos inteligentes modernos están equipados con una variedad de sensores, como acelerómetros y giroscopios. Google puede utilizar estos sensores para detectar automáticamente tu movimiento y velocidad, lo que les permite inferir si estás caminando, conduciendo, montando en bicicleta, etc.

Datos de aplicaciones de terceros: Google permite a las aplicaciones de terceros acceder a la ubicación del dispositivo si el usuario lo autoriza. Estas aplicaciones pueden compartir datos de ubicación con Google, aunque Google ha implementado restricciones y políticas de privacidad para controlar cómo se utilizan estos datos.

Información de torres de telefonía y puntos de acceso Wi-Fi: Google recopila datos de ubicación basados en la proximidad a torres de telefonía móvil y puntos de acceso Wi-Fi cercanos. Esto se utiliza para mejorar la precisión de la ubicación en áreas urbanas y densamente pobladas.

Colaboración con otros servicios de mapeo y navegación: Google también colabora con otros servicios de mapeo y navegación para recopilar datos de movilidad y mejorar la precisión de sus propios servicios.

# Toda esta información la puedes desgargar siguiendo estos pasos:
Accede a tu Cuenta de Google: Abre un navegador web y ve a la página de inicio de sesión de Google en https://accounts.google.com.

Inicia sesión: Ingresa tu dirección de correo electrónico y contraseña para acceder a tu cuenta de Google.

Accede a tu Historial de Ubicaciones: Una vez que hayas iniciado sesión, haz clic en tu imagen de perfil (o inicial) en la esquina superior derecha de la página y selecciona "Cuenta de Google".

Accede a la sección "Datos y personalización": En la página de tu cuenta, desplázate hacia abajo y busca la sección llamada "Datos y personalización". Haz clic en "Administrar tus datos y personalización".

Accede a la configuración de actividad de ubicación: En la sección "Datos y personalización", busca la opción "Actividad de ubicación" y haz clic en ella.

Ver tu Historial de Ubicaciones: Aquí podrás ver y administrar tu historial de ubicaciones. Si deseas descargar tus datos de ubicación, busca la sección "Historial de ubicaciones" y haz clic en "Administrar actividad".

Descargar tus Datos de Ubicación: En la página de historial de ubicaciones, verás un icono de engranaje o tres puntos verticales en la parte superior derecha. Haz clic en él y selecciona "Descargar".

Configurar tu solicitud de descarga: Te llevará a una página donde puedes configurar tu solicitud de descarga. Aquí puedes seleccionar el rango de fechas para los datos que deseas descargar y el tipo de archivo. Por lo general, se recomienda seleccionar el formato ZIP y dejar las demás opciones como están.

Solicitar la descarga: Después de configurar tus preferencias, haz clic en el botón "Siguiente" o "Crear archivo" para iniciar la solicitud de descarga.

Verificar tu identidad: Dependiendo de la configuración de seguridad de tu cuenta, es posible que se te solicite que verifiques tu identidad a través de un mensaje de texto o correo electrónico.

Descargar tus datos: Una vez que se haya verificado tu identidad, Google comenzará a preparar tus datos para su descarga. Esto puede llevar algún tiempo, especialmente si tienes un historial de ubicaciones extenso. Recibirás un correo electrónico cuando tus datos estén listos para descargar.

Descarga tus datos: Abre el correo electrónico que recibiste de Google y sigue las instrucciones para descargar tus datos de ubicación.

Una vez que hayas descargado tus datos, tendrás un archivo comprimido (ZIP) que contiene la información de ubicación en formato que puedes explorar o utilizar según tus necesidades. Puedes abrirlo en tu computadora para ver tus registros de ubicación.

# limpieza de los datos

Una vez decargados los datos tendrás que limpiarlos. En el archivo /Extraccion_datos_google_maps-Copy1.ipynb
tienes como preparar un csv que te permitirá empezar con la visualización
OJO: este código tiene que ser repasado porque en la última descarga, el código no ha funcionado debido a un cambio en la entrega de los datos. 

# ¿para que sirve?
## Comparador de Movimientos
Este proyecto utiliza la biblioteca Streamlit para crear una aplicación web interactiva que permite comparar los datos de movilidad de dos usuarios (Usuario A y Usuario B) a partir de archivos CSV de ubicaciones históricas. La aplicación presenta información sobre los movimientos de los usuarios, incluyendo estadísticas de distancia, duración, medios de transporte utilizados y patrones de actividad diaria.

## Características Principales
### Filtrado de Datos
Los usuarios pueden aplicar filtros basados en:
Distancia recorrida.
Momento del día.
Medio de transporte utilizado.
Rango de fechas.
### Análisis de Datos
La aplicación calcula y muestra información como:
Distancia total recorrida en kilómetros.
Cantidad de "vueltas al mundo" basadas en la distancia recorrida.
Tiempo total de movimiento en días, horas, minutos y segundos.
Gráficos de barras que muestran la distancia media por tipo de transporte.
Tablas que muestran la cantidad de veces que se utilizó cada tipo de transporte.
Calendarios que resaltan los días en los que se realizaron más actividades.
### Visualización de Mapas
Se utiliza la biblioteca Folium para visualizar los movimientos en un mapa interactivo.
Se marcan los puntos de inicio y fin de los movimientos, y se traza una línea que representa el recorrido.
Los movimientos extremos se destacan con iconos de colores en el mapa.

### Configuración y Uso
Clona este repositorio en tu sistema local.
Asegúrate de tener todas las bibliotecas requeridas instaladas (Streamlit, Pandas, Folium, Plotly Express, entre otras).
Coloca los archivos CSV de ubicaciones históricas para Usuario A y Usuario B en el mismo directorio y asegúrate de que estén nombrados como 'ubicaciones_historicas_usuario1.csv' y 'ubicaciones_historicas_usuario2.csv', respectivamente.
Ejecuta la aplicación Streamlit utilizando el comando streamlit run nombre_del_archivo.py, donde nombre_del_archivo.py es el nombre de tu script.
### Notas
Los archivos CSV de ubicaciones históricas deben contener columnas como 'start_timestamp', 'end_timestamp', 'start_latitude', 'start_longitude', 'end_latitude', 'end_longitude', 'distance', 'duration_formatted', 'momento_del_dia' y 'activity_type'.

## Siguientes Pasos

Lo primero que tengo que hacer es finalizar el código y ver como evitar que los cambios en las entregas de google afecten a todo.
Lo segundo que quiero llevar a cabo es la generación de parcelas que permitan localizar puntos calientes y saber así cuales son los destinos mas frecuentados. (google te puede dar varios cientos de coordenadas muy similares pero no exactas para la misma posicion geográfica, por ejemplo tu casa.)
Otra de las cosas que quiero ver es si la visualización de los mapas puede mejorar con otros sistemas como kepler. 
Utilizar machile learning para rellenar huecos en esas fechas en las que no he llevado mi teléfono conmigo. 
Ver como el usuario puede encontrar posiblidades de eficiencia en sus vidas con estos datos tales como: Usar un medio de trasnsporte frente a otro.



