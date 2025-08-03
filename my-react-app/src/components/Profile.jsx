import React, { useState } from 'react';

import Button from './UI/Button';
import Input from "./UI/Input";
import NavBar from './NavBar';

function Profile() {
   const [photo, setPhoto] = useState();


   return (
      <div>
         <NavBar></NavBar>
         {/* <div>
            <img src="" alt="фото профиля"/>
         </div>
         <Button
         onClick={}>Редактировать профиль</Button> */}
      </div>
   );
}

export default Profile;