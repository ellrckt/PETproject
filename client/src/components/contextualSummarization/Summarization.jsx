import { useState } from "react";
import Button from "../UI/Button";
import SummarizationWindow from "./SummarizationWindow";

function Summarization() {
   const [isExpanded, setIsExpanded] = useState(false);

   const handleWindowExpansion = () => {
      setIsExpanded(!isExpanded);
   };

   if (isExpanded) {
      return (
         <SummarizationWindow
            handleWindowClosing={handleWindowExpansion}
         ></SummarizationWindow>
      );
   } else {
      return (
         <div>
            <Button onClick={handleWindowExpansion}>
               Generate resume
            </Button>
         </div>
      );
   }
}

export default Summarization;
