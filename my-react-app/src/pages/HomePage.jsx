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
      const state = params.get('state');
      async function getData() {
         const res = await reqService.post('/login/get_google_token', {code: code, state: state});
         console.log('Результат: ', res);
         return res;
      }
      if (code && state) {
         getData();
      } else {
         console.log('there is no code in url');
      }
   }, []);

   const checkRefreshToken = async () => await reqService.get('/login/check_refresh_token');
   checkRefreshToken().then(res => console.log(res)).catch(err => console.log(err));


   if (!checkRefreshToken()) {
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