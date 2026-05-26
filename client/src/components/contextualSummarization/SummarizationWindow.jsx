import { useSelector } from "react-redux";
import { useState } from "react";
import Button from "../UI/Button";
import Input from "../UI/Input";
import {
   X,
   CheckSquare,
   Calendar,
   Lightbulb,
   HelpCircle,
   Sparkles,
} from "lucide-react";
import { getActiveChat } from "../../store/chats/chatsSlice";
import reqService from "../../API/RequestService";

function SummarizeWindow({ handleWindowClosing }) {
   const activeChat = useSelector(getActiveChat);

   const [timeMode, setTimeMode] = useState("unread");
   const [summaryType, setSummaryType] = useState("tasks");
   const [customQuery, setCustomQuery] = useState("");
   const [dateRange, setDateRange] = useState({ from: "", to: "" });
   const [summaryResult, setSummaryResult] = useState(null);
   const [isLoading, setIsLoading] = useState(false);

   const handleDateChange = (e) => {
      const { name, value } = e.target;
      setDateRange((prev) => ({ ...prev, [name]: value }));
   };

   const handleGenerateSummary = async () => {
      setIsLoading(true);

      try {
         const response = await reqService.post();
         setSummaryResult(response.data.data);
      } catch (error) {
         console.error(error);
      } finally {
         setIsLoading(false);
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
                     className={`flex items-center gap-3 p-3 rounded-lg border cursor-pointer select-none text-sm font-medium transition-all ${timeMode === "unread" ? "border-stone-800 bg-stone-50 text-stone-800 font-semibold" : "border-stone-300 hover:bg-stone-50 text-stone-700"}`}
                  >
                     <input
                        type="radio"
                        name="timeMode"
                        checked={timeMode === "unread"}
                        onChange={() => setTimeMode("unread")}
                        className="w-4 h-4 text-stone-800 accent-stone-800 focus:ring-stone-500"
                     />
                     <span>Unread messages</span>
                  </label>

                  <label
                     className={`flex items-center gap-3 p-3 rounded-lg border cursor-pointer select-none text-sm font-medium transition-all ${timeMode === "range" ? "border-stone-800 bg-stone-50 text-stone-800 font-semibold" : "border-stone-300 hover:bg-stone-50 text-stone-700"}`}
                  >
                     <input
                        type="radio"
                        name="timeMode"
                        checked={timeMode === "range"}
                        onChange={() => setTimeMode("range")}
                        className="w-4 h-4 text-stone-800 accent-stone-800 focus:ring-stone-500"
                     />
                     <span>Select date range</span>
                  </label>
               </div>

               <div
                  className={`flex items-center gap-2 transition-opacity duration-200 ${timeMode === "unread" ? "opacity-40 pointer-events-none" : "opacity-100"}`}
               >
                  <input
                     type="date"
                     name="from"
                     disabled={timeMode === "unread"}
                     value={dateRange.from}
                     onChange={handleDateChange}
                     className="w-full px-3 py-2 border border-stone-300 rounded-lg focus:outline-none focus:ring-1 focus:ring-stone-400 focus:border-stone-400 text-stone-800 bg-white text-sm"
                  />
                  <span className="text-stone-400 text-sm">to</span>
                  <input
                     type="date"
                     name="to"
                     disabled={timeMode === "unread"}
                     value={dateRange.to}
                     onChange={handleDateChange}
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
                     onClick={() => setSummaryType("tasks")}
                     className={`flex items-center gap-3 p-3 rounded-lg border text-left text-sm font-medium transition-all ${summaryType === "tasks" ? "border-stone-800 bg-stone-50 text-stone-800 font-semibold" : "border-stone-300 text-stone-700 hover:bg-stone-50"}`}
                  >
                     <CheckSquare className="w-4 h-4 text-stone-600" />
                     <span>Tasks & Actions</span>
                  </button>

                  <button
                     onClick={() => setSummaryType("meetings")}
                     className={`flex items-center gap-3 p-3 rounded-lg border text-left text-sm font-medium transition-all ${summaryType === "meetings" ? "border-stone-800 bg-stone-50 text-stone-800 font-semibold" : "border-stone-300 text-stone-700 hover:bg-stone-50"}`}
                  >
                     <Calendar className="w-4 h-4 text-stone-600" />
                     <span>Meetings & Plans</span>
                  </button>

                  <button
                     onClick={() => setSummaryType("custom")}
                     className={`flex items-center gap-3 p-3 rounded-lg border text-left text-sm font-medium transition-all ${summaryType === "custom" ? "border-stone-800 bg-stone-50 text-stone-800 font-semibold" : "border-stone-300 text-stone-700 hover:bg-stone-50"}`}
                  >
                     <HelpCircle className="w-4 h-4 text-stone-600" />
                     <span>Custom Question</span>
                  </button>
               </div>

               {summaryType === "custom" && (
                  <div className="mt-1">
                     <Input
                        placeholder="Your query..."
                        value={customQuery}
                        onChange={(e) => setCustomQuery(e.target.value)}
                     />
                  </div>
               )}
            </div>

            <Button
               onClick={handleGenerateSummary}
               disabled={
                  isLoading || (summaryType === "custom" && !customQuery.trim())
               }
            >
               {isLoading ? "Generating summary..." : "Generate Summary"}
            </Button>

            {summaryResult || !isLoading ? (
               <div className="flex flex-col gap-2">
                  <h3 className="text-lg font-bold text-stone-600 pr-6">
                     Summary:
                  </h3>
                  <div className="w-full rounded-lg px-4 py-3 bg-stone-100 text-stone-800 text-sm whitespace-pre-line leading-relaxed border border-stone-200">
                     {summaryResult ||
                        `• Исправить баг с типами в файле auth/utils.py (из-за него бэкенд падал).\n• Добавить новые миграции Alembic в базу данных.\n• Настроить отправку параметров из формы поиска через тело JSON, а не через URL-строку.`}
                  </div>
               </div>
            ) : null}
         </div>
      </div>
   );
}

export default SummarizeWindow;
