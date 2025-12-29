import { Outlet } from "react-router-dom";

import NavBar from "./NavBar";

function Layout() {
   return (
      <div className="app">
         <header>
            <NavBar />
         </header>

         <main>
            <Outlet />
         </main>

         {/* <footer></footer> */}
      </div>
   );
}

export default Layout;
