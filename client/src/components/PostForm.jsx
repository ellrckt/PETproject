import { useState } from "react";

import Button from "./UI/Button";
import CloseButton from "./UI/CloseButton";
import Input from "./UI/Input";
import PhotoLoader from "./UI/PhotoLoader";

function PostForm() {
   const [isOpen, setIsOpen] = useState(false);
   const [postText, setPostText] = useState("");

   const post = async () => {
      //post endpoint
   };

   const closeForm = () => {
      //close logic
   };

   return (
      <div>
         <Button
            onClick={() => {
               setIsOpen(true);
            }}
         >
            Create a new post
         </Button>

         {isOpen ? (
            <div>
               <CloseButton onClick={closeForm}></CloseButton>
               <PhotoLoader placeholder={"Upload post image"}></PhotoLoader>
               <Input
                  placeholder={"Post something..."}
                  value={postText}
                  onChange={(e) => setPostText(e.target.value)}
               ></Input>
               <Button onClick={post}>Post</Button>
            </div>
         ) : (
            <span></span>
         )}
      </div>
   );
}

export default PostForm;
