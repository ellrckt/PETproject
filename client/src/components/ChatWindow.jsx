import { useEffect, useState, useRef } from "react";
import Input from "./UI/Input";
import Button from "./UI/Button";

function ChatWindow({ receiverId, receiverName }) {
   const [message, setMessage] = useState("");
   const [messages, setMessages] = useState([]);
   const [isConnected, setIsConnected] = useState(false);

   // WebSocket реф
   const wsRef = useRef(null);

   useEffect(() => {
      if (!receiverId) return;

      const ws = new WebSocket(`ws://localhost:8000/chats/ws/${receiverId}`);
      wsRef.current = ws;

      ws.onopen = () => {
         console.log("Соединение открыто");
         setIsConnected(true);
      };

      ws.onmessage = (event) => {
         const data = JSON.parse(event.data);
         console.log("Получено:", data);

         if (data.content) {
            setMessages((prev) => [...prev, data]);
         }
      };


      ws.onclose = () => {
         console.log("Соединение закрыто");
         setIsConnected(false);
      };

      ws.onerror = (error) => {
         console.error("Ошибка:", error);
         setIsConnected(false);
      };

      return () => {
         if (ws.readyState === WebSocket.OPEN) {
            ws.close();
         }
      };
   }, [receiverId]);

   const sendMessage = () => {
      if (!message.trim()) return;

      if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
         wsRef.current.send(message);
         setMessage("")
      }
   };





   return (
      <div>
         {}

         <Input
            placeholder={"Type message here..."}
            value={message}
            onChange={(e) => setMessage(e.target.value)}
         />
         <Button onClick={() => {}} children={"Send"} />
      </div>
   );
}

export default ChatWindow;
