import { Link } from "react-router-dom";

function Ref({ path, text }) {
   return (
      <Link
         to={path}
         className="px-4 py-2 text-sm font-semibold text-slate-600 hover:text-slate-900 border-b-2 border-transparent hover:border-slate-500 transition-colors duration-150"
      >
         {text}
      </Link>
   );
}

export default Ref;
