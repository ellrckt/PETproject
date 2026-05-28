import NotLoggedIn from "../components/NotLoggegIn";
import Loader from "./UI/Loader";
import useGoogleAuth from "../hooks/useGoogleAuth";
import reqService from "../API/RequestService";
import ChatsList from "./ChatsList";
import ChatWindow from "./ChatWindow";
import { useState, useEffect } from "react";
import UsersSearch from "./UsersSearch";
import { useDispatch } from "react-redux";
import { setActiveChatId, setChatsList } from "../store/chats/chatsSlice";
import { addInfo } from "./../store/profile/profileSlice";

function Home() {
   const { loading, isRefreshTokenAlive } = useGoogleAuth();
   const [userChats, setUserChats] = useState([]);
   const [receiverId, setReceiverId] = useState(null);
   const [receiverName, setReceiverName] = useState("");
   const [isSearchCollapsed, setIsSearchCollapsed] = useState(false);
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
         getUserId();
      }
   }, [isRefreshTokenAlive]);

   const getUserId = async () => {
      const res = await reqService.get("user/get_current_user");
      dispatch(
         addInfo({
            name: "",
            photo: "",
            id: res.data.user_id,
         }),
      );
      return res.data.user_id;
   };

   const getUserChats = async () => {
      const res = await reqService.get("/chats/get_user_rooms");
      if (res.data.data) {
         setUserChats(res.data.data);
         dispatch(setChatsList(res.data.data));
      } else {
         console.log("ошибка сервера");
      }
   };

   if (loading) return <Loader />;
   if (!isRefreshTokenAlive) return <NotLoggedIn />;

   return (
      <div className="flex h-[calc(100vh-3.5rem)] bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-zinc-900 via-slate-950 to-black p-4 gap-4 overflow-hidden w-full fixed">
         <div className="w-64 h-full flex-shrink-0 bg-white/90 backdrop-blur-md rounded-3xl shadow-[0_8px_30px_rgb(0,0,0,0.04)] border border-white/60 overflow-hidden transition-all duration-300 hover:shadow-[0_8px_30px_rgb(0,0,0,0.08)]">
            <ChatsList
               userChatsArray={userChats}
               onChatSelect={handleChatOpen}
            />
         </div>

         <main className="flex-1 min-w-0 h-full bg-white rounded-3xl shadow-[0_8px_30px_rgb(0,0,0,0.04)] border border-white/60 flex flex-col overflow-hidden">
            {receiverId ? (
               <ChatWindow
                  receiverId={receiverId}
                  receiverName={receiverName}
               />
            ) : (
               <div className="flex-1 flex items-center justify-center p-8 bg-sky-50 from-white to-slate-50/50">
                  <div className="text-center max-w-sm">
                     <div className="w-20 h-20 bg-gradient-to-tr from-slate-100 to-white border border-slate-200/80 rounded-3xl flex items-center justify-center mx-auto mb-6 shadow-[0_10px_20px_rgba(0,0,0,0.02)]">
                        <svg
                           className="w-9 h-9 text-slate-400/90 animate-pulse"
                           fill="none"
                           stroke="currentColor"
                           viewBox="0 0 24 24"
                        >
                           <path
                              strokeLinecap="round"
                              strokeLinejoin="round"
                              strokeWidth={1.25}
                              d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"
                           />
                        </svg>
                     </div>
                     <h3 className="text-xl font-bold tracking-tight text-slate-800 mb-2">
                        Your Workspace
                     </h3>
                     <p className="text-sm text-slate-400 font-medium leading-relaxed">
                        Select a chat from the left deck or find a colleague
                        using the global search to start line of communication.
                     </p>
                  </div>
               </div>
            )}
         </main>

         <div
            className={`h-full bg-white/90 backdrop-blur-md rounded-3xl shadow-[0_8px_30px_rgb(0,0,0,0.04)] border border-white/60 flex-shrink-0 overflow-hidden transition-all duration-300 ease-out ${
               isSearchCollapsed ? "w-20" : "w-80"
            }`}
         >
            <UsersSearch
               onUserSelect={handleUserSelect}
               isCollapsed={isSearchCollapsed}
               setIsCollapsed={setIsSearchCollapsed}
            />
         </div>
      </div>
   );
}

export default Home;
