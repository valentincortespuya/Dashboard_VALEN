import streamlit as st
import pandas as pd
import folium
import plotly.express as px
from datetime import datetime
from datetime import timedelta
from PIL import Image
import numpy as np
import calplot
import matplotlib.pyplot as plt
import tempfile
import pylab

st.set_page_config(layout = 'wide', initial_sidebar_state = 'collapsed', page_title = '', page_icon = '')

# Título principal
st.title("Comparador de Movimientos")
st.subheader('Usando los filtros podrás analizar tus movimientos y encontrar patrones curiosos', divider='rainbow')
st.subheader('seguro que cambias algo tras el  :blue[analisis] :sunglasses:')
st.text
col1, col2 = st.columns(2)

# Usuario 1
with col1:
    st.header("Momento A")
    df_user1 = pd.read_csv('ubicaciones_historicas_usuario1.csv')
    
    df_user1['start_timestamp'] = pd.to_datetime(df_user1['start_timestamp'])
    df_user1['end_timestamp'] = pd.to_datetime(df_user1['end_timestamp'])
    
    st.sidebar.header('Momento A')
    selected_distances_user1 = st.sidebar.multiselect('Selecciona una distancia A:', df_user1['distance_group'].unique())
    selected_confidences_user1 = st.sidebar.multiselect('Selecciona un momento del día A:', df_user1['momento_del_dia'].unique())
    selected_activities_user1 = st.sidebar.multiselect('Selecciona medio de transporte A:', df_user1['activity_type'].unique())
    
    date_range_user1 = st.sidebar.date_input('Selecciona un rango de fechas A', 
                                    min_value=df_user1['start_timestamp'].min().date(),
                                    max_value=df_user1['start_timestamp'].max().date(),
                                    value=(df_user1['start_timestamp'].min().date(), df_user1['start_timestamp'].max().date()))

    if selected_distances_user1 or selected_confidences_user1 or selected_activities_user1:
        df_filtrado_user1 = df_user1[
            (df_user1['momento_del_dia'].isin(selected_confidences_user1)) & 
            (df_user1['distance_group'].isin(selected_distances_user1)) &
            (df_user1['activity_type'].isin(selected_activities_user1)) &
            (df_user1['start_timestamp'].dt.date.between(date_range_user1[0], date_range_user1[1]))
        ]
        
        distancia_media_por_transporte_user1 = df_filtrado_user1.groupby('activity_type')['distance'].mean().reset_index()

        if not df_filtrado_user1.empty:
            center_lat_user1 = df_user1['start_latitude'].mean()
            center_lon_user1 = df_user1['start_longitude'].mean()
        else:
            center_lat_user1 = 40.468159
            center_lon_user1 = -3.875562

        m_user1 = folium.Map(location=[center_lat_user1, center_lon_user1], zoom_start=10)

        for index, row in df_filtrado_user1.iterrows():
            start_lat_user1 = row['start_latitude']
            start_lon_user1 = row['start_longitude']
            end_lat_user1 = row['end_latitude']
            end_lon_user1 = row['end_longitude']
            distance_user1 = row['distance']
            duration_user1 = row['duration_formatted']

            is_extreme_distance_user1 = distance_user1 == df_filtrado_user1["distance"].min() or distance_user1 == df_filtrado_user1["distance"].max()
            is_extreme_duration_user1 = duration_user1 == df_filtrado_user1["duration_formatted"].min() or duration_user1 == df_filtrado_user1["duration_formatted"].max()

            if is_extreme_distance_user1 or is_extreme_duration_user1:
                folium.Marker([start_lat_user1, start_lon_user1], icon=folium.Icon(color='red')).add_to(m_user1)
                folium.Marker([end_lat_user1, end_lon_user1], icon=folium.Icon(color='pink')).add_to(m_user1)
            else:
                folium.Marker([start_lat_user1, start_lon_user1], icon=None).add_to(m_user1)
                folium.Marker([end_lat_user1, end_lon_user1], icon=None).add_to(m_user1)
            
            folium.PolyLine([(start_lat_user1, start_lon_user1), (end_lat_user1, end_lon_user1)], color="blue").add_to(m_user1)

        total_distance_user1 = df_filtrado_user1['distance'].sum()/1000

        custom_text_user1 = f'Desde "{date_range_user1[0].strftime("%Y-%m-%d")}" hasta "{date_range_user1[1].strftime("%Y-%m-%d")}", te has movido.'
        
        st.write(custom_text_user1)
        col3, col4= st.columns(2)

        with col3:
            
            st.markdown('total distance')
            st.metric(label='km', value = total_distance_user1)

        with col4:
            
            st.markdown('vueltas al mundo')
            st.metric(label='vueltas al mundo', value = total_distance_user1/40000)

       

       # Calcular la diferencia entre las fechas de inicio y fin en segundos
        df_filtrado_user1['duration_seconds'] = (df_filtrado_user1['end_timestamp'] - df_filtrado_user1['start_timestamp']).dt.total_seconds()

        # Calcular la suma de la columna duration_seconds
        total_duration_seconds_user1 = df_filtrado_user1['duration_seconds'].sum()

        # Convertir el resultado en un formato legible (días, horas, minutos, segundos)
        total_duration_user1 = timedelta(seconds=total_duration_seconds_user1)
        days_user1 = total_duration_user1.days
        seconds_user1 = total_duration_user1.seconds
        hours_user1, remainder_user1 = divmod(seconds_user1, 3600)
        minutes_user1, seconds_user1 = divmod(remainder_user1, 60)

        # Mostrar el resultado
        st.write(f'Total de tiempo moviéndote: {days_user1:02d} días {hours_user1:02d} horas {minutes_user1:02d} minutos {seconds_user1:02d} segundos')

        # Mostrar el mapa en Streamlit
        st.components.v1.html(m_user1._repr_html_(), width=400, height=300)
       
        
        # Gráfico de barras para la distancia media por tipo de transporte
        st.subheader('Distancia Media por Tipo de Transporte - A')
        chart_distance_user1 = px.bar(distancia_media_por_transporte_user1, x='activity_type', y='distance', title='Distancia Media por Tipo de Transporte - Usuario 1')
        chart_distance_user1.update_xaxes(title_text='Tipo de Transporte')
        chart_distance_user1.update_yaxes(title_text='Distancia Media (metros)')
        st.plotly_chart(chart_distance_user1)
        
        # Calcular la cantidad de veces que se han usado los diferentes medios de transporte
        transport_counts_user1 = df_filtrado_user1['activity_type'].value_counts()
        
        st.subheader('Cantidad de veces que has desplazado en... - A')
        # Mostrar los contadores de uso de medios de transporte en un formato de tabla
        st.write(transport_counts_user1)
        #grafico
        df_filtrado_user1['start_timestamp'] = pd.to_datetime(df_filtrado_user1['start_timestamp'])

        actividades_por_dia = df_filtrado_user1.groupby(df_filtrado_user1['start_timestamp'].dt.floor('D'))['activity_type'].count()
        st.subheader('Y en que días te mueves más... - A')
        fig = calplot.calplot(actividades_por_dia,
                    suptitle='Calendario',
                    suptitle_kws={'x': 0.0, 'y': 1.0})
        
        plt.savefig('temp_calendar.png')
        plt.show()
        # Muestra la figura en Streamlit
        st.image('temp_calendar.png')
        
                
    else:
        st.warning('Por favor, selecciona filtros para generar información.')
        # Cargar una imagen desde tu sistema de archivos local
        image_user1 = Image.open('estaciones.jpg')  # Cambio la imagen para el Usuario 1

        # Mostrar la imagen en Streamlit
        st.image(image_user1, caption='Crees que te mueves lo mismo en vernano que en invierno, por la mañana que por la tarde...', use_column_width=True)



