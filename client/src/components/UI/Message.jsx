

function Message({ children }) {
   return (
      <div className="mt-4 p-3 bg-white border border-stone-200 rounded-lg shadow-sm">
         <p className="font-medium text-stone-800">{children}</p>
      </div>
   );
}

export default Message;
