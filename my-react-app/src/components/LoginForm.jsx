import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

import jwtService from "../API/JwtService";
import Button from "./UI/Button";
import Input from "./UI/Input";

import logo from '../assets/images/google-icon.svg'

function LoginForm() {
   const [email, setEmail] = useState("");
   const [password, setPassword] = useState("");
   const [error, setError] = useState(null);

   const nav = useNavigate();

   async function loginUser(email, password) {
      const res = await jwtService.post("/login", {
         email: email.toLowerCase(),
         password: password,
      });

      typeof res === 'string' ? setError(res) : nav("/home");
   }

   function getGoogleUri(e) {
      e.preventDefault();
      window.location.href = 'http://localhost:8000/login/get_google_uri';
   }

   return (
      <form className="max-w-md mx-auto bg-white rounded-md shadow-lg shadow-stone-300 p-8">
         <h1 className="text-2xl font-bold text-gray-800 mb-8 text-left">
            Login
         </h1>

         <Input
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
         />

         <Input
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            type='password'
         />

         {error && (
            <div className="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">{error}</div>
         )}

         <Button
            onClick={(e) => {
               e.preventDefault();
               setError(null);
               loginUser(email, password);
            }}
         >
            Log in
         </Button>

         <button 
            onClick={getGoogleUri}
            className="flex items-center justify-center w-full px-4 py-3 mt-6 text-gray-700 bg-white border border-stone-300 rounded-lg shadow-sm hover:bg-stone-50">
            <img src={logo} alt="Google" className="w-5 h-5 mr-3" />
            Login with Google
         </button>
      </form>
   );
}

export default LoginForm;