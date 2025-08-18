import React from 'react';
import { useState } from 'react';

//! добавить проверки на 3 элемента, на повторения в селектед, стилизовать, удаление из селектед

function DropDown({options, text, selected, setSelected}) {
   const [isClicked, setIsClicked] = useState(false);
   const [error, setError] = useState('');

   const handleSelect = (item) => {
      if (selected.length === 3) {
         setError('Maximum is reached.')
      } else {
         selected.includes(item) ? setError('Hobbies cannot repeat.') : setSelected([...selected, item]);
      }
   }


   return (
      <div>
         <div>
            {selected.map((el, ind) => (<p key={ind}>{el}</p>))}
         </div>

         {error
            ? (<div>{error}</div>)
            : (<span></span>)
         }

         <button onClick={() => setIsClicked(!isClicked)}>{text}</button>

         {isClicked 
            ? (<ul>
            {options.map((el, ind) => (<li key={ind} className="px-4 py-2 hover:bg-gray-100 cursor-pointer" onClick={() => handleSelect(el)}>{ind+1}. {el}</li>))}
            </ul>)
            : (<span></span>)
         }
      </div>
   );
}

export default DropDown;