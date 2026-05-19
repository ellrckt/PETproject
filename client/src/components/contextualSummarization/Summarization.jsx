import { useState } from "react";
import Button from "../UI/Button";
import SummarizationWindow from "./SummarizationWindow";

function Summarization() {
   const [isExpanded, setIsExpanded] = useState(false);

   const handleButtonClick = () => {
      setIsExpanded(true);
   };

   if (isExpanded) {
      return <SummarizationWindow></SummarizationWindow>;
   } else {
      return (
         <div>
            <Button onClick={handleButtonClick}>
               Generate summary with AI
            </Button>
         </div>
      );
   }
}

export default Summarization;
