import { BACKEND_URL } from "@/lib/constants";
import { askCustomerService } from "@/services/ai";
import axios from "axios";
import React from "react";
import { ReactMediaRecorder } from "react-media-recorder";

interface Message {
  sender: "user" | "ai";
  content: string;
  timestamp: string;
}

export default function MicRecorder({
  setMessages,
  sessionId,
  userInput,
  setIsRecording,
  isRecording,
}: {
  setMessages: React.Dispatch<React.SetStateAction<Message[]>>;
  sessionId: number;
  userInput: string;
  setIsRecording: React.Dispatch<React.SetStateAction<boolean>>;
  isRecording: boolean;
}) {
  return (
    <ReactMediaRecorder
      audio
      onStop={async (blobUrl, blob) => {
        console.log("Blob URL:", blobUrl);
        console.log("Blob object:", blob);

        // Example: send to backend
        const formData = new FormData();
        formData.append("file", blob);

        const res1 = await axios.post(
          `${BACKEND_URL}/api/speech-to-text/`,
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          }
        );
        console.log(res1);

        // Add transcribed text to messages
        if (res1.data && res1.data.transcribed_text) {
          setMessages((prev) => [
            ...prev,
            {
              sender: "user",
              content: res1.data.transcribed_text,
              timestamp: new Date().toISOString(),
            },
          ]);
        }

        const res2 = await askCustomerService(
          res1.data.transcribed_text,
          Number(sessionId)
        );

        setMessages((prev) => [
          ...prev,
          {
            sender: "ai",
            content: res2.result.ai_output,
            timestamp: new Date().toISOString(),
          },
        ]);
      }}
      render={({ startRecording, stopRecording }) => (
        <div className="flex gap-2">
          <button
            onClick={() => {
              if (isRecording) {
                stopRecording();
                setIsRecording(false);
              } else {
                startRecording();
                setIsRecording(true);
              }
            }}
            className={`px-3 py-1 rounded-full text-white text-sm disabled:cursor-not-allowed cursor-pointer ${
              isRecording
                ? "bg-red-500 hover:bg-red-600"
                : "bg-green-500 hover:bg-green-600"
            }`}
            disabled={userInput.length > 0}
          >
            {isRecording ? "Stop" : "Start"}
          </button>
        </div>
      )}
    />
  );
}
