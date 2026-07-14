# ==============================================================
# SJBot — Agente conversacional (Groq + LangChain + tool calling)
# ==============================================================
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage, ToolMessage

import sjbot_engine as eng

SYSTEM_PROMPT = (
    "Eres SJBot, el asistente virtual del colegio privado Steve Jobs College de Tacna. "
    "Atiendes a docentes y apoderados en español, con un tono cordial, cercano y profesional. "
    "Tienes 6 herramientas, elige la correcta según lo que te pidan:\n"
    "- emitir_libreta: SOLO si piden el documento/PDF/libreta oficial para descargar.\n"
    "- consultar_notas_curso: si preguntan por UN curso puntual (ej. 'cómo va en matemática', "
    "'quién le enseña inglés', 'notas de comunicación'). Menciona siempre el docente.\n"
    "- consultar_resumen_general: si preguntan en general por todos los cursos/notas sin especificar uno.\n"
    "- consultar_asistencia_tool: si preguntan por asistencia, faltas, tardanzas o qué día faltó. "
    "Menciona siempre el porcentaje y, si faltó o llegó tarde, las fechas exactas.\n"
    "- ver_catalogo: si el pedido es ambiguo o no encuentras al estudiante, para mostrar los nombres reales.\n"
    "- consultar_info_institucional: para cualquier pregunta sobre el colegio en general (admisión, "
    "matrícula, uniforme, historia, talleres, servicios, horarios, contacto, estadísticas). No inventes "
    "información institucional: usa siempre esta tool para eso.\n"
    "Nunca inventes notas, docentes, fechas ni nombres: todo sale de los registros oficiales del Drive. "
    "Escala peruana: AD=Logro destacado, A=Logrado, B=En proceso, C=En inicio. Si te preguntan por un "
    "promedio, exprésalo siempre en la letra de la escala peruana, no en números."
)


