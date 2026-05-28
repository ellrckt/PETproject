function Input({ placeholder, value, onChange, type, name }) {
   return (
      <div className="w-full">
         <input
            className="w-full px-3.5 py-2.5 bg-white border border-slate-300 rounded-lg text-slate-800 placeholder-slate-400 text-sm focus:outline-none focus:border-slate-500 focus:ring-1 focus:ring-slate-500/30 transition-all duration-150"
            id={placeholder}
            type={type || "text"}
            placeholder={placeholder}
            value={value || ""}
            onChange={onChange}
            name={name || "name"}
         />
      </div>
   );
}

export default Input;
