import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useDispatch } from "react-redux";
import { addInfo } from "./../store/profile/profileSlice";
import reqService from "../API/RequestService";
import Button from "./UI/Button";
import Input from "./UI/Input";
//import useLocation from "../hooks/useLocation";
import jwtService from "../API/JwtService";

function RegistForm() {
   const dispatch = useDispatch();

   const [username, setName] = useState("");
   const [email, setEmail] = useState("");
   const [password, setPassword] = useState("");
   const [repeatPassword, setRepeatPassword] = useState("");
   const [error, setError] = useState(null);

   const nav = useNavigate();

   // const coords = useLocation();

   async function registUser(username, email, password, repeatPassword) {
      const res = await reqService.post("/registration", {
         username: username,
         email: email.toLowerCase(),
         password: password,
         repit_password: repeatPassword,
      });

      const userData = res.data;
      jwtService.setAccessToken(userData.access_token);
      console.log(res.data);

      dispatch(
         addInfo({
            name: "",
            photo: "",
            id: userData.id,
         }),
      );

      nav("/");

      // user location
      // if (typeof res === "string") {
      //    setError(res);
      // } else {
      //    await reqService.post("/user_location/set_user_lat_lng", coords);
      //    // user coords are in db, localstorage - alternative
      //    //localStorage.setItem('location', JSON.stringify(userLocation.data));
      //    nav("/home");
      // }
   }

   return (
      <form className="w-full max-w-md mx-auto bg-white rounded-xl border border-slate-300 p-8 shadow-[0_10px_25px_-5px_rgba(148,163,184,0.1)]">
         <div className="text-center mb-8">
            <h1 className="text-2xl font-bold tracking-tight text-slate-800">
               Create account
            </h1>
            <p className="text-xs text-slate-500 mt-1.5 uppercase tracking-wider font-semibold">
               Join the messenger application
            </p>
         </div>

         <div className="space-y-4 mb-6">
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
               type="password"
            />

            <Input
               placeholder="Repeat password"
               value={repeatPassword}
               onChange={(e) => setRepeatPassword(e.target.value)}
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
                  registUser(username, email, password, repeatPassword);
               }}
            >
               Sign up
            </Button>

            <div className="text-center pt-2">
               <span className="text-sm text-slate-500">
                  Already have an account?{" "}
               </span>
               <Link
                  to="/login"
                  className="text-sm text-slate-700 hover:text-slate-900 font-semibold underline decoration-slate-300 underline-offset-4 transition-colors"
               >
                  Log in here
               </Link>
            </div>
         </div>
      </form>
   );
}

export default RegistForm;
