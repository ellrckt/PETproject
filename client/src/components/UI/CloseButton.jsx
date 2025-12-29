import React from "react";
import { FiX } from "react-icons/fi";

function CloseButton({ onClick }) {
   return (
      <div>
         <button
            onClick={onClick}
            className="text-gray-400 hover:text-red-500 transition-colors"
         >
            {/* react icon */}
            <FiX className="h-5 w-5" />
         </button>
      </div>
   );
}

export default CloseButton;
