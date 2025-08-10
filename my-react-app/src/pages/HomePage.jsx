import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

import jwtService from "../API/JwtService";
import reqService from "../API/RequestService";

//import Button from "../components/UI/Button";
import NavBar from "../components/NavBar";
import NotLoggedIn from "../components/NotLoggegIn"

function HomePage() {
   const nav = useNavigate();

   //for oauth and check if user is logged in
   useEffect(() => {
      const params = new URLSearchParams(window.location.search);
      const code = params.get('code');
      //const state = params.get('state');

      console.log(typeof code, code);

      async function checkRefreshToken() {
         const res = await reqService.get('/login/check_refresh_token');
         if (res.data === true) {
            setRefrToken(true);
         } else {
            setRefrToken(false);
         }
      }

      async function getData() {
         const res = await reqService.post('/login/get_google_token', code);
         console.log('Результат: ', res);

         checkRefreshToken();
         nav('/home');
      }

      if (code) {
         getData();
      } else {
         checkRefreshToken();
      }
   }, [nav]);

   

   const [refrToken, setRefrToken] = useState(null);


   if (!refrToken) {
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