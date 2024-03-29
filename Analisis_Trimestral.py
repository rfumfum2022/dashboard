import streamlit as st
import openpyxl
import pandas as pd #pip install pandas
import plotly.express as px #pip install plotly-express
import streamlit as st #pip install streamlit
from PIL import Image
import altair as alt

def app():
    #set page
    im = Image.open("LOGO_IES_Andres_Bello.ico")
    #st.set_page_config(page_title="Analytics Dashboard", page_icon = im, layout="wide")  
    st.subheader("📈 I.E.S. ANDRéS BELLO - DASHBOARD ")

    st.title(':clipboard: Análisis TRIMESTRAL de Resultados') #Titulo del Dash
    #st.subheader('1ª EVALUACIóN')
    st.markdown('##') #Para separar el titulo de los KPIs, se inserta un paragrafo usando un campo de markdown

    #st.sidebar.header('Dashboard')

    st.link_button('Normativa Evaluación-Promoción-Titulación', 
                'https://www.gobiernodecanarias.org/educacion/web/bachillerato/informacion/evaluacion_promocion_titulacion/',
                type='primary')

    @st.cache_data
    def load_data(file):
        if file == "Excel":
            df_t = pd.read_excel(file, engine='openpyxl',errors='ignore')
            #df_t = openpyxl.load_workbook(file)
        else:
            columnas = ["Grupo_Clase","Primer_apellido","Segundo_apellido","Nombre","Materia","Materia_curso","Nombre_materia","Fecha","Evaluacion","Nota"] 
            df_t = pd.read_csv(file)
            df_t.columns = columnas 
        return df_t

    # Seleccionar tipo de archivo
    tipo_archivo = st.radio("Seleccione el tipo de archivo", ("Excel", "CSV"))
    uploaded_file = st.file_uploader(f"Subir archivo {tipo_archivo}", type=["csv", "xlsx"])

    if uploaded_file is None:
        st.info('Subir un fichero',icon="ℹ️")
        st.stop()

    df_t = load_data(uploaded_file)

    
    df_t = df_t.sort_values(by='Grupo_Clase')

    df_t['Evaluacion'] = df_t['Evaluacion'].replace({'Primera Evaluación': '1EVA', 'Segunda Evaluación': '2EVA', 'Evaluación final ordinaria': 'ORD', 'Evaluación final extraordinaria': 'EXT'})

    # Cambiamos las NOTAS por valores numéricos
    df_t['Nota'] = df_t['Nota'].replace({'IN':'3','5 (SU)': '5', '6 (BI)': '6', 'NT':'7', 'SB':'9', '100 (N.P.)':'0', 'PTE.':'1', '100 (Pt.1)':'1', 'NP':'1', 'NC':'1'})
    df_t['Nota'] = df_t['Nota'].str.replace(',','.')
    

    df_t['Nota'] = pd.to_numeric(df_t['Nota'])

    # Suponiendo que df es tu DataFrame y la columna se llama 'fecha'
    df_t['Fecha'] = pd.to_datetime(df_t['Fecha'], format='%d/%m/%Y')

    # Extraer el año de la columna de fecha
    df_t['Año'] = df_t['Fecha'].dt.year

    #st.dataframe(df_t) 

    st.sidebar.header("Opciones a filtrar:") #sidebar lo que nos va a hacer es crear en la parte izquierda un cuadro para agregar los filtros que queremos tener

    #side bar evaluación
    st.sidebar.header("Filtro EVA")
    Evaluacion = st.sidebar.multiselect(
        label = "Evaluacion",
        options = df_t["Evaluacion"].unique(),
        #default=df["docente"].unique(),
    )


    df_selection_t = df_t.query(
        "Evaluacion==@Evaluacion")


   
    def table():
        with st.expander("Tabular"):
        #st.dataframe(df_selection,use_container_width=True)
            shwdata = st.multiselect('Filter :', df_t.columns, default=["Grupo_Clase","Primer_apellido","Segundo_apellido","Nombre","Materia","Materia_curso","Nombre_materia","Fecha","Evaluacion","Nota"])
            st.dataframe(df_selection_t[shwdata],use_container_width=True)
    table()

    # Crear un DataFrame con el número de materias aprobadas y no aprobadas por estudiante
    def contar_aprobadas_y_no_aprobadas(nota):
        if nota >= 5.0:
            return 1
        else:
            return 0

    # Función para mapear los valores de grupo_clase a los nombres de los cursos
    def identificar_curso(grupo):
        if grupo.startswith("1"):
            return "1ESO"
        elif grupo.startswith("2"):
            return "2ESO"
        elif grupo.startswith("3"):
            return "3ESO"
        elif grupo.startswith("4"):
            return "4ESO"
        elif grupo.startswith("BACH-1"):
            return "1BAC"
        elif grupo.startswith("BACH-2"):
            return "2BAC"
        elif grupo.startswith("BSP-1"):
            return "1BSP"
        elif grupo.startswith("BSP-2"):
            return "2BSP"
        elif grupo.startswith("Cert Idiomas - A2"):
            return "EOI"
        elif grupo.startswith("Cert Idiomas - B1"):
            return "EOI"
        elif grupo.startswith("Cert Idiomas - B2"):
            return "EOI"
        else:
            return "Otro"

    df_selection_t['materias_aprobadas'] = df_selection_t['Nota'].apply(contar_aprobadas_y_no_aprobadas)

    # Añadir una nueva columna con el nombre del curso
    df_selection_t['Nivel'] = df_selection_t['Grupo_Clase'].apply(identificar_curso)

    # Agrupar por grupo y nombre, sumar el número de materias aprobadas y no aprobadas
    df_materias_aprobadas = df_selection_t.groupby(['Grupo_Clase', 'Nombre']).agg({
        'materias_aprobadas': 'sum',
        'Materia': 'count'
    }).reset_index()

    df_materias_aprobadas .columns = ['Grupo_Clase', 'Nombre', 'numero_materias_aprobadas', 'numero_materias_totales']
    df_materias_aprobadas ['diferencia'] = df_materias_aprobadas ['numero_materias_totales'] - df_materias_aprobadas ['numero_materias_aprobadas']

    #st.dataframe(nuevo_df)

    # Calcular el porcentaje de alumnos con dos o menos en la columna "diferencia"
    porcentaje_alumnos_eso_1bac = (df_materias_aprobadas [df_materias_aprobadas ['diferencia'] <= 2].groupby('Grupo_Clase').size() / df_materias_aprobadas .groupby('Grupo_Clase').size()) * 100
    porcentaje_alumnos_2bac = (df_materias_aprobadas [df_materias_aprobadas ['diferencia'] <= 1].groupby('Grupo_Clase').size() / df_materias_aprobadas .groupby('Grupo_Clase').size()) * 100

    # Agregar una columna con el número total de integrantes por grupo
    df_materias_aprobadas ['integrantes_grupo'] = df_materias_aprobadas .groupby('Grupo_Clase')['Nombre'].transform('size')

    # Crear un DataFrame con el porcentaje de alumnos por grupo con dos o menos materias suspendidas
    porcentaje_df_eso_1bac = pd.DataFrame({
        'Grupo_Clase': porcentaje_alumnos_eso_1bac.index,
        'porcentaje': porcentaje_alumnos_eso_1bac.values
    })
    # Crear un DataFrame con el porcentaje de alumnos por grupo con una o ninguna materias suspendidas
    porcentaje_df_2bac = pd.DataFrame({
        'Grupo_Clase': porcentaje_alumnos_2bac.index,
        'porcentaje': porcentaje_alumnos_2bac.values
    })

    # Combinar ambos DataFrames
    resultado_df_eso_1bac = porcentaje_df_eso_1bac.merge(df_materias_aprobadas [['Grupo_Clase', 'integrantes_grupo']], on='Grupo_Clase')
    resultado_df_eso_1bac['Nivel'] = resultado_df_eso_1bac['Grupo_Clase'].apply(identificar_curso)
    resultado_final_eso_1bac = resultado_df_eso_1bac.groupby('Grupo_Clase').first().reset_index()
    #st.dataframe(resultado_df)
    resultado_df_2bac = porcentaje_df_2bac.merge(df_materias_aprobadas [['Grupo_Clase', 'integrantes_grupo']], on='Grupo_Clase')
    resultado_df_2bac['Nivel'] = resultado_df_2bac['Grupo_Clase'].apply(identificar_curso)
    resultado_final_2bac = resultado_df_2bac.groupby('Grupo_Clase').first().reset_index()

    # Separar el DataFrame en varios dependiendo del valor de la columna 'Nivel'
    df_eso_2 = resultado_final_eso_1bac[resultado_final_eso_1bac['Nivel'].isin(['1ESO', '2ESO', '3ESO', '4ESO'])]
    df_1bac_2 = resultado_final_eso_1bac[resultado_final_eso_1bac['Nivel'].isin(['1BAC', '1BSP'])]
    df_2bac_2 = resultado_final_eso_1bac[resultado_final_eso_1bac['Nivel'].isin(['2BAC', '2BSP'])]
    df_EOI_2 = resultado_final_eso_1bac[resultado_final_eso_1bac['Nivel'] == 'EOI']
    #st.dataframe(df_eso)
    df_eso_1 = resultado_final_2bac[resultado_final_2bac['Nivel'].isin(['1ESO', '2ESO', '3ESO', '4ESO'])]
    df_1bac_1 = resultado_final_2bac[resultado_final_2bac['Nivel'].isin(['1BAC', '1BSP'])]
    df_2bac_1 = resultado_final_2bac[resultado_final_2bac['Nivel'].isin(['2BAC', '2BSP'])]
    df_EOI_1 = resultado_final_2bac[resultado_final_2bac['Nivel'] == 'EOI']

    #representqció gráfica barras para promociones dos o menos suspensos
    col1, col2 = st.columns([3, 2])
    col2.write(df_eso_2)
    col1.write("### Gráfico de Promociones ESO (Susp<=2)")
    bar_chart_data = df_eso_2.set_index('Grupo_Clase')['porcentaje']
    col1.bar_chart(bar_chart_data)

    col1, col2 = st.columns([3, 2])
    col2.write(df_1bac_2)
    col1.write("### Gráfico de Promociones 1ºBAC (Susp<=2)")
    bar_chart_data = df_1bac_2.set_index('Grupo_Clase')['porcentaje']
    col1.bar_chart(bar_chart_data)

    #representqció gráfica barras para promociones una o ningún suspensos
    col1, col2 = st.columns([3, 2])
    col2.write(df_2bac_1)
    col1.write("### Gráfico de Titulaciones 2ºBAC (Susp<=1)")
    bar_chart_data = df_2bac_1.set_index('Grupo_Clase')['porcentaje']
    col1.bar_chart(bar_chart_data)

    # Función para calcular el número de aprobados y suspendidos por materia y el porcentaje de aprobados
    def calcular_estadisticas_grupo(df_grupo):
        aprobados = df_grupo[df_grupo['Nota'] >= 5.0]['Materia'].value_counts()
        suspendidos = df_grupo[df_grupo['Nota'] < 5.0]['Materia'].value_counts()
        total_alumnos = df_grupo['Materia'].value_counts()
        porcentaje_aprobados = (aprobados / total_alumnos) * 100
        return pd.DataFrame({'aprobados': aprobados, 'suspendidos': suspendidos, 'porcentaje_aprobados': porcentaje_aprobados})

    # Aplicar la función a cada grupo
    resultado_por_grupo = df_selection_t.groupby('Grupo_Clase').apply(calcular_estadisticas_grupo)

    # Reorganizar el DataFrame final para que tenga la estructura deseada
    resultado_por_grupo = resultado_por_grupo.reset_index().rename(columns={'level_1': 'Materia'})
    resultado_por_grupo['suspendidos'] = resultado_por_grupo['suspendidos'].fillna(0)
    resultado_por_grupo['aprobados'] = resultado_por_grupo['aprobados'].fillna(0)
    resultado_por_grupo['porcentaje_aprobados'] = resultado_por_grupo['porcentaje_aprobados'].fillna(0)
    #st.write(resultado_por_grupo)


    # Crear sidebar para seleccionar el grupo
    selected_group = st.sidebar.selectbox("%Aprobado vs Materia", resultado_por_grupo["Grupo_Clase"].unique())

    # Filtrar el DataFrame por el grupo seleccionado
    filtered_df = resultado_por_grupo[resultado_por_grupo["Grupo_Clase"] == selected_group]

    # Mostrar los datos filtrados
    col1, col2 = st.columns([3, 3])


    col2.write(filtered_df)
    grupo = filtered_df['Grupo_Clase'].unique()
    col1.write(f"### %Aprobados vs Materia {grupo}")
    bar_chart_data = filtered_df.set_index('Materia')['porcentaje_aprobados']
    col1.bar_chart(bar_chart_data)



    # Añadir una nueva columna con el nombre del curso
    resultado_final_eso_1bac['Nivel'] = resultado_final_eso_1bac['Grupo_Clase'].apply(identificar_curso)


    # Obtener los niveles únicos
    niveles = resultado_final_eso_1bac['Nivel'].unique()

    # Barra lateral para seleccionar el nivel
    nivel_seleccionado = st.sidebar.selectbox('%Promociones vs Nivel', niveles)

    # Filtrar el DataFrame por el nivel seleccionado
    df_filtrado = resultado_final_eso_1bac[resultado_final_eso_1bac['Nivel'] == nivel_seleccionado]

    # Crear un gráfico de barras con Altair
    chart = alt.Chart(df_filtrado).mark_bar().encode(
        x='Grupo_Clase',
        y='porcentaje'
    ).properties(
        width=200,
        height=300
    )

    # Mostrar el gráfico en Streamlit
    # Mostrar los datos filtrados
    col1, col2 = st.columns([3, 3])


    col1.write(df_filtrado)
    nivel = df_filtrado['Nivel'].unique()
    col2.write(f"#### %Promociones vs Nivel {nivel} (Susp<=2)")
    #bar_chart_data = filtered_df.set_index('Materia')['porcentaje_aprobados']
    col2.altair_chart(chart, use_container_width=True)






    # Hide Streamlit Style

    hide_st_style = """
                <style>
    
                footer {visibility: hidden;}
            
                </style>
                """

    st.markdown(hide_st_style, unsafe_allow_html= True)


