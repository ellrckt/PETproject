import React from "react";

interface IButtonProps {
   onClick(): void;
   children: React.ReactNode;
}

function Button({ onClick, children }: IButtonProps) {
   return (
      <button
         data-ripple-light="true"
         className="rounded-md bg-stone-600 py-2 px-5 border border-stone-500 text-center text-base text-white transition-all shadow-md hover:shadow-lg focus:bg-stone-500 focus:shadow-none active:bg-stone-500 hover:bg-stone-500 active:shadow-none disabled:pointer-events-none disabled:opacity-50 disabled:shadow-none"
         type="button"
         onClick={onClick}
      >
         {children}
      </button>
   );
}

export default Button;
