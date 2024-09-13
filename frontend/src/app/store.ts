import type { ThunkAction, Action } from "@reduxjs/toolkit";
import { configureStore } from "@reduxjs/toolkit";
import rootReducer from "./reducers";

const store = configureStore({
  reducer: rootReducer,
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        // Ignore these action types
        ignoredActions: [
          "file/fetchFile/fulfilled",
          "file/downloadCWUpload/fulfilled",
        ],
        // Ignore these field paths in all actions
        ignoredActionPaths: ["meta.arg", "payload"],
        // Ignore these paths in the state
        ignoredPaths: ["file.pdfBlob", "file.cwUpload"],
      },
    }),
});

export type RootState = ReturnType<typeof rootReducer>;
export type AppDispatch = typeof store.dispatch;
export type AppThunk = ThunkAction<void, RootState, null, Action<string>>;

export default store;
