import { useState } from "react";
import { Alert, Box, Button, Toolbar } from "@mui/material";
import { uploadDocument } from "../../api";
import ChatList from "../ChatList/ChatList";
import ChatInput from "../ChatInput/ChatInput";

interface ChatBoxProps {
  handleSendMessage: (message: string) => void;
}

export default function ChatBox({
  handleSendMessage,
}: ChatBoxProps) {
  const [status, setStatus] = useState<{ ok: boolean; text: string } | null>(
    null
  );
  const [uploading, setUploading] = useState(false);

  const onFile = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    e.target.value = "";
    if (!file) return;
    setUploading(true);
    setStatus(null);
    try {
      const res = await uploadDocument(file);
      setStatus({ ok: true, text: `Added ${res.file} (${res.chunks} chunks)` });
    } catch (err) {
      setStatus({ ok: false, text: (err as Error).message });
    } finally {
      setUploading(false);
    }
  };

  return (
    <Box
      component="main"
      sx={{
        display: "flex",
        flexDirection: "column",
        height: "100vh",
        overflow: "hidden",
      }}
    >
      <Toolbar />
      <Box sx={{ display: "flex", alignItems: "center", gap: 2, px: 2, py: 1 }}>
        <Button variant="outlined" component="label" disabled={uploading}>
          {uploading ? "Uploading..." : "Upload document"}
          <input type="file" hidden accept=".pdf,.txt,.md" onChange={onFile} />
        </Button>
        {status && (
          <Alert severity={status.ok ? "success" : "error"} sx={{ py: 0 }}>
            {status.text}
          </Alert>
        )}
      </Box>
      <Box sx={{ overflowY: "auto", width: "100%", height: "90%" }}>
        <ChatList />
      </Box>
      <Box
        sx={{
          display: "flex",
          justifyContent: "center",
          mt: "auto",
          width: "100%",
          p: 2,
          maxWidth: 600,
          margin: "auto",
          position: "sticky",
          bottom: 0,
        }}
      >
        <ChatInput onSendMessage={handleSendMessage} />
      </Box>
    </Box>
  );
}
