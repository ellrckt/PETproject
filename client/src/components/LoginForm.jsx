import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useDispatch } from "react-redux";
import { addInfo } from "./../store/profile/profileSlice";
import jwtService from "../API/JwtService";
import Button from "./UI/Button";
import Input from "./UI/Input";
import logo from "../assets/images/google-icon.svg";

function LoginForm() {
   const dispatch = useDispatch();

   const [email, setEmail] = useState("");
   const [password, setPassword] = useState("");
   const [error, setError] = useState(null);

   const nav = useNavigate();

   async function loginUser(email, password) {
      const res = await jwtService.post("/login", {
         email: email.toLowerCase(),
         password: password,
      });

      const userData = res.data;

      console.log(userData);

      dispatch(
         addInfo({
            name: "",
            photo: "",
            id: userData.id,
         }),
      );

      typeof res === "string" ? setError(res) : nav("/");
   }

   function getGoogleUri(e) {
      e.preventDefault();
      window.location.href = "http://localhost:8000/login/get_google_uri";
   }

   return (
      <form className="w-full max-w-md mx-auto bg-white rounded-xl border border-slate-300 p-8 shadow-[0_10px_25px_-5px_rgba(148,163,184,0.1)]">
         <div className="text-center mb-8">
            <h1 className="text-2xl font-bold tracking-tight text-slate-800">
               Login
            </h1>
            <p className="text-xs text-slate-500 mt-1.5 uppercase tracking-wider font-semibold">
               Enter your credentials
            </p>
         </div>

         <div className="space-y-4 mb-6">
            <Input
               placeholder="Email"
               value={email}
               onChange={(e) => setEmail(e.target.value)}
            />

            <Input
               placeholder="Password"
               value={password}
               onChange={(e) => setPassword(e.target.value)}
               type="password"
            />
         </div>

         {error && (
            <div className="mb-4 p-3 bg-rose-50 border border-rose-300 text-rose-700 text-sm rounded-lg">
               {error}
            </div>
         )}

         <div className="space-y-4">
            <Button
               onClick={(e) => {
                  e.preventDefault();
                  setError(null);
                  loginUser(email, password);
               }}
            >
               Log in
            </Button>

            <div className="relative flex py-1 items-center text-xs text-slate-300 uppercase select-none">
               <div className="flex-grow border-t border-slate-300"></div>
               <span className="flex-shrink mx-3 text-slate-500 font-semibold">
                  or
               </span>
               <div className="flex-grow border-t border-slate-300"></div>
            </div>

            <button
               onClick={getGoogleUri}
               className="flex items-center justify-center w-full px-4 py-2.5 text-sm font-medium text-slate-700 bg-white hover:bg-slate-50 border border-slate-300 rounded-lg transition-colors duration-150"
            >
               <img
                  src={logo}
                  alt="Google"
                  className="w-4 h-4 mr-2.5 select-none"
               />
               Login with Google
            </button>
         </div>
      </form>
   );
}

export default LoginForm;
