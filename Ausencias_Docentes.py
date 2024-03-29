import streamlit as st
import openpyxl
import pandas as pd #pip install pandas
import plotly.express as px #pip install plotly-express
import streamlit as st #pip install streamlit
from PIL import Image

def app():
    #set page
    im = Image.open("LOGO_IES_Andres_Bello.ico")
    #st.set_page_config(page_title="Analytics Dashboard", page_icon = im, layout="wide")  
    st.subheader("📈 I.E.S. ANDRéS BELLO - DASHBOARD ")

    st.title(':clipboard: Ausencia Docentes') #Titulo del Dash
    #st.subheader('1ª EVALUACIóN')
    st.markdown('##') #Para separar el titulo de los KPIs, se inserta un paragrafo usando un campo de markdown

    #st.sidebar.header('Dashboard')

    st.link_button('Normativa Permiso-Licencias', 
                'https://www.gobiernodecanarias.org/educacion/web/servicios/inspeccion_educativa/normativa_clasificada/personal_docente/permisos-y-licencias/',
                type='primary')
    @st.cache_data
    #@st.cache_resourse(suppress_st_warning = True)
    def load_data(file):
        if file == "Excel":
            df_t = pd.read_excel(file, engine='openpyxl',errors='ignore')
            #df_t = openpyxl.load_workbook(file)
        else:
            df_t = pd.read_csv(file)
        return df_t

    # Seleccionar tipo de archivo
    tipo_archivo = st.radio("Seleccione el tipo de archivo HORARIO", ("Excel", "CSV"))
    uploaded_file = st.file_uploader(f"Subir archivo {tipo_archivo}", type=["csv", "xlsx"])

    if uploaded_file is None:
        st.info('Subir un fichero',icon="ℹ️")
        st.stop()

    df_t = load_data(uploaded_file)
    df_t = df_t.sort_values(by='Comienzo')
    #st.dataframe(df_t)

    #side bar dpto
    st.sidebar.header("Filtro Docente")
    Docentes = st.sidebar.multiselect(
        label = "Filtro Docentes",
        options = df_t["Docentes"].unique(),
        #default=df["dpto"].unique(),
    )

    #side bar hora
    st.sidebar.header("Filtro Día")
    df = df_t.sort_values(by='Dia_semana')
    Dia_semana = st.sidebar.multiselect(
        label = "Filtro Día",
        options = df["Dia_semana"].unique(),
        #default=df["hora"].unique(),
    )

    df_selection_grupo = df.query(
        "Docentes==@Docentes & Dia_semana==@Dia_semana")
    # Filtrar el DataFrame por Tipo_actividad = 'Guardia'
    
    df_guardia = df.query("Dia_semana==@Dia_semana")[df['Tipo_actividad'] == 'Guardia']
    #df_guardia = df_guardia.drop(columns=['Lectiva','Con_alumnado','Materias','Grupos_clase','Aula'], inplace=True)
    df_guardia = df_guardia.drop(columns=['Lectiva','Con_alumnado','Materias','Grupos_clase','Aula'])
    # Guardar DataFrame como CSV
    ruta_archivo = '/Users/rfumfum/Documents/PYTHON/Dashboard/project_ies/guardias.csv'  # Ruta donde se guardará el archivo CSV
    df_guardia.to_csv(ruta_archivo, index=False)  # index=False evita que se guarde el índice del DataFrame

    #df.drop(columns=['col1', 'col2'], inplace=True)  # Elimina las columnas 'col1' y 'col2'


    def table_grupo():
        with st.expander("Tabular"):
        #st.dataframe(df_selection,use_container_width=True)
            shwdata_grupo = st.multiselect('Filter :', df.columns, default=["Tipo_actividad","Lectiva","Con_alumnado","Comienzo","Fin","Docentes","Materias","Grupos_clase","Aula","Dia_semana"])
            st.dataframe(df_selection_grupo[shwdata_grupo],use_container_width=True)
            sustituciones = df_selection_grupo[shwdata_grupo]
            sustituciones = sustituciones.drop(columns=["Tipo_actividad","Lectiva","Con_alumnado"])
            sustituciones['SUSTITUCIóN'] = {}
            sustituciones['PSC'] = {}
            
            st.dataframe(sustituciones)
            # Guardar DataFrame como CSV
            ruta_archivo = '/Users/rfumfum/Documents/PYTHON/Dashboard/project_ies/sustituciones.csv'  # Ruta donde se guardará el archivo CSV
            sustituciones.to_csv(ruta_archivo, index=False)  # index=False evita que se guarde el índice del DataFrame

            st.dataframe(df_guardia)


    
    table_grupo()
    st.write('FINAL')

   
    # Función para cargar o crear el DataFrame
    def cargar_dataframe():
        try:
            df = pd.read_csv('/Users/rfumfum/Documents/PYTHON/Dashboard/project_ies/sustituciones.csv')
        except FileNotFoundError:
            df = pd.DataFrame({'Tipo_actividad': [], 'Lectiva': [], 'Con_alumnado': [], 'Comienzo': [], 'Fin': [], 'Docentes': [], 'Materias': [],'Grupos_clase': [],'Aula': [],'Dia_semana': [],'Contador': []})
        return df

    def mostrar_dataframe(df):
        st.write('DataFrame:')
        st.write(df)

    # Función para añadir una nueva fila al DataFrame
    def agregar_fila(df, nombre, edad):
        nueva_fila = pd.DataFrame({'Nombre': [nombre], 'Edad': [edad]})
        df = pd.concat([df, nueva_fila], ignore_index=True)
        return df

    # Función para actualizar una fila del DataFrame
    def actualizar_fila(df, indice, nombre, aula):
        df.at[indice, 'Docentes'] = nombre
        df.at[indice, 'Aula'] = aula
        df.to_csv('/Users/rfumfum/Documents/PYTHON/Dashboard/project_ies/sustituciones.csv', index=False)

        return df

    # Función para borrar una fila del DataFrame
    def borrar_fila(df, indice):
        df.drop(indice, inplace=True)
        df.to_csv('/Users/rfumfum/Documents/PYTHON/Dashboard/project_ies/sustituciones.csv', index=False)

        return df

    # Cargar el DataFrame
    df = cargar_dataframe()

    # Título de la aplicación
    st.title('Operaciones CRUD con DataFrame y CSV')

    # Mostrar el DataFrame
    mostrar_dataframe(df)

    # Seleccionar operación
    operacion = st.radio('Seleccionar Operación:', ['Crear', 'Leer', 'Actualizar', 'Borrar'])

    # Realizar operaciones CRUD
    if operacion == 'Crear':
        nombre = st.text_input('Docentes:')
        aula = st.number_input('Aula:', min_value=0, max_value=150)
        if st.button('Crear Fila'):
            df = agregar_fila(df, nombre, aula)
            st.success('Fila creada exitosamente!')

    elif operacion == 'Leer':
        pass  # No es necesario realizar ninguna acción para la operación de lectura

    elif operacion == 'Actualizar':
        indice = st.number_input('Índice de Fila a Actualizar:', min_value=0, max_value=len(df)-1)
        nombre = st.text_input('Nuevo Docente:', value=df.at[indice, 'Docentes'])
        aula = st.number_input('Nueva Aula:', value=df.at[indice, 'Aula'])
        if st.button('Actualizar Fila'):
            df = actualizar_fila(df, indice, nombre, aula)
            st.success('Fila actualizada exitosamente!')

    elif operacion == 'Borrar':
        indice = st.number_input('Índice de Fila a Borrar:', min_value=0, max_value=len(df)-1)
        if st.button('Borrar Fila'):
            df = borrar_fila(df, indice)
            st.success('Fila borrada exitosamente!')

    # Guardar cambios en el archivo CSV
    if st.button('Guardar Cambios'):
        df.to_csv('/Users/rfumfum/Documents/PYTHON/Dashboard/project_ies/sustituciones.csv', index=False)
        st.success('Cambios guardados exitosamente en "sustituciones.csv"!')
