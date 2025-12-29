import { useState, useEffect } from 'react';

import reqService from '../API/RequestService';

export default function useCheckToken() {
   const [isRefreshTokenAlive, setIsRefreshTokenAlive] = useState(false);

   useEffect(() => {
      async function checkRefreshToken() {
         const res = await reqService.get("/login/check_refresh_token");
         if (res.data === true) {
            setIsRefreshTokenAlive(true);
         } else {
            setIsRefreshTokenAlive(false);
         }
      }

      checkRefreshToken();
   }, [])

   return isRefreshTokenAlive;
}