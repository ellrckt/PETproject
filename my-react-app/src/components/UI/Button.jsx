import React from "react";

function Button({ onClick, children }) {
   return (
      <div className="flex items-center justify-between">
         <a
            href="#_"
            className="rounded relative inline-flex group items-center justify-center px-3.5 py-2 m-1 cursor-pointer border-b-4 border-l-2 active:border-purple-700 active:shadow-none shadow-lg bg-purple-200 border-purple-400 text-purple-800"
            onClick={onClick}
         >
            <span className="absolute w-0 h-0 transition-all duration-300 ease-out bg-white rounded-full group-hover:w-32 group-hover:h-32 opacity-10"></span>
            <span className="relative">{children}</span>
         </a>

         {/* <a
            href="#_"
            className="relative inline-flex items-center justify-start py-3 pl-4 pr-12 overflow-hidden font-semibold text-amber-700 transition-all duration-150 ease-in-out rounded hover:pl-10 hover:pr-6 bg-amber-100 group"
            onClick={onClick}
         >
            <span className="absolute bottom-0 left-0 w-full h-1 transition-all duration-150 ease-in-out bg-amber-700 group-hover:h-full"></span>
            <span className="absolute right-0 pr-4 duration-200 ease-out group-hover:translate-x-12">
               <svg
                  className="w-5 h-5 text-amber-400"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                  xmlns="http://www.w3.org/2000/svg"
               >
                  <path
                     strokeLinecap="round"
                     strokeLinejoin="round"
                     strokeWidth="2"
                     d="M14 5l7 7m0 0l-7 7m7-7H3"
                  ></path>
               </svg>
            </span>
            <span className="absolute left-0 pl-2.5 -translate-x-12 group-hover:translate-x-0 ease-out duration-200">
               <svg
                  className="w-5 h-5 text-amber-400"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                  xmlns="http://www.w3.org/2000/svg"
               >
                  <path
                     strokeLinecap="round"
                     strokeLinejoin="round"
                     strokeWidth="2"
                     d="M14 5l7 7m0 0l-7 7m7-7H3"
                  ></path>
               </svg>
            </span>
            <span className="relative w-full text-left transition-colors duration-200 ease-in-out group-hover:text-white">
               {children}
            </span>
         </a> */}
      </div>
   );
}

export default Button;