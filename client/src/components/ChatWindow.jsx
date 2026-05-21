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
      <div className="flex flex-col h-full">
         <div className="p-4 border-b border-stone-200 flex items-center justify-between gap-4">
            <h2 className="text-lg font-semibold text-stone-800 truncate">
               {receiverId ? `Chat with ${receiverName}` : "Messages"}
            </h2>
            <SearchButton />
         </div>

         <div
            className={`px-4 py-2 text-sm ${
               isConnected
                  ? "bg-green-100 text-green-800"
                  : "bg-red-100 text-red-800"
            }`}
         >
            {isConnected ? `Connected to ${receiverName}` : "Disconnected"}
         </div>

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
                        <div className="flex justify-between items-center">
                           <div className="text-xs opacity-70">
                              {formatDate(msg.date)}
                              {msg.is_viewed === false && (
                                 <span className="ml-2">• Unread</span>
                              )}
                           </div>
                           {/* {!msg.is_translated &&
                              msg.sender_id === receiverId && (
                                 <button
                                    onClick={() =>
                                       translateMessage(
                                          msg.message_id.toString(),
                                          msg.message,
                                       )
                                    }
                                    disabled={translatingIds.has(
                                       msg.message_id,
                                    )}
                                    className="ml-2 text-xs px-2 py-1 bg-gray-200 hover:bg-gray-300 rounded disabled:opacity-50 disabled:cursor-not-allowed"
                                 >
                                    {translatingIds.has(msg.message_id)
                                       ? "Translating..."
                                       : "Translate"}
                                 </button>
                              )} */}
                        </div>
                     </div>
                  </div>
               ))
            )}
            <div ref={messagesEndRef} />
         </div>

         <div className="border-t p-2 bg-white">
            <div className="flex items-center gap-2 w-full">
               <Input
                  placeholder="Type message here..."
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                  onKeyPress={handleKeyPress}
                  className="flex-1 w-full"
               />
               <Button
                  onClick={sendMessage}
                  disabled={!message.trim() || !isConnected}
                  className="whitespace-nowrap"
               >
                  <Send h-4 w-4 />
               </Button>
               {/* <Summarization></Summarization> */}
            </div>
         </div>
      </div>
   );
}

export default ChatWindow;
