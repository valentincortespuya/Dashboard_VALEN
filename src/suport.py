import pandas as pd

import os
import pandas as pd
from datetime import datetime

# Función para convertir coordenadas en formato E7 a valores decimales
def e7_to_decimal(e7_value):
    if e7_value is None:
        return None
    return e7_value * 1e-7

# Función para formatear coordenadas en formato decimal a español con comas
def format_coordinates(latitude, longitude):
    if latitude is None or longitude is None:
        return None
    return f"{latitude:.7f}, {longitude:.7f}"

# Función para convertir una cadena ISO8601 en un objeto datetime
def iso8601_to_datetime(iso8601_string):
    if iso8601_string is None:
        return None
    try:
        return datetime.strptime(iso8601_string, '%Y-%m-%dT%H:%M:%S.%fZ')
    except ValueError:
        return datetime.strptime(iso8601_string, '%Y-%m-%dT%H:%M:%SZ')

# Función para calcular la duración formateada
def format_duration(start_timestamp, end_timestamp):
    if start_timestamp is None or end_timestamp is None:
        return None
    
    # Calcular la diferencia en segundos
    time_difference = (end_timestamp - start_timestamp).total_seconds()
    
    # Calcular los componentes de la duración en días, horas, minutos y segundos
    days = int(time_difference // (24 * 3600))
    time_difference %= 24 * 3600
    hours = int(time_difference // 3600)
    time_difference %= 3600
    minutes = int(time_difference // 60)
    seconds = int(time_difference % 60)
    
    # Formatear la duración en el formato "DD:HH:MM:SS"
    duration_formatted = f"{days:02d}:{hours:02d}:{minutes:02d}:{seconds:02d}"
    return duration_formatted

# Función para convertir el timestamp en el momento del día
def timestamp_to_moment(timestamp):
    if timestamp is None:
        return None
    hour = timestamp.hour
    if 5 <= hour < 12:
        return "mañana"
    elif 12 <= hour < 16:
        return "medio día"
    elif 16 <= hour < 21:
        return "tarde"
    else:
        return "noche"

# Función para agrupar la distancia en bloques
def group_distance(distance):
    if pd.isna(distance):
        return "desconocido"
    elif distance < 1000:
        return "menos de 1km"
    elif 1000 <= distance < 10000:
        return "de 1km a 10km"
    elif 10000 <= distance < 100000:
        return "de 10km a 100km"
    else:
        return "más de 100km"
    


def proceso_completo(root_folder):
    # Lista para almacenar todos los DataFrames resultantes
    all_dfs = []

    # Recorrer todas las carpetas desde "2022" hasta "2023"
    for year in range(2021, 2024):
        year_folder = os.path.join(root_folder, str(year))
        if os.path.exists(year_folder):
            # Recorrer todas las carpetas y subcarpetas dentro de cada año
            for dirpath, dirnames, filenames in os.walk(year_folder):
                for filename in filenames:
                    if filename.endswith('.json'):
                        # Leer el archivo JSON y cargarlo como un DataFrame
                        file_path = os.path.join(dirpath, filename)
                        df = pd.read_json(file_path)

                        # Extraer columnas 'timelineObjects' y expandir en un nuevo DataFrame
                        df2 = df['timelineObjects'].apply(pd.Series)

                        # Eliminar filas con NaN en la columna 'activitySegment'
                        df2_cleaned = df2.dropna(subset=['activitySegment'])

                        # Aplicar las funciones de extracción y transformación de datos
                        df_extracted = df2_cleaned['activitySegment'].apply(extract_data)
                        df_extracted['momento_del_dia'] = df_extracted['start_timestamp'].apply(timestamp_to_moment)
                        df_extracted['distance_group'] = df_extracted['distance'].apply(group_distance)

                        # Concatenar las columnas extraídas con el DataFrame original
                        df_final = pd.concat([df2_cleaned, df_extracted], axis=1)

                        # Eliminar la columna original 'activitySegment' que contenía los datos completos (opcional)
                        df_final = df_final.drop(columns=['activitySegment'])

                        # Agregar el DataFrame resultante a la lista
                        all_dfs.append(df_final)

    # Concatenar todos los DataFrames en uno solo
    df_combined = pd.concat(all_dfs, ignore_index=True)

    # Mapeo de los valores de la columna 'activity_type'
    mapping = {
        'IN_PASSENGER_VEHICLE': 'COCHE',
        'IN_BUS': 'BUS',
        'IN_TRAIN': 'TREN',
        'WALKING': 'ANDANDO',
        'IN_SUBWAY': 'METRO',
        'UNKNOWN_ACTIVITY_TYPE': 'OTROS',
        'FLYING': 'AVION',
        'CYCLING': 'BICI',
        'IN_FERRY': 'BARCO'
    }

    # Reemplazar los valores en la columna 'activity_type'
    df_combined['activity_type'] = df_combined['activity_type'].replace(mapping)

    # Exportar el DataFrame combinado a un archivo CSV
    df_combined.to_csv("ubicaciones_historicas.csv", index=False)


