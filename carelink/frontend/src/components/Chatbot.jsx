import { useState } from "react"
import { api } from "../services/api"
export default function Chatbot({ language }) {
  const [messages, setMessages] = useState([{ from: "bot", text: "Hello, I am the Care-Link Support Assistant." }])
  const [input, setInput] = useState("")
  async function send() {
    if (!input.trim()) return
    const userMsg = { from: "user", text: input }
    setMessages((prev) => [...prev, userMsg])
    setInput("")
    try {
      const res = await api.chatMessage({ message: userMsg.text, language })
      setMessages((prev) => [...prev, { from: "bot", text: res.reply }])
    } catch (err) {
      setMessages((prev) => [...prev, { from: "bot", text: "Sorry, I could not process that right now." }])
    }
  }
  return (
    <div className="chatbot">
      <div className="chatbot-messages">
        {messages.map((m, i) => (
          <div key={i} className={`chat-bubble ${m.from}`}>{m.text}</div>
        ))}
      </div>
      <div className="chatbot-input">
        <input value={input} onChange={(e) => setInput(e.target.value)} onKeyDown={(e) => e.key === "Enter" && send()} placeholder="Type a message..." />
        <button onClick={send}>Send</button>
      </div>
    </div>
  )
}
