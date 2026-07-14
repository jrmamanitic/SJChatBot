# ==============================================================
# SJBot — Interfaz web
# Steve Jobs College (Tacna) · Chatbot institucional y académico
# ==============================================================
import streamlit as st

import sjbot_engine as eng
from sjbot_agent import crear_tools, responder, SYSTEM_PROMPT
from sjbot_rag import construir_retriever

st.set_page_config(page_title="SJBot · Steve Jobs College", page_icon="🎓", layout="wide")

# ---------------------------------------------------------------
# ESTILOS — tema oscuro moderno, acento naranja institucional
# ---------------------------------------------------------------
st.markdown("""
<style>
    :root {
        --sj-orange: #F26B21;
        --sj-orange-dim: #C9531A;
        --sj-bg: #0f1115;
        --sj-panel: #161920;
        --sj-border: #262b36;
    }
    .stApp { background-color: var(--sj-bg); }
    section[data-testid="stSidebar"] {
        background-color: var(--sj-panel);
        border-right: 1px solid var(--sj-border);
    }
    [data-testid="stChatMessage"] {
        background-color: var(--sj-panel);
        border: 1px solid var(--sj-border);
        border-radius: 14px;
        padding: 4px 6px;
    }
    .sjbot-brand {
        display: flex; align-items: center; gap: 10px;
        padding: 6px 0 18px 0;
        border-bottom: 1px solid var(--sj-border);
        margin-bottom: 16px;
    }
    .sjbot-brand .logo {
        width: 38px; height: 38px; border-radius: 10px;
        background: linear-gradient(135deg, var(--sj-orange), var(--sj-orange-dim));
        display: flex; align-items: center; justify-content: center;
        font-size: 20px; font-weight: 700; color: white;
        box-shadow: 0 0 18px rgba(242,107,33,0.35);
    }
    .sjbot-brand .title { font-size: 19px; font-weight: 700; color: #f2f2f2; line-height: 1.1; }
    .sjbot-brand .subtitle { font-size: 12px; color: #9aa1ad; }
    .sj-pill {
        display: inline-block; font-size: 11px; padding: 3px 9px;
        border-radius: 999px; margin: 2px 4px 2px 0;
        border: 1px solid var(--sj-border); color: #c7cbd3; background: #1b1f28;
    }
    .sj-pill.ok { border-color: #2e6b3e; color: #7fd99a; background: #10241a; }
    .sj-pill.warn { border-color: #6b5a2e; color: #d9c07f; background: #241f10; }
    div[data-testid="stChatInput"] textarea { background-color: var(--sj-panel) !important; }
    #MainMenu, footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

AVATAR_BOT = "🎓"
AVATAR_USER = "🧑"

# ---------------------------------------------------------------
# SIDEBAR — branding, fuente de datos, estado
# ---------------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div class="sjbot-brand">
        <div class="logo">SJ</div>
        <div>
            <div class="title">SJBot</div>
            <div class="subtitle">Steve Jobs College · Tacna</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    tiene_drive_secrets = "gcp_service_account" in st.secrets and "DRIVE_FOLDER_ID" in st.secrets
    opciones = ["Google Drive (automático)", "Subir archivos"] if tiene_drive_secrets else ["Subir archivos"]
    fuente = st.radio("Fuente de datos", opciones, label_visibility="collapsed")

    archivos = {}
    if fuente.startswith("Google Drive"):
        try:
            archivos = eng.cargar_archivos_drive(st.secrets["DRIVE_FOLDER_ID"])
        except Exception as e:
            st.error(f"No se pudo conectar a Drive: {e}")
    else:
        st.caption("Sube la PLANTILLA_SECUNDARIA.xlsx y los archivos REG_SECUNDARIA de cada grado.")
        subidos = st.file_uploader("Archivos .xlsx", type="xlsx", accept_multiple_files=True,
                                    label_visibility="collapsed")
        if subidos:
            archivos = eng.cargar_archivos_subidos(subidos)
            # la plantilla se guarda también como asset local para generar PDFs
            for f in subidos:
                if "PLANTILLA" in f.name.upper():
                    eng.RUTA_PLANTILLA_LOCAL.parent.mkdir(exist_ok=True, parents=True)
                    eng.RUTA_PLANTILLA_LOCAL.write_bytes(f.getvalue())

    st.divider()

    if archivos:
        idx = eng.indexar_registros(archivos)
        regs = idx["registros"]
        if regs:
            total_alumnos = sum(len(eng._leer_alumnos(r, archivos)) for bims in regs.values() for r in bims.values())
            st.markdown(f'<span class="sj-pill ok">✓ {len(regs)} grados</span>'
                        f'<span class="sj-pill ok">✓ {total_alumnos} alumnos</span>', unsafe_allow_html=True)
            with st.expander("Ver registros cargados"):
                for g, bims in regs.items():
                    for b, nombre in bims.items():
                        st.caption(f"**{g}** ({b}) — {nombre}")
        if idx["sin_match"] or idx["errores"]:
            st.markdown('<span class="sj-pill warn">⚠ revisar archivos</span>', unsafe_allow_html=True)
            with st.expander("Archivos no reconocidos"):
                for n in idx["sin_match"]:
                    st.caption(f"Sin patrón de grado: {n}")
                for e in idx["errores"]:
                    st.caption(f"Error: {e}")
    else:
        st.info("Todavía no hay datos cargados.")

    st.divider()
    if st.button("🗑️ Nueva conversación", use_container_width=True):
        st.session_state.pop("messages", None)
        st.session_state.pop("lc_history", None)
        st.rerun()

# ---------------------------------------------------------------
# VALIDACIONES PREVIAS
# ---------------------------------------------------------------
if "GROQ_API_KEY" not in st.secrets:
    st.error("Falta configurar `GROQ_API_KEY` en los Secrets de la app. Revisa el README para desplegarla.")
    st.stop()

if not archivos:
    st.title("🎓 SJBot")
    st.markdown("Asistente virtual del **Steve Jobs College — Tacna**. Carga los datos desde el panel "
                "izquierdo para empezar a conversar.")
    st.stop()

import os
os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]

# ---------------------------------------------------------------
# INICIALIZAR AGENTE (una vez, o cuando cambian los archivos)
# ---------------------------------------------------------------
archivos_key = tuple(sorted(archivos.keys()))
if st.session_state.get("archivos_key") != archivos_key:
    from langchain_groq import ChatGroq
    from langchain_core.messages import SystemMessage

    retriever = construir_retriever()
    tools, estado_tools = crear_tools(archivos, retriever)
    llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0.3)
    st.session_state.llm_tools = llm.bind_tools(tools)
    st.session_state.mapa_tools = {t.name: t for t in tools}
    st.session_state.estado_tools = estado_tools
    st.session_state.lc_history = [SystemMessage(content=SYSTEM_PROMPT)]
    st.session_state.messages = []
    st.session_state.archivos_key = archivos_key

# ---------------------------------------------------------------
# CHAT
# ---------------------------------------------------------------
st.markdown("### 🎓 SJBot — Asistente virtual")
st.caption("Notas, asistencia, cursos, libretas en PDF e información institucional.")

for m in st.session_state.get("messages", []):
    avatar = AVATAR_USER if m["role"] == "user" else AVATAR_BOT
    with st.chat_message(m["role"], avatar=avatar):
        st.markdown(m["content"])
        if m.get("pdf_bytes"):
            st.download_button("📄 Descargar libreta (PDF)", data=m["pdf_bytes"],
                                file_name=m["pdf_label"], mime="application/pdf",
                                key=f"dl_{id(m)}")

prompt = st.chat_input("Escribe tu consulta… (ej. 'notas de matemática de Campano de 3ro')")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=AVATAR_USER):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar=AVATAR_BOT):
        with st.spinner("Pensando…"):
            texto, pdf_path, pdf_label = responder(
                prompt, st.session_state.lc_history,
                st.session_state.llm_tools, st.session_state.mapa_tools,
                st.session_state.estado_tools,
            )
        st.markdown(texto)
        pdf_bytes = None
        if pdf_path:
            with open(pdf_path, "rb") as f:
                pdf_bytes = f.read()
            st.download_button("📄 Descargar libreta (PDF)", data=pdf_bytes,
                                file_name=pdf_label, mime="application/pdf",
                                key=f"dl_new_{len(st.session_state.messages)}")
            st.session_state.estado_tools["pdf_path"] = None

    st.session_state.messages.append({
        "role": "assistant", "content": texto,
        "pdf_bytes": pdf_bytes, "pdf_label": pdf_label,
    })
