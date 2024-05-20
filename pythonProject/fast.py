from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import textwrap

# Configurar API Key de Google para el modelo Gemini Pro
GOOGLE_API_KEY = 'AIzaSyAlrya-gRP9XIEb169o7RKH0NSasirm0bs'
genai.configure(api_key=GOOGLE_API_KEY)

# Usar modelo generativo de Gemini Pro
modelo = genai.GenerativeModel('gemini-pro')

# Información específica sobre VetMed
informacion_vetmed = """
1. ¿Cuáles son los horarios de atención?
Lunes: 8 a.m. – 8 p.m.
Martes: 8 a.m. – 8 p.m.
Miércoles: 8 a.m. – 8 p.m.
Jueves: 8 a.m. – 8 p.m.
Viernes: 8 a.m. – 6 p.m.
Sábado: SOLO EMERGENCIAS
Domingo: 7:30 a.m. – 7:30 p.m.
2. ¿Cuáles son los horarios de atención en la sucursal de llano grande?
Lunes: 7:00 a.m. – 10:00 p.m.
Martes: 7:00 a.m. – 10:00 p.m.
Miércoles: 7:00 a.m. – 10:00 p.m.
Jueves: 7:00 a.m. – 10:00 p.m.
Viernes: 7:00 a.m. – 6:00 p.m.
Sábado: NO HAY ATENCION
Domingo: 7:00 a.m. – 10:00 p.m.
3. ¿ATenden en este feriado?
Todos los feriados con normalidad (excepto el día sábado)
4. ¿Cuál es el precio de la peluquería canina?
Base de $14,00 el valor incrementa dependiendo el Tpo de corte, tamaño de la
mascota y el estado del pelaje de la mascota.
5. ¿Cuentan con servicio de domicilio?
Si, con recargo adicional
6. ¿Cuál es el precio de la consulta?
$16,00
7. ¿Cuál es el precio de la esterilización para mi mascota?
Depende del peso de la mascota, contáctanos para darte valores exactos
8. ¿Disponen de tal medicamento?
Un asesor te indicara si disponemos
9. ¿Qué costo Tenen las vacunas anuales?
Son 3 vacunas anuales
MúlTple, Bordetella, Rabia cada una en $15,00 incluye desparasitación
10. ¿A qué edad se les pone la primera vacuna?
Perros 6 semanas
Gastos 8 semanas
11. ¿Cuáles son los servicios que ofrecen?
Pet Shop, peluquería canina, farmacia, rayos x, ecograia, consulta general y
especialidad como ojalmología, neurología, oncología, dermatología,
odontología, medicina de felinos, cirugía, traumatología, emergencias las 24
horas
12. ¿Ponen el chip?
Si
13. ¿Cuál es el precio de la petdulacion?
14. ¿Qué incluye la petdulacion?
Implantación de microchip, placa Qr, cerTficado de, cedula
15. ¿Qué incluye el servicio de peluquería?
Corte de acuerdo a la raza o gusto del propietario, baño, corte de uñas, limpieza
de oídos, limpieza de glándulas perianales, accesorio.
16. ¿Qué incluye la vacuna?
Chequeo veterinario previo, vacuna, desparasitación
17. ¿Cuáles son sus métodos de pago?
18. EfecTvo, tarjeta débito y crédito y transferencia
19. ¿En dónde están ubicados?
Matriz Carapungo: Av. Galo Plaza Lasso N15 – 396 (Frente al estadio de la liga
barrial)
Sucursal Llano Grande: Av. Gabriel García Moreno y Psje. Orquídeas (Plaza
Comercial Cesarin)
20. ¿Cuáles son las vacunas para perros?
Puppy
Rabia
Bordetella
MulTple
21. ¿Cuáles son las vacunas para gato?
Triple Felina
Leucemia Felina
Rabia
22. ¿Cuántas vacunas son para perro?
Depende de la edad en la que empieza el plan vacunal
23. ¿Cuántas vacunas son para gato?
24. ¿Cómo agendo una cita?
Puedes dejarnos tus datos y tu Tempo de disponibilidad, y nos contactamos
conTgo
25. ¿A que numero puedo comunicarme para una emergencia?
0997545626
"""

# Inicializar la aplicación FastAPI
app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todas las fuentes, en producción es mejor especificar el dominio.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo de datos para la solicitud
class QueryModel(BaseModel):
    user_prompt: str

# Ruta para la raíz
@app.get("/")
async def root():
    return {"message": "Bienvenido a VetMed. Este es VETMEDicito, tu asistente virtual para información comercial sobre la veterinaria."}

# Ruta para manejar la consulta del usuario
@app.post("/ask")
async def ask_vetmed(query: QueryModel):
    # Ajustar el prompt para dar contexto al modelo generativo
    full_prompt = f"""Eres VETMEDicito, un asistente virtual para VetMed, una veterinaria. Aquí está la información que debes usar para responder preguntas:
{informacion_vetmed}

Basándote en esa información, responde la siguiente pregunta sobre VetMed: {query.user_prompt}
"""
    # Obtener respuesta del modelo
    respuesta = modelo.generate_content(full_prompt).text

    # Validar la respuesta
    if "Lo siento" in respuesta or "no encontré información" in respuesta or "Esa información" in respuesta or "información" in respuesta:
        return {
            "response": f"""**Lo siento, no encontré información suficiente en mi base de datos para responder tu pregunta con precisión.** 

Para brindarte la mejor atención, te recomiendo que te acerques a una de nuestras sucursales o nos llames al 0997545626. 

Nuestros veterinarios expertos estarán encantados de atenderte y resolver todas tus dudas.**"""
        }
    else:
        return {"response": respuesta}
