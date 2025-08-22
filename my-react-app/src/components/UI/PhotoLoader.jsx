import React from 'react';
import { useState } from 'react';

function PhotoLoader({placeholder}) {
   const [photo, setPhoto] = useState(null);

   function handleImageUpload (e) {
      const image = e.target.files[0];
      if (image) {
         //creates special url for uploaded file
         const url = URL.createObjectURL(image);
         setPhoto(url);
      }
   }

   return (
      <div className="mb-6">
         <input
            className="block w-full text-sm text-gray-500
                     file:mr-4 file:py-2 file:px-4
                     file:rounded-md file:border-0
                     file:text-sm file:font-medium
                     file:bg-stone-50 file:text-stone-700
                     hover:file:bg-stone-100
                     cursor-pointer"
            id={placeholder}
            type='file'
            accept=".png,.jpg,.jpeg"
            onChange={handleImageUpload}
         />
         {photo && (
            <div className="mt-4 flex justify-center">
               <img 
                  src={photo} 
                  alt="Profile preview" 
                  className="w-40 h-40 rounded-full object-cover border-2 border-stone-200"
               />
            </div>
         )}
      </div>
   );
}

export default PhotoLoader;