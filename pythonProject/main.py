import streamlit as st
import google.generativeai as genai
import textwrap
from IPython.display import Markdown
import sys
import smtplib
from email.mime.text import MIMEText

# Configuración de Gemini AI
sys.stdout.reconfigure(encoding='utf-8')
modelo = genai.GenerativeModel('gemini-pro')
GOOGLE_API_KEY = 'AIzaSyAlrya-gRP9XIEb169o7RKH0NSasirm0bs'  # Reemplazar con su clave API de Google
genai.configure(api_key=GOOGLE_API_KEY)

# Función para analizar el comentario
def analizar_comentario(comentario):
  # Generar respuesta de Gemini AI
  respuesta = modelo.generate_content(comentario)
  respuesta = respuesta.text

  # Analizar si el comentario es positivo o negativo
  if "positivo" in respuesta.lower() or "bueno" in respuesta.lower():
    return "Comentario positivo. No se requiere acción."
  else:
    return f"Comentario negativo o con sugerencias de mejora: {respuesta}"

# Función para enviar correo electrónico
def enviar_correo(comentario, analisis):
  # Configurar correo electrónico Outlook
  remitente = "willianvargas1995@hotmail.com"  # Reemplazar con su correo electrónico de Outlook
  destinatario = "wsvargas@uce.edu.ec"
  asunto = "Análisis de comentario"
  mensaje = f"""
  Comentario: {comentario}

  Análisis: {analisis}
  """

  # Crear mensaje de correo electrónico
  msg = MIMEText(mensaje)
  msg['Subject'] = asunto
  msg['From'] = remitente
  msg['To'] = destinatario

  # Enviar correo electrónico con Outlook SMTP
  with smtplib.SMTP('smtp.office365.com', 587) as server:
    server.starttls()
    # **Cambio:** Usar el método `login()` con el correo electrónico y la contraseña de la aplicación
    server.login(remitente, 'ygvjkhnihbufsrbb')  # Reemplazar con su contraseña de aplicación de Outlook
    server.sendmail(remitente, destinatario, msg.as_string())

# Interfaz de usuario con Streamlit
st.title("Análisis de comentarios")

# Cuadro de texto para ingresar el comentario
comentario = st.text_input("Ingrese su comentario:")

# Botón para enviar el comentario
if st.button("Enviar"):
  # Analizar el comentario
  analisis = analizar_comentario(comentario)

  # Mostrar el resultado del análisis
  st.markdown(f"**Análisis:** {analisis}")

  # Enviar correo electrónico si es necesario
  if "negativo" in analisis.lower() or "sugerencias" in analisis.lower():
    enviar_correo(comentario, analisis)
    st.markdown("**Correo electrónico enviado a wsvargas@uce.edu.ec**")
