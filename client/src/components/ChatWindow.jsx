import { useEffect, useState, useRef } from "react";
import Input from "./UI/Input";
import Button from "./UI/Button";

function ChatWindow({ receiverId, receiverName }) {
   const [message, setMessage] = useState("");
   const [messages, setMessages] = useState([]);
   const [isConnected, setIsConnected] = useState(false);

   // WebSocket реф
   const wsRef = useRef(null);
   const messagesEndRef = useRef(null);

   useEffect(() => {
      if (!receiverId) return;

      const ws = new WebSocket(`ws://localhost:8000/chats/ws/${receiverId}`);
      wsRef.current = ws;

      ws.onopen = () => {
         setIsConnected(true);
      };

      ws.onmessage = (event) => {
         const data = JSON.parse(event.data);

         if (data.message) {
            setMessages((prev) => [...prev, data]);
         }
      };

      ws.onclose = () => {
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

   // Скролл к ласт сообщению
   useEffect(() => {
      if (messagesEndRef.current) {
         messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
      }
   }, [messages]);

   const sendMessage = () => {
      if (!message.trim()) return;

      if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
         wsRef.current.send(message);
         setMessage("");
      }
   };

   const handleKeyPress = (e) => {
      if (e.key === "Enter" && !e.shiftKey) {
         e.preventDefault();
         sendMessage();
      }
   };

   const formatDate = (dateString) => {
      if (!dateString) return "";
      const date = new Date(dateString);
      return `${date.getHours().toString().padStart(2, "0")}:${date
         .getMinutes()
         .toString()
         .padStart(2, "0")}`;
   };

   return (
      <div className="flex flex-col h-full">
         {/* Статус соединения */}
         <div
            className={`px-4 py-2 text-sm ${
               isConnected
                  ? "bg-green-100 text-green-800"
                  : "bg-red-100 text-red-800"
            }`}
         >
            {isConnected ? `Connected to ${receiverName}` : "Disconnected"}
         </div>

         {/* Список сообщений */}
         <div className="flex-1 overflow-y-auto p-4 space-y-4">
            {messages.length === 0 ? (
               <div className="text-center text-gray-500 py-8">
                  No messages yet. Start the conversation!
               </div>
            ) : (
               messages.map((msg, index) => (
                  <div
                     key={msg.message_id || index}
                     className={`flex ${
                        msg.sender_id === receiverId
                           ? "justify-start"
                           : "justify-end"
                     }`}
                  >
                     <div
                        className={`max-w-xs lg:max-w-md rounded-lg px-4 py-2 ${
                           msg.sender_id === receiverId
                              ? "bg-gray-100 text-gray-800"
                              : "bg-blue-500 text-white"
                        }`}
                     >
                        <div className="font-medium mb-1">
                           {msg.sender_id === receiverId ? receiverName : "You"}
                        </div>
                        <div className="mb-1">{msg.message}</div>
                        <div className="text-xs opacity-70">
                           {formatDate(msg.date)}
                           {msg.is_viewed === false && (
                              <span className="ml-2">• Unread</span>
                           )}
                        </div>
                     </div>
                  </div>
               ))
            )}
            <div ref={messagesEndRef} />
         </div>

         <div className="border-t p-4">
            <div className="flex gap-2">
               <Input
                  placeholder="Type message here..."
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                  onKeyPress={handleKeyPress}
                  className="flex-1"
               />
               <Button
                  onClick={sendMessage}
                  disabled={!message.trim() || !isConnected}
               >
                  Send
               </Button>
            </div>
         </div>
      </div>
   );
}

export default ChatWindow;
