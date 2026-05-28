import { useSelector } from "react-redux";
import { useState } from "react";
import Button from "../UI/Button";
import Input from "../UI/Input";
import { X, CheckSquare, Calendar, HelpCircle, Sparkles } from "lucide-react";
import { getActiveChat } from "../../store/chats/chatsSlice";
import reqService from "../../API/RequestService";

function SummarizeWindow({ handleWindowClosing }) {
   const activeChat = useSelector(getActiveChat);

   const [summaryResult, setSummaryResult] = useState(null);
   const [isLoading, setIsLoading] = useState(false);
   const [sumData, setSumData] = useState({
      query: null,
      timeMode: "unread",
      limit: null,
      date_from: null,
      date_to: null,
      sumMode: "tasks",
   });

   const handleSumDataChange = (event) => {
      const { name, value } = event.target;

      setSumData((prev) => ({
         ...prev,
         [name]: value,
      }));
   };

   const handleGenerateSummary = async () => {
      setIsLoading(true);

      const payload = {
         ...sumData,
         timeMode: sumData.timeMode === "range" ? null : "unread",
         limit:
            sumData.timeMode === "unread"
               ? activeChat.unread_messages_count || 0
               : null,
         date_from: sumData.timeMode === "unread" ? null : sumData.date_from,
         date_to: sumData.timeMode === "unread" ? null : sumData.date_to,
      };

      try {
         const response = await reqService.post(
            `/search/${activeChat.room_id}/smart-sum`,
            payload,
         );

         //const cleanText = JSON.parse(response.data).summary;

         setSummaryResult(response.data.summary);
      } catch (error) {
         console.error(error);
      } finally {
         setIsLoading(false);
         console.log(summaryResult);
      }
   };

   return (
      <div className="fixed inset-0 z-50 flex items-center justify-center bg-stone-900/40 backdrop-blur-sm p-4">
         <div className="relative w-full max-w-lg bg-white rounded-xl shadow-xl border border-stone-200 p-6 flex flex-col gap-6 max-h-[90vh] overflow-y-auto transition-all">
            <button
               onClick={handleWindowClosing}
               className="absolute top-4 right-4 p-1 rounded-md text-stone-400 hover:text-stone-700 hover:bg-stone-100 transition-colors"
            >
               <X className="w-5 h-5" />
            </button>

            <div className="flex items-center gap-2">
               <div className="p-2 bg-stone-100 text-stone-600 rounded-lg">
                  <Sparkles className="w-5 h-5" />
               </div>
               <div>
                  <h3 className="text-lg font-bold text-stone-600">
                     Context Summarization Assistant
                  </h3>
               </div>
            </div>

            <div className="flex flex-col gap-3">
               <label className="text-xs font-semibold text-stone-500 uppercase tracking-wider">
                  Select Context Range
               </label>

               <div className="grid grid-cols-2 gap-3">
                  <label
                     className={`flex items-center gap-3 p-3 rounded-lg border cursor-pointer select-none text-sm font-medium transition-all ${sumData.timeMode === "unread" ? "border-stone-800 bg-stone-50 text-stone-800 font-semibold" : "border-stone-300 hover:bg-stone-50 text-stone-700"}`}
                  >
                     <input
                        type="radio"
                        name="timeMode"
                        value="unread"
                        checked={sumData.timeMode === "unread"}
                        onChange={handleSumDataChange}
                        className="w-4 h-4 text-stone-800 accent-stone-800 focus:ring-stone-500"
                     />
                     <span>Unread messages</span>
                  </label>

                  <label
                     className={`flex items-center gap-3 p-3 rounded-lg border cursor-pointer select-none text-sm font-medium transition-all ${sumData.timeMode === "range" ? "border-stone-800 bg-stone-50 text-stone-800 font-semibold" : "border-stone-300 hover:bg-stone-50 text-stone-700"}`}
                  >
                     <input
                        type="radio"
                        name="timeMode"
                        value={"range"}
                        checked={sumData.timeMode === "range"}
                        onChange={handleSumDataChange}
                        className="w-4 h-4 text-stone-800 accent-stone-800 focus:ring-stone-500"
                     />
                     <span>Select date range</span>
                  </label>
               </div>

               <div
                  className={`flex items-center gap-2 transition-opacity duration-200 ${sumData.timeMode === "unread" ? "opacity-40 pointer-events-none" : "opacity-100"}`}
               >
                  <input
                     type="date"
                     name="date_from"
                     disabled={sumData.timeMode === "unread"}
                     value={sumData.date_from}
                     onChange={handleSumDataChange}
                     className="w-full px-3 py-2 border border-stone-300 rounded-lg focus:outline-none focus:ring-1 focus:ring-stone-400 focus:border-stone-400 text-stone-800 bg-white text-sm"
                  />
                  <span className="text-stone-400 text-sm">to</span>
                  <input
                     type="date"
                     name="date_to"
                     disabled={sumData.timeMode === "unread"}
                     value={sumData.date_to}
                     onChange={handleSumDataChange}
                     className="w-full px-3 py-2 border border-stone-300 rounded-lg focus:outline-none focus:ring-1 focus:ring-stone-400 focus:border-stone-400 text-stone-800 bg-white text-sm"
                  />
               </div>
            </div>

            <div className="flex flex-col gap-3">
               <label className="text-xs font-semibold text-stone-500 uppercase tracking-wider">
                  Select Assistant Mode
               </label>

               <div className="grid grid-cols-2 gap-2.5">
                  <button
                     type="button"
                     onClick={() =>
                        setSumData((prev) => ({ ...prev, sumMode: "tasks" }))
                     }
                     className={`flex items-center gap-3 p-3 rounded-lg border text-left text-sm font-medium transition-all ${sumData.sumMode === "tasks" ? "border-stone-800 bg-stone-50 text-stone-800 font-semibold" : "border-stone-300 text-stone-700 hover:bg-stone-50"}`}
                  >
                     <CheckSquare className="w-4 h-4 text-stone-600" />
                     <span>Tasks</span>
                  </button>

                  <button
                     type="button"
                     onClick={() =>
                        setSumData((prev) => ({ ...prev, sumMode: "plans" }))
                     }
                     className={`flex items-center gap-3 p-3 rounded-lg border text-left text-sm font-medium transition-all ${sumData.sumMode === "plans" ? "border-stone-800 bg-stone-50 text-stone-800 font-semibold" : "border-stone-300 text-stone-700 hover:bg-stone-50"}`}
                  >
                     <Calendar className="w-4 h-4 text-stone-600" />
                     <span>Meetings & Plans</span>
                  </button>

                  <button
                     type="button"
                     onClick={() =>
                        setSumData((prev) => ({ ...prev, sumMode: "custom" }))
                     }
                     className={`flex items-center gap-3 p-3 rounded-lg border text-left text-sm font-medium transition-all ${sumData.sumMode === "custom" ? "border-stone-800 bg-stone-50 text-stone-800 font-semibold" : "border-stone-300 text-stone-700 hover:bg-stone-50"}`}
                  >
                     <HelpCircle className="w-4 h-4 text-stone-600" />
                     <span>Custom Question</span>
                  </button>
               </div>

               {sumData.sumMode === "custom" && (
                  <div className="mt-1">
                     <Input
                        name="query"
                        placeholder="Your query..."
                        value={sumData.query}
                        onChange={handleSumDataChange}
                     />
                  </div>
               )}
            </div>

            <Button
               onClick={handleGenerateSummary}
               disabled={
                  isLoading ||
                  (sumData.sumMode === "custom" && !sumData.query?.trim())
               }
            >
               {isLoading ? "Generating summary..." : "Generate Summary"}
            </Button>

            {summaryResult && !isLoading ? (
               <div className="flex flex-col gap-2">
                  <h3 className="text-lg font-bold text-stone-600 pr-6">
                     Summary:
                  </h3>
                  <div className="w-full rounded-lg px-4 py-3 bg-stone-100 text-stone-800 text-sm whitespace-pre-line leading-relaxed border border-stone-200">
                     {summaryResult}
                  </div>
               </div>
            ) : null}
         </div>
      </div>
   );
}

export default SummarizeWindow;
