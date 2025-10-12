import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import { UserProvider } from "./UserContext";
import { SnackbarProvider } from "notistack";
import { BrowserRouter } from "react-router-dom";
import "./index.css";
import { GoogleOAuthProvider } from "@react-oauth/google";

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <GoogleOAuthProvider clientId="9656575814-i0rc5aehtlvhkv8fu23gnmgrtnspf5ps.apps.googleusercontent.com">
    <React.StrictMode>
      <UserProvider>
        <SnackbarProvider maxSnack={3}>
          <BrowserRouter>
            <App />
          </BrowserRouter>
        </SnackbarProvider>
      </UserProvider>
    </React.StrictMode>
  </GoogleOAuthProvider>
);
