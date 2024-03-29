import streamlit as st

from streamlit_option_menu import option_menu

import Analisis_Anual, Analisis_Trimestral, Anotaciones, Ausencias_Docentes, Cuadrante_Guardias
from PIL import Image

im = Image.open("LOGO_IES_Andres_Bello.ico")
st.set_page_config(
        page_title="DASHBOARD",
        #page_title="Analytics Dashboard",
        page_icon = im ,
        layout="wide",  
)

class MultiApp:

    def __init__(self):
        self.apps = []

    def add_app(self, title, func):

        self.apps.append({
            "title": title,
            "function": func
        })

    def run():
        # app = st.sidebar(
        with st.sidebar:        
            app = option_menu(
                menu_title='MENú ',
                options=['Ausencias Docentes','Cuadrante Guardias','Anotaciones','Analisis Anual','Analisis Trimestral'],
                icons=['archive-fill','archive','clipboard','bar-chart-line-fill','bar-chart-line'],
                menu_icon='house-fill',
                default_index=1,
                styles={
                    "container": {"padding": "5!important","background-color":'black'},
        "icon": {"color": "white", "font-size": "23px"}, 
        "nav-link": {"color":"white","font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "blue"},
        "nav-link-selected": {"background-color": "#02ab21"},}
                
                )

        
        if app == "Ausencias Docentes":
            Ausencias_Docentes.app()
        if app == "Cuadrante Guardias":
            Cuadrante_Guardias.app()    
        if app == "Anotaciones":
            Anotaciones.app()        
        if app == "Analisis Anual":
            Analisis_Anual.app()
        if app == "Analisis Trimestral":
            Analisis_Trimestral.app()    
                    
    run()            
         