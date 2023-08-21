# %%

#estoy jungando con streamlit para ver si funciona o no

import streamlit as st
import pandas as pd
import folium


# importamos matplotlibexpres


import plotly.express as px
# %%
a =42
# %%
 


st.title("Sabes donde estuviste el otro día?")

fichero = st.file_uploader("carga tus datos")


#-----------------------------------------------------------
import streamlit as st
import pandas as pd
import folium
from datetime import datetime
from datetime import timedelta

# Cargar el archivo CSV
df_combined = pd.read_csv('ubicaciones_historicas.csv')

# Convierte las columnas de tiempo a objetos datetime
df_combined['start_timestamp'] = pd.to_datetime(df_combined['start_timestamp'])
df_combined['end_timestamp'] = pd.to_datetime(df_combined['end_timestamp'])

# Filtros
st.sidebar.header('Filtros')
selected_distances = st.sidebar.multiselect('Selecciona una distancia:', df_combined['distance_group'].unique())
selected_confidences = st.sidebar.multiselect('Selecciona un momento del día:', df_combined['momento_del_dia'].unique())
selected_activities = st.sidebar.multiselect('Selecciona medio de transporte:', df_combined['activity_type'].unique())

# Filtro de fecha usando un rango de fechas
date_range = st.sidebar.date_input('Selecciona un rango de fechas', 
                                   min_value=df_combined['start_timestamp'].min().date(),
                                   max_value=df_combined['start_timestamp'].max().date(),
                                   value=(df_combined['start_timestamp'].min().date(), df_combined['start_timestamp'].max().date()))

# Verificar si al menos un filtro está seleccionado
if selected_distances or selected_confidences or selected_activities:
    # Filtrar el DataFrame por los valores seleccionados
    df_filtrado = df_combined[
        (df_combined['momento_del_dia'].isin(selected_confidences)) & 
        (df_combined['distance_group'].isin(selected_distances)) &
        (df_combined['activity_type'].isin(selected_activities)) &
        (df_combined['start_timestamp'].dt.date.between(date_range[0], date_range[1]))
    ]
    
    # Calcular el centro de las coordenadas
    if not df_filtrado.empty:
        center_lat = df_filtrado['start_latitude'].mean()
        center_lon = df_filtrado['start_longitude'].mean()
    else:
        # Valores de respaldo en caso de que no haya datos filtrados
        center_lat = 40.468159
        center_lon = -3.875562

    # Crear un mapa centrado en el centro calculado
    m = folium.Map(location=[center_lat, center_lon], zoom_start=10)

    # Iterar a través del DataFrame filtrado y agregar marcadores y líneas al mapa
    for index, row in df_filtrado.iterrows():
        start_lat = row['start_latitude']
        start_lon = row['start_longitude']
        end_lat = row['end_latitude']
        end_lon = row['end_longitude']
        distance = row['distance']
        duration = row['duration_formatted']

        # Verificar si la distancia o la duración son valores extremos
        is_extreme_distance = distance == df_filtrado["distance"].min() or distance == df_filtrado["distance"].max()
        is_extreme_duration = duration == df_filtrado["duration_formatted"].min() or duration == df_filtrado["duration_formatted"].max()

        # Agregar marcadores de inicio y fin con íconos de colores para valores extremos
        if is_extreme_distance or is_extreme_duration:
            folium.Marker([start_lat, start_lon], icon=folium.Icon(color='red')).add_to(m)
            folium.Marker([end_lat, end_lon], icon=folium.Icon(color='pink')).add_to(m)
        else:
            # Agregar marcadores sin íconos
            folium.Marker([start_lat, start_lon], icon=None).add_to(m)
            folium.Marker([end_lat, end_lon], icon=None).add_to(m)
        
        # Agregar líneas
        folium.PolyLine([(start_lat, start_lon), (end_lat, end_lon)], color="blue").add_to(m)

    # Calcular y mostrar la suma de la columna "distance" después del filtrado
    total_distance = df_filtrado['distance'].sum()/1000

    # Crear un texto personalizado con el rango de fechas y la distancia total
    custom_text = f'Desde "{date_range[0].strftime("%Y-%m-%d")}" hasta "{date_range[1].strftime("%Y-%m-%d")}", te has movido.'
    custom_text += f' La distancia total recorrida es de {total_distance} kms. el equivalente a {total_distance/40000} vueltas al mundo por el ecuador'
    
    # Calcular la diferencia entre las fechas de inicio y fin en segundos
    df_filtrado['duration_seconds'] = (df_filtrado['end_timestamp'] - df_filtrado['start_timestamp']).dt.total_seconds()

# Calcular la suma de la columna duration_seconds
    total_duration_seconds = df_filtrado['duration_seconds'].sum()

# Convertir el resultado en un formato legible (días, horas, minutos, segundos)
    total_duration = timedelta(seconds=total_duration_seconds)
    days = total_duration.days
    seconds = total_duration.seconds
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

# Mostrar el resultado
    st.write(custom_text) 
    st.write(f'Total de tiempo moviéndote: {days:02d} dias {hours:02d} horas {minutes:02d} minutos {seconds:02d} segundos')
   

    


    # Mostrar el mapa en Streamlit
    st.components.v1.html(m._repr_html_(), width=800, height=600)
    
    # Mostrar el rango de fechas seleccionado
    # st.write(f'Desde {date_range[0]} hasta {date_range[1]}, te has movido.')

else:
    st.warning('Por favor, selecciona en los filtros para generar conocimiento máximo .')
