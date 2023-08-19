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

st.text("aqui voy a explicar los filtros")


st.title("tu ruta mas corta")

# Ruta al archivo HTML
ruta_html = "mapa_con_lineas.html"

# Leer el contenido del archivo HTML
with open(ruta_html, "r") as archivo_html:
    contenido_html = archivo_html.read()

# Mostrar el HTML en Streamlit
st.components.v1.html(contenido_html, width=200, height=150)
#-----------------------------------------------------------
import streamlit as st
import pandas as pd
import folium

# Cargar el archivo CSV
df_combined = pd.read_csv('ubicaciones_historicas.csv')

# Filtros
st.sidebar.header('Filtros')
selected_distance = st.sidebar.selectbox('Selecciona una distancia:', df_combined['distance_group'].unique())
selected_confidence = st.sidebar.selectbox('Selecciona una confianza:', df_combined['momento_del_dia'].unique())
selected_activity = st.sidebar.selectbox('Selecciona un tipo de actividad:', df_combined['activity_type'].unique())

# Verificar si todos los filtros están seleccionados
if selected_distance and selected_confidence and selected_activity:
    # Filtrar el DataFrame por los valores seleccionados
    df_filtrado = df_combined[(df_combined['momento_del_dia'] == selected_confidence) & 
                              (df_combined['distance_group'] == selected_distance) &
                              (df_combined['activity_type'] == selected_activity)]
    
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

    # Iterar a través del DataFrame filtrado y agregar marcadores al mapa
    for index, row in df_filtrado.iterrows():
        start_lat = row['start_latitude']
        start_lon = row['start_longitude']
        end_lat = row['end_latitude']
        end_lon = row['end_longitude']
        
        if not pd.isna(start_lat) and not pd.isna(start_lon) and not pd.isna(end_lat) and not pd.isna(end_lon):
            folium.Marker([start_lat, start_lon]).add_to(m)
            folium.Marker([end_lat, end_lon]).add_to(m)
            folium.PolyLine([(start_lat, start_lon), (end_lat, end_lon)], color="blue").add_to(m)

    # Mostrar el mapa en Streamlit
    st.components.v1.html(m._repr_html_(), width=800, height=600)

    # Crear un DataFrame auxiliar para mostrar las columnas debajo del mapa
    if not df_filtrado.empty:
        df_info = df_filtrado[['start_timestamp', 'end_timestamp', 'duration_formatted']]
        st.write('Información adicional:')
        st.write(df_info)
else:
    st.warning('Por favor, selecciona una distancia, una confianza y un tipo de actividad para mostrar el mapa y la información adicional.')
