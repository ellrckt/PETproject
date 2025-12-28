import ChatsListItem from "./ChatsListItem";
import Button from "./UI/Button";

function ChatsList({ userChatsArray }) {
   // const handleClick = () => {
   //    const input = document.getElementById("users-search-input");
   //    input?.focus();
   // };

   return (
      <aside className="w-80 bg-stone-50 border-r border-stone-200 flex flex-col h-full">
         <div className="p-4 border-b border-stone-200 flex-shrink-0">
            <h2 className="text-xl font-bold text-stone-800">Your Chats</h2>
         </div>

         <div className="flex-1 overflow-y-auto">
            {userChatsArray.length ? (
               userChatsArray.map((chat, index) => (
                  <ChatsListItem
                     key={chat.id || index}
                     userImageLink={chat.profile_photo_url}
                     contactUserName={chat.username}
                     numberOfUnreadMessages={chat.number_of_unread_messages}
                  />
               ))
            ) : (
               <div className="h-full flex flex-col items-center justify-center text-center p-8 text-stone-600">
                  <svg
                     className="w-16 h-16 mb-4 text-stone-300"
                     fill="none"
                     stroke="currentColor"
                     viewBox="0 0 24 24"
                  >
                     <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={1}
                        d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"
                     />
                  </svg>
                  <p className="text-lg font-medium mb-2">No chats yet</p>
                  <p className="text-sm mb-6">
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
