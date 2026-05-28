import { ArrowRight } from "lucide-react";
import Button from "./UI/Button";

function ChatsListItem({
   roomId,
   userImageLink,
   contactUserName,
   numberOfUnreadMessages,
   last_message,
   receiverId,
   receiverUsername,
   openChat,
}) {
   return (
      <div className="flex items-center p-3 hover:bg-slate-50 active:bg-slate-100 cursor-pointer transition-colors border-b border-slate-100">
         <div className="mr-3 flex-shrink-0">
            <img
               src={userImageLink || "../../public/default-avatar.png"}
               alt="profile photo"
               className="w-12 h-12 rounded-full object-cover border border-slate-200"
            />
         </div>

         <div className="flex-1 min-w-0">
            <h3 className="font-bold text-slate-800 text-sm truncate mb-0.5">
               {contactUserName}
            </h3>
            <p className="text-xs text-slate-500 font-medium truncate">
               {last_message}
            </p>
         </div>

         {numberOfUnreadMessages > 0 && (
            <div className="ml-2 flex-shrink-0">
               <span className="bg-slate-800 text-white text-[10px] font-bold rounded-full min-w-5 h-5 px-1.5 flex items-center justify-center">
                  {numberOfUnreadMessages}
               </span>
            </div>
         )}

         <div className="w-12 flex-shrink-0 ml-3">
            <Button
               onClick={() => {
                  openChat(receiverId, receiverUsername, roomId);
               }}
            >
               <div className="flex items-center justify-center w-full">
                  <ArrowRight className="w-4 h-4" />
               </div>
            </Button>
         </div>
      </div>
   );
}

export default ChatsListItem;
