import React from 'react'
import ReactDOM from 'react-dom/client'
import { Provider } from "react-redux";
import { SnackbarProvider } from "notistack";
import { CssBaseline } from "@mui/material";
import store from "@/app/store";
import App from './App.tsx'
import './index.css'
import ColorModeProvider from './theme';
import AuthGuard from "./guard/AuthGuard";


ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <Provider store={store}>
      <ColorModeProvider>
        <SnackbarProvider
          maxSnack={5}
          autoHideDuration={3000}
          anchorOrigin={{ vertical: "top", horizontal: "right" }}
        >
          <CssBaseline />
          {/* <AuthGuard> */}
            <App />
          {/* </AuthGuard> */}
        </SnackbarProvider>
      </ColorModeProvider>
    </Provider>
  </React.StrictMode>
);
