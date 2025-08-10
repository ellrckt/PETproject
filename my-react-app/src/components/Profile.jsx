import React, { useState } from 'react';

import Button from './UI/Button';
import Input from "./UI/Input";
import NavBar from './NavBar';

function Profile() {
   const [photo, setPhoto] = useState();
   const [name, setName] = useState('');
   const [about, setAbout] = useState('');

   const [edit, setEdit] = useState(false);


   return (
      <div>
         <NavBar></NavBar>
         <div className='m-10'>
            <div>Фото</div>
            <div>
               {
               edit
                  ? (
                     <div>
                        <Input
                        placeholder={'Name'}
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                        >
                        </Input>

                        <h2>Место</h2>

                        <Input
                        placeholder={'About you (max. 200 symbols)'}
                        value={about}
                        onChange={(e) => setAbout(e.target.value)}
                        >
                        </Input>

                        <Button
                           onClick={() => {setEdit(false)}}
                        >Save</Button>
                     </div>
                  )
                  : (
                     <div>
                        <h2>{name}</h2>
                        <h2>*Location*</h2>
                        <h2>{about}</h2>
                        
                     </div>
                  )
               }
               

               <Button
                  onClick={() => {setEdit(true)}}
               >
                  Edit profile
               </Button>
            </div>
         </div>
      </div>
   );
}

export default Profile;