import { createSlice } from "@reduxjs/toolkit";

const chatsSlice = createSlice({
   name: "chats",
   initialState: {
      chatsList: [],
      activeChatId: null,
   },
   reducers: {
      setChatsList: (state, action) => {
         state.chatsList = action.payload;
      },
      setActiveChatId: (state, action) => {
         state.activeChatId = action.payload;
      },
   },
});

export const { setChatsList, setActiveChatId } = chatsSlice.actions;

export const getActiveChat = (state) => {
   return (
      state.chats.chatsList.find(
         (chat) => chat.room_id === state.chats.activeChatId,
      ) || null
   );
};

export default chatsSlice.reducer;
