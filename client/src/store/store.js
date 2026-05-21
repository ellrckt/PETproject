import { configureStore } from "@reduxjs/toolkit";
import profileReducer from "./profile/profileSlice";
import chatsReducer from "./chats/chatsSlice";

export const store = configureStore({
   reducer: {
      profile: profileReducer,
      chats: chatsReducer,
   },
});
