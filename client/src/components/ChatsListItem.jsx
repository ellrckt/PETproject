import { ArrowRight } from "lucide-react";
import Button from "./UI/Button";

function ChatsListItem({
   userImageLink,
   contactUserName,
   numberOfUnreadMessages,
   last_message,
   receiverId,
   receiverUsername,
   openChat,
}) {
   return (
      <div className="flex items-center p-3 hover:bg-stone-100 active:bg-stone-200 cursor-pointer transition-colors border-b border-stone-100">
         <div className="mr-3 flex-shrink-0">
            <img
               src={userImageLink || "../../public/default-avatar.png"}
               alt="profile photo"
               className="w-12 h-12 rounded-full object-cover border border-stone-200"
            />
         </div>

         <div className="flex-1 min-w-0">
            <h3 className="font-semibold text-stone-800 text-sm truncate mb-0.5">
               {contactUserName}
            </h3>
            <p className="text-xs text-stone-500 truncate">{last_message}</p>
         </div>

         {numberOfUnreadMessages > 0 && (
            <div className="ml-2 flex-shrink-0">
               <span className="bg-stone-800 text-white text-[10px] font-bold rounded-full min-w-5 h-5 px-1.5 flex items-center justify-center">
                  {numberOfUnreadMessages}
               </span>
            </div>
         )}

         <Button
            onClick={() => {
               openChat(receiverId, receiverUsername);
            }}
         >
            <ArrowRight className="w-4 h-4"></ArrowRight>
         </Button>
      </div>
   );
}

export default ChatsListItem;
