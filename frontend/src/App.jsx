import { useState, useEffect } from "react";
import { sendMessage, getWords } from "./api";

function App() {
  const [input, setInput] = useState("");
  const [chat, setChat] = useState([]);
  const [wordsLearned, setWordsLearned] = useState(0);

  useEffect(() => {
    refreshWords();
  }, []);

  const refreshWords = async () => {
    const words = await getWords();
    setWordsLearned(words.length);
  };

  const handleSend = async () => {
    if (!input.trim()) return;

    setChat(prev => [...prev, { sender: "user", text: input }]);
    const res = await sendMessage(input);
    setChat(prev => [...prev, { sender: "bot", text: res.response }]);

    await refreshWords();
    setInput("");
  };

  return (
    <div className="app">
      <h1>PalabrIA 👶🤖</h1>
      <p>Palabras conocidas: {wordsLearned}</p>
      <div className="chat-box" style={{maxHeight:"400px",overflowY:"auto",border:"1px solid #ccc",padding:"10px",marginBottom:"10px"}}>
        {chat.map((msg, i) => (
          <div key={i} style={{textAlign: msg.sender === "user" ? "right" : "left"}}>
            <b>{msg.sender === "user" ? "Tú" : "Bot"}:</b> {msg.text}
          </div>
        ))}
      </div>
      <input
        value={input}
        onChange={e => setInput(e.target.value)}
        onKeyDown={e => { if(e.key === 'Enter') handleSend(); }}
        placeholder="Escribe algo..."
        style={{width:"80%",padding:"10px"}}
      />
      <button onClick={handleSend} style={{padding:"10px 15px",marginLeft:"10px"}}>Enviar</button>
    </div>
  );
}

export default App;
