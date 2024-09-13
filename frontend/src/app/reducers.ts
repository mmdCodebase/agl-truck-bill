import { combineReducers } from "@reduxjs/toolkit";
// slices
import { emailSlice, fileSlice, dataSlice, actionSlice, chargeSlice } from "./slices";

const rootReducer = combineReducers({
  email: emailSlice,
  file: fileSlice,
  data: dataSlice,
  charge: chargeSlice,
  action: actionSlice,
});

export default rootReducer;
