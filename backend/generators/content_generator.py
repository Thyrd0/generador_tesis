from datetime import datetime, timedelta
import random
from typing import List, Dict

class ContentGenerator:
    def __init__(self):
        self.lineas_investigacion = [
            "Gestión de Gobierno y Servicios de TIC",
            "Gestión de Proyectos de TIC", 
            "Gestión de Desarrollo de Software",
            "Gestión de Infraestructura y Comunicaciones",
            "Gestión de la Seguridad de la Información"
        ]

    def generar_contenido_completo(self, request):
        import os
        api_key = getattr(request, "gemini_api_key", None) or os.environ.get("GEMINI_API_KEY")
        
        gemini_active = False
        if api_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=api_key)
                _ = genai.GenerativeModel("gemini-2.5-flash")
                gemini_active = True
            except Exception as e:
                print(f"Error configurando Gemini API: {e}")
                gemini_active = False
                
        if gemini_active:
            try:
                print("Iniciando generación con Gemini API...")
                return self._generar_con_gemini(request)
            except Exception as e:
                print(f"Error durante generación con Gemini: {e}. Usando generador simulado.")
        
        return {
            "caratula": self._generar_caratula(request),
            "jurado": self._generar_jurado(request),
            "introduccion": self._generar_introduccion(request),
            "referencias": self._generar_referencias(request.tema),
            "anexos": self._generar_anexos(request.tema)
        }

    def _generar_caratula(self, request):
        return {
            "titulo": request.tema,
            "autores": request.autores,
            "asesor": request.asesor,
            "linea_investigacion": request.linea_investigacion,
            "ciudad": request.ciudad,
            "año": request.año
        }

    def _generar_jurado(self, request):
        if request.jurados:
            return request.jurados
        
        # Jurados simulados
        return {
            "presidente": {
                "nombre": "Dr. Juan Carlos Mendoza Ramirez",
                "grado": "Doctor"
            },
            "secretario": {
                "nombre": "Dr. Roberto Sanchez Gonzales",
                "grado": "Doctor"
            },
            "vocal": {
                "nombre": f"Dr. {request.asesor}",
                "grado": "Doctor"
            }
        }

    def _generar_introduccion(self, request):
        tema = request.tema
        linea = request.linea_investigacion
        
        # Realidad Problemática
        realidad = f"""En el contexto actual de transformación digital, la {linea} se ha convertido en un factor crítico para el desarrollo organizacional. La problemática relacionada con {tema} presenta desafíos significativos que requieren atención inmediata.

A nivel global, las organizaciones enfrentan dificultades para implementar soluciones efectivas en el ámbito de {tema}. Estudios recientes demuestran que más del 60% de las iniciativas relacionadas no alcanzan los objetivos esperados debido a la falta de metodologías adecuadas y herramientas especializadas.

En el contexto nacional, particularmente en {request.ciudad}, la situación es aún más crítica. Las instituciones locales carecen de frameworks específicos para abordar {tema}, lo que resulta en ineficiencias operativas y pérdida de oportunidades de mejora. Los indicadores muestran que solo el 25% de las organizaciones cuentan con estrategias definidas en esta área.

El problema de investigación se centra en cómo desarrollar e implementar una solución tecnológica que permita optimizar los procesos relacionados con {tema}, considerando las limitaciones y características específicas del entorno local."""
        
        # Antecedentes
        antecedentes = f"""A nivel internacional, diversos autores han abordado temáticas relacionadas con {tema}. Smith y Johnson (2023) en su estudio publicado en el Journal of Systems Engineering demostraron que la aplicación de metodologías ágiles mejora significativamente los resultados en proyectos de TIC. Por su parte, García et al. (2024) desarrollaron un framework integral para la gestión de proyectos tecnológicos en el sector educativo.

En el ámbito nacional, Pérez (2023) en su tesis doctoral analizó el impacto de las soluciones tecnológicas en la eficiencia organizacional. Asimismo, Rodríguez (2024) propuso un modelo de implementación para sistemas de información en empresas peruanas, demostrando mejoras del 40% en los indicadores clave."""
        
        # Marco Teórico con 3 metodologías
        marco_teorico = f"""El marco teórico de esta investigación se fundamenta en tres metodologías estándar para el desarrollo de soluciones tecnológicas:

1. Metodología Scrum: Framework ágil que permite el desarrollo iterativo e incremental de software. Caracterizado por sprints de 2-4 semanas, roles definidos (Product Owner, Scrum Master, Development Team) y artefactos como Product Backlog y Sprint Backlog. Su aplicación en proyectos de {tema} ha demostrado reducir el tiempo de desarrollo en un 30%.

2. Metodología DevOps: Enfoque que integra desarrollo y operaciones, automatizando el ciclo de vida del software. Incluye integración continua, entrega continua, monitoreo y retroalimentación. Para {tema}, DevOps permite una implementación más rápida y confiable.

3. Metodología ITIL (Information Technology Infrastructure Library): Conjunto de mejores prácticas para la gestión de servicios de TI. Proporciona un framework sistemático para alinear los servicios de TI con las necesidades del negocio. Su aplicación en {tema} garantiza calidad y mejora continua.

Además, se consideran conceptos fundamentales como arquitectura de software, bases de datos, seguridad informática y experiencia de usuario, todos ellos relevantes para el desarrollo de la solución propuesta."""
        
        # Justificación
        justificacion = f"""La presente investigación se justifica desde tres perspectivas:

Justificación Teórica: Esta investigación contribuirá al conocimiento existente sobre {tema} mediante la aplicación y adaptación de metodologías reconocidas internacionalmente, generando nuevo conocimiento aplicable al contexto local.

Justificación Práctica: Los resultados permitirán a las organizaciones de {request.ciudad} implementar soluciones efectivas para {tema}, mejorando su eficiencia operativa y competitividad en el mercado.

Justificación Metodológica: Se desarrollará e implementará un procedimiento sistemático para abordar {tema}, que servirá como referencia para futuras investigaciones en el campo de la Ingeniería de Sistemas."""
        
        # Problema
        problema = f"""¿De qué manera la implementación de una solución basada en metodologías ágiles y buenas prácticas de ingeniería de software puede mejorar los procesos relacionados con {tema} en las organizaciones de {request.ciudad}?"""
        
        # Hipótesis
        hipotesis = f"""La implementación de una solución tecnológica basada en metodologías ágiles (Scrum, DevOps e ITIL) mejorará significativamente los procesos relacionados con {tema}, evidenciándose en indicadores de eficiencia, calidad y satisfacción de los usuarios finales."""
        
        # Objetivos
        objetivos = {
            "general": f"Desarrollar e implementar una solución tecnológica basada en metodologías ágiles para mejorar los procesos relacionados con {tema} en las organizaciones de {request.ciudad}.",
            "especificos": [
                f"Analizar el estado actual de los procesos relacionados con {tema} en organizaciones de {request.ciudad}.",
                "Seleccionar y adaptar las metodologías más adecuadas (Scrum, DevOps, ITIL) para el desarrollo de la solución.",
                f"Diseñar la arquitectura de la solución tecnológica para {tema} considerando los requisitos funcionales y no funcionales.",
                f"Implementar un prototipo funcional que aborde los principales problemas identificados en {tema}.",
                f"Evaluar el impacto de la solución implementada mediante indicadores clave de rendimiento.",
                "Documentar las lecciones aprendidas y mejores prácticas para futuras implementaciones."
            ]
        }
        
        # Limitaciones
        limitaciones = f"""El estudio presenta las siguientes limitaciones:

Limitación Espacial: La investigación se circunscribe a organizaciones ubicadas en la ciudad de {request.ciudad}, por lo que los resultados pueden no ser directamente generalizables a otros contextos geográficos con características diferentes.

Limitación Temporal: El desarrollo e implementación de la solución se realizará en un período de 12 meses, tiempo que puede ser insuficiente para observar todos los beneficios a largo plazo de la solución propuesta.

Otras limitaciones incluyen la disponibilidad de recursos tecnológicos, la curva de aprendizaje de los usuarios, y posibles resistencias al cambio durante la implementación."""
        
        # Combinar todo en prosa sin subtítulos
        introduccion_completa = f"""{realidad}

{antecedentes}

{marco_teorico}

{justificacion}

Problema: {problema}

Hipótesis: {hipotesis}

Objetivo General: {objetivos['general']}

Objetivos Específicos:
{chr(10).join([f'- {obj}' for obj in objetivos['especificos']])}

Limitaciones del Estudio: {limitaciones}"""
        
        return introduccion_completa

    def _generar_referencias(self, tema):
        referencias = []
        autores_ejemplo = [
            "Smith, J.", "Johnson, M.", "García, R.", "Pérez, A.", 
            "Rodríguez, C.", "Martínez, L.", "Wilson, K.", "Brown, T.",
            "Davis, S.", "Anderson, P.", "Thompson, R.", "White, J.",
            "Harris, M.", "Martin, L.", "Lee, S.", "Walker, D.",
            "Hall, R.", "Allen, K.", "Young, P.", "King, M."
        ]
        
        temas_variados = [
            f"Advances in {tema} for digital transformation",
            f"Systematic approach to {tema} implementation",
            f"Impact of agile methodologies on {tema}",
            f"Framework for {tema} in developing countries",
            f"Security considerations in {tema}",
            f"Performance evaluation of {tema} solutions",
            f"User experience in {tema} applications",
            f"Cost-benefit analysis of {tema} projects",
            f"Integration challenges in {tema}",
            f"Future trends in {tema} research"
        ]
        
        años = list(range(datetime.now().year - 5, datetime.now().year + 1))
        años_antiguos = list(range(datetime.now().year - 10, datetime.now().year - 5))
        
        # Generar 30 referencias (80% últimos 5 años = 24, 20% últimos 10 años = 6)
        for i in range(24):
            autor = random.choice(autores_ejemplo)
            año = random.choice(años)
            titulo = random.choice(temas_variados)
            referencia = f"{autor} ({año}). {titulo}. *Journal of Systems Engineering and Technology*, {random.randint(10, 50)}({random.randint(1, 4)}), {random.randint(100, 500)}-{random.randint(501, 1000)}. https://doi.org/10.1000/{random.randint(10000, 99999)}"
            referencias.append(referencia)
        
        for i in range(6):
            autor = random.choice(autores_ejemplo)
            año = random.choice(años_antiguos)
            titulo = f"Foundational concepts in {tema}"
            referencia = f"{autor} ({año}). {titulo}. *International Journal of Computer Science*, {random.randint(1, 20)}({random.randint(1, 3)}), {random.randint(50, 200)}-{random.randint(201, 500)}."
            referencias.append(referencia)
        
        # Ordenar alfabéticamente
        referencias.sort()
        
        return referencias

    def _generar_anexos(self, tema):
        return {
            "arbol_problemas": self._generar_arbol_problemas(tema),
            "arbol_objetivos": self._generar_arbol_objetivos(tema)
        }

    def _generar_arbol_problemas(self, tema):
        return f"""
ÁRBOL DE PROBLEMAS - {tema}

EFECTO CENTRAL:
- Baja eficiencia en los procesos relacionados con {tema}
- Altos costos operativos
- Insatisfacción de los usuarios

CAUSAS PRINCIPALES:
1. Falta de metodologías estandarizadas
2. Tecnología obsoleta
3. Personal no capacitado
4. Ausencia de automatización
5. Procesos manuales ineficientes

EFECTOS:
- Pérdida de productividad
- Mayor tiempo de respuesta
- Errores frecuentes
- Baja competitividad
- Incremento de quejas

RELACIONES CAUSA-EFECTO:
La falta de metodologías estandarizadas (causa) genera procesos inconsistentes que llevan a baja eficiencia (efecto central). La tecnología obsoleta y la ausencia de automatización provocan altos costos operativos y pérdida de productividad.
"""

    def _generar_arbol_objetivos(self, tema):
        return f"""
ÁRBOL DE OBJETIVOS - {tema}

OBJETIVO CENTRAL:
- Implementar solución tecnológica eficiente para {tema}
- Reducir costos operativos significativamente
- Alcanzar alta satisfacción de usuarios

MEDIOS PRINCIPALES:
1. Implementar metodologías estandarizadas (Scrum, DevOps, ITIL)
2. Actualizar infraestructura tecnológica
3. Capacitar al personal
4. Automatizar procesos clave
5. Optimizar flujos de trabajo

FINES:
- Incrementar productividad en 40%
- Reducir tiempo de respuesta en 50%
- Eliminar errores recurrentes
- Mejorar posicionamiento competitivo
- Disminuir quejas en 80%

RELACIONES MEDIOS-FINES:
La implementación de metodologías estandarizadas (medio) junto con la automatización de procesos permitirá alcanzar el objetivo central. La capacitación del personal y actualización tecnológica son medios habilitantes para lograr los fines propuestos.
"""

    def _generar_con_gemini(self, request):
        tema = request.tema
        linea = request.linea_investigacion
        ciudad = request.ciudad

        # 1. Generar secciones de Introducción por separado para evitar límites y asegurar 10+ páginas
        realidad = self._generar_realidad_gemini(tema, linea, ciudad)
        antecedentes = self._generar_antecedentes_gemini(tema)
        marco = self._generar_marco_teorico_gemini(tema, linea)
        justificacion = self._generar_justificacion_gemini(tema, ciudad)
        formulaciones = self._generar_formulaciones_gemini(tema, ciudad)
        limitaciones = self._generar_limitaciones_gemini(tema, ciudad)

        # Unir toda la introducción estructuradamente en prosa académica
        introduccion = f"""{realidad}

{antecedentes}

{marco}

{justificacion}

{formulaciones}

{limitaciones}"""

        # 2. Generar referencias en formato APA v7 (exactamente 30)
        referencias_texto = self._generar_referencias_gemini(tema)
        # Parsear las referencias en una lista
        referencias = []
        for line in referencias_texto.split("\n"):
            line = line.strip()
            # Quitar viñetas, números al inicio (ej. '1. ', '- ')
            if line:
                cleaned_line = line
                # Quitar número al inicio si existe
                if cleaned_line.startswith(("-", "*", "•")):
                    cleaned_line = cleaned_line[1:].strip()
                elif cleaned_line[0].isdigit():
                    # quitar el número y el punto/paréntesis posterior
                    idx = 0
                    while idx < len(cleaned_line) and cleaned_line[idx].isdigit():
                        idx += 1
                    if idx < len(cleaned_line) and cleaned_line[idx] in [".", ")", "-", " "]:
                        cleaned_line = cleaned_line[idx+1:].strip()
                if cleaned_line:
                    referencias.append(cleaned_line)

        # Si por alguna razón falló el parseo o quedó vacío, usar el simulador de fallback
        if len(referencias) < 15:
            referencias = self._generar_referencias(tema)

        # 3. Generar anexos
        anexos_texto = self._generar_anexos_gemini(tema)
        arbol_problemas = ""
        arbol_objetivos = ""
        if "[PROBLEMAS]" in anexos_texto and "[OBJETIVOS]" in anexos_texto:
            parts = anexos_texto.split("[OBJETIVOS]")
            arbol_problemas = parts[0].replace("[PROBLEMAS]", "").strip()
            arbol_objetivos = parts[1].strip()
        else:
            arbol_problemas = self._generar_arbol_problemas(tema)
            arbol_objetivos = self._generar_arbol_objetivos(tema)

        return {
            "caratula": self._generar_caratula(request),
            "jurado": self._generar_jurado(request),
            "introduccion": introduccion,
            "referencias": referencias,
            "anexos": {
                "arbol_problemas": arbol_problemas,
                "arbol_objetivos": arbol_objetivos
            }
        }

    def _call_gemini(self, prompt: str, system_instruction: str = None) -> str:
        import google.generativeai as genai
        # Intentamos usar gemini-2.5-flash primero; fallback a gemini-1.5-flash
        models_to_try = ["gemini-2.5-flash", "gemini-1.5-flash"]
        last_error = None
        for model_name in models_to_try:
            try:
                # El parámetro system_instruction es soportado por los modelos más recientes
                model = genai.GenerativeModel(
                    model_name=model_name,
                    system_instruction=system_instruction or "Eres un metodólogo experto en proyectos de tesis e Ingeniería de Sistemas, y dominas las normas APA v7."
                )
                response = model.generate_content(prompt)
                if response and response.text:
                    return response.text.strip()
            except Exception as e:
                last_error = e
                continue
        raise last_error or RuntimeError("No se pudo comunicar con ningún modelo de Gemini")

    def _generar_realidad_gemini(self, tema, linea, ciudad):
        prompt = f"""
        Genera la sección 'Realidad Problemática' para un proyecto de tesis de Ingeniería de Sistemas.
        
        Tema de la tesis: {tema}
        Línea de investigación: {linea}
        Ciudad/Contexto local: {ciudad}
        
        Requisitos de redacción:
        - Escribe en prosa fluida y académica formal, sin subtítulos intermedios.
        - Debe tener al menos 800 palabras de contenido denso.
        - Organiza la redacción en tres niveles de análisis claro:
          1. Contexto Internacional: problemática global relacionada con el tema, tendencias y desafíos tecnológicos en otros países, citando al menos 2 autores internacionales (por ejemplo, Smith & Johnson, 2023; Davis, 2024).
          2. Contexto Nacional: situación actual en el país (Perú), brechas digitales, infraestructura, citando al menos 2 autores nacionales (por ejemplo, Pérez, 2023; Rodríguez, 2024).
          3. Contexto Local: situación y problemática específica observada en las organizaciones o el entorno de {ciudad}, indicando ineficiencias concretas y la necesidad de una solución.
        - Finaliza formulando claramente la problemática y cómo el estudio propone abordarla.
        
        Devuelve únicamente el texto de la Realidad Problemática en prosa formal.
        """
        return self._call_gemini(prompt)

    def _generar_antecedentes_gemini(self, tema):
        prompt = f"""
        Genera la sección de 'Antecedentes de la Investigación' para un proyecto de tesis de Ingeniería de Sistemas sobre: "{tema}".
        
        Requisitos estrictos:
        - Debes detallar al menos 3 antecedentes internacionales y 3 antecedentes nacionales (Perú).
        - Para cada uno de los 6 antecedentes, escribe en prosa fluida (sin viñetas simples) explicando detalladamente:
          * Autor(es) y año de publicación (formato de citación APA v7, ej. García et al., 2024).
          * Título de la investigación.
          * Objetivo principal del estudio.
          * Metodología empleada (tipo, diseño, herramientas o frameworks usados).
          * Resultados o hallazgos clave.
          * Conclusión principal y cómo se relaciona o aporta directamente a nuestra tesis.
        - Escribe una prosa continua, formal e hilada de al menos 1000 palabras en total.
        
        Devuelve únicamente los antecedentes estructurados en párrafos académicos fluidos.
        """
        return self._call_gemini(prompt)

    def _generar_marco_teorico_gemini(self, tema, linea):
        prompt = f"""
        Genera el 'Marco Teórico' detallado para un proyecto de tesis de Ingeniería de Sistemas sobre: "{tema}".
        
        Requisitos estrictos:
        - Debe fundamentar conceptualmente la investigación y explicar en profundidad al menos tres metodologías estándar o frameworks tecnológicos de la Ingeniería de Sistemas que sean directamente aplicables a la solución (por ejemplo: Scrum para la gestión ágil, DevOps para la integración y despliegue continuo, ITIL para la gestión de servicios de TI, TOGAF para arquitectura empresarial, etc. o los que mejor se adapten al tema).
        - Para cada metodología, explica:
          * Origen y principios fundamentales.
          * Fases, procesos o componentes clave.
          * Justificación técnica de por qué y cómo se aplicará a la solución de esta tesis.
        - Incluye bases teóricas y conceptos fundamentales de ingeniería (arquitectura de software, bases de datos, seguridad, calidad de software, etc.).
        - Debe redactarse en prosa académica formal con citas en formato APA v7 (ej. Harris, 2022; Thompson, 2023).
        - Debe tener al menos 1200 palabras de contenido en prosa para ser lo suficientemente denso y riguroso.
        
        Devuelve únicamente el texto del Marco Teórico.
        """
        return self._call_gemini(prompt)

    def _generar_justificacion_gemini(self, tema, ciudad):
        prompt = f"""
        Genera la sección de 'Justificación de la Investigación' para un proyecto de tesis de Ingeniería de Sistemas sobre: "{tema}" en la ciudad de {ciudad}.
        
        Debes redactar con alta densidad académica y en prosa formal y fluida las siguientes perspectivas:
        - Justificación Teórica: Explicar cómo la investigación aporta a la discusión científica actual, al desarrollo de nuevas metodologías de ingeniería y teorías de sistemas.
        - Justificación Práctica: Explicar cómo la implementación de la solución resuelve problemas operativos reales en el contexto local de {ciudad}, y sus beneficios directos en costos o eficiencia.
        - Justificación Metodológica: Explicar cómo el enfoque sistémico u operacional desarrollado servirá como pauta para que futuros investigadores aborden problemáticas similares.
        
        Escribe párrafos detallados para cada justificación. Extensión aproximada: 500 palabras.
        """
        return self._call_gemini(prompt)

    def _generar_formulaciones_gemini(self, tema, ciudad):
        prompt = f"""
        Genera las formulaciones metodológicas claves para un proyecto de tesis de Ingeniería de Sistemas sobre: "{tema}" en la ciudad de {ciudad}.
        
        Debes formular de manera sumamente precisa y formal:
        1. Formulación del Problema: La pregunta general de investigación de forma interrogativa.
        2. Hipótesis General: La respuesta tentativa que asocia variables tecnológicas y operacionales.
        3. Objetivo General: El fin principal del proyecto (usualmente comienza con Desarrollar, Implementar, Diseñar o Proponer).
        4. Objetivos Específicos: Una lista de al menos 6 objetivos específicos que describan las etapas secuenciales del proyecto de ingeniería (ej. analizar la problemática, diseñar la arquitectura, desarrollar los módulos principales, validar o probar el sistema, evaluar la eficiencia, etc.).
        
        Formato de respuesta estricto:
        Devuelve el contenido en el siguiente formato textual (puedes usar saltos de línea):
        
        Problema: ¿De qué manera la implementación de... ?
        
        Hipótesis: La implementación de ...
        
        Objetivo General: Desarrollar ...
        
        Objetivos Específicos:
        - Analizar ...
        - Diseñar ...
        - Implementar ...
        - Validar ...
        - Evaluar ...
        - Documentar ...
        """
        return self._call_gemini(prompt)

    def _generar_limitaciones_gemini(self, tema, ciudad):
        prompt = f"""
        Genera la sección de 'Limitaciones de la Investigación' para un proyecto de tesis de Ingeniería de Sistemas sobre: "{tema}" en la ciudad de {ciudad}.
        
        Debes redactar en prosa formal y detallada las limitaciones en tres dimensiones:
        - Limitación Espacial: Delimitación geográfica de la investigación en la ciudad de {ciudad}.
        - Limitación Temporal: El período de tiempo establecido para el estudio y evaluación de resultados.
        - Limitaciones de Recursos y Acceso: Consideraciones sobre presupuesto, acceso a bases de datos y resistencia al cambio organizativo.
        
        Escribe de forma continua y sumamente profesional. Extensión aproximada: 300 palabras.
        """
        return self._call_gemini(prompt)

    def _generar_referencias_gemini(self, tema):
        prompt = f"""
        Genera una lista de exactamente 30 referencias bibliográficas académicas en formato APA v7 para el tema: "{tema}".
        
        Requisitos estrictos de la lista de referencias:
        - Debe contener exactamente 30 referencias reales o simuladas con alto realismo científico.
        - Al menos el 80% (24 referencias) deben ser de los últimos 5 años (2021-2026).
        - Al menos el 80% (24 referencias) deben estar redactadas en inglés.
        - Al menos el 80% (24 referencias) deben pertenecer a artículos científicos indexados de revistas de alto impacto (IEEE, Scopus, Springer, Elsevier, etc.) e incluir su correspondiente DOI simulado o real (ej. https://doi.org/10.1109/...).
        - Deben estar ordenadas rigurosamente de forma alfabética por el apellido del autor principal.
        - Deben incluir autores clave que se asocien con los citados en las secciones de la tesis (como Smith, Johnson, García, Pérez, Davis, Rodriguez, Harris, Thompson, etc.).
        - El formato debe ser estrictamente APA v7: Autor, A. A., & Autor, B. B. (Año). Título del artículo. Nombre de la Revista, Volumen(Número), páginas. https://doi.org/...
        
        Devuelve únicamente la lista ordenada alfabéticamente de las 30 referencias.
        """
        return self._call_gemini(prompt)

    def _generar_anexos_gemini(self, tema):
        prompt = f"""
        Genera el Anexo 1: Árbol de Problemas y el Anexo 2: Árbol de Objetivos para un proyecto de tesis sobre: "{tema}".
        
        Debes estructurar el texto con diagramas legibles en formato de texto y listas con sangría muy detalladas que expliquen con rigor metodológico:
        
        Para el Árbol de Problemas:
        [PROBLEMAS]
        EFECTO CENTRAL e Indirectos (los impactos negativos de no resolver el problema).
        PROBLEMA CENTRAL (la situación insatisfactoria identificada).
        CAUSAS DIRECTAS e Indirectas (raíces tecnológicas, humanas y de procesos que originan el problema).
        Explicación de las relaciones causa-efecto.
        
        Para el Árbol de Objetivos:
        [OBJETIVOS]
        FIN CENTRAL e Indirectos (los impactos positivos esperados).
        OBJETIVO CENTRAL (la situación deseada a alcanzar).
        MEDIOS DIRECTOS e Indirectos (estrategias, metodologías ágiles y automatización para alcanzar el objetivo).
        Explicación de las relaciones medios-fines.
        
        Debe ser amplio, detallado y metodológicamente riguroso.
        Usa obligatoriamente las etiquetas exactas [PROBLEMAS] y [OBJETIVOS] en líneas separadas para delimitar cada sección.
        """
        return self._call_gemini(prompt)