const BASE = "http://localhost:8000/api";

export async function sendMessage(text) {
  const res = await fetch(`${BASE}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text }),
  });
  return await res.json();
}

export async function getWords() {
  const res = await fetch(`${BASE}/words`);
  return await res.json();
}

export async function teachWord(word) {
  await fetch(`${BASE}/learn`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ word }),
  });
}