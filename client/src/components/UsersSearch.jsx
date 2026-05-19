import jwtService from "../API/JwtService";
import Button from "./UI/Button";
import { useState } from "react";

function UsersSearch({ onUserSelect }) {
   const [foundUsers, setFoundUsers] = useState([]);
   const [userName, setUserName] = useState("");
   const [isCollapsed, setIsCollapsed] = useState(false);

   const getUserByName = async (name) => {
      const res = await jwtService.get(`/profile/search/${name}`);
      setFoundUsers(res.data);
   };

   return (
      <div
         className={`${isCollapsed ? "w-16" : "w-80"} bg-stone-50 border-l border-stone-200 h-full transition-all duration-300 flex flex-col`}
      >
         <div className="p-4 flex items-center justify-between border-b border-stone-100 bg-stone-100/50">
            {!isCollapsed && (
               <h3 className="text-lg font-bold text-stone-800">
                  Search for users
               </h3>
            )}
            <button
               onClick={() => setIsCollapsed(!isCollapsed)}
               className={`p-1.5 hover:bg-stone-200 rounded-md text-stone-600 transition-colors ${isCollapsed ? "mx-auto" : "ml-auto"}`}
               title={isCollapsed ? "Expand search" : "Collapse search"}
            >
               <svg
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  strokeWidth={2}
                  stroke="currentColor"
                  className={`w-5 h-5 transition-transform duration-300 ${isCollapsed ? "rotate-180" : ""}`}
               >
                  <path
                     strokeLinecap="round"
                     strokeLinejoin="round"
                     d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3"
                  />
               </svg>
            </button>
         </div>

         {!isCollapsed && (
            <div className="p-4 flex-1 overflow-y-auto">
               <div className="flex mb-4">
                  <input
                     id="users-search-input"
                     type="text"
                     placeholder="Enter username"
                     onChange={(e) => setUserName(e.target.value)}
                     value={userName}
                     className="flex-1 px-3 py-2 border border-stone-300 rounded-l-lg focus:outline-none focus:ring-1 focus:ring-stone-400 focus:border-stone-400 text-stone-800"
                  />
                  <Button
                     onClick={async () => {
                        await getUserByName(userName);
                     }}
                     children={"Search"}
                     className="rounded-l-none"
                  />
               </div>

               {foundUsers.length > 0 ? (
                  <div className="space-y-3">
                     {foundUsers.map((user, index) => (
                        <div
                           key={user.id || index}
                           className="p-3 bg-white border border-stone-200 rounded-lg shadow-sm flex items-center justify-between hover:bg-stone-50 transition-colors"
                        >
                           <p className="font-medium text-stone-800">
                              {user.username}
                           </p>

                           <button
                              className="ml-2 p-1.5 text-stone-500 hover:text-stone-800 hover:bg-stone-100 rounded-md transition-colors"
                              onClick={() => {
                                 onUserSelect(user);
                              }}
                           >
                              <span className="text-lg font-bold">+</span>
                           </button>
                        </div>
                     ))}
                  </div>
               ) : (
                  <div className="mt-8 text-center text-stone-500">
                     <p>Enter username</p>
                  </div>
               )}
            </div>
         )}
      </div>
   );
}

export default UsersSearch;
