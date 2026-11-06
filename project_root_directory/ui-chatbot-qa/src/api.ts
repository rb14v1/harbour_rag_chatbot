import { ChatMessage } from "./types";

const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";
const TOKEN_KEY = "authToken";

export const getToken = (): string | null => localStorage.getItem(TOKEN_KEY);
export const clearToken = () => localStorage.removeItem(TOKEN_KEY);

const request = async (path: string, init: RequestInit = {}) => {
  const token = getToken();
  const response = await fetch(`${API_URL}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Token ${token}` } : {}),
    },
  });
  if (response.status === 401) {
    clearToken();
    window.dispatchEvent(new Event("auth-expired"));
  }
  if (!response.ok) throw new Error(`Request failed: ${response.status}`);
  return response.json();
};

export const login = async (email: string, password: string) => {
  const response = await fetch(`${API_URL}/api/user/token/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  if (!response.ok) throw new Error("Invalid credentials");
  const data = await response.json();
  localStorage.setItem(TOKEN_KEY, data.token);
};

export const fetchChats = (): Promise<ChatMessage[]> => request("/api/chat/");

export const postChat = (message: string): Promise<ChatMessage> =>
  request("/api/chat/", { method: "POST", body: JSON.stringify({ message }) });

export const uploadDocument = async (
  file: File
): Promise<{ file: string; chunks: number }> => {
  const form = new FormData();
  form.append("file", file);
  const response = await fetch(`${API_URL}/api/embeddings/upload/`, {
    method: "POST",
    headers: { Authorization: `Token ${getToken()}` },
    body: form,
  });
  if (!response.ok) {
    const err = await response.json().catch(() => ({}));
    throw new Error(err.detail || `Upload failed: ${response.status}`);
  }
  return response.json();
};
