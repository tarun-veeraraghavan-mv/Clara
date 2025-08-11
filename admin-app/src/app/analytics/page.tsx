"use client";

import React, { useEffect, useState } from "react";
import { getAnalytics } from "@/services/analyticsService";

interface AnalyticsData {
  total_chat_messages: number;
  avg_response_time_ai: number;
  avg_user_satisfaction: number;
}

const AnalyticsPage: React.FC = () => {
  const [analyticsData, setAnalyticsData] = useState<AnalyticsData | null>(
    null
  );
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        const data = await getAnalytics();
        setAnalyticsData(data);
      } catch (err) {
        setError("Failed to fetch analytics data.");
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchAnalytics();
  }, []);

  if (loading) {
    return <div>Loading analytics...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div>
      <h1>Analytics Dashboard</h1>
      {analyticsData ? (
        <div>
          <p>Total Chat Messages: {analyticsData.total_chat_messages}</p>
          <p>
            Average AI Response Time: {analyticsData.avg_response_time_ai}{" "}
            seconds
          </p>
          <p>
            Average User Satisfaction: {analyticsData.avg_user_satisfaction}{" "}
            (out of 5)
          </p>
        </div>
      ) : (
        <p>No analytics data available.</p>
      )}
    </div>
  );
};

export default AnalyticsPage;
