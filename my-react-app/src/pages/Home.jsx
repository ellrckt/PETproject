import React, { useState } from "react";
import jwtService from "../API/JwtService";
import Button from "../components/UI/Button";

function Home() {
   // const [users, setUsers] = useState([]);

   // async function getUsers() {
   //    const res = await jwtService.get("/user/get_users");
   //    setUsers(res.data);
   //    return res.data;
   // }

   return (
      // <div>
      //    <button onClick={getUsers}>Получить всех юзеров</button>
      //    <ul>
      //       {users.map((el, ind) => (
      //          <li key={ind}>{el.email}</li>
      //       ))}
      //    </ul>
      // </div>
      <div className="fixed top-4 right-4 flex space-x-4">
         <Button
            onClick={(e) => {
               e.preventDefault();
            }}
            className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
         >
            Регистрация
         </Button>

         <Button
            onClick={(e) => {
               e.preventDefault();
            }}
            className="px-4 py-2 bg-gray-200 text-gray-800 rounded hover:bg-gray-300 transition-colors"
         >
            Вход
         </Button>
      </div>
      
   );
}

export default Home;