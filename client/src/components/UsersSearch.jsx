import jwtService from "../API/JwtService";
import Button from "./UI/Button";
import { useState } from "react";

// Принимаем isCollapsed и setIsCollapsed как пропсы из Home.jsx
function UsersSearch({ onUserSelect, isCollapsed, setIsCollapsed }) {
   const [foundUsers, setFoundUsers] = useState([]);
   const [userName, setUserName] = useState("");

   const getUserByName = async (name) => {
      const res = await jwtService.get(`/profile/search/${name}`);
      setFoundUsers(res.data);
   };

   return (
      /* Убрали отсюда динамические классы ширины, так как шириной теперь рулит родительский div в Home.jsx */
      <div className="w-full h-full bg-white flex flex-col">
         <div className="p-4 flex items-center justify-between border-b border-slate-300 h-16 shrink-0">
            {!isCollapsed && (
               <h3 className="text-base font-bold tracking-tight text-slate-800">
                  Search for users
               </h3>
            )}
            <button
               onClick={() => setIsCollapsed(!isCollapsed)}
               className={`p-1.5 hover:bg-slate-100 rounded-lg text-slate-600 transition-colors ${isCollapsed ? "mx-auto" : "ml-auto"}`}
               title={isCollapsed ? "Expand search" : "Collapse search"}
            >
               <svg
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  strokeWidth={2}
                  stroke="currentColor"
                  className={`w-4 h-4 transition-transform duration-300 ${isCollapsed ? "rotate-180" : ""}`}
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
            <div className="p-4 flex-1 overflow-y-auto bg-slate-50">
               <div className="flex mb-4 w-full">
                  <input
                     id="users-search-input"
                     type="text"
                     placeholder="Enter username"
                     onChange={(e) => setUserName(e.target.value)}
                     value={userName}
                     className="flex-1 min-w-0 px-3 py-2 text-sm bg-white border border-slate-300 rounded-l-xl focus:outline-none focus:border-slate-400 text-slate-800 placeholder-slate-400"
                  />
                  <div className="w-24 flex-shrink-0">
                     <Button
                        onClick={async () => {
                           await getUserByName(userName);
                        }}
                        className="rounded-l-none"
                     >
                        Search
                     </Button>
                  </div>
               </div>

               {foundUsers.length > 0 ? (
                  <div className="space-y-3">
                     {foundUsers.map((user, index) => (
                        <div
                           key={user.id || index}
                           className="p-3 bg-white border border-slate-300 rounded-xl shadow-[0_2px_4px_rgba(148,163,184,0.05)] flex items-center justify-between hover:bg-slate-50 transition-colors"
                        >
                           <p className="text-sm font-semibold text-slate-800 truncate pr-2">
                              {user.username}
                           </p>

                           <button
                              className="flex-shrink-0 w-8 h-8 flex items-center justify-center text-slate-500 hover:text-slate-800 hover:bg-slate-100 border border-transparent hover:border-slate-200 rounded-lg transition-colors"
                              onClick={() => {
                                 onUserSelect(user);
                              }}
                           >
                              <span className="text-xl font-medium leading-none mb-0.5">
                                 +
                              </span>
                           </button>
                        </div>
                     ))}
                  </div>
               ) : (
                  <div className="mt-8 text-center text-slate-400 font-medium text-sm">
                     <p>Enter username to find contacts</p>
                  </div>
               )}
            </div>
         )}
      </div>
   );
}

export default UsersSearch;
