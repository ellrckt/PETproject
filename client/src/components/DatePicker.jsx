import { useState } from "react";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";

export default function DateSelector() {
   const [startDate, setStartDate] = useState(null);
   const [endDate, setEndDate] = useState(null);

   // Календарь возвращает массив [start, end] при каждом клике
   const handleDateChange = (update) => {
      const [start, end] = update;
      setStartDate(start);
      setEndDate(end);
   };

   return (
      <div style={{ padding: "20px", fontFamily: "sans-serif" }}>
         <label
            style={{
               display: "block",
               marginBottom: "8px",
               fontWeight: "bold",
            }}
         >
            Choose date for searching:
         </label>

         <DatePicker
            selectsRange={true}
            startDate={startDate}
            endDate={endDate}
            onChange={handleDateChange}
            dateFormat="dd.MM.yyyy"
            isClearable={true}
            placeholderText=""
            className="custom-input"
         />

         {startDate && (
            <div style={{ marginTop: "15px", fontSize: "14px", color: "#333" }}>
               <strong>Your choice: </strong>
               {startDate.toLocaleDateString("ru-RU")}
               {endDate && ` — ${endDate.toLocaleDateString("ru-RU")}`}
            </div>
         )}
      </div>
   );
}
