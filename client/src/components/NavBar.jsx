import Ref from "./UI/Ref";

function NavBar() {
   return (
      <div className="w-full flex items-center justify-between px-6 bg-sky-50 border-b border-sky-100 h-16">
         <nav className="flex items-center h-full space-x-1">
            <Ref path="/" text="Chats"></Ref>
            <Ref path="/profile" text="Profile"></Ref>
         </nav>
      </div>
   );
}

export default NavBar;
