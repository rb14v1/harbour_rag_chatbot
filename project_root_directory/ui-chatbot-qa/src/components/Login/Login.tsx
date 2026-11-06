import React, { useState } from "react";
import { Alert, Box, Button, Paper, TextField, Typography } from "@mui/material";
import { login } from "../../api";

const Login: React.FC<{ onLogin: () => void }> = ({ onLogin }) => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await login(email, password);
      onLogin();
    } catch {
      setError("Invalid email or password");
    }
  };

  return (
    <Box sx={{ display: "flex", justifyContent: "center", mt: 12 }}>
      <Paper component="form" onSubmit={submit} sx={{ p: 4, width: 360 }}>
        <Typography variant="h5" sx={{ mb: 2 }}>
          Sign in
        </Typography>
        {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
        <TextField
          label="Email"
          type="email"
          fullWidth
          required
          sx={{ mb: 2 }}
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <TextField
          label="Password"
          type="password"
          fullWidth
          required
          sx={{ mb: 2 }}
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <Button type="submit" variant="contained" fullWidth>
          Sign in
        </Button>
      </Paper>
    </Box>
  );
};

export default Login;
