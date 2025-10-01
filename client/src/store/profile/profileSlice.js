import { createSlice } from "@reduxjs/toolkit";

const profileSlice = createSlice({
   name: "profile",
   initialState: {
      name: "",
      photo: "",
   },
   reducers: {
      addInfo: (state, action) => {
         state.name = action.payload.name;
         state.photo = action.payload.photo;
      },
   },
});

export const { addInfo } = profileSlice.actions;
export default profileSlice.reducer;
