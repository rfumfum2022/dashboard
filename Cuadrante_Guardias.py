import streamlit as st
import pandas as pd
from PIL import Image

def app():
    #set page
    im = Image.open("LOGO_IES_Andres_Bello.ico")
    #st.set_page_config(page_title="Analytics Dashboard", page_icon = im, layout="wide")  
    st.subheader("📈 I.E.S. ANDRéS BELLO - DASHBOARD ")

    st.title(':clipboard: Cuadrante GUARDIAS') #Titulo del Dash
    #st.subheader('1ª EVALUACIóN')
    st.markdown('##') #Para separar el titulo de los KPIs, se inserta un paragrafo usando un campo de markdown

    st.link_button('Normativa ROC Organización-Funcionamiento', 
                'https://www3.gobiernodecanarias.org/medusa/edublog/cpmlaspalmasdegrancanaria/wp-content/uploads/sites/166/2018/09/roc_organizacion_y_func_2013.pdf',
                type='primary')
    #st.sidebar.header('Dashboard')

    # Función para cargar o crear el DataFrame
    df_guardias = pd.read_csv('/Users/rfumfum/Documents/PYTHON/Dashboard/project_ies/Guardia_2023.csv')
    # Suponiendo que df_guardias es tu DataFrame
    #df_guardias['Contador'] = pd.to_numeric(df_guardias['Contador'])
    #df_guardias.dtypes

    def cargar_dataframe():
        try:
            df = pd.read_csv('/Users/rfumfum/Documents/PYTHON/Dashboard/project_ies/sustituciones.csv')
        
        except FileNotFoundError:
            df = pd.DataFrame({'Comienzo': [], 'Fin': [], 'Docentes': [], 'Materias': [],'Grupos_clase': [],'Aula': [],'Dia_semana': []})
        return df

    def mostrar_dataframe(df):
        st.write('DataFrame:')
        st.data_editor(df)
        #st.write(df_guardias)

    # Función para añadir una nueva fila al DataFrame
    def agregar_fila(df, comienzo, fin, nombre,materias, grupo_clase, aula, dia_semana):
        nueva_fila = pd.DataFrame({'Comienzo': [comienzo],'Fin': [fin],'Docentes': [nombre],'Materias': [materias],'Grupos_clase': [grupo_clase], 'Aula': [aula],'Dia_semana':[dia_semana]})
        df = pd.concat([df, nueva_fila], ignore_index=True)
        df.to_csv('/Users/rfumfum/Documents/PYTHON/Dashboard/project_ies/sustituciones.csv', index=False)

        return df

    # Función para actualizar una fila del DataFrame
    def actualizar_fila(df, df_guardias, indice, comienzo, fin, nombre,materias, grupo_clase, aula, dia_semana, selected_guardias, selected_psc):
        
        df.at[indice, 'Comienzo'] = comienzo 
        df.at[indice, 'Fin'] = fin
    
        df.at[indice, 'Docentes'] = nombre
        df.at[indice, 'Materias'] = materias
        df.at[indice, 'Grupos_clase'] = grupo_clase
        df.at[indice, 'Aula'] = aula 
        df.at[indice, 'Dia_semana'] = dia_semana
        #df.at[indice, 'Contador'] = contador
        df.at[indice, 'SUSTITUCIóN'] =  selected_guardias
        df.at[indice, 'PSC'] =  selected_psc
    
        
        # Seleccionar las filas que cumplen las condiciones
        filas_seleccionadas = df_guardias[(df_guardias['Comienzo'] == comienzo) & 
                                    (df_guardias['Docentes'] == selected_guardias) & 
                                    (df_guardias['Dia_semana'] == dia_semana)]
        st.write(filas_seleccionadas)
        
        # Incrementar en una unidad el valor de 'Contador' para la fila específica que cumple con las condiciones
        df_guardias.loc[(df_guardias['Comienzo'] == comienzo) & (df_guardias['Docentes'] == selected_guardias ) & (df_guardias['Dia_semana'] == dia_semana), 'Contador'] += 1

        df.to_csv('/Users/rfumfum/Documents/PYTHON/Dashboard/project_ies/sustituciones.csv', index=False)
        df_guardias.to_csv('/Users/rfumfum/Documents/PYTHON/Dashboard/project_ies/Guardia_2023.csv', index=False)

        return df, df_guardias

    # Función para borrar una fila del DataFrame
    def borrar_fila(df, indice):
        df.drop(indice, inplace=True)
        df.to_csv('/Users/rfumfum/Documents/PYTHON/Dashboard/project_ies/sustituciones.csv', index=False)

        return df

    # Cargar el DataFrame
    df = cargar_dataframe()

    # Título de la aplicación
    #st.title('Operaciones CRUD con DataFrame y CSV')

    # Mostrar el DataFrame
    mostrar_dataframe(df)

    # Seleccionar operación
    operacion = st.radio('Seleccionar Operación:', ['Crear', 'Leer', 'Actualizar', 'Borrar'])

    # Realizar operaciones CRUD
    if operacion == 'Crear':
        comienzo = st.text_input('Comienzo:') 
        fin = st.text_input('Fin:')
        nombre = st.text_input('Docentes:')
        materias = st.text_input('Materias:')
        grupo_clase = st.text_input('Grupos_clase:')
        aula = st.text_input('Aula:')
        dia_semana = st.text_input('Dia_semana:')
        #contador = st.text_input('Contador:')

        if st.button('Crear Fila'):
            df = agregar_fila(df,comienzo,fin,nombre,materias,grupo_clase, aula, dia_semana)
            st.success('Fila creada exitosamente!')

    elif operacion == 'Leer':
        pass  # No es necesario realizar ninguna acción para la operación de lectura

    elif operacion == 'Actualizar':

        indice = st.number_input('Índice de Fila a Actualizar:', min_value=0, max_value=len(df)-1)
        


        comienzo = st.text_input('Comienzo:', value=df.at[indice, 'Comienzo'])
        fin = st.text_input('Fin:', value=df.at[indice, 'Fin'])
        nombre = st.text_input('Nuevo Docente:', value=df.at[indice, 'Docentes'])
        materias = st.text_input('Materias:', value=df.at[indice, 'Materias'])
        grupo_clase = st.text_input('Grupos_clase:', value=df.at[indice, 'Grupos_clase'])
        aula = st.text_input('Nueva Aula:', value=df.at[indice, 'Aula'])
        dia_semana = st.text_input('Dia_semana:', value=df.at[indice, 'Dia_semana'])
        #contador = st.text_input('Contador:', value=df.at[indice, 'Contador'])

            # Interfaz de Streamlit
        selected_day = dia_semana
        selected_start_time = comienzo

        # Filtrar los registros del DataFrame de guardias que coincidan con el día y la hora de inicio seleccionados
        filtered_guardias = df_guardias['Docentes'][(df_guardias['Dia_semana'] == selected_day) & (df_guardias['Comienzo'] == selected_start_time)& (df_guardias['Tipo_actividad'] == 'Guardia')] 
        filtered_psc = df_guardias['Docentes'][(df_guardias['Dia_semana'] == selected_day) & (df_guardias['Comienzo'] == selected_start_time)& (df_guardias['Tipo_actividad'] != 'Guardia')] 
        filtered_guardias = filtered_guardias 
    
        selected_guardias = st.selectbox('Seleccionar SUSTITUCIóN:', filtered_guardias, index=None, placeholder="Select SUSTITUCIóN..")
        contador_guardias = df_guardias['Contador'][(df_guardias['Dia_semana'] == selected_day) & (df_guardias['Comienzo'] == selected_start_time) & (df_guardias['Docentes'] == selected_guardias)]
        st.write(contador_guardias)
        
        selected_psc = st.selectbox('Seleccionar PSC:', filtered_psc, index=None, placeholder="Select PSC..")
        contador_psc = df_guardias['Contador'][(df_guardias['Dia_semana'] == selected_day) & (df_guardias['Comienzo'] == selected_start_time) & (df_guardias['Docentes'] == selected_psc)]
        st.write(contador_psc)

        if st.button('Actualizar Fila'):
            df = actualizar_fila(df, df_guardias, indice, comienzo, fin,nombre,materias,grupo_clase, aula, dia_semana,selected_guardias,selected_psc)
            st.success('Fila actualizada exitosamente!')

    elif operacion == 'Borrar':
        indice = st.number_input('Índice de Fila a Borrar:', min_value=0, max_value=len(df)-1)
        if st.button('Borrar Fila'):
            df = borrar_fila(df, indice)
            st.success('Fila borrada exitosamente!')

    # Guardar cambios en el archivo CSV
    nombre_archivo = st.text_input('Nombre del archivo-sutitución:')

    if st.button('Guardar Cambios'):
        df.to_csv(f'{nombre_archivo}.csv', index=False)
        st.success('Cambios guardados exitosamente en "sustituciones.csv"!')




