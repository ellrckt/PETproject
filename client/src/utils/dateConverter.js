export const formatDate = (isoString) => {
   if (!isoString) return "";

   const date = new Date(isoString);

   return new Intl.DateTimeFormat("ru-RU", {
      day: "numeric",
      month: "long",
      hour: "2-digit",
      minute: "2-digit",
   }).format(date);
};
