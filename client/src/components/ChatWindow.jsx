import { useEffect, useState, useRef } from "react";
import { Send } from "lucide-react";
import Input from "./UI/Input";
import Button from "./UI/Button";
import reqService from "../API/RequestService";
import Summarization from "./contextualSummarization/Summarization";
import SearchButton from "./contextualSearch/SearchButton";

function ChatWindow({ receiverId, receiverName }) {
   const [message, setMessage] = useState("");
   const [messages, setMessages] = useState([]);
   const [isConnected, setIsConnected] = useState(false);
   const [translatingIds, setTranslatingIds] = useState(new Set());

   const wsRef = useRef(null);
   const messagesEndRef = useRef(null);

   useEffect(() => {
      if (!receiverId) return;

      setMessages([]);

      const ws = new WebSocket(`ws://localhost:8000/chats/ws/${receiverId}`);
      wsRef.current = ws;

      ws.onopen = () => {
         setIsConnected(true);
      };

      ws.onmessage = (event) => {
         const data = JSON.parse(event.data);

         if (data.type === "history") {
            setMessages((prev) => [...prev, data.data]);
         } else if (data.message) {
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
         ws.onmessage = null;

         if (ws.readyState === WebSocket.OPEN) {
            ws.close();
         }
      };
   }, [receiverId]);

   useEffect(() => {
      if (messagesEndRef.current && messages.length > 0) {
         messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
      }
   }, [messages]);

   const translateMessage = async (messageId, text) => {
      setTranslatingIds((prev) => new Set([...prev, messageId]));

      try {
         const res = await reqService.post("/chats/translate_message", {
            message_id: messageId.toString(),
            message_to_translate: text,
         });

         if (!res || !res.data) {
            console.error("Некорректный ответ от сервера");
            return;
         }

         console.log("Ответ от сервера:", res);

         if (!res || !res.data) {
            console.error("Некорректный ответ от сервера");
            return;
         }

         const data = res.data;
         console.log("Данные перевода:", data);

         setMessages((prev) =>
            prev.map((msg) => {
               return String(msg.message_id) === String(data.message_id)
                  ? { ...msg, message: data.translation, is_translated: true }
                  : msg;
            }),
         );
      } catch (error) {
         console.error("Translation error:", error);
      } finally {
         setTranslatingIds((prev) => {
            const newSet = new Set([...prev]);
            newSet.delete(messageId);
            return newSet;
         });
      }
   };

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
      <div className="flex flex-col h-full bg-sky-50 w-full">
         <div className="p-4 bg-white border-b border-slate-300 flex items-center justify-between gap-4 h-16 shrink-0">
            <h2 className="text-base font-bold tracking-tight text-slate-800 truncate">
               {receiverId ? `Chat with ${receiverName}` : "Messages"}
            </h2>
            {/* <SearchButton /> */}
         </div>

         <div
            className={`px-4 py-2 text-xs font-bold uppercase tracking-wider border-b border-slate-300 select-none shrink-0 ${
               isConnected
                  ? "bg-emerald-50 border-emerald-200 text-emerald-800"
                  : "bg-rose-50 border-rose-200 text-rose-800"
            }`}
         >
            {isConnected ? `Connected to ${receiverName}` : "Disconnected"}
         </div>

         <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-slate-50">
            {messages.length === 0 ? (
               <div className="text-center text-slate-400 font-medium py-8 text-sm">
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
                        className={`max-w-xs lg:max-w-md rounded-xl p-3 border ${
                           msg.sender_id === receiverId
                              ? "bg-white border-slate-300 text-slate-800"
                              : "bg-slate-800 border-slate-900 text-white"
                        }`}
                     >
                        <div
                           className={`text-xs font-bold mb-1 uppercase tracking-wide ${
                              msg.sender_id === receiverId
                                 ? "text-slate-500"
                                 : "text-slate-300"
                           }`}
                        >
                           {msg.sender_id === receiverId ? receiverName : "You"}
                        </div>
                        <div className="text-sm leading-relaxed font-medium break-words mb-1.5">
                           {msg.message}
                        </div>
                        <div className="flex justify-between items-center gap-4">
                           <div
                              className={`text-[10px] font-bold uppercase tracking-wide ${
                                 msg.sender_id === receiverId
                                    ? "text-slate-400"
                                    : "text-slate-400"
                              }`}
                           >
                              {formatDate(msg.date)}
                              {msg.is_viewed === false && (
                                 <span className="ml-2 text-amber-600 font-extrabold">
                                    • Unread
                                 </span>
                              )}
                           </div>
                        </div>
                     </div>
                  </div>
               ))
            )}
            <div ref={messagesEndRef} />
         </div>

         <div className="border-t border-slate-300 p-3 bg-white shrink-0">
            <div className="flex items-center gap-3 w-full max-w-none">
               <div className="flex-1">
                  <Input
                     placeholder="Type message here..."
                     value={message}
                     onChange={(e) => setMessage(e.target.value)}
                     onKeyPress={handleKeyPress}
                  />
               </div>

               <div className="w-12 flex-shrink-0">
                  <Button
                     onClick={sendMessage}
                     disabled={!message.trim() || !isConnected}
                  >
                     <div className="flex items-center justify-center w-full">
                        <Send className="h-4 w-4" />
                     </div>
                  </Button>
               </div>

               <Summarization></Summarization>
            </div>
         </div>
      </div>
   );
}

export default ChatWindow;
