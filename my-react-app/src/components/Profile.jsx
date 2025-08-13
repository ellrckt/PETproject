import React, { useEffect, useState } from 'react';

import Button from './UI/Button';
import Input from "./UI/Input";
import NavBar from './NavBar';
import PhotoLoader from './UI/PhotoLoader';
import DropDown from './UI/DropDown';

import reqService from '../API/RequestService';


function Profile() {
   const [name, setName] = useState('');
   const [about, setAbout] = useState('');
   const [country, setCountry] = useState('');
   const [city, setCity] = useState('');
   const [hobbiesList, setHobbiesList] = useState([]);
   const [edit, setEdit] = useState(false);
   
   const getHobbiesList = async () => {
      const res = await reqService.get('/profile/get_hobbies');
      setHobbiesList(res.data);
   }

   useEffect(() => {
      getHobbiesList();
   }, [])

   return (
      <div className="min-h-screen bg-gray-50">
         <NavBar />
         <div className="max-w-4xl mx-auto bg-white rounded-lg shadow-md shadow-stone-300 p-8 mt-10">
            <div className="flex flex-col md:flex-row gap-8">
               <div className="w-full md:w-1/3 flex flex-col items-center">
                  <PhotoLoader 
                     placeholder={'Upload photo'}
                  />
               </div>
               
               <div className="w-full md:w-2/3">
                  {edit ? (
                     <div className="space-y-4">
                        <Input
                           placeholder={'Name'}
                           value={name}
                           onChange={(e) => setName(e.target.value)}
                           className="w-full"
                        />

                        <h2 className="text-gray-500 text-sm mt-6 mb-2">Location</h2>
                        <div className="p-2 border border-gray-300 rounded-md bg-gray-50 text-gray-500">
                           *Location*
                        </div>

                        <Input
                           placeholder={'About you (max. 200 symbols)'}
                           value={about}
                           onChange={(e) => setAbout(e.target.value)}
                           className="w-full"
                           multiline
                        />

                        <div className="flex justify-end mt-6">
                           <Button
                              onClick={() => {setEdit(false)}}
                           >
                              Save
                           </Button>
                        </div>
                     </div>
                  ) : (
                     <div className="space-y-4">
                        <h2 className="text-2xl font-bold text-gray-800">{name || 'Your Name'}</h2>
                        
                        <div className="mt-6">
                           <h3 className="text-gray-500 text-sm">Location</h3>
                           <p className="text-gray-700">Country: {country}   City:{city}</p>
                        </div>
                        
                        <div className="mt-6">
                           <h3 className="text-gray-500 text-sm">About</h3>
                           <p className="text-gray-700 whitespace-pre-line">
                              {about || 'Tell something about yourself...'}
                           </p>
                        </div>

                        <DropDown options={hobbiesList} text='Select your interests (max. 3)' />
                        
                        <div className="flex justify-end mt-6">
                           <Button
                              onClick={() => {setEdit(true)}}
                           >
                              Edit profile
                           </Button>
                        </div>
                     </div>
                  )}
               </div>
            </div>
         </div>
      </div>
   );
}

export default Profile;