import { useState, useEffect } from "react";
import "./App.css";
import { sendMessage, getWords, teachWord } from "./api";

function App() {
  const [input, setInput] = useState("");
  const [chat, setChat] = useState([]);
  const [wordsLearned, setWordsLearned] = useState(0);

  useEffect(() => {
    getWords().then(words => setWordsLearned(words.length));
  }, []);

  const handleSend = async () => {
    if (!input) return;
    setChat([...chat, { sender: "user", text: input }]);
    const res = await sendMessage(input);
    setChat((prev) => [...prev, { sender: "bot", text: res.response }]);
    setInput("");
  };

  const handleTeach = async () => {
    if (!input) return;
    await teachWord(input.trim());
    setInput("");
    const updated = await getWords();
    setWordsLearned(updated.length);
    alert("¡Palabra enseñada!");
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
      <button onClick={handleTeach}>Enseñar palabra</button>
    </div>
  );
}

export default App;