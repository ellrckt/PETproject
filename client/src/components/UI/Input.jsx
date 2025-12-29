import React from "react";

function Input({ placeholder, value, onChange, type }) {
   return (
      <div className="mb-8">
         <div className="relative">
            <input
               className="w-full px-3 py-2 border-b-2 border-gray-300 rounded-none text-gray-700 focus:outline-none focus:border-stone-500 focus:ring-0 transition-colors duration-200 bg-transparent"
               id={placeholder}
               type={type || 'text'}
               placeholder={placeholder}
               value={value}
               onChange={onChange}
            />
            <div className="absolute bottom-0 left-0 w-full h-0.5 bg-stone-500 transform scale-x-0 origin-left transition-transform duration-200 focus-within:scale-x-100"></div>
         </div>
      </div>
   );
}

export default Input;