// import DateSelector from "../DatePicker";
import Button from "../UI/Button";
import Input from "../UI/Input";
import { X } from "lucide-react";

function SearchWindow({ handleWindowClosing }) {
   const handleSearch = async () => {};


   return (
      <div className="fixed inset-0 z-50 flex items-center justify-center bg-stone-900/40 backdrop-blur-sm p-4">
         <div className="relative w-full max-w-md bg-white rounded-xl shadow-xl border border-stone-200 p-6 flex flex-col gap-5">
            <button
               onClick={handleWindowClosing}
               className="absolute top-4 right-4 p-1 rounded-md text-stone-400 hover:text-stone-700 hover:bg-stone-100 transition-colors"
            >
               <X className="w-5 h-5" />
            </button>

            <h3 className="text-lg font-bold text-stone-600 pr-6">
               Advanced Search
            </h3>

            <div>
               <Input placeholder="Search query..." />
            </div>

            <div className="flex flex-col gap-2.5">
               <label className="flex items-center gap-2 cursor-pointer text-sm font-medium text-stone-700 select-none">
                  <input
                     type="checkbox"
                     className="w-4 h-4 rounded border-stone-300 text-stone-800 focus:ring-stone-500 accent-stone-800"
                  />
                  <span>Search in titles only</span>
               </label>

               <label className="flex items-center gap-2 cursor-pointer text-sm font-medium text-stone-700 select-none">
                  <input
                     type="checkbox"
                     className="w-4 h-4 rounded border-stone-300 text-stone-800 focus:ring-stone-500 accent-stone-800"
                  />
                  <span>Exact match</span>
               </label>
            </div>

            {/* <DateSelector></DateSelector> */}

            <div className="flex flex-col gap-1.5">
               <label className="text-xs font-semibold text-stone-500 uppercase tracking-wider">
                  Select Date Range
               </label>
               <div className="flex items-center gap-2">
                  <input
                     type="date"
                     className="w-full px-3 py-2 border border-stone-300 rounded-lg focus:outline-none focus:ring-1 focus:ring-stone-400 focus:border-stone-400 text-stone-800 bg-white"
                  />
                  <span className="text-stone-400 text-sm">to</span>
                  <input
                     type="date"
                     className="w-full px-3 py-2 border border-stone-300 rounded-lg focus:outline-none focus:ring-1 focus:ring-stone-400 focus:border-stone-400 text-stone-800 bg-white"
                  />
               </div>
            </div>

            <Button onClick={handleSearch}>Search</Button>
         </div>
      </div>
   );
}

export default SearchWindow;
