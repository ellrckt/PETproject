import { useState } from "react";
import Button from "../UI/Button";
import { Search } from "lucide-react";
import SearchWindow from "./SearchWindow";

function SearchButton() {
   const [isSearchWindowExpanded, setIsSearchWindowExpanded] = useState(false);

   const handleWindowExpansion = () => {
      setIsSearchWindowExpanded(!isSearchWindowExpanded);
   };

   if (isSearchWindowExpanded) {
      return (
         <SearchWindow
            handleWindowClosing={handleWindowExpansion}
         ></SearchWindow>
      );
   } else {
      return (
         <div>
            <Button onClick={handleWindowExpansion}>
               <Search className="w-4 h-4"></Search>
            </Button>
         </div>
      );
   }
}

export default SearchButton;
