"use client";

import MicRecorder from "@/components/MicRecorder";
import { askCustomerService, getSessionMessages } from "@/services/ai";
import { AxiosError } from "axios";
import { useParams, useRouter } from "next/navigation";
import { useEffect, useRef, useState } from "react";
import ReactMarkdown from "react-markdown";

interface Message {
  sender: "user" | "ai";
  content: string;
  timestamp: string;
}

export default function Page() {
  const params = useParams<{ sessionId: string }>();

  const router = useRouter();
  const [userInput, setUserInput] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const [isRecording, setIsRecording] = useState(false);

  useEffect(() => {
    async function fetchSessionMessages() {
      const res = await getSessionMessages(Number(params.sessionId));
      const data: Message[] = res.map((m) => {
        const isoDate = m.timestamp.replace(" ", "T").slice(0, 23) + "Z";
        return {
          sender: m.sender,
          content: m.content,
          timestamp: isoDate,
        };
      });
      setMessages(data);
    }
    fetchSessionMessages();
  }, [params.sessionId]);

  const bottomRef = useRef<HTMLDivElement | null>(null);
  useEffect(() => {
    if (bottomRef.current) {
      bottomRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages]);

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();

    if (!userInput) {
      return;
    }

    setMessages((prev) => [
      ...prev,
      {
        sender: "user",
        content: userInput,
        timestamp: new Date().toISOString(),
      },
    ]);

    setUserInput("");

    try {
      setLoading(true);
      const res = await askCustomerService(userInput, Number(params.sessionId));

      setMessages((prev) => [
        ...prev,
        {
          sender: "ai",
          content: res.result.ai_output,
          timestamp: new Date().toISOString(),
        },
      ]);

      console.log(res);
    } catch (err) {
      if (err instanceof AxiosError) {
        console.log(err.response?.data);
      }
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <div className="max-w-[650px] mx-auto my-7">
        <div className="mb-4">
          <button
            className="bg-red-400 px-2 py-1 font-bold rounded-full text-white hover:cursor-pointer"
            onClick={() => router.push(`/feedback/${params.sessionId}`)}
          >
            End this conversation
          </button>
        </div>

        <ul className="bg-gray-100 p-3 flex flex-col gap-3 h-[500px] overflow-y-auto">
          {messages.map((m, index) => (
            <li
              key={index}
              className={`${
                m.sender === "user" ? "bg-blue-400" : "bg-gray-300"
              } p-1 rounded-lg`}
            >
              <p className="font-bold">
                {m.sender === "user" ? "Me" : "Agent"}
              </p>
              {m.sender === "ai" ? (
                <ReactMarkdown>{m.content}</ReactMarkdown>
              ) : (
                <p>{m.content}</p>
              )}
              <p>{new Date(m.timestamp).toLocaleString()}</p>
            </li>
          ))}

          {loading && <p>Agent is typing...</p>}

          <div ref={bottomRef} />
        </ul>

        <div className="p-3 bg-gray-100 border-t-gray-200 border-t-2">
          <form
            onSubmit={handleSubmit}
            className="relative w-full flex items-center gap-2"
          >
            <input
              type="text"
              placeholder="Your message"
              value={userInput}
              onChange={(e) => setUserInput(e.target.value)}
              disabled={loading || isRecording}
              className="p-3 bg-gray-300 w-full outline-none rounded-full flex-grow"
            />
            <button
              disabled={loading || isRecording}
              className="bg-blue-500 text-white px-4 py-2 text-sm rounded-full hover:bg-blue-600 disabled:cursor-not-allowed hover:cursor-pointer"
            >
              {loading ? "Generating answer..." : "Ask"}
            </button>
            <MicRecorder
              setMessages={setMessages}
              sessionId={Number(params.sessionId)}
              userInput={userInput}
              setIsRecording={setIsRecording}
              isRecording={isRecording}
            />
          </form>
        </div>
      </div>
    </div>
  );
}
