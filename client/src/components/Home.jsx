import NotLoggedIn from "../components/NotLoggegIn";
import Loader from "./UI/Loader";
import useGoogleAuth from "../hooks/useGoogleAuth";
import { useState, useEffect } from "react";
import reqService from "@/API/RequestService";

function Home() {
   const { loading, isRefreshTokenAlive } = useGoogleAuth();

   if (loading) {
      return <Loader/>;
   }

   if (!isRefreshTokenAlive) {
      return <NotLoggedIn/>;
   } else {
      const [userChats, setUserChats] = useState([]);

      useEffect(() => {
         getUserChats();
      }, []);

      const getUserChats = async () => {
         const res = await reqService.get('/ws/chats/get_user_rooms');
         setUserChats(res.data)
      }

      return (
         <div>
            <ChatsList userChatsArray={userChats}/>
         </div>
      );
   }
}

export default Home;
