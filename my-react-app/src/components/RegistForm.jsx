import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import reqService from "../API/RequestService";
import Button from "./UI/Button";
import Input from "./UI/Input";

function RegistForm() {
   const [username, setName] = useState("");
   const [email, setEmail] = useState("");
   const [password, setPassword] = useState("");
   const [repeatPassword, setRepeatPassword] = useState("");
   const [error, setError] = useState(null);

   const nav = useNavigate();

   async function registUser(username, email, password, repeatPassword) {
      const res = await reqService.post("/registration", {
         username: username,
         email: email,
         password: password,
         repit_password: repeatPassword,
      });
      
      typeof res === 'string' ? setError(res) : nav("/home");
   }

   return (
      <form className="max-w-md mx-auto bg-white rounded-md shadow-lg shadow-stone-300 p-8">
         <h1 className="text-2xl font-bold text-gray-800 mb-8 text-left">
            Create account
         </h1>

         <Input
            placeholder="Name"
            value={username}
            onChange={(e) => setName(e.target.value)}
         />

         <Input
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
         />

         <Input
            placeholder="Password (at least 4 symbols)"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            type='password'
         />

         <Input
            placeholder="Repeat password"
            value={repeatPassword}
            onChange={(e) => setRepeatPassword(e.target.value)}
            type='password'
         />

         {error && (
            <div className="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">{error}</div>
         )}

         <Button
            onClick={(e) => {
               e.preventDefault();
               setError(null);
               registUser(username, email, password, repeatPassword);
            }}
         >
            Sign up
         </Button>
         <div className="text-center mt-4">
            <span className="text-gray-600">Already have an account? </span>
            <Link
               to="/login"
               className="text-stone-500 hover:text-stone-700 font-medium"
            >
               Sign in here
            </Link>
         </div>
      </form>
   );
}

export default RegistForm;