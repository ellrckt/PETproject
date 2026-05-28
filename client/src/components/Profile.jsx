import { useEffect, useState } from "react";
import { useSelector } from "react-redux";
import Button from "./UI/Button";
import Input from "./UI/Input";
import PhotoLoader from "./UI/PhotoLoader";
import DropDown from "./UI/DropDown";
import reqService from "../API/RequestService";
import { addInfo } from "./../store/profile/profileSlice";
import { useDispatch } from "react-redux";

function Profile() {
   const [name, setName] = useState("");
   const [age, setAge] = useState("");
   const [about, setAbout] = useState("");
   const [country, setCountry] = useState("");
   const [city, setCity] = useState("");
   const [userHobbies, setUserHobbies] = useState([]);
   const [image, setImage] = useState("");

   // const [hobbiesList, setHobbiesList] = useState([]);
   const [edit, setEdit] = useState(false);

   const dispatch = useDispatch();

   useEffect(() => {
      // getHobbiesList();
      getProfile();
   }, []);

   // const getHobbiesList = async () => {
   //    const res = await reqService.get("/profile/get_habits");
   //    setHobbiesList(res.data);
   // };

   const updateProfile = async (data) => {
      await reqService.patch("/profile/update_profile", data);
   };

   const getUserId = async () => {
      const res = await reqService.get("user/get_current_user");
      return res.data.user_id;
   };

   const getProfile = async () => {
      const profile = await getUserId();
      const res = await reqService.get(`profile/profiles/${profile}`);

      dispatch(
         addInfo({
            name: res.data.username,
            photo: res.data.profile_photo_url,
            id: res.data.user_id,
         }),
      );

      try {
         setName(res.data.username || "");
         setAge(res.data.age || "");
         setCity(res.data.city || "");
         setCountry(res.data.country || "");
         setAbout(res.data.about_user || "");
         setUserHobbies(res.data.user_habits || []);
         setImage(res.data.profile_photo_url || "");
      } catch (error) {
         console.log(error);
      }
   };

   const uploadUserImage = async (image) => {
      const formData = new FormData();
      formData.append("file", image);
      await reqService.post("/profile/upload_user_profile_photo", formData);
   };

   return (
      <div className="min-h-[calc(100vh-3.5rem)] bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-zinc-900 via-slate-950 to-black p-6 md:p-12 w-full flex items-center justify-center">
         <div className="w-full max-w-4xl bg-sky-50 rounded-3xl shadow-[0_20px_50px_rgba(0,0,0,0.4)] border border-sky-100 p-6 md:p-10 transition-all duration-300">
            <div className="flex flex-col md:flex-row gap-8 md:gap-12">
               <div className="w-full md:w-1/3 flex flex-col items-center shrink-0">
                  <div className="p-2 bg-white rounded-2xl border border-sky-200/60 shadow-sm">
                     <PhotoLoader
                        placeholder={"Upload photo"}
                        state={image}
                        setState={setImage}
                     />
                  </div>
               </div>

               <div className="w-full md:w-2/3">
                  {edit ? (
                     <div className="space-y-6">
                        <Input
                           placeholder={"Name"}
                           value={name}
                           onChange={(e) => setName(e.target.value)}
                           className="w-full"
                        />

                        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                           <div className="sm:col-span-1">
                              <Input
                                 placeholder={"Age"}
                                 value={age}
                                 onChange={(e) => setAge(e.target.value)}
                                 className="w-full"
                              />
                           </div>
                           {/* <div className="sm:col-span-1">
                              <Input
                                 placeholder={"Country"}
                                 value={country}
                                 onChange={(e) => setCountry(e.target.value)}
                                 className="w-full"
                              />
                           </div> */}
                           {/* <div className="sm:col-span-1">
                              <Input
                                 placeholder={"City"}
                                 value={city}
                                 onChange={(e) => setCity(e.target.value)}
                                 className="w-full"
                              />
                           </div> */}
                        </div>

                        <Input
                           placeholder={"About you (max. 200 symbols)"}
                           value={about}
                           onChange={(e) => setAbout(e.target.value)}
                           className="w-full"
                           multiline
                        />

                        {/* <DropDown
                           options={hobbiesList}
                           text="Select your hobbies (max. 3)"
                           selected={userHobbies}
                           setSelected={setUserHobbies}
                        /> */}

                        <div className="flex justify-end pt-4">
                           <Button
                              onClick={() => {
                                 setEdit(false);
                                 updateProfile({
                                    username: name,
                                    age: age,
                                    city: city,
                                    country: country,
                                    about_user: about,
                                    user_habits: userHobbies,
                                 });
                                 if (typeof image !== "string")
                                    uploadUserImage(image);
                              }}
                           >
                              Save Changes
                           </Button>
                        </div>
                     </div>
                  ) : (
                     <div className="space-y-6">
                        <div className="mb-6">
                           <h2 className="text-3xl font-black tracking-tight text-slate-900">
                              {name || "Your Name"}
                           </h2>
                           <div className="w-16 h-1 bg-slate-900 mt-3 rounded-full"></div>
                        </div>

                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                           <div className="bg-white p-4 rounded-xl border border-sky-100 shadow-sm">
                              <h3 className="text-[10px] font-bold text-slate-900 uppercase tracking-wider mb-1">
                                 Age
                              </h3>
                              <p className="text-base text-slate-800 font-semibold">
                                 {age || "Not specified"}
                              </p>
                           </div>

                           {/* <div className="bg-white p-4 rounded-xl border border-sky-100 shadow-sm">
                              <h3 className="text-[10px] font-bold text-slate-900 uppercase tracking-wider mb-1">
                                 Location
                              </h3>
                              <p className="text-base text-slate-800 font-semibold truncate">
                                 {country || city
                                    ? `${country}${country && city ? ", " : ""}${city}`
                                    : "Not specified"}
                              </p>
                           </div> */}
                        </div>

                        <div className="bg-white p-4 rounded-xl border border-sky-100 shadow-sm">
                           {/* Надпись изменена на text-slate-900 */}
                           <h3 className="text-[10px] font-bold text-slate-900 uppercase tracking-wider mb-2">
                              About
                           </h3>
                           <p className="text-slate-700 text-sm font-medium leading-relaxed whitespace-pre-line">
                              {about || "Tell something about yourself..."}
                           </p>
                        </div>

                        {/* <div className="bg-white p-4 rounded-xl border border-sky-100 shadow-sm">
                           <h3 className="text-[10px] font-bold text-slate-900 uppercase tracking-wider mb-3">
                              Hobbies
                           </h3>
                           <div className="flex flex-wrap gap-2">
                              {userHobbies?.length > 0 ? (
                                 userHobbies.map((hobby, index) => (
                                    <span
                                       key={index}
                                       className="px-3 py-1 bg-sky-100 text-slate-900 rounded-lg text-xs font-bold border border-sky-200/40"
                                    >
                                       {hobby}
                                    </span>
                                 ))
                              ) : (
                                 <p className="text-slate-400 italic text-sm">
                                    No hobbies specified
                                 </p>
                              )}
                           </div>
                        </div> */}

                        <div className="flex justify-end pt-2">
                           <Button onClick={() => setEdit(true)}>
                              Edit Profile
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
