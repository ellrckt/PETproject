import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";


import reqService from "../API/RequestService";

export default function useGoogleAuth() {
   const nav = useNavigate();

   const [loading, setLoading] = useState(true);
   const [isRefreshTokenAlive, setIsRefreshTokenAlive] = useState(true);

   //for oauth and check if user is logged in
   useEffect(() => {
      const params = new URLSearchParams(window.location.search);
      const code = params.get("code");
      //const state = params.get('state');

      async function checkRefreshToken() {
         const res = await reqService.get("/login/check_refresh_token");
         if (res.data === true) {
            setIsRefreshTokenAlive(true);
         } else {
            setIsRefreshTokenAlive(false);
         }
      }

      async function getData() {
         await reqService.post("/login/get_google_token", code);
         nav("/home");
         checkRefreshToken();
      }

      if (code) {
         getData();
      } else {
         checkRefreshToken();
      }
      setLoading(false);
   }, [nav]);

   return { loading, isRefreshTokenAlive };
}