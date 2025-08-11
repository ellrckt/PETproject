import React from 'react';
import { useState } from 'react';

//! добавить проверки на 3 элемента, на повторения в селектед, стилизовать, удаление из селектед

function DropDown(props) {
   const [isClicked, setIsClicked] = useState(false);
   const [selected, setSelected] = useState([]);

   function addSelected(newItem) {
      setSelected([...selected, newItem]);   
   }


   return (
      <div>
         <div>
            {
               selected.map((el) => (<p>{el}</p>))
            }
         </div>

         <button onClick={() => setIsClicked(!isClicked)}>{props.text}</button>

         {isClicked 
            ? (<ul>
            {props.options.map((el, ind) => (<li key={ind} className="px-4 py-2 hover:bg-gray-100 cursor-pointer" onClick={() => addSelected(el)}>{ind}. {el}</li>))}
            </ul>)
            : (<span></span>)
         }
      </div>
   );
}

export default DropDown;