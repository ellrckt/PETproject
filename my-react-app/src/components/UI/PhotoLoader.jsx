import React, { useState } from "react";
import { Camera } from "lucide-react";

function PhotoLoader({ placeholder = "photo-upload" }) {
   const [photo, setPhoto] = useState(null);

   function handleImageUpload(e) {
      const image = e.target.files[0];
      if (image) {
         if (photo) {
            URL.revokeObjectURL(photo);
         }
         const url = URL.createObjectURL(image);
         setPhoto(url);
      }
   }

   return (
      <div className="flex flex-col items-center justify-center h-full">
         <label
            htmlFor={placeholder}
            className="relative flex items-center justify-center w-52 h-52 rounded-full border-2 border-dashed border-stone-300 cursor-pointer hover:border-stone-400 transition-colors bg-stone-50 group"
         >
            {photo ? (
               <img
                  src={photo}
                  alt="Profile preview"
                  className="w-full h-full rounded-full object-cover"
               />
            ) : (
               <div className="flex flex-col items-center justify-center text-stone-400 group-hover:text-stone-600 transition-colors">
                  <Camera className="w-12 h-12 mb-2" />
                  <span className="text-sm">Upload</span>
               </div>
            )}
            
            {photo && (
               <div className="absolute inset-0 flex items-center justify-center bg-black bg-opacity-40 rounded-full opacity-0 group-hover:opacity-100 transition-opacity">
                  <Camera className="w-10 h-10 text-white" />
               </div>
            )}
         </label>

         <input
            id={placeholder}
            type="file"
            className="hidden"
            accept=".png,.jpg,.jpeg,.webp"
            onChange={handleImageUpload}
         />
      </div>
   );
}

export default PhotoLoader;