# Usuario 2
with col2:
    st.header("Momento B")
    
    # Cargar el archivo CSV para el Usuario 2
    df_user2 = pd.read_csv('ubicaciones_historicas_usuario2.csv')  # Reemplaza 'ubicaciones_historicas_usuario2.csv' con el nombre del archivo del Usuario 2
    
    # Convierte las columnas de tiempo a objetos datetime
    df_user2['start_timestamp'] = pd.to_datetime(df_user2['start_timestamp'])
    df_user2['end_timestamp'] = pd.to_datetime(df_user2['end_timestamp'])
    
    # Filtros para el Usuario 2
    st.sidebar.header('Momento B')
    selected_distances_user2 = st.sidebar.multiselect('Selecciona una distancia b:', df_user2['distance_group'].unique())
    selected_confidences_user2 = st.sidebar.multiselect('Selecciona un momento del día B:', df_user2['momento_del_dia'].unique())
    selected_activities_user2 = st.sidebar.multiselect('Selecciona medio de transporte B:', df_user2['activity_type'].unique())
    
    # Filtro de fecha usando un rango de fechas
    date_range_user2 = st.sidebar.date_input('Selecciona un rango de fechas B', 
                                    min_value=df_user2['start_timestamp'].min().date(),
                                    max_value=df_user2['start_timestamp'].max().date(),
                                    value=(df_user2['start_timestamp'].min().date(), df_user2['start_timestamp'].max().date()))

    # Verificar si al menos un filtro está seleccionado
    if selected_distances_user2 or selected_confidences_user2 or selected_activities_user2:
        # Filtrar el DataFrame por los valores seleccionados
        df_filtrado_user2 = df_user2[
            (df_user2['momento_del_dia'].isin(selected_confidences_user2)) & 
            (df_user2['distance_group'].isin(selected_distances_user2)) &
            (df_user2['activity_type'].isin(selected_activities_user2)) &
            (df_user2['start_timestamp'].dt.date.between(date_range_user2[0], date_range_user2[1]))
        ]
        # Calcular la distancia media por tipo de transporte
        distancia_media_por_transporte_user2 = df_filtrado_user2.groupby('activity_type')['distance'].mean().reset_index()

        # Calcular el centro de las coordenadas
        if not df_filtrado_user2.empty:
            center_lat_user2 = df_filtrado_user2['start_latitude'].mean()
            center_lon_user2 = df_filtrado_user2['start_longitude'].mean()
        else:
            # Valores de respaldo en caso de que no haya datos filtrados
            center_lat_user2 = 40.468159
            center_lon_user2 = -3.875562

        # Crear un mapa centrado en el centro calculado
        m_user2 = folium.Map(location=[center_lat_user2, center_lon_user2], zoom_start=10)

        # Iterar a través del DataFrame filtrado y agregar marcadores y líneas al mapa
        for index, row in df_filtrado_user2.iterrows():
            start_lat_user2 = row['start_latitude']
            start_lon_user2 = row['start_longitude']
            end_lat_user2 = row['end_latitude']
            end_lon_user2 = row['end_longitude']
            distance_user2 = row['distance']
            duration_user2 = row['duration_formatted']

            # Verificar si la distancia o la duración son valores extremos
            is_extreme_distance_user2 = distance_user2 == df_filtrado_user2["distance"].min() or distance_user2 == df_filtrado_user2["distance"].max()
            is_extreme_duration_user2 = duration_user2 == df_filtrado_user2["duration_formatted"].min() or duration_user2 == df_filtrado_user2["duration_formatted"].max()

            # Agregar marcadores de inicio y fin con íconos de colores para valores extremos
            if is_extreme_distance_user2 or is_extreme_duration_user2:
                folium.Marker([start_lat_user2, start_lon_user2], icon=folium.Icon(color='red')).add_to(m_user2)
                folium.Marker([end_lat_user2, end_lon_user2], icon=folium.Icon(color='pink')).add_to(m_user2)
            else:
                # Agregar marcadores sin íconos
                folium.Marker([start_lat_user2, start_lon_user2], icon=None).add_to(m_user2)
                folium.Marker([end_lat_user2, end_lon_user2], icon=None).add_to(m_user2)
            
            # Agregar líneas
            folium.PolyLine([(start_lat_user2, start_lon_user2), (end_lat_user2, end_lon_user2)], color="blue").add_to(m_user2)

        # Calcular y mostrar la suma de la columna "distance" después del filtrado
        total_distance_user2 = df_filtrado_user2['distance'].sum()/1000
        custom_text_user2 = f'Desde "{date_range_user2[0].strftime("%Y-%m-%d")}" hasta "{date_range_user1[1].strftime("%Y-%m-%d")}", te has movido.'

        st.write(custom_text_user2)
        
        col5, col6= st.columns(2)

        with col5:
            
            st.markdown('total distance')
            st.metric(label='km', value = total_distance_user2)

        with col6:
            
            st.markdown('vueltas al mundo')
            st.metric(label='vueltas al mundo', value = total_distance_user2/40000)

        # Calcular la diferencia entre las fechas de inicio y fin en segundos
        df_filtrado_user2['duration_seconds'] = (df_filtrado_user2['end_timestamp'] - df_filtrado_user2['start_timestamp']).dt.total_seconds()

        # Calcular la suma de la columna duration_seconds
        total_duration_seconds_user2 = df_filtrado_user2['duration_seconds'].sum()

        # Convertir el resultado en un formato legible (días, horas, minutos, segundos)
        total_duration_user2 = timedelta(seconds=total_duration_seconds_user2)
        days_user2 = total_duration_user2.days
        seconds_user2 = total_duration_user2.seconds
        hours_user2, remainder_user2 = divmod(seconds_user2, 3600)
        minutes_user2, seconds_user2 = divmod(remainder_user2, 60)

        # Mostrar el resultado
        
        st.write(f'Total de tiempo moviéndote: {days_user2:02d} días {hours_user2:02d} horas {minutes_user2:02d} minutos {seconds_user2:02d} segundos')

        # Mostrar el mapa en Streamlit
        st.components.v1.html(m_user2._repr_html_(), width=400, height=300)
        
        # Gráfico de barras para la distancia media por tipo de transporte
        st.subheader('Distancia Media por Tipo de Transporte - B')
        chart_distance_user2 = px.bar(distancia_media_por_transporte_user2, x='activity_type', y='distance', title='Distancia Media por Tipo de Transporte - Usuario 2')
        chart_distance_user2.update_xaxes(title_text='Tipo de Transporte')
        chart_distance_user2.update_yaxes(title_text='Distancia Media (metros)')
        st.plotly_chart(chart_distance_user2)
         # Calcular la cantidad de veces que se han usado los diferentes medios de transporte
        transport_counts_user2 = df_filtrado_user2['activity_type'].value_counts()
        
        st.subheader('Cantidad de veces que has desplazado en... - B')
        # Mostrar los contadores de uso de medios de transporte en un formato de tabla
        st.write(transport_counts_user2)
        df_user1['start_timestamp'] = pd.to_datetime(df_user1['start_timestamp'])

        # Configura el índice como un DatetimeIndex
        actividades_por_dia = df_user1.groupby(df_user1['start_timestamp'].dt.floor('D'))['activity_type'].count()

        #grafico
        df_filtrado_user2['start_timestamp'] = pd.to_datetime(df_filtrado_user2['start_timestamp'])

        actividades_por_dia = df_filtrado_user2.groupby(df_filtrado_user2['start_timestamp'].dt.floor('D'))['activity_type'].count()
        st.subheader('Y en que días te mueves más... - B')
        fig = calplot.calplot(actividades_por_dia,
                    suptitle='Calendario',
                    suptitle_kws={'x': 0.0, 'y': 1.0})
        
        plt.savefig('temp_calendar.png')
        plt.show()
        # Muestra la figura en Streamlit
        st.image('temp_calendar.png')
    else:
        st.warning('Por favor, selecciona filtros para generar información.')  # Cambio el mensaje para el Usuario 2
        # Cargar una imagen desde tu sistema de archivos local
        image_user2 = Image.open('estaciones.jpg')  # Cambio la imagen para el Usuario 2

        # Mostrar la imagen en Streamlit
        st.image(image_user2, caption='...ya te digo yo que YO no.', use_column_width=True)
