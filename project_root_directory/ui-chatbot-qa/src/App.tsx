import React, { useCallback, useEffect, useState } from "react";
import "./App.css";
import { Box, CssBaseline, ThemeProvider } from "@mui/material";
import theme from "./theme";
import ResponsiveDrawer from "./components/ResponsiveDrawer/ResponsiveDrawer";
import ResponsiveAppBar from "./components/ResponsiveAppBar/ResponsiveAppBar";
import ChatBox from "./components/ChatBox/ChatBox";
import useSendMessage from "./hooks/useSendMessage";
import Login from "./components/Login/Login";
import { useAppContext } from "./context/AppContext";
import { clearToken, fetchChats, getToken } from "./api";

const App: React.FC = () => {
  const [mobileOpen, setMobileOpen] = useState(false);
  const [isClosing, setIsClosing] = useState(false);
  const { handleSendMessage } = useSendMessage();
  const { dispatch } = useAppContext();
  const [authed, setAuthed] = useState(!!getToken());

  const loadChats = useCallback(async () => {
    try {
      dispatch({ type: "SET_MESSAGES", payload: await fetchChats() });
    } catch (error) {
      console.error("Failed to load chats:", error);
    }
  }, [dispatch]);

  useEffect(() => {
    const onExpired = () => setAuthed(false);
    window.addEventListener("auth-expired", onExpired);
    return () => window.removeEventListener("auth-expired", onExpired);
  }, []);

  useEffect(() => {
    if (authed) loadChats();
    else {
      clearToken();
      dispatch({ type: "SET_MESSAGES", payload: [] });
    }
  }, [authed, loadChats, dispatch]);

  if (!authed) {
    return (
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Login onLogin={() => setAuthed(true)} />
      </ThemeProvider>
    );
  }

  return (
    <ThemeProvider theme={theme}>
      <Box sx={{ display: "flex" }}>
        <CssBaseline />
        <ResponsiveAppBar
          isClosing={isClosing}
          mobileOpen={mobileOpen}
          setMobileOpen={setMobileOpen}
        />
        <ResponsiveDrawer
          isClosing={isClosing}
          mobileOpen={mobileOpen}
          setIsClosing={setIsClosing}
          setMobileOpen={setMobileOpen}
        />
        <Box sx={{ flexGrow: 1 }}>
          <ChatBox handleSendMessage={handleSendMessage} />
        </Box>
      </Box>
    </ThemeProvider>
  );
};

export default App;
