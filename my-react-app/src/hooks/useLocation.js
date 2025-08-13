import { useState, useEffect } from 'react';

export default function useLocation() {
   const [coords, setCoords] = useState({lat: null, lng: null});

   useEffect(() => {
      if ("geolocation" in navigator) {
         navigator.geolocation.getCurrentPosition(
            (position) => {
               const {latitude, longitude } = position.coords;
               setCoords({lat: latitude, lng: longitude});
            },
            (error) => {
               return error.message;
            }
         );
         } else {
         return 'this browser doesnt support geo';
      }
   }, [])

   return coords;
}