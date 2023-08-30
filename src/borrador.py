# Configuración de la página de Streamlit
st.title("Te mueves más que los ojos de Espinete")

# Componente para ingresar la ruta de la carpeta
root_folder = st.text_input("Ingresa la ruta de la carpeta que deseas procesar:")

# Verificar si se ha ingresado una ruta
if root_folder:
    st.title("Hoy descubrirás que te mueves mucho, pero no vas a ninguna parte")

    try:
        st.info(f"Procesando la carpeta en la ruta: {root_folder}")
        sp.proceso_completo(root_folder)
        st.success("Procesamiento completado exitosamente.")
    except Exception as e:
        st.error(f"Ocurrió un error al procesar los datos: {str(e)}")




        # Gráfico de barras para tiempo promedio por tipo de transporte
    st.subheader('Tiempo Promedio por Tipo de Transporte')
    chart_time = px.bar(df_combined, x='activity_type', y='duration_seconds', title='Tiempo Promedio por Tipo de Transporte')
    chart_time.update_xaxes(title_text='Tipo de Transporte')
    chart_time.update_yaxes(title_text='Tiempo Promedio (segundos)')
    st.plotly_chart(chart_time)
