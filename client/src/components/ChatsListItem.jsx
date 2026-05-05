function ChatsListItem({ userImageLink, contactUserName, numberOfUnreadMessages  }) {
   return (
      <div className="flex items-center p-4 hover:bg-stone-100 cursor-pointer">
         <div className="mr-3">
            <img
               src={userImageLink}
               alt={contactUserName}
               className="w-12 h-12 rounded-full object-cover"
            />
         </div>

         <div className="flex-1">
            <h3 className="font-medium text-stone-800">{contactUserName}</h3>
         </div>

         {numberOfUnreadMessages > 0 && (
            <div className="ml-2">
               <span className="bg-stone-800 text-white text-xs font-medium rounded-full w-6 h-6 flex items-center justify-center">
                  {numberOfUnreadMessages}
               </span>
            </div>
         )}
      </div>
   );
}

export default ChatsListItem;
