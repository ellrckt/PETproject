import { Outlet } from "react-router-dom";
import { useSelector } from "react-redux";
import { getProfileInfo } from "../store/profile/profileSlice";
import NavBar from "./NavBar";

function Layout() {
   const profile = useSelector(getProfileInfo);
   const isAuth = profile.id !== 0;

   return (
      <div className="min-h-screen flex flex-col bg-slate-50 text-slate-800">
         {isAuth && (
            <header className="w-full bg-white border-b border-slate-200 sticky top-0 z-40">
               <NavBar />
            </header>
         )}

         <main className="flex-1 flex items-center justify-center w-full">
            <Outlet />
         </main>
      </div>
   );
}

export default Layout;
