import React from 'react';
import { Link } from "react-router-dom";

function Ref({path, text}) {
   return (
      <Link 
         to={path}
         className="px-4 py-2 text-gray-800 hover:text-stone-500 transition-colors duration-300 border-b-2 border-transparent hover:border-stone-500"
      >
         {text}
      </Link>
   );
}

export default Ref;