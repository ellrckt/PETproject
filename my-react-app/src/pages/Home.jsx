import React, { useState } from "react";
import jwtService from "../API/JwtService";
import Button from "../components/UI/Button";
import NavBar from "../components/NavBar";

function Home() {
   return (
      <div>
         <NavBar></NavBar>
         <div className="flex space-x-4">
            <Button
               onClick={(e) => {
                  e.preventDefault();
               }}
               className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
            >
               Регистрация
            </Button>

            <Button
               onClick={(e) => {
                  e.preventDefault();
               }}
               className="px-4 py-2 bg-gray-200 text-gray-800 rounded hover:bg-gray-300 transition-colors"
            >
               Вход
            </Button>
         </div>
      </div>
      
   );
}

export default Home;