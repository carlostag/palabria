import { useState, useEffect } from "react";
import "./App.css";
import { sendMessage, getWords, teachWord } from "./api";

function App() {
  const [input, setInput] = useState("");
  const [chat, setChat] = useState([]);
  const [wordsLearned, setWordsLearned] = useState(0);

  // Obtener número de palabras conocidas al cargar
  useEffect(() => {
    updateWordsLearned();
  }, []);

  const updateWordsLearned = async () => {
    try {
      const words = await getWords();
      setWordsLearned(words.length);
    } catch (err) {
      console.error("Error al obtener palabras:", err);
    }
  };

  const handleSend = async () => {
    if (!input.trim()) return;

    // Mostrar mensaje del usuario
    setChat((prev) => [...prev, { sender: "user", text: input }]);

    try {
      // Enviar mensaje al bot
      const res = await sendMessage(input);
      setChat((prev) => [...prev, { sender: "bot", text: res.response }]);

      // Enseñar automáticamente
      await teachWord(input.trim());

      // Actualizar el contador
      await updateWordsLearned();
    } catch (err) {
      console.error("Error al enviar mensaje o enseñar palabra:", err);
    }

    setInput("");
  };

  return (
    <div className="app">
      <h1>PalabrIA 👶🤖</h1>
      <p>Palabras conocidas: {wordsLearned}</p>
      <div className="chat-box">
        {chat.map((msg, i) => (
          <div key={i} className={msg.sender}>
            {msg.text}
          </div>
        ))}
      </div>
      <input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Escribe algo..."
      />
      <button onClick={handleSend}>Hablar</button>
    </div>
  );
}

export default App;
