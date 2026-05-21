import NotLoggedIn from "../components/NotLoggegIn";
import Loader from "./UI/Loader";
import useGoogleAuth from "../hooks/useGoogleAuth";
import reqService from "../API/RequestService";
import ChatsList from "./ChatsList";
import ChatWindow from "./ChatWindow";
import { useState, useEffect } from "react";
import UsersSearch from "./UsersSearch";
import { useDispatch } from "react-redux";
import { setChatsList } from "@/store/chats/chatsSlice";

function Home() {
   const { loading, isRefreshTokenAlive } = useGoogleAuth();
   const [userChats, setUserChats] = useState([]);
   const [receiverId, setReceiverId] = useState(null);
   const [receiverName, setReceiverName] = useState("");
   const dispatch = useDispatch();

   const handleChatOpen = (id, username) => {
      setReceiverId(id);
      setReceiverName(username);
   };

   const handleUserSelect = (user) => {
      setReceiverId(user.user_id);
      setReceiverName(user.username);
   };

   useEffect(() => {
      if (isRefreshTokenAlive) {
         getUserChats();
      }
   }, [isRefreshTokenAlive]);

   const getUserChats = async () => {
      const res = await reqService.get("/chats/get_user_rooms");

      if (res.data.data) {
         setUserChats(res.data.data);
         dispatch(setChatsList(res.data.data));
      } else {
         console.log("ошибка сервера");
      }
   };

   if (loading) {
      return <Loader />;
   }

   if (!isRefreshTokenAlive) {
      return <NotLoggedIn />;
   }

   return (
      <div className="flex h-screen bg-white">
         <ChatsList userChatsArray={userChats} onChatSelect={handleChatOpen} />

         <main className="flex-1 flex flex-col">
            {receiverId ? (
               <ChatWindow
                  receiverId={receiverId}
                  receiverName={receiverName}
               />
            ) : (
               <div className="flex-1 flex items-center justify-center p-8">
                  <div className="text-center text-stone-500">
                     <svg
                        className="w-20 h-20 mx-auto mb-4 text-stone-300"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                     >
                        <path
                           strokeLinecap="round"
                           strokeLinejoin="round"
                           strokeWidth={1}
                           d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"
                        />
                     </svg>
                     <h3 className="text-xl font-medium mb-2">
                        Welcome to Messenger
                     </h3>
                     <p className="mb-4">
                        Select a chat from the left panel or search for users on
                        the right
                     </p>
                  </div>
               </div>
            )}
         </main>

         <UsersSearch onUserSelect={handleUserSelect} />
      </div>
   );
}

export default Home;
