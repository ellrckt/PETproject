import ChatsListItem from "./ChatsListItem";

function ChatsList({ userChatsArray }) {
   return (
      <aside className="w-80 h-screen bg-stone-50 border-r border-stone-200">
         <div className="p-4 border-b border-stone-200">
            <h2 className="text-xl font-bold text-stone-800">Your Chats</h2>
         </div>

         {userChatsArray.length ? (
            userChatsArray.map((chat) => (
               <ChatsListItem
                  userImageLink={chat.profile_photo_url}
                  contactUserName={chat.username}
                  numberOfUnreadMessages={chat.number_of_unread_messages}
               />
            ))
         ) : (
            <p className="text-lg font-medium mb-2">No Chats</p>
         )}
      </aside>
   );
}

export default ChatsList;
