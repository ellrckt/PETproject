import React, { useState } from "react";
import { FiChevronDown } from "react-icons/fi";

import CloseButton from "./CloseButton";

function DropDown({ options, text, selected, setSelected }) {
   const [isOpen, setIsOpen] = useState(false);
   const [error, setError] = useState("");

   const handleSelect = (item) => {
      setError("");
      if (selected.length >= 3) {
         setError("Maximum of 3 items reached.");
         setIsOpen(false);
      } else {
         if (selected.includes(item)) {
            setError("Items cannot repeat.");
            setIsOpen(false);
         } else {
            setSelected([...selected, item]);
         }
      }
   };

   const handleDelete = (ind) => {
      const newState = [...selected];
      newState.splice(ind, 1);
      setSelected(newState);
      setError("");
   };

   return (
      <div className="relative max-w-md mx-auto mb-6">
         <div className="mb-2 space-y-2">
            {selected.map((el, ind) => (
               <div
                  key={ind}
                  className="flex items-center justify-between bg-white p-3 rounded-md shadow-sm border border-gray-200"
               >
                  <p className="text-gray-800">{el}</p>
                  <CloseButton onClick={() => handleDelete(ind)}></CloseButton>
               </div>
            ))}
         </div>

         <button
            onClick={() => setIsOpen(!isOpen)}
            className="w-full flex items-center justify-between bg-white p-3 rounded-md shadow-sm border border-gray-200 hover:border-gray-300 transition-colors"
         >
            <span className="text-gray-600">{text}</span>
            {/* react icon */}
            <FiChevronDown
               className={`h-5 w-5 text-gray-400 transition-transform ${
                  isOpen ? "transform rotate-180" : ""
               }`}
            />
         </button>

         {isOpen && (
            <ul className="absolute z-10 w-full mt-1 bg-white rounded-md shadow-lg border border-gray-200 max-h-60 overflow-auto">
               {options.map((el, ind) => (
                  <li
                     key={ind}
                     onClick={() => handleSelect(el)}
                     className="px-4 py-3 hover:bg-gray-50 cursor-pointer flex items-center"
                  >
                     <span className="text-gray-500 mr-2">{ind + 1}.</span>
                     <span className="text-gray-800">{el}</span>
                  </li>
               ))}
            </ul>
         )}

         {error && (
            <div className="mt-2 p-2 bg-red-100 border border-red-400 text-red-700 rounded text-sm">
               {error}
            </div>
         )}
      </div>
   );
}

export default DropDown;
