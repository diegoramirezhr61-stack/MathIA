from flask import Flask, render_template, request, jsonify
from groq import Groq

app = Flask(__name__)

# =========================================================
# GROQ
# =========================================================

cliente = Groq(
    api_key=""
)

# =========================================================
# IA
# =========================================================

def preguntar_ia(prompt):

    try:

        respuesta = cliente.chat.completions.create(

            model="llama-3.1-8b-instant",

            messages=[
                {
                    "role": "system",
                    "content": (
                        "Eres MathIA v5.0, un asistente matemático experto. "
                        "Hablas español y explicas paso a paso."
                         )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.3,
            max_tokens=800
        )

        return respuesta.choices[0].message.content

    except Exception as e:
        return f"Error: {e}"

# =========================================================
# RUTAS
# =========================================================

@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/preguntar", methods=["POST"])
def preguntar():

    datos = request.get_json()

    pregunta = datos.get("pregunta", "")

    respuesta = preguntar_ia(pregunta)

    return jsonify({
        "respuesta": respuesta
    })

# =========================================================
# INICIO
# =========================================================

if __name__ == "__main__":
    app.run(debug=True)