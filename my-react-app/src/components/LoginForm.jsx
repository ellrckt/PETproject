import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

import jwtService from "../API/JwtService";
import Button from "./UI/Button";
import Input from "./UI/Input";

function LoginForm() {
   const [email, setEmail] = useState("");
   const [password, setPassword] = useState("");
   const [error, setError] = useState(null);

   const nav = useNavigate();

   async function loginUser(email, password) {
      const res = await jwtService.post("/login", {
         email: email,
         password: password,
      });

      typeof res === 'string' ? setError(res) : nav("/home");
   }

   return (
      <form className="max-w-md mx-auto bg-white rounded-md shadow-lg p-8">
         <h1 className="text-2xl font-bold text-gray-800 mb-8 text-left">
            Вход
         </h1>

         <Input
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
         />

         <Input
            placeholder="Пароль"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
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
            Войти
         </Button>
      </form>
   );
}

export default LoginForm;