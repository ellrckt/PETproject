import React from 'react';
import { useNavigate } from 'react-router-dom';

import Button from './UI/Button';

function ComponentName() {
   const nav = useNavigate();

   return (
      <div className="min-h-screen bg-gradient-to-br from-stone-50 to-stone-100 flex items-center justify-center p-4">
         <div className="max-w-md w-full bg-white rounded-xl shadow-lg shadow-stone-300 p-8 text-center">
            <div className="mb-6">
               {/* <div className="w-16 h-16 bg-stone-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <svg className="w-8 h-8 text-stone-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                     <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path>
                  </svg>
               </div> */}
               <h1 className="text-2xl font-bold text-gray-800 mb-2">
                  Welcome!
               </h1>
               <h2 className="text-gray-600">
                  It seems you're not logged in. Please proceed with one of the options below.
               </h2>
            </div>

            <div className="flex flex-col sm:flex-row gap-4 justify-center mt-8">
               <Button
                  onClick={(e) => {
                     e.preventDefault();
                     nav('/signup');
                  }}
                  className="px-6 py-3 bg-stone-600 text-white rounded-lg hover:bg-stone-700 focus:outline-none focus:ring-2 focus:ring-stone-500 focus:ring-offset-2 transition-all duration-200 shadow-md hover:shadow-lg"
               >
                  Sign up
               </Button>

               <Button
                  onClick={(e) => {
                     e.preventDefault();
                     nav('/login');
                  }}
                  className="px-6 py-3 bg-white text-stone-700 border border-stone-300 rounded-lg hover:bg-stone-50 focus:outline-none focus:ring-2 focus:ring-stone-500 focus:ring-offset-2 transition-all duration-200 shadow-sm hover:shadow-md"
               >
                  Log in
               </Button>
            </div>
         </div>
      </div>
   );
}

export default ComponentName;