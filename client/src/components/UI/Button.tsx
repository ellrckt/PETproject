import React from "react";

interface IButtonProps {
   onClick(): void;
   children: React.ReactNode;
}

function Button({ onClick, children }: IButtonProps) {
   return (
      <button
         data-ripple-light="true"
         className="w-full rounded-xl bg-slate-700 py-2.5 px-4 text-center text-sm font-medium text-white border border-slate-800/10 transition-all duration-200 shadow-[0_2px_4px_rgba(71,85,105,0.08)] hover:bg-slate-600 active:bg-slate-800 focus:outline-none focus:ring-2 focus:ring-slate-500/20 disabled:pointer-events-none disabled:opacity-40 disabled:shadow-none"
         type="button"
         onClick={onClick}
      >
         {children}
      </button>
   );
}

export default Button;
