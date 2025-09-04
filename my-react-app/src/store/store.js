import { configureStore } from "@reduxjs/toolkit";
import profileReducer from "profile/profileSlice";

export const store = configureStore({
   reducer: {
      profile: profileReducer,
   },
});
