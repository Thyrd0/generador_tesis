import streamlit as st
import requests
import json
from datetime import datetime
import os

# Configuración de la página
st.set_page_config(
    page_title="Generador de Proyecto de Tesis",
    page_icon="📚",
    layout="wide"
)

# API endpoint
API_URL = "http://localhost:8000"

# Líneas de investigación disponibles
LINEAS_INVESTIGACION = [
    "Gestión de Gobierno y Servicios de TIC",
    "Gestión de Proyectos de TIC",
    "Gestión de Desarrollo de Software",
    "Gestión de Infraestructura y Comunicaciones",
    "Gestión de la Seguridad de la Información"
]

def main():
    # Estilos CSS premium y responsivos
    st.markdown("""
        <style>
        /* Estilos generales */
        body {
            color: #2b2b2b;
        }
        h1 {
            color: #1e3d59;
            font-family: 'Outfit', sans-serif;
            font-weight: 700;
        }
        h2, h3 {
            color: #17b978;
            font-family: 'Outfit', sans-serif;
        }
        /* Botón de generación */
        div.stButton > button:first-child {
            background-color: #1e3d59;
            color: white;
            border-radius: 8px;
            font-weight: bold;
            font-size: 16px;
            padding: 10px 24px;
            border: 2px solid #1e3d59;
            transition: all 0.3s ease;
        }
        div.stButton > button:first-child:hover {
            background-color: #17b978;
            border-color: #17b978;
            box-shadow: 0 4px 15px rgba(23, 185, 120, 0.4);
            transform: translateY(-2px);
        }
        /* Botón de descarga PDF */
        .pdf-btn button {
            background-color: #ff4b4b !important;
            color: white !important;
            font-weight: bold !important;
            border-radius: 8px !important;
        }
        /* Botón de descarga Word */
        .word-btn button {
            background-color: #1d72b8 !important;
            color: white !important;
            font-weight: bold !important;
            border-radius: 8px !important;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("📚 Generador Automático de Proyecto de Tesis")
    st.markdown("Generación académica inteligente con formato riguroso de la Universidad Nacional de Trujillo (UNT) y normas APA v7.")
    st.markdown("---")
    
    # Inicializar Session State para evitar que se borre al hacer clic en descargas
    if "contenido" not in st.session_state:
        st.session_state["contenido"] = None
    if "pdf_data" not in st.session_state:
        st.session_state["pdf_data"] = None
    if "pdf_filename" not in st.session_state:
        st.session_state["pdf_filename"] = None
    if "docx_data" not in st.session_state:
        st.session_state["docx_data"] = None
    if "docx_filename" not in st.session_state:
        st.session_state["docx_filename"] = None
    
    # Sidebar con instrucciones y configuración
    with st.sidebar:
        st.header("📋 Instrucciones")
        st.markdown("""
        1. Complete todos los campos del formulario
        2. Ingrese el tema de su tesis
        3. Provea una API Key de Gemini para el modo de generación real (+10 páginas)
        4. Haga clic en **Generar Proyecto de Tesis**
        5. Visualice la previsualización y descargue los archivos
        """)
        st.markdown("---")
        
        st.header("🔑 Configuración IA")
        gemini_api_key = st.text_input(
            "Gemini API Key",
            type="password",
            placeholder="AIzaSy...",
            help="Ingrese su clave de Google Gemini. Si se deja en blanco, se usará el generador simulado con datos predefinidos."
        )
        
        st.markdown("---")
        st.header("📌 Formato del Esquema")
        st.markdown("""
        - **Márgenes**: Izquierdo 3 cm, Derecho/Sup/Inf 2.5 cm
        - **Fuente**: Arial Narrow 12pt
        - **Interlineado**: 1.5 líneas (Justificado)
        - **Numeración**: Esquina inferior derecha (excluye carátula)
        """)
    
    # Formulario principal
    with st.form("tesis_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            tema = st.text_area(
                "Título del Proyecto de Tesis",
                placeholder="Ej: Sistema Inteligente de Monitoreo de Parámetros Clínicos Basado en IoT para la Optimización del Tiempo de Respuesta en Pacientes de UCI",
                help="Sea claro, conciso y técnico. Se usará este título para contextualizar toda la tesis."
            )
            
            autores = st.text_input(
                "Autor(es)",
                placeholder="Ej: Pérez Gonzales, Juan Carlos, Ruiz Diaz, Maria Fe",
                help="Nombres completos tal como aparecen en DNI. Separe con comas si son varios."
            )
            
            asesor = st.text_input(
                "Nombre del Asesor",
                placeholder="Ej: Dr. Carlos Alberto Mendoza Ríos",
                help="Nombre y grado académico completo del asesor."
            )
        
        with col2:
            linea_investigacion = st.selectbox(
                "Línea de Investigación",
                options=LINEAS_INVESTIGACION
            )
            
            ciudad = st.selectbox(
                "Ciudad",
                options=["Trujillo", "Guadalupe", "Lima", "Arequipa", "Cusco"]
            )
            
            año = st.number_input(
                "Año",
                min_value=2020,
                max_value=2030,
                value=datetime.now().year,
                step=1
            )
        
        # Botón de generación
        submitted = st.form_submit_button("🚀 Generar Proyecto de Tesis (10+ Páginas)", use_container_width=True)
    
    if submitted:
        if not tema or not autores or not asesor:
            st.warning("⚠️ Por favor complete todos los campos requeridos (Título, Autores y Asesor)")
        else:
            with st.spinner("Generando contenido académico inteligente... Esto puede tomar de 15 a 45 segundos ya que genera múltiples capítulos en profundidad..."):
                autores_list = [autor.strip() for autor in autores.split(",")]
                
                payload = {
                    "tema": tema,
                    "autores": autores_list,
                    "asesor": asesor,
                    "linea_investigacion": linea_investigacion,
                    "ciudad": ciudad,
                    "año": año,
                    "jurados": None,
                    "gemini_api_key": gemini_api_key if gemini_api_key else None
                }
                
                try:
                    # 1. Llamar a la API para generar el contenido estructurado
                    response = requests.post(f"{API_URL}/generar_tesis", json=payload)
                    
                    if response.status_code == 200:
                        data = response.json()
                        contenido = data["contenido"]
                        
                        st.session_state["contenido"] = contenido
                        
                        # 2. Generar PDF inmediatamente en el backend
                        export_payload = {
                            "request_data": payload,
                            "contenido": contenido
                        }
                        
                        st.session_state["pdf_data"] = None
                        st.session_state["docx_data"] = None
                        
                        # Generar PDF
                        pdf_resp = requests.post(f"{API_URL}/exportar_pdf", json=export_payload)
                        if pdf_resp.status_code == 200:
                            pdf_path = pdf_resp.json()["pdf_path"]
                            file_resp = requests.get(f"{API_URL}/descargar_archivo", params={"filepath": pdf_path})
                            if file_resp.status_code == 200:
                                st.session_state["pdf_data"] = file_resp.content
                                st.session_state["pdf_filename"] = os.path.basename(pdf_path)
                                
                        # Generar Word
                        docx_resp = requests.post(f"{API_URL}/exportar_docx", json=export_payload)
                        if docx_resp.status_code == 200:
                            docx_path = docx_resp.json()["docx_path"]
                            file_resp = requests.get(f"{API_URL}/descargar_archivo", params={"filepath": docx_path})
                            if file_resp.status_code == 200:
                                st.session_state["docx_data"] = file_resp.content
                                st.session_state["docx_filename"] = os.path.basename(docx_path)
                                
                        st.success("✅ ¡Proyecto de tesis e informes complementarios generados exitosamente!")
                        
                        if gemini_api_key:
                            st.info("💡 Modo de Generación Real de Alta Capacidad activo: Se ha generado un documento denso de más de 10 páginas utilizando la API de Gemini.")
                        else:
                            st.warning("⚠️ Modo Simulado activo: No se ingresó API Key, por lo que se usaron plantillas predefinidas. Ingrese una Gemini API Key en la barra lateral para un informe dinámico de alta calidad.")
                            
                    else:
                        st.error(f"Error al generar el proyecto: Código de estado {response.status_code}. Detalles: {response.text}")
                        
                except requests.exceptions.ConnectionError:
                    st.error("❌ No se pudo conectar al servidor backend. Asegúrese de que FastAPI esté ejecutándose en http://localhost:8000")
                except Exception as e:
                    st.error(f"❌ Error durante el proceso: {str(e)}")
                    
    # Renderizar contenido si existe en session state
    if st.session_state["contenido"] is not None:
        contenido = st.session_state["contenido"]
        
        # Previsualización
        st.markdown("---")
        st.header("📄 Previsualización del Contenido Generado")
        
        # Pestañas para navegar el contenido
        tab1, tab2, tab3, tab4 = st.tabs(["Carátula e Introducción", "Referencias Bibliográficas", "Anexos", "Jurado Dictaminador"])
        
        with tab1:
            st.subheader("Carátula")
            st.markdown(f"""
            **Universidad:** Universidad Nacional de Trujillo  
            **Facultad:** Facultad de Ingeniería  
            **Título:** {contenido['caratula']['titulo'].upper()}  
            **Autores:** {', '.join(contenido['caratula']['autores'])}  
            **Asesor:** {contenido['caratula']['asesor']}  
            **Línea de Investigación:** {contenido['caratula']['linea_investigacion']}  
            **Ciudad y Año:** {contenido['caratula']['ciudad']} - {contenido['caratula']['año']}
            """)
            
            st.subheader("Capítulo I: Introducción")
            with st.expander("Ver introducción completa generada en prosa (márgenes y fuente formateados en las descargas)"):
                st.write(contenido['introduccion'])
        
        with tab2:
            st.subheader("Referencias Bibliográficas (Estilo APA v7)")
            st.info(f"Total de referencias listadas: {len(contenido['referencias'])} (Mínimo 30 referencias requeridas)")
            
            for i, ref in enumerate(contenido['referencias'], 1):
                st.markdown(f"{i}. {ref}")
        
        with tab3:
            st.subheader("Anexo 1: Árbol de Problemas")
            st.text(contenido['anexos']['arbol_problemas'])
            
            st.subheader("Anexo 2: Árbol de Objetivos")
            st.text(contenido['anexos']['arbol_objetivos'])
        
        with tab4:
            st.subheader("Jurado Dictaminador Evaluador")
            jurado = contenido['jurado']
            st.markdown(f"""
            - **Presidente:** {jurado['presidente']['grado']} {jurado['presidente']['nombre']}
            - **Secretario:** {jurado['secretario']['grado']} {jurado['secretario']['nombre']}
            - **Vocal (Asesor):** {jurado['vocal']['grado']} {jurado['vocal']['nombre']}
            """)
            
            st.caption("Nota: Las firmas se renderizan elegantemente en los documentos descargados.")
        
        # Botones de descarga persistentes
        st.markdown("---")
        st.header("💾 Descargar Documento Formateado (Margen Izquierdo 3cm, Superior/Derecho/Inferior 2.5cm, Arial Narrow 12pt, Interlineado 1.5)")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.session_state["pdf_data"] is not None:
                st.markdown('<div class="pdf-btn">', unsafe_allow_html=True)
                st.download_button(
                    label="📥 Descargar Documento Completo en PDF",
                    data=st.session_state["pdf_data"],
                    file_name=st.session_state["pdf_filename"],
                    mime="application/pdf",
                    use_container_width=True
                )
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.warning("El PDF no está listo para descargar.")
                
        with col2:
            if st.session_state["docx_data"] is not None:
                st.markdown('<div class="word-btn">', unsafe_allow_html=True)
                st.download_button(
                    label="📝 Descargar Documento Completo en Word (.docx)",
                    data=st.session_state["docx_data"],
                    file_name=st.session_state["docx_filename"],
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True
                )
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.warning("El archivo Word no está listo para descargar.")

if __name__ == "__main__":
    main()