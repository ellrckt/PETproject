import React, { useState, useEffect } from "react";

import jwtService from "../API/JwtService";
import reqService from "../API/RequestService";

//import Button from "../components/UI/Button";
import NavBar from "../components/NavBar";
import NotLoggedIn from "../components/NotLoggegIn"

function HomePage() {
   useEffect(() => {
      const params = new URLSearchParams(window.location.search);
      const code = params.get('code');
      async function getData() {
         const res = await reqService.post('/login/get_google_token', code);
         console.log('Результат: ', res);
         return res;
      }
      if (code) {
         //console.log(code);
         getData();
      } else {
         console.log('there is no code in url');
      }
   }, []);

   console.log(jwtService.getAccessToken());

   if (!jwtService.getAccessToken()) {
      return (<NotLoggedIn></NotLoggedIn>);
   } else {
      return (
         <div>
            <NavBar></NavBar>
         </div>
      );
   }
}

export default HomePage;