# ==============================================================
# CORPUS INSTITUCIONAL — Steve Jobs College (Tacna)
# Redactado a partir de información pública de stevejobscollege.edu.pe
# y del Padrón MINEDU (vía miguiadecolegios.org, datos al 05-01-2026).
# Se usa como base de conocimiento para el RAG del chatbot.
# ==============================================================

DOCUMENTOS_INSTITUCIONALES = [
    {
        "titulo": "Historia e identidad institucional",
        "texto": (
            "Steve Jobs College es un colegio privado de Tacna que inició su labor educativa en el año 2020, "
            "autorizado mediante Resolución Directoral Regional N° 000007 del 7 de enero de 2020. Su primer "
            "director fue el profesor Joel Alciviadys Urbano Inquilla, quien continúa siendo el director "
            "reportado ante el MINEDU. El promotor fundador de la institución es el Magíster Helfer Jesús "
            "Loayza Chipana. El colegio está ubicado en Calle Sir Jones S/N, Tacna, a unos 80 metros de la "
            "cochera de Plaza Vea, y pertenece a la UGEL Tacna."
        ),
    },
    {
        "titulo": "Propuesta pedagógica",
        "texto": (
            "La propuesta pedagógica del colegio es de enfoque humanista y cristiano, orientada a que el "
            "estudiante construya su propio aprendizaje de forma activa ('aprende haciendo'), con énfasis en "
            "el pensamiento crítico y creativo. Toma como referencia la pedagogía de Marie Poussepin. El "
            "nombre del colegio rinde homenaje al legado tecnológico de Steve Jobs, y la institución busca "
            "integrar el cultivo de las artes, los idiomas, las ciencias y la investigación dentro de esa "
            "misma orientación humanista."
        ),
    },
    {
        "titulo": "Niveles educativos",
        "texto": (
            "El colegio atiende los niveles de Primaria y Secundaria. En Primaria se busca que el estudiante "
            "desarrolle su potencial intelectual, emocional y físico en un ambiente seguro, formando bases "
            "sólidas para exigencias académicas futuras. En Secundaria se acompaña a los adolescentes en sus "
            "cambios intelectuales, físicos, emocionales y sociales, con foco en la definición de valores, "
            "el desarrollo del talento personal y la preparación hacia su proyecto de vida. El horario de "
            "ingreso en ambos niveles es de 7:00 a 7:40 a.m."
        ),
    },
    {
        "titulo": "Estadísticas oficiales (Padrón MINEDU, datos al 5 de enero de 2026)",
        "texto": (
            "Según el Padrón de Instituciones Educativas del MINEDU, el nivel Primaria de Steve Jobs College "
            "cuenta con 134 alumnos distribuidos en 6 secciones y 11 docentes (ratio aproximado de 12.2 "
            "alumnos por docente). El nivel Secundaria cuenta con 81 alumnos distribuidos en 5 secciones, "
            "también con 11 docentes (ratio aproximado de 7.4 alumnos por docente). Ambos niveles funcionan "
            "en turno mañana."
        ),
    },
    {
        "titulo": "Proceso de admisión",
        "texto": (
            "Para postular a una vacante en Primaria o Secundaria se requiere: ficha de inscripción (publicada "
            "en la web o Facebook del colegio), partida de nacimiento original y actualizada, copia del DNI "
            "del alumno y de los padres, copia de la libreta de notas si el alumno viene trasladado de otra "
            "institución, carnet de vacunación (solo para primer grado de primaria), ficha o constancia de "
            "matrícula del SIAGIE, y constancia de no adeudo si viene de un colegio privado o parroquial. La "
            "edad mínima para ingresar a primer grado de primaria es 6 años cumplidos al 31 de marzo del año "
            "de ingreso. El proceso continúa con el envío del expediente completo por correo electrónico, "
            "una entrevista familiar con el área de Psicología, una entrevista con la coordinadora del nivel, "
            "y los resultados se comunican dentro de las 72 horas siguientes. Si el alumno es admitido, se "
            "envía por correo la resolución de vacante con el detalle de la matrícula. La meta de atención es "
            "de 27 alumnos por aula, y se reservan 2 vacantes por grado para estudiantes con Necesidades "
            "Educativas Especiales (NEE)."
        ),
    },
    {
        "titulo": "Proceso de matrícula",
        "texto": (
            "La matrícula se realiza vía internet dentro del periodo anual que publica el colegio (por "
            "ejemplo, en 2024 fue del 23 de enero al 24 de febrero). Se requiere el voucher de pago de "
            "matrícula, el contrato de prestación de servicio educativo firmado, copia de DNI del alumno y "
            "los padres, y una declaración jurada del seguro de salud del estudiante. Los alumnos que se "
            "trasladan de otro colegio deben presentar además la resolución de traslado y su ficha SIAGIE. "
            "El pago del derecho de matrícula se realiza mediante depósito en la cuenta del colegio en Caja "
            "Tacna. Los padres con pensiones pendientes de pago no pueden matricular a sus hijos, conforme al "
            "artículo 2 de la Ley 26549 que regula a las instituciones educativas privadas. Toda la "
            "documentación se envía por correo electrónico a la secretaría del colegio."
        ),
    },
    {
        "titulo": "Uniforme escolar",
        "texto": (
            "El colegio maneja dos tipos de uniforme. El uniforme de gala se usa en la hora cívica, "
            "actuaciones, desfiles y premiaciones: para los varones consiste en pantalón de vestir plomo, "
            "camisa blanca de manga larga y corbata naranja; para las mujeres, falda de vestir plomo, blusa "
            "blanca de manga larga y corbatín naranja; ambos se completan con medias blancas y zapatos "
            "negros. El buzo deportivo institucional se usa en las clases de educación física y actividades "
            "deportivas, e incluye polo blanco con cuello naranja, casaca deportiva institucional, pantalón "
            "de buzo institucional y zapatillas blancas o negras."
        ),
    },
    {
        "titulo": "Servicio de Psicología y Orientación Vocacional",
        "texto": (
            "El Departamento de Psicología y Orientación Educativa evalúa a los estudiantes que presentan "
            "dificultades de aprendizaje o de conducta, participa en las entrevistas del proceso de admisión, "
            "y apoya la ejecución de los planes de tutoría y la Escuela de Padres. La Orientación Vocacional y "
            "Profesional (OVP) es un proceso continuo a lo largo de toda la etapa escolar, que combina el "
            "componente vocacional (autoconocimiento del estudiante) y el profesional (información sobre "
            "carreras y oportunidades), acompañando a los estudiantes en la construcción de su proyecto de "
            "vida mediante asesoría individual y grupal."
        ),
    },
    {
        "titulo": "Escuela de Padres",
        "texto": (
            "La Escuela de Padres es un espacio de formación, información y reflexión dirigido a las familias "
            "sobre su rol educativo, con el objetivo de fortalecer la comunicación familiar, acompañar el "
            "desarrollo evolutivo de los hijos, y detectar oportunamente posibles dificultades dentro del "
            "núcleo familiar, en coordinación con el Departamento de Psicología del colegio."
        ),
    },
    {
        "titulo": "Servicio de comedor escolar",
        "texto": (
            "El colegio cuenta con un servicio de comedor escolar concesionado. La inscripción y el pago se "
            "realizan únicamente en efectivo, con anticipación, los días jueves y viernes de cada semana, en "
            "el horario de 8:00 a 9:00 a.m. y de 2:00 a 3:30 p.m., directamente en el comedor. El costo "
            "referencial del servicio es de S/ 40 por semana o S/ 160 por mes (4 semanas). Solo se atiende a "
            "los estudiantes que hayan pagado con anticipación y figuren en la lista correspondiente."
        ),
    },
    {
        "titulo": "Talleres y áreas curriculares de secundaria",
        "texto": (
            "Además de las áreas curriculares regulares del Ministerio de Educación (Matemática, Comunicación, "
            "Ciencias Sociales, Ciencia y Tecnología, Inglés, Educación Física, Arte y Cultura, Educación "
            "Religiosa, Desarrollo Personal Ciudadanía y Cívica), el nivel secundario del colegio ofrece "
            "talleres propios de Taller de Cómputo y Taller de Programación y Robótica, y el área de Educación "
            "para el Trabajo con enfoque en proyectos de emprendimiento, en línea con el legado tecnológico "
            "que da nombre a la institución."
        ),
    },
    {
        "titulo": "Documentos institucionales y contacto",
        "texto": (
            "El colegio publica en su web institucional documentos como el Reglamento Interno, el Plan de "
            "Convivencia Democrática y Disciplina Escolar, el Plan de Tutoría y Convivencia, el Plan de "
            "Gestión del Riesgo de Desastres, el Boletín de Sana Convivencia (para estudiantes y para padres) "
            "y el Protocolo de contingencia en caso de accidentes. Para consultas de admisión, el correo de "
            "contacto es admision@stevejobscollege.edu.pe y los teléfonos publicados son 987 238 844 y "
            "992 720 861. El colegio también atiende consultas por Facebook (Colegio Steve Jobs Tacna) e "
            "Instagram."
        ),
    },
]
