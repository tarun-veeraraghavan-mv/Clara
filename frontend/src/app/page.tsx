"use client";

import { createSession, getUserSessions } from "@/services/ai";
import { useRouter } from "next/navigation";
import { useEffect, useState, useMemo } from "react";

interface ChatSession {
  id: number;
  timestamp: string;
}

export default function Home() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [sessions, setSessions] = useState<ChatSession[]>([]);
  const [dataLoading, setDataLoading] = useState(true);
  const [sortOrder, setSortOrder] = useState<"desc" | "asc">("desc"); // 'desc' for newest first, 'asc' for oldest first
  const userId = 1;

  useEffect(() => {
    async function fetchSessions() {
      try {
        setDataLoading(true);
        const data = await getUserSessions(userId);
        setSessions(data.sessions);
      } catch (err) {
        console.error("Failed to fetch sessions:", err);
      } finally {
        setDataLoading(false);
      }
    }
    fetchSessions();
  }, [userId]);

  const sortedSessions = useMemo(() => {
    const sorted = [...sessions].sort((a, b) => {
      const dateA = new Date(a.timestamp).getTime();
      const dateB = new Date(b.timestamp).getTime();
      if (sortOrder === "asc") {
        return dateA - dateB;
      } else {
        return dateB - dateA;
      }
    });
    return sorted;
  }, [sessions, sortOrder]);

  async function handleAccessCustomerAgent() {
    try {
      setLoading(true);

      const data = await createSession();

      router.push(`/customer-service-agent/${data.session_id}`);
    } catch (err) {
      console.log(err);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="max-w-[1100px] mx-auto my-6 px-[32px]">
      <div className="flex justify-between items-center mb-5">
        <p className="text-3xl font-bold ">Chat sessions</p>
        <button
          onClick={handleAccessCustomerAgent}
          className="cursor-pointer disabled:cursor-not-allowed p-2 rounded-lg bg-gray-200 text-md hover:bg-gray-300"
        >
          {loading ? "Setting you up..." : "Create new session"}
        </button>
      </div>

      {dataLoading ? (
        <p>Loading sessions...</p>
      ) : sessions.length === 0 ? (
        <p>No previous sessions found.</p>
      ) : (
        <div>
          <div className="mb-3 flex justify-between align-middle">
            <h2 className="font-bold text-lg ">Your Previous Sessions:</h2>
            <select
              name="sortOrder"
              id="sortOrder"
              value={sortOrder}
              onChange={(e) => setSortOrder(e.target.value as "asc" | "desc")}
              className="p-1 border rounded-md"
            >
              <option value="desc">Start Date (Newest First)</option>
              <option value="asc">Start Date (Oldest First)</option>
            </select>
          </div>
          <ul className="flex flex-col gap-4">
            {sortedSessions.map((session) => (
              <li
                key={session.id}
                onClick={() =>
                  router.push(`/customer-service-agent/${session.id}`)
                }
                className="p-2 rounded-lg cursor-pointer flex justify-between align-middle bg-gray-200 hover:bg-gray-300"
              >
                <p>
                  Session ID: {session.id} -{" "}
                  {new Date(session.timestamp).toLocaleString()}
                </p>
                <button>Resume</button>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
