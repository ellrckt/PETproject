// import DateSelector from "../DatePicker";
import { useSelector } from "react-redux";
import { useState } from "react";
import Button from "../UI/Button";
import Input from "../UI/Input";
import { X } from "lucide-react";
import { getActiveChat } from "../../store/chats/chatsSlice";
import reqService from "../../API/RequestService";

function SearchWindow({ handleWindowClosing }) {
   const [searchData, setSearchData] = useState({
      query: "",
      author_id: null,
      date_from: null,
      date_to: null,
   });
   const [foundMessages, setFoundMessages] = useState([]);

   const handleSearchDataChange = (event) => {
      const { name, value } = event.target;

      setSearchData((prev) => ({
         ...prev,
         [name]: value,
      }));
   };

   const handleSearch = async () => {
      console.log(searchData);

      const response = await reqService.post(
         `/search/${activeChat.room_id}/smart-filter`,
         searchData,
      );

      if (response.data.data) {
         setFoundMessages(response.data.data);
      }
   };

   const activeChat = useSelector(getActiveChat);
   return (
      <div className="fixed inset-0 z-50 flex items-center justify-center bg-stone-900/40 backdrop-blur-sm p-4">
         <div className="relative w-full max-w-md bg-white rounded-xl shadow-xl border border-stone-200 p-6 flex flex-col gap-5">
            <button
               onClick={handleWindowClosing}
               className="absolute top-4 right-4 p-1 rounded-md text-stone-400 hover:text-stone-700 hover:bg-stone-100 transition-colors"
            >
               <X className="w-5 h-5" />
            </button>

            <h3 className="text-lg font-bold text-stone-600 pr-6">AI Search</h3>

            <div>
               <Input
                  placeholder="Search query..."
                  name="query"
                  value={searchData.query}
                  onChange={handleSearchDataChange}
               />
            </div>

            <div className="flex flex-col gap-1.5">
               <label className="text-xs font-semibold text-stone-500 uppercase tracking-wider">
                  Search In
               </label>
               <select
                  name="author_id"
                  value={searchData.author_id}
                  onChange={handleSearchDataChange}
                  className="w-full px-3 py-2 border border-stone-300 rounded-lg focus:outline-none focus:ring-1 focus:ring-stone-400 focus:border-stone-400 text-stone-800 bg-white cursor-pointer text-sm font-medium"
               >
                  <option value="">All messages</option>
                  <option value={activeChat.sender_id}>My messages only</option>
                  <option value={activeChat.receiver_id}>
                     {activeChat.username || "User"} messages only
                  </option>
               </select>
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
                     name="date_from"
                     value={searchData.date_from}
                     onChange={handleSearchDataChange}
                  />
                  <span className="text-stone-400 text-sm">to</span>
                  <input
                     type="date"
                     className="w-full px-3 py-2 border border-stone-300 rounded-lg focus:outline-none focus:ring-1 focus:ring-stone-400 focus:border-stone-400 text-stone-800 bg-white"
                     name="date_to"
                     value={searchData.date_to}
                     onChange={handleSearchDataChange}
                  />
               </div>
            </div>

            <Button onClick={handleSearch}>Search</Button>

            {foundMessages.length ? (
               <div>
                  <h3 className="text-lg font-bold text-stone-600 pr-6">
                     Search results:
                  </h3>

                  {foundMessages.map((message) => {
                     return (
                        <div className="flex justify-start">
                           <div className="max-w-xs lg:max-w-md rounded-lg px-4 py-2 bg-gray-100 text-gray-800">
                              <div className="font-medium mb-1">
                                 {message.username}
                              </div>
                              <div className="mb-1">{message.message}</div>
                              <div className="flex justify-between items-center">
                                 <div className="text-xs opacity-70">
                                    {message.date}
                                 </div>
                              </div>
                           </div>
                        </div>
                     );
                  })}
               </div>
            ) : null}
         </div>
      </div>
   );
}

export default SearchWindow;
