# 🎓 SJBot — Asistente virtual de Steve Jobs College (Tacna)

Chatbot web con interfaz moderna (Streamlit) que responde sobre notas, asistencia, cursos,
información institucional, y genera la libreta de notas oficial en PDF — todo leyendo en vivo
desde Google Drive, usando **LangChain + Groq** (`openai/gpt-oss-120b`) con *tool calling* y un
**RAG** institucional con FAISS.

## Estructura del proyecto

```
sjbot_web/
├── app.py                  # Interfaz (Streamlit) — lo que ves en pantalla
├── sjbot_engine.py          # Lectura de Drive/Excel, libretas PDF, notas, asistencia
├── sjbot_agent.py            # Tools del agente + lógica de conversación (LangChain + Groq)
├── sjbot_rag.py               # Índice RAG institucional (FAISS + embeddings)
├── corpus_institucional.py     # Base de conocimiento del colegio (admisión, talleres, etc.)
├── assets/PLANTILLA_SECUNDARIA.xlsx   # Molde visual de la libreta
├── requirements.txt          # Dependencias Python
├── packages.txt               # Dependencias del sistema (LibreOffice + fuentes)
└── .streamlit/config.toml      # Tema visual (oscuro, acento naranja institucional)
```

## Dos formas de cargar los datos

La app detecta automáticamente cuál usar:

1. **Google Drive (automático)** — si configuras las credenciales (ver abajo), el bot lee los
   archivos directamente de tu Drive, en vivo. Así, con solo actualizar las notas en Drive, el
   bot ya responde con la información nueva.
2. **Subir archivos** — si no configuras Drive (o quieres una demo rápida sin depender de
   internet de Google), puedes arrastrar la `PLANTILLA_SECUNDARIA.xlsx` y los `REG_SECUNDARIA...`
   directamente en la barra lateral de la app.

Para tu sustentación, te recomiendo tener **ambas** listas: Drive como demo "real", y la opción
de subir archivos como respaldo si algo falla con la conexión en el momento.

---

## 🚀 Despliegue gratuito (Streamlit Community Cloud) — paso a paso

### 1. Consigue tu API key de Groq
Ve a [console.groq.com](https://console.groq.com) → API Keys → Create API Key. Guárdala, la
necesitas en el paso 5.

### 2. (Opcional pero recomendado) Crea una cuenta de servicio de Google para leer Drive
Esto permite que el bot lea el Drive sin que nadie tenga que "iniciar sesión" cada vez.

1. Ve a [console.cloud.google.com](https://console.cloud.google.com) y crea un proyecto nuevo
   (o usa uno existente).
2. En el buscador, entra a **"Google Drive API"** y haz clic en **Habilitar**.
3. Ve a **IAM y administración → Cuentas de servicio → Crear cuenta de servicio**. Ponle un
   nombre (ej. `sjbot-drive-reader`), no necesita permisos de proyecto adicionales, clic en
   **Listo**.
4. Entra a la cuenta de servicio creada → pestaña **Claves** → **Agregar clave → Crear clave
   nueva → JSON**. Se descarga un archivo `.json` — **guárdalo, lo necesitas en el paso 5**.
5. Abre ese JSON y copia el valor de `"client_email"` (algo como
   `sjbot-drive-reader@tu-proyecto.iam.gserviceaccount.com`).
6. Ve a tu carpeta `LIBRETAS` en Google Drive → **Compartir** → pega ese correo → dale acceso de
   **Lector** → Enviar. Sin este paso, el bot no podrá ver los archivos aunque tenga la clave.

### 3. Sube el proyecto a GitHub
1. Crea un repositorio nuevo en [github.com](https://github.com) (puede ser privado).
2. Sube **todos los archivos de esta carpeta** (`app.py`, `sjbot_engine.py`, etc.) — puedes
   arrastrarlos directamente en la interfaz web de GitHub ("Add file → Upload files").
3. **Importante**: no subas ningún `secrets.toml` real (el `.gitignore` ya lo protege si usas
   Git desde la terminal; si usas la web de GitHub, simplemente no lo arrastres).

### 4. Despliega en Streamlit Community Cloud
1. Ve a [share.streamlit.io](https://share.streamlit.io) e inicia sesión con tu cuenta de
   GitHub (es gratis).
2. Clic en **"New app"**.
3. Selecciona tu repositorio, la rama (`main`), y como **Main file path** escribe `app.py`.
4. Clic en **Deploy**. La primera vez tarda unos 5-8 minutos (instala LibreOffice y los modelos
   de embeddings) — es normal, no lo canceles.

### 5. Configura los Secrets
Mientras se despliega (o después, desde el menú **⋮ → Settings → Secrets** de tu app):

1. Pega esto, reemplazando con tus valores reales:

```toml
GROQ_API_KEY = "gsk_tu_key_real_aqui"
DRIVE_FOLDER_ID = "1CjqtuNxa28iipNCSK8pP3IvVP1V7_Xjs"

[gcp_service_account]
type = "service_account"
project_id = "..."
private_key_id = "..."
private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
client_email = "..."
client_id = "..."
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "..."
```

2. Todos esos campos (excepto `GROQ_API_KEY` y `DRIVE_FOLDER_ID`) los copias **tal cual** del
   JSON que descargaste en el paso 2.4 — solo cambia las comillas de JSON a formato TOML (ya
   están así en la plantilla de arriba).
3. Guarda. La app se reinicia sola y ya debería funcionar.

Si **no** quieres configurar Google Cloud antes de tu entrega, omite el bloque
`[gcp_service_account]` y `DRIVE_FOLDER_ID` — la app detectará que no están y mostrará
automáticamente la opción de **subir archivos manualmente**, que funciona igual de bien para
una demo.

### 6. Comparte el link
Streamlit te da una URL pública (`https://tu-app.streamlit.app`) que puedes compartir con tu
profesor, compañeros, o el colegio directamente.

---

## Probarlo en tu computadora antes de desplegar (opcional)

```bash
pip install -r requirements.txt
# instala también libreoffice-calc y las fuentes fonts-crosextra-carlito/caladea en tu sistema
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# edita secrets.toml con tus datos reales
streamlit run app.py
```

## Notas de seguridad y privacidad

- Los datos de notas de los estudiantes solo se leen en memoria durante cada sesión; no se
  guardan en ningún lado fuera de Drive.
- El JSON de la cuenta de servicio es sensible: solo dale acceso de **Lector** (nunca Editor) a
  la carpeta de Drive, y nunca lo subas a un repositorio público.
- Para producción real (uso cotidiano por el colegio), se recomienda agregar autenticación de
  usuarios antes de exponer notas de menores — este proyecto es una base funcional para el
  trabajo académico, no un reemplazo del sistema oficial del colegio.
