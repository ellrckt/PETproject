import React, { useEffect, useState } from "react";

import Button from "./UI/Button";
import Input from "./UI/Input";
import NavBar from "./NavBar";
import PhotoLoader from "./UI/PhotoLoader";
import DropDown from "./UI/DropDown";

import reqService from "../API/RequestService";

function Profile() {
   const [name, setName] = useState("");
   const [age, setAge] = useState("");
   const [about, setAbout] = useState("");
   const [country, setCountry] = useState("");
   const [city, setCity] = useState("");
   const [userHobbies, setUserHobbies] = useState([]);

   const [hobbiesList, setHobbiesList] = useState([]);
   const [edit, setEdit] = useState(false);

   useEffect(() => {
      getHobbiesList();
      getProfile();
   }, []);

   const getHobbiesList = async () => {
      const res = await reqService.get("/profile/get_hobbies");
      setHobbiesList(res.data);
   };

   const updateProfile = async (data) => {
      await reqService.patch("/profile/update_profile", data);
   };

   const getProfile = async () => {
      const res = await reqService.get("profile/get_user_profile");
      try {
         setName(res.data.username || "");
         setAge(res.data.age || "");
         setCity(res.data.city || "");
         setCountry(res.data.country || "");
         setAbout(res.data.about_user || "");
         setUserHobbies(res.data.user_habits || []);
      } catch (error) {
         console.log(error);
      }
   };

   return (
      <div className="min-h-screen bg-gray-50">
         <NavBar />
         <div className="max-w-4xl mx-auto bg-white rounded-lg shadow-md shadow-stone-300 p-8 mt-10">
            <div className="flex flex-col md:flex-row gap-8">
               <div className="w-full md:w-1/3 flex flex-col items-center">
                  <PhotoLoader placeholder={"Upload photo"} />
               </div>

               <div className="w-full md:w-2/3">
                  {edit ? (
                     <div className="space-y-8">
                        <Input
                           placeholder={"Name"}
                           value={name}
                           onChange={(e) => setName(e.target.value)}
                           className="w-full"
                        />

                        <Input
                           placeholder={"Age"}
                           value={age}
                           onChange={(e) => setAge(e.target.value)}
                           className="w-full"
                        />

                        <Input
                           placeholder={"About you (max. 200 symbols)"}
                           value={about}
                           onChange={(e) => setAbout(e.target.value)}
                           className="w-full"
                           multiline
                        />

                        <DropDown
                           options={hobbiesList}
                           text="Select your hobbies (max. 3)"
                           selected={userHobbies}
                           setSelected={setUserHobbies}
                        />

                        <div className="flex justify-end mt-6">
                           <Button
                              onClick={() => {
                                 setEdit(false);
                                 updateProfile({
                                    username: name,
                                    age: age,
                                    city: "city",
                                    country: "country",
                                    about_user: about,
                                    user_habits: userHobbies,
                                 });
                              }}
                           >
                              Save
                           </Button>
                        </div>
                     </div>
                  ) : (
                     <div className="space-y-6 max-w-2xl mx-auto p-6 bg-white rounded-xl shadow-sm">
                        <div className="text-center mb-8">
                           <h2 className="text-3xl font-bold text-gray-900">
                              {name || "Your Name"}
                           </h2>
                           <div className="w-24 h-1 bg-stone-500 mx-auto mt-3 rounded-full"></div>
                        </div>

                        <div className="space-y-6">
                           <div className="bg-stone-50 p-4 rounded-lg border border-stone-200">
                              <h3 className="text-xs font-semibold text-stone-500 uppercase tracking-wider mb-1">
                                 Age
                              </h3>
                              <p className="text-lg text-stone-800 font-medium">
                                 {age || "Not specified"}
                              </p>
                           </div>

                           <div className="bg-stone-50 p-4 rounded-lg border border-stone-200">
                              <h3 className="text-xs font-semibold text-stone-500 uppercase tracking-wider mb-1">
                                 Location
                              </h3>
                              <div className="flex flex-wrap gap-4">
                                 <div>
                                    {/* <p className="text-sm text-stone-600">Country</p> */}
                                    <p className="text-lg text-stone-800 font-medium">
                                       {country || "Not specified"}
                                    </p>
                                 </div>
                                 <div>
                                    {/* <p className="text-sm text-stone-600">City</p> */}
                                    <p className="text-lg text-stone-800 font-medium">
                                       {city || "Not specified"}
                                    </p>
                                 </div>
                              </div>
                           </div>

                           <div className="bg-stone-50 p-4 rounded-lg border border-stone-200">
                              <h3 className="text-xs font-semibold text-stone-500 uppercase tracking-wider mb-1">
                                 About
                              </h3>
                              <p className="text-stone-700 whitespace-pre-line">
                                 {about || "Tell something about yourself..."}
                              </p>
                           </div>

                           <div className="bg-stone-50 p-4 rounded-lg border border-stone-200">
                              <h3 className="text-xs font-semibold text-stone-500 uppercase tracking-wider mb-1">
                                 Hobbies
                              </h3>
                              <div className="flex flex-wrap gap-2">
                                 {userHobbies?.length > 0 ? (
                                    userHobbies.map((hobby, index) => (
                                       <span
                                          key={index}
                                          className="px-3 py-1 bg-stone-200 text-stone-800 rounded-full text-sm border border-stone-300"
                                       >
                                          {hobby}
                                       </span>
                                    ))
                                 ) : (
                                    <p className="text-stone-500 italic">
                                       No hobbies specified
                                    </p>
                                 )}
                              </div>
                           </div>

                           <div className="flex justify-end pt-4">
                              <Button onClick={() => setEdit(true)}>
                                 Edit Profile
                              </Button>
                           </div>
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
