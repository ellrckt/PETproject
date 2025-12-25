import { createSlice } from "@reduxjs/toolkit";

const profileSlice = createSlice({
   name: "profile",
   initialState: {
      name: "",
      photo: "",
      id: 0,
   },
   reducers: {
      addInfo: (state, action) => {
         state.name = action.payload.name;
         state.photo = action.payload.photo;
         state.id = action.payload.id;
      },
   },
});

export const { addInfo } = profileSlice.actions;
export default profileSlice.reducer;
