import React from "react";

import NavBar from "../components/NavBar";
import NotLoggedIn from "../components/NotLoggegIn";
import Loader from "./UI/Loader";
import useGoogleAuth from "../hooks/useGoogleAuth";

function Home() {
   const { loading, isRefreshTokenAlive } = useGoogleAuth();

   if (loading) {
      return <Loader/>;
   }

   if (!isRefreshTokenAlive) {
      return <NotLoggedIn/>;
   } else {
      return (
         <div>
            <NavBar/>
         </div>
      );
   }
}

export default Home;
