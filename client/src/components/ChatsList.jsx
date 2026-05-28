import { useDispatch, useSelector } from "react-redux";
import ChatsListItem from "./ChatsListItem";
import { setActiveChatId } from "../store/chats/chatsSlice";
// import Button from "./UI/Button";

function ChatsList({ userChatsArray, onChatSelect }) {
   // const handleClick = () => {
   //    const input = document.getElementById("users-search-input");
   //    input?.focus();
   // };
   const dispatch = useDispatch();

   const chatsList = useSelector((state) => state.chats.chatsList);

   const handleChatOpen = (receiverId, username, roomId) => {
      onChatSelect(receiverId, username);

      dispatch(setActiveChatId(roomId));
   };

   return (
      <aside className="w-full h-full bg-white flex flex-col">
         <div className="p-4 border-b border-slate-300 flex-shrink-0 flex items-center h-16">
            <h2 className="text-base font-bold tracking-tight text-slate-800">
               Your Chats
            </h2>
         </div>

         <div className="flex-1 overflow-y-auto divide-y divide-slate-100">
            {chatsList && chatsList.length ? (
               chatsList.map((chat, index) => (
                  <ChatsListItem
                     key={chat.room_id || index}
                     roomId={chat.room_id}
                     userImageLink={chat.profile_photo_url}
                     contactUserName={chat.username}
                     numberOfUnreadMessages={
                        chat.number_of_unread_messages || 0
                     }
                     last_message={chat.last_message.message}
                     receiverId={chat.receiver_id}
                     receiverUsername={chat.username}
                     openChat={handleChatOpen}
                  />
               ))
            ) : (
               <div className="h-full flex flex-col items-center justify-center text-center p-6 bg-slate-50">
                  <div className="w-12 h-12 bg-white border border-slate-300 rounded-xl flex items-center justify-center mb-4 shadow-sm">
                     <svg
                        className="w-6 h-6 text-slate-400"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                     >
                        <path
                           strokeLinecap="round"
                           strokeLinejoin="round"
                           strokeWidth={1.5}
                           d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"
                        />
                     </svg>
                  </div>
                  <p className="text-sm font-bold text-slate-800 mb-1">
                     No chats yet
                  </p>
                  <p className="text-xs text-slate-500 font-medium max-w-[180px] mx-auto leading-relaxed">
                     Start a conversation to see chats here
                  </p>
               </div>
            )}
         </div>

         {/* {userChatsArray.length === 0 && (
            <div className="p-4 border-t border-stone-200 flex-shrink-0">
               <Button onClick={handleClick} className="w-full">
                  Start a new chat
               </Button>
            </div>
         )} */}
      </aside>
   );
}

export default ChatsList;
