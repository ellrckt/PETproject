import React from 'react';
import Ref from './UI/Ref';
import logo from '../assets/images/logo.svg'

function NavBar() {
   return (
      <div className="flex items-center justify-between px-7 py-2 bg-white shadow-sm">
         <img src={logo} alt="logo" className="h-10" />
         <div className="absolute left-1/2 transform -translate-x-1/2 flex items-center space-x-10">
            <Ref path='/home' text='Home'></Ref>
            <Ref path='/profile' text='Profile'></Ref>
         </div>
      </div>
   );
}

export default NavBar;