import React, { useEffect, useState } from 'react';

import Button from './UI/Button';
import Input from "./UI/Input";
import NavBar from './NavBar';
import PhotoLoader from './UI/PhotoLoader';
import DropDown from './UI/DropDown';

import reqService from '../API/RequestService';


function Profile() {
   const [name, setName] = useState('');
   const [age, setAge] = useState(undefined);
   const [about, setAbout] = useState('');
   const [country, setCountry] = useState('');
   const [city, setCity] = useState('');
   const [userHobbies, setUserHobbies] = useState([]);

   const [hobbiesList, setHobbiesList] = useState([]);
   const [edit, setEdit] = useState(false);

   useEffect(() => {
      getHobbiesList();
      //getProfile();
   }, [])
   
   const getHobbiesList = async () => {
      const res = await reqService.get('/profile/get_hobbies');
      setHobbiesList(res.data);
   }

   const updateProfile = async (data) => {
      await reqService.patch('/profile/update_profile', data);
   }

   const getProfile = async () => {
      const res = await reqService.get('profile/get_user_profile');
      //console.log(res);
      setName(res.data.username);
      setAge(res.data.age);
      setCity(res.data.city);
      setCountry(res.data.country);
      setAbout(res.data.about_user);
      setUserHobbies(res.data.user_habits);
   }

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
                     <div className="space-y-8">
                        <Input
                           placeholder={'Name'}
                           value={name}
                           onChange={(e) => setName(e.target.value)}
                           className="w-full"
                        />

                        <Input
                           placeholder={'Age'}
                           value={age}
                           onChange={(e) => setAge(e.target.value)}
                           className="w-full"
                        />

                        <Input
                           placeholder={'About you (max. 200 symbols)'}
                           value={about}
                           onChange={(e) => setAbout(e.target.value)}
                           className="w-full"
                           multiline
                        />

                        <DropDown options={hobbiesList} text='Select your hobbies (max. 3)' selected={userHobbies} setSelected={setHobbiesList}/>

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
                           <h3 className="text-gray-500 text-sm">Age</h3>
                           <p className="text-gray-700">{age || 'Set your age'}</p>
                        </div>
                        
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

                        <div className="mt-6">
                           <h3 className="text-gray-500 text-sm">Hobbies</h3>
                           <p className="text-gray-700 whitespace-pre-line">
                              {userHobbies.map((el) => el) || 'set your hobbies'}
                           </p>
                        </div>

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