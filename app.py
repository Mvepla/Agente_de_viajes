from flask import Flask, request, render_template, jsonify
import cohere

app = Flask(__name__)

API_KEY= 'RXh0wPt6dOwpB2G6iJ0rlADOOBgUZLBBU8LulmDN'

co = cohere.Client(API_KEY)

def agente_viajes(user_prompt):
    contexto_inicial = """Eres un asistente de viajes que tiene la funcion de ayudar a los usuarios a planificar sus vacaciones. 
    Como asistente proporcionas recomendaciones de destinos, sugieres alojamientos, informas sobre actividades locales, ofreces consejos gastronómicos y brindas información sobre el clima y las mejores fechas para viajar. 
    Personaliza las recomendaciones según el nivel de detalle proporcionado por el usuario en su prompt, teniendo en cuenta su presupuesto y el tipo de experiencia que busca (e.g., aventura, relajación, familiar). 
    El asistente debe proporcionar opciones de diferentes presupuestos. 
    Además, ofrece información sobre requisitos de viaje, como visas y vacunas, y sugiere opciones de transporte, incluyendo vuelos, alquiler de autos y transporte público. 
    Mantén un tono amigable y profesional, asegurándote de que las respuestas sean detalladas pero concisas, y considera la accesibilidad para personas con discapacidades al hacer recomendaciones. 
    Proporciona toda la información complementaria y necesaria para que el usuario tenga una experiencia de viaje completa y satisfactoria.
    IMPORTANTE: TODA la informacion de la respuesta no exceda los 150 tokens en total.
    IMPORTANTE: Solo respondes a preguntas de viajes, si te hacen una pregunta que no sea de viajes tienes que responder: 'lo siento, solo estoy capacitado a responder cuestiones sobre viajes'
"""
    prompt_completo = f"{contexto_inicial}\n{user_prompt}"

    response = co.chat(
        model='command-r-plus',
        message=prompt_completo,
        prompt_truncation="auto",
        connectors=[{"id": "web-search"}],
    )
    return response.text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_prompt = request.form['user_prompt']
    response = agente_viajes(user_prompt)
    # Formatear la respuesta para que esté en párrafos
    formatted_response = response.replace("\n", "<br>")
    return jsonify({'response': formatted_response})

if __name__ == "__main__":
    app.run(debug=True)

