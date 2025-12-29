import { useState, useEffect } from "react";

//ToDo - add types

export default function useLocation() {
   const [coords, setCoords] = useState({ lat: null, lng: null });
   1;

   useEffect(() => {
      if ("geolocation" in navigator) {
         navigator.geolocation.getCurrentPosition(
            (position) => {
               const { latitude, longitude } = position.coords;
               setCoords({ lat: latitude, lng: longitude });
            },
            (error) => {
               return error.message;
            }
         );
      } else {
         return "this browser doesnt support geo";
      }
   }, []);

   return coords;
}
