import { BACKEND_URL } from "@/lib/constants";
import axios from "axios";

interface APIMessage {
  id: number;
  sender: "user" | "ai";
  content: string;
  timestamp: string;
  user: number;
  session: number;
}

export async function createSession() {
  const res = await axios.post(`${BACKEND_URL}/api/create-session/`, {
    user_id: 1,
  });

  console.log(res.data);

  return res.data;
}

export async function askCustomerService(
  user_input: string,
  session_id: number
) {
  const res = await axios.post(`${BACKEND_URL}/api/ai/`, {
    user_input: user_input,
    user_id: 1,
    session_id: session_id,
  });

  console.log(res.data);

  return res.data;
}

export async function analyzeCustomerFeedback(
  rating: number,
  review: string,
  userId: number,
  sessionId: number
) {
  const res = await axios.post(`${BACKEND_URL}/api/analyze-feedback/`, {
    user_id: userId,
    session_id: sessionId,
    customer_feedback: {
      rating,
      review,
    },
  });

  console.log(res.data);

  return res.data;
}

export async function getUserSessions(userId: number) {
  const res = await axios.get(
    `${BACKEND_URL}/api/user-sessions/?user_id=${userId}`
  );
  return res.data;
}

export async function getSessionMessages(sessionId: number) {
  const res = await axios.get(
    `${BACKEND_URL}/api/session-messages/${sessionId}/`
  );

  const data: APIMessage[] = res.data.messages;
  console.log(data);

  return data;
}

export async function testHF(text_input: string) {
  const res = await axios.post(
    `${BACKEND_URL}/api/run-huggingface-inference/`,
    {
      text_input: text_input,
    }
  );

  console.log(res.data);

  return res.data;
}