def crear_tools(archivos: dict, retriever):
    """Crea las tools del agente, ligadas a los archivos y al retriever de esta sesión."""
    estado = {"pdf_path": None, "pdf_label": None}

    @tool
    def ver_catalogo() -> str:
        """Muestra los grados, bimestres y alumnos disponibles en los registros del Drive."""
        lineas = []
        for g, bims in eng.catalogo(archivos).items():
            for b, alumnos in bims.items():
                lineas.append(f"{g} ({b}):")
                lineas += [f"  {n}: {nom}" for n, nom in alumnos.items()]
        return "\n".join(lineas) if lineas else "No se encontraron registros."

    @tool
    def emitir_libreta(estudiante: str, grado: str = "", bimestre: str = "") -> str:
        """Genera la libreta de notas COMPLETA en PDF de un estudiante (todas las áreas, actitudes
        y asistencia). Úsala solo cuando el usuario pida explícitamente el documento/PDF/libreta oficial.
        estudiante: nombre o N° de lista. grado y bimestre opcionales."""
        cand = eng.buscar_alumno(estudiante, archivos, grado or None, bimestre or None)
        if not cand:
            return f'No encontré a "{estudiante}". Usa ver_catalogo para revisar los nombres disponibles.'
        if len(cand) > 1:
            return "Coinciden varios, pide al usuario precisar: " + "; ".join(
                f"{g} N°{n} {nom}" for g, b, n, nom in cand
            )
        g, b, n, nom = cand[0]
        ruta, nombre, g, b = eng.generar_libreta_pdf(g, n, archivos, b)
        estado["pdf_path"] = ruta
        estado["pdf_label"] = f"Libreta_{nombre.replace(' ', '_')}.pdf"
        return f"✅ Libreta de {nombre} ({g}, {b}, N° {n}) generada correctamente."

    @tool
    def consultar_notas_curso(estudiante: str, curso: str, grado: str = "", bimestre: str = "") -> str:
        """Da las notas por competencia de UN curso específico (ej. 'matemática', 'inglés') y el
        nombre del docente que lo dicta. Úsala cuando pregunten por un curso puntual."""
        r = eng.notas_por_curso(estudiante, curso, archivos, grado or None, bimestre or None)
        if "error" in r:
            return r["error"]
        lineas = [f"{r['estudiante']} - {r['area']} ({r['grado']}, {r['bimestre']})",
                  f"Docente: {r['docente']}", "Competencias:"]
        for c in r["competencias"]:
            lineas.append(f"  - {c['competencia']}: U1={c['U1']} U2={c['U2']} BIM={c['BIM']}")
        lineas.append(f"Promedio del curso: {r['promedio_area']}")
        return "\n".join(lineas)

    @tool
    def consultar_resumen_general(estudiante: str, grado: str = "", bimestre: str = "") -> str:
        """Da el promedio de TODOS los cursos de un estudiante y su promedio general del bimestre.
        Úsala cuando pregunten '¿cómo va en general/en todos los cursos?'."""
        r = eng.resumen_notas_general(estudiante, archivos, grado or None, bimestre or None)
        if "error" in r:
            return r["error"]
        lineas = [f"{r['estudiante']} ({r['grado']}, {r['bimestre']})", "Promedio por área:"]
        for a in r["por_area"]:
            lineas.append(f"  - {a['area']}: {a['promedio']}")
        lineas.append(f"Promedio general del bimestre: {r['promedio_general']}")
        return "\n".join(lineas)

    @tool
    def consultar_asistencia_tool(estudiante: str, grado: str = "", bimestre: str = "") -> str:
        """Da la asistencia de un estudiante: % de asistencia, tardanzas/faltas, y las FECHAS EXACTAS
        en que faltó o llegó tarde. Úsala para cualquier pregunta sobre asistencia o inasistencias."""
        r = eng.consultar_asistencia(estudiante, archivos, grado or None, bimestre or None)
        if "error" in r:
            return r["error"]
        lineas = [
            f"{r['estudiante']} ({r['grado']}, {r['bimestre']})",
            f"Asistencia: {r['porcentaje_asistencia']} ({r['total_dias_asistidos']} días asistidos)",
            f"Tardanzas: {r['total_tardanzas']}" + (f" -> {', '.join(r['fechas_tardanzas'])}" if r["fechas_tardanzas"] else ""),
            f"Faltas injustificadas: {r['total_faltas_injustificadas']}" + (f" -> {', '.join(r['fechas_faltas'])}" if r["fechas_faltas"] else ""),
            f"Faltas justificadas: {r['total_faltas_justificadas']}" + (f" -> {', '.join(r['fechas_faltas_justificadas'])}" if r["fechas_faltas_justificadas"] else ""),
        ]
        return "\n".join(lineas)

    @tool
    def consultar_info_institucional(pregunta: str) -> str:
        """Responde preguntas sobre el COLEGIO en general (no sobre notas de un alumno): admisión,
        matrícula, uniforme, historia, propuesta pedagógica, talleres, servicios, estadísticas,
        documentos institucionales o contacto."""
        docs = retriever.invoke(pregunta)
        if not docs:
            return "No encontré información institucional relacionada con esa pregunta."
        return "\n\n".join(f"[{d.metadata['titulo']}]\n{d.page_content}" for d in docs)

    tools = [ver_catalogo, emitir_libreta, consultar_notas_curso, consultar_resumen_general,
             consultar_asistencia_tool, consultar_info_institucional]
    return tools, estado


def responder(mensaje: str, historial_msgs: list, llm_tools, mapa_tools: dict, estado: dict):
    """Ejecuta un turno del agente: invoca el LLM, resuelve tool calls en bucle, devuelve texto final."""
    from langchain_core.messages import HumanMessage

    historial_msgs.append(HumanMessage(content=mensaje))
    resp = llm_tools.invoke(historial_msgs)
    while resp.tool_calls:
        historial_msgs.append(resp)
        for tc in resp.tool_calls:
            salida = mapa_tools[tc["name"]].invoke(tc["args"])
            historial_msgs.append(ToolMessage(content=str(salida), tool_call_id=tc["id"]))
        resp = llm_tools.invoke(historial_msgs)
    historial_msgs.append(resp)
    return resp.content, estado.get("pdf_path"), estado.get("pdf_label")
