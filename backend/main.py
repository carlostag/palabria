from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
from datetime import datetime
import random

app = FastAPI()

# Habilitar CORS para que frontend pueda acceder
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambiar en producción a tu dominio frontend
    allow_methods=["*"],
    allow_headers=["*"],
)

# Conexión a base de datos SQLite (local)
conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

# Crear tablas necesarias
cursor.execute("""
CREATE TABLE IF NOT EXISTS words (
    word TEXT PRIMARY KEY,
    date_added TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS chat_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender TEXT,
    text TEXT,
    timestamp TEXT
)
""")
conn.commit()

class Message(BaseModel):
    text: str

def save_message(sender: str, text: str):
    cursor.execute("INSERT INTO chat_history (sender, text, timestamp) VALUES (?, ?, ?)",
                   (sender, text, datetime.utcnow().isoformat()))
    conn.commit()

def get_last_user_messages(limit=5):
    # Trae las últimas n frases del usuario para contexto simple
    cursor.execute("SELECT text FROM chat_history WHERE sender='user' ORDER BY id DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    return [row[0] for row in rows]

@app.get("/api/words")
def get_words():
    cursor.execute("SELECT word FROM words ORDER BY date_added DESC")
    return [row[0] for row in cursor.fetchall()]

@app.post("/api/learn")
def learn_word(message: Message):
    word = message.text.strip().lower()
    cursor.execute("INSERT OR IGNORE INTO words (word, date_added) VALUES (?, ?)", (word, datetime.utcnow().date().isoformat()))
    conn.commit()
    return {"status": "ok", "learned_word": word}

@app.post("/api/chat")
def chat(message: Message):
    user_text = message.text.lower().strip()
    user_words = user_text.split()

    # Guardar mensaje del usuario
    save_message("user", message.text)

    # Obtener palabras conocidas
    cursor.execute("SELECT word FROM words")
    known_words = set(row[0] for row in cursor.fetchall())

    # Detectar palabras nuevas y aprenderlas automáticamente
    unknown_words = [w for w in user_words if w not in known_words]
    for w in unknown_words:
        cursor.execute("INSERT OR IGNORE INTO words (word, date_added) VALUES (?, ?)", (w, datetime.utcnow().date().isoformat()))
    conn.commit()

    # Detectar palabras entendidas
    understood_words = [w for w in user_words if w in known_words]

    # Construir respuesta inteligente
    if not understood_words and not unknown_words:
        bot_response = "No entiendo lo que dices aún. ¿Puedes enseñarme alguna palabra?"
    else:
        response_parts = []

        if understood_words:
            response_parts.append(f"He entendido: {', '.join(understood_words)}.")

        if unknown_words:
            response_parts.append(f"He aprendido nuevas palabras: {', '.join(unknown_words)}.")

        # Añadir contexto simple: últimas frases del usuario
        recent_msgs = get_last_user_messages()
        if recent_msgs:
            response_parts.append("Me has dicho antes: " + " | ".join(recent_msgs[::-1]))

        # Añadir frase natural aleatoria para hacer la conversación más fluida
        greetings = [
            "¿Quieres contarme más?",
            "Estoy aprendiendo rápido, ¡gracias!",
            "¿Me enseñas otra palabra?",
            "Cuéntame algo más.",
            "Me gusta esta conversación."
        ]
        response_parts.append(random.choice(greetings))

        bot_response = " ".join(response_parts)

    # Guardar respuesta del bot
    save_message("bot", bot_response)

    return {"response": bot_response}
