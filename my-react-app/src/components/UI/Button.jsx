import React from "react";

function Button({ onClick, children }) {
   return (
      // <div className="flex items-center justify-between">
      //    <a
      //       href="#_"
      //       className="rounded relative inline-flex group items-center justify-center px-3.5 py-2 m-1 cursor-pointer border-b-4 border-l-2 active:border-purple-700 active:shadow-none shadow-lg bg-purple-200 border-purple-400 text-purple-800"
      //       onClick={onClick}
      //    >
      //       <span className="absolute w-0 h-0 transition-all duration-300 ease-out bg-white rounded-full group-hover:w-32 group-hover:h-32 opacity-10"></span>
      //       <span className="relative">{children}</span>
      //    </a>
      // </div>
      <button 
         data-ripple-light="true"
         class="rounded-md bg-stone-600 py-2 px-5 border border-stone-500 text-center text-base text-white transition-all shadow-md hover:shadow-lg focus:bg-stone-500 focus:shadow-none active:bg-stone-500 hover:bg-stone-500 active:shadow-none disabled:pointer-events-none disabled:opacity-50 disabled:shadow-none"
         type="button"
         onClick={onClick}
      >
         {children}
      </button>
   );
}

export default Button;