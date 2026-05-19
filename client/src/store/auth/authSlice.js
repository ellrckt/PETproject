import { createSlice } from "@reduxjs/toolkit";

const authSlice = createSlice({
   name: "auth",
   initialState: {
      isLoggedIn: false
   },
   reducers: {
      checkToken: (state, action) => {
         state.
      },
   },
});

export const { addInfo } = profileSlice.actions;
export default profileSlice.reducer;