from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
import os
import uvicorn

app = FastAPI()

# Habilitar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB INIT
conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS words (word TEXT PRIMARY KEY, date_added TEXT)")
conn.commit()

# Schemas
class Message(BaseModel):
    text: str

class WordData(BaseModel):
    word: str

# Endpoint: obtener palabras conocidas
@app.get("/api/words")
def get_words():
    cursor.execute("SELECT word FROM words")
    return [row[0] for row in cursor.fetchall()]

# Endpoint: agregar palabra
@app.post("/api/learn")
def learn_word(data: WordData):
    cursor.execute("INSERT OR IGNORE INTO words (word, date_added) VALUES (?, date('now'))", (data.word.lower(),))
    conn.commit()
    return {"status": "ok"}

# Endpoint: responder al usuario
@app.post("/api/chat")
def chat(message: Message):
    user_text = message.text.lower().split()
    cursor.execute("SELECT word FROM words")
    known_words = set(row[0] for row in cursor.fetchall())

    understood = [word for word in user_text if word in known_words]
    unknown = [word for word in user_text if word not in known_words]

    if not understood:
        return {"response": "No entiendo lo que dices aún. ¿Puedes enseñarme alguna palabra?"}

    response = " ".join(understood)
    if unknown:
        response += " (pero aún no conozco: " + ", ".join(unknown) + ")"
    return {"response": response}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
