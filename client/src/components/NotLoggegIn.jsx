import React from "react";
import { useNavigate } from "react-router-dom";
import Button from "./UI/Button";

function ComponentName() {
   const nav = useNavigate();

   return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center p-4">
         <div className="max-w-md w-full bg-white rounded-xl border border-slate-300 p-8 text-center shadow-[0_10px_25px_-5px_rgba(148,163,184,0.1)]">
            <div className="mb-6">
               <h1 className="text-2xl font-bold tracking-tight text-slate-800 mb-2">
                  Messenger Application
               </h1>
               <h2 className="text-sm text-slate-500 font-medium">
                  Authentication is required to access chats and profile. Please
                  log in to your account or create a new one.
               </h2>
            </div>

            <div className="flex flex-col sm:flex-row gap-3.5 justify-center mt-8">
               <Button
                  onClick={(e) => {
                     e.preventDefault();
                     nav("/signup");
                  }}
               >
                  Sign Up
               </Button>

               <button
                  onClick={(e) => {
                     e.preventDefault();
                     nav("/login");
                  }}
                  className="w-full px-4 py-2.5 text-sm font-medium text-slate-700 bg-white hover:bg-slate-50 border border-slate-300 rounded-xl transition-colors duration-150"
               >
                  Log In
               </button>
            </div>
         </div>
      </div>
   );
}

export default ComponentName;
