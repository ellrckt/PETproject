import { createSlice } from "@reduxjs/toolkit";

const chatsSlice = createSlice({
   name: "chats",
   initialState: {
      chatsList: [],
   },
   reducers: {
      setChatsList: (state, action) => {
         state.chatsList = action.payload;
      },
   },
});

export const { setChatsList } = chatsSlice.actions;
export default chatsSlice.reducer;
