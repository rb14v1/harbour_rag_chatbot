import { useAppContext } from "../context/AppContext";
import { ChatMessage } from "../types";
import { postChat } from "../api";

const useSendMessage = () => {
  const { state, dispatch } = useAppContext();

  const handleSendMessage = async (message: string) => {
    try {
      const newChat: ChatMessage = {
        message,
        created_at: new Date().toISOString(),
      };
      const updatedMessages = [...state.messages, newChat];
      dispatch({ type: "SET_MESSAGES", payload: updatedMessages });
      dispatch({ type: "SET_LOADING", payload: true });

      const data = await postChat(message);

      updatedMessages[updatedMessages.length - 1].response = data.response;
      dispatch({ type: "SET_LOADING", payload: false });
      dispatch({ type: "SET_MESSAGES", payload: updatedMessages });
    } catch (error) {
      console.error("Error posting message:", error);
      dispatch({ type: "SET_LOADING", payload: false });
    }
  };

  return { handleSendMessage };
};

export default useSendMessage;
