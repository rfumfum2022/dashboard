import streamlit as st
#import streamlit.components.v1 as components
import pandas as pd
from PIL import Image
#import matplotlib.pyplot as plt
#import altair as alt
#import pygwalker as pyg

def app():
    #set page
    im = Image.open("LOGO_IES_Andres_Bello.ico")
    #st.set_page_config(page_title="Analytics Dashboard", page_icon = im, layout="wide")  
    st.subheader("📈 I.E.S. ANDRéS BELLO - DASHBOARD ")

    st.title(':clipboard: Análisis ANOTACIONES') #Titulo del Dash
    #st.subheader('1ª EVALUACIóN')
    st.markdown('##') #Para separar el titulo de los KPIs, se inserta un paragrafo usando un campo de markdown

    #st.sidebar.header('Dashboard')

    st.link_button('Normativa Convivencia Escolar', 
                'https://www.gobiernodecanarias.org/educacion/web/servicios/convivencia_escolar/decreto-convivencia/',
                type='primary')
    @st.cache_data

    def load_data(file):
        if file == "Excel":
            df_anotaciones = pd.read_excel(file, engine='openpyxl',errors='ignore')
            df_anotaciones.drop(['ESTUDIO', 'TURNO'], axis=1, inplace=True)    

            #df_t = openpyxl.load_workbook(file)
        else:
            #columnas = ["Grupo_Clase","Primer_apellido","Segundo_apellido","Nombre","Materia","Materia_curso","Nombre_materia","Fecha","Evaluacion","Nota"] 
            df_anotaciones = pd.read_csv(file)
            df_anotaciones.drop(['TURNO'], axis=1, inplace=True) 
            #df_anotaciones.columns = columnas 
        return df_anotaciones

    # Seleccionar tipo de archivo
    tipo_archivo = st.radio("Seleccione el tipo de archivo", ("Excel", "CSV"))
    uploaded_file = st.file_uploader(f"Subir archivo {tipo_archivo}", type=["csv", "xlsx"])

    if uploaded_file is None:
        st.info('Subir un fichero',icon="ℹ️")
        st.stop()

    df_anotaciones = load_data(uploaded_file)
    # def cargar_dataframe():
    #     try:
    #         df_anotaciones = pd.read_csv('/Users/rfumfum/Documents/PYTHON/Dashboard/project_ies/Anotaciones_2023.csv')
    #     #Eliminar las columnas 'ESTUDIO' y 'TURNO' del DataFrame df_anotaciones
    #         df_anotaciones.drop(['ESTUDIO', 'TURNO'], axis=1, inplace=True)    
    #     # # Reemplazar comas por puntos en todo el DataFrame
    #     #     df_anotaciones = df_anotaciones.replace(',', '.', regex=True)
    #     except FileNotFoundError:
    #         st.info('No tenemos FICHERO cargado!!!')
    #         #df_anotaciones = pd.DataFrame({'Comienzo': [], 'Fin': [], 'Docentes': [], 'Materias': [],'Grupos_clase': [],'Aula': [],'Dia_semana': []})
    #     return df_anotaciones

    # # def mostrar_dataframe(df_anotaciones):
    # #     st.write('DataFrame:')
    # #     st.data_editor(df_anotaciones)
    # #     #st.write(df_guardias)


    # # Cargar el DataFrame
    # df_anotaciones = cargar_dataframe()

    # Título de la aplicación
    #st.title('Operaciones CRUD con DataFrame y CSV')

    # # Mostrar el DataFrame
    # mostrar_dataframe(df_anotaciones)

    # Filtrar las filas del DataFrame según la condición df_anotaciones['ÁREA'] == 'TOTAL'
    df_filtrado = df_anotaciones[df_anotaciones['ÁREA'] == 'TOTAL']
    # Eliminar la columna 'ÁREA'
    df_filtrado_area = df_filtrado.drop(columns=['ÁREA'])


    # Mostrar el DataFrame filtrado
    st.write('## Filtrado del DataFrame por TOTALES:')
    st.write(df_filtrado_area)

    st.write(' ')

    #########################################################################################################
    # Obtener lista de ESTUDIOS únicos
    df_filtrado_area['ESTUDIO'] = df_filtrado_area['ESTUDIO'].replace({'1º Educación Secundaria Obligatoria (LOMLOE)': '1ºESO', '2º Educación Secundaria Obligatoria (LOMLOE)': '2ºESO',
                                                                        '3º Educación Secundaria Obligatoria (LOMLOE)': '3ºESO', '4º Educación Secundaria Obligatoria (LOMLOE)': '4ºESO',
                                                                        '1º BAC Modalidad de Ciencias y Tecnología (LOMLOE)':'1ºBAC', '1º BAC Modalidad de Artes (LOMLOE)':'1ºBAC',
                                                                        '1º BAC Modalidad de Humanidades y Ciencias Sociales (LOMLOE)':'1ºBAC','2º BAC Modalidad de Artes (LOMLOE)':'2ºBAC', 
                                                                        '2º BAC Modalidad de Ciencias y Tecnología (LOMLOE)':'2ºBAC','2º BAC Modalidad de Humanidades y Ciencias Sociales (LOMLOE)':'2ºBAC',
                                                                        'Primer curso Diversificación Curricular (LOMLOE)':'3ºESO','Segundo curso Diversificación Curricular (LOMLOE)':'4ºESO'})

    estudio = df_filtrado_area['ESTUDIO'].unique()
    # Widget para seleccionar el grupo
    selected_estudio = st.selectbox('SELECCIONAR NIVEL:', estudio)

    # Filtrar DataFrame por el grupo seleccionado
    df_selected_estudio = df_filtrado_area[df_filtrado_area['ESTUDIO'] == selected_estudio]

    st.write(df_selected_estudio)

    ########################################################################################################


    # Convertir las columnas FJ, FI, RJ y RI a formato numérico
    columnas_numericas = ['SESIONES','FJ', 'FI', 'RJ', 'RI','SJ','SI','AP','AN','OA']
    df_selected_estudio[columnas_numericas] = df_selected_estudio[columnas_numericas].apply(pd.to_numeric, errors='coerce')

    # Ordenar los datos por 'FI' y 'RI' de forma descendente por grupo
    df_sorted = df_selected_estudio.groupby('GRUPO').apply(lambda x: x.nlargest(6, ['FI', 'RI']))


    # Resetear el índice para obtener un DataFrame plano
    df_sorted = df_sorted.reset_index(drop=True)
    #df_sorted = df_sorted.drop(df_sorted.index[[0,1,5,10,17,20,21]])
    st.write('## Alumnado con problemas de ABSENTISMO por GRUPO:')
    st.write(df_sorted)

    # Ordenar los datos por 'AN'  de forma descendente por grupo
    df_sorted_disciplina = df_selected_estudio.groupby('GRUPO').apply(lambda x: x.nlargest(3, ['AN']))

    # Resetear el índice para obtener un DataFrame plano
    df_sorted_disciplina = df_sorted_disciplina.reset_index(drop=True)
    #df_sorted_disciplina = df_sorted_disciplina.drop(df_sorted_disciplina.index[[0,1,11,12]])
    st.write('## Alumnado con problemas de DISCIPLINA por GRUPO:')
    st.write(df_sorted_disciplina)

    # Agrupar por el campo 'GRUPO' y calcular la suma de las columnas para cada grupo
    sum_por_grupo = df_selected_estudio.groupby('GRUPO',as_index=False).sum()


    #sum_por_grupo = sum_por_grupo.drop(sum_por_grupo.index[[0, 1,5]])
    # Eliminar la columna 'TUTORES/AS' ,'ALUMNADO' y 'ÁREA'
    columnas_a_eliminar = ['TUTORES/AS','ALUMNADO','ESTUDIO']
    sum_por_grupo = sum_por_grupo.drop(columns= columnas_a_eliminar)
    #st.write(sum_por_grupo)

    # Calcular el porcentaje entre SESIONES y las otras columnas
    sum_por_grupo['Porcentaje_FJ'] = (sum_por_grupo['FJ'] / sum_por_grupo['SESIONES']) * 100
    sum_por_grupo['Porcentaje_FI'] = (sum_por_grupo['FI'] / sum_por_grupo['SESIONES']) * 100
    sum_por_grupo['Porcentaje_RJ'] = (sum_por_grupo['RJ'] / sum_por_grupo['SESIONES']) * 100
    sum_por_grupo['Porcentaje_RI'] = (sum_por_grupo['RI'] / sum_por_grupo['SESIONES']) * 100
    sum_por_grupo['Porcentaje_SJ'] = (sum_por_grupo['SJ'] / sum_por_grupo['SESIONES']) * 100
    sum_por_grupo['Porcentaje_SI'] = (sum_por_grupo['SI'] / sum_por_grupo['SESIONES']) * 100
    sum_por_grupo['Porcentaje_AP'] = (sum_por_grupo['AP'] / sum_por_grupo['SESIONES']) * 100
    sum_por_grupo['Porcentaje_AN'] = (sum_por_grupo['AN'] / sum_por_grupo['SESIONES']) * 100
    sum_por_grupo['Porcentaje_OA'] = (sum_por_grupo['OA'] / sum_por_grupo['SESIONES']) * 100

    # Mostrar el DataFrame con los porcentajes calculados
    #st.write(sum_por_grupo)

    # Calcular el porcentaje entre SESIONES y las otras columnas
    sum_por_grupo['%_FJ'] = (sum_por_grupo['FJ'] / sum_por_grupo['FJ'].sum()) * 100
    sum_por_grupo['%_FI'] = (sum_por_grupo['FI'] / sum_por_grupo['FI'].sum()) * 100
    sum_por_grupo['%_RJ'] = (sum_por_grupo['RJ'] / sum_por_grupo['RJ'].sum()) * 100
    sum_por_grupo['%_RI'] = (sum_por_grupo['RI'] / sum_por_grupo['RI'].sum()) * 100
    sum_por_grupo['%_SJ'] = (sum_por_grupo['SJ'] / sum_por_grupo['SJ'].sum()) * 100
    sum_por_grupo['%_SI'] = (sum_por_grupo['SI'] / sum_por_grupo['SI'].sum()) * 100
    sum_por_grupo['%_AP'] = (sum_por_grupo['AP'] / sum_por_grupo['AP'].sum()) * 100
    sum_por_grupo['%_AN'] = (sum_por_grupo['AN'] / sum_por_grupo['AN'].sum()) * 100
    sum_por_grupo['%_OA'] = (sum_por_grupo['OA'] / sum_por_grupo['OA'].sum()) * 100


    #sum_por_grupo.set_index()
    #st.write(sum_por_grupo)

    # Configurar Streamlit
    st.title('Gráfico de TOTALES por Grupo de FJ, FI, RJ, RI')
    st.write('FJ(Faltas Justificadas), FI(Faltas Injustificadas), RJ(Retraso Justificado), RI(Retraso Injustificado)')
    st.write('Datos:')

    # Eliminar la columna 'TUTORES/AS' ,'ALUMNADO' y 'ÁREA'
    # columnas_a_eliminar = ['SESIONES','RJ','RI','SJ','SI','AP','AN','OA','Porcentaje_FJ','Porcentaje_FI','Porcentaje_RJ','Porcentaje_RI','Porcentaje_SJ','Porcentaje_SI','Porcentaje_AP','Porcentaje_AN','Porcentaje_OA','%_FI','%_FJ','%_RJ','%_RI','%_SJ','%_SI','%_AP','%_AN','%_OA']
    # sum_por_grupo_faltas = sum_por_grupo.drop(columns= columnas_a_eliminar)


    st.dataframe(sum_por_grupo)

    col_izquierda, col_derecha = st.columns(2)

    with col_izquierda: 
        # Crear el gráfico
        chart_data = pd.DataFrame(
        {
            "GRUPO": sum_por_grupo['GRUPO'],
            "Falta Justificada": sum_por_grupo['%_FJ'],  
            "Falta Injustificada": sum_por_grupo['%_FI'],
        }
        )

        st.bar_chart(chart_data, x="GRUPO", y=["Falta Justificada", "Falta Injustificada"], color=["#FF0000", "#0000FF"])

    with col_derecha:
        # Crear el gráfico
        sum_por_grupo = sum_por_grupo
        chart_data = pd.DataFrame(
        {
            "GRUPO": sum_por_grupo['GRUPO'],
            "Retraso Justificado": sum_por_grupo['%_RJ'],
            "Retraso Injustificado": sum_por_grupo['%_RI'],
        }
        )

        st.bar_chart(chart_data, x="GRUPO", y=["Retraso Justificado", "Retraso Injustificado"], color=["#FF0000", "#0000FF"])



    # Configurar Streamlit
    st.title('Gráfico de TOTALES por Grupo de SJ, SI, AP, AN, OA')
    st.write('SJ(Faltas Justificadas), SI(Faltas Injustificadas), AP(Anotaciones Positivas), AN(Anotaciones Negativas), OA(Otras Anotaciones)')
    st.write('Datos:')
    # Eliminar la columna 'TUTORES/AS' ,'ALUMNADO' y 'ÁREA'
    # columnas_a_eliminar = ['SESIONES','FJ','FI','RJ','RI','SJ','SI','OA','Porcentaje_FJ','Porcentaje_FI','Porcentaje_RJ','Porcentaje_RI','Porcentaje_SJ','Porcentaje_SI','Porcentaje_AP','Porcentaje_AN','Porcentaje_OA','%_FI','%_FJ','%_RJ','%_RI','%_SJ','%_SI','%_AP','%_AN','%_OA']
    # sum_por_grupo_disciplina = sum_por_grupo.drop(columns= columnas_a_eliminar)
    st.dataframe(sum_por_grupo)

    col_izquierda, col_derecha = st.columns(2)

    with col_izquierda: 
    # Crear el gráfico
        chart_data = pd.DataFrame(
        {
            "GRUPO": sum_por_grupo['GRUPO'],
            "Anotaciones Positivas": sum_por_grupo['%_AP'],
            "Anotaciones Negativas": sum_por_grupo['%_AN'],
            "Otras Anotaciones": sum_por_grupo['%_OA'],
        }
        )

        st.bar_chart(chart_data, x="GRUPO", y=["Anotaciones Positivas", "Anotaciones Negativas", "Otras Anotaciones"], color=["#FF0000", "#0000FF", "#FF9033"])

    with col_derecha:
        # Crear el gráfico
        chart_data = pd.DataFrame(
        {
            "GRUPO": sum_por_grupo['GRUPO'],
            "Salidas Justificadas": sum_por_grupo['%_SJ'],
            "Salidas Injustificadas": sum_por_grupo['%_SI'],
        }
        )

        st.bar_chart(chart_data, x="GRUPO", y=["Salidas Justificadas", "Salidas Injustificadas"], color=["#FF0000", "#0000FF"])

    