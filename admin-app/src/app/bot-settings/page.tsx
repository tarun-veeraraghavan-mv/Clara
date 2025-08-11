"use client";
import React, { useState, useEffect } from 'react';
import { createBotSettings, getBotSettings } from '@/services/botSettingsService'; // Import getBotSettings

const BotSettingsPage = () => {
  const [greetingMessage, setGreetingMessage] = useState('');
  const [fallbackReply, setFallbackReply] = useState('');
  const [maxConvoHistory, setMaxConvoHistory] = useState(10);
  const [confidenceThreshold, setConfidenceThreshold] = useState(0.8);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [settingsExist, setSettingsExist] = useState(false); // To track if settings were fetched

  useEffect(() => {
    const fetchSettings = async () => {
      try {
        const data = await getBotSettings();
        setGreetingMessage(data.greeting_message);
        setFallbackReply(data.fallback_reply);
        setMaxConvoHistory(data.max_conversation_history);
        setConfidenceThreshold(data.confidence_threshold);
        setSettingsExist(true); // Settings were found
      } catch (err: any) {
        if (err.response && err.response.status === 404) {
          // No settings found, form will remain empty for creation
          setSettingsExist(false);
        } else {
          setError('Failed to fetch bot settings.');
          console.error('Error fetching bot settings:', err);
        }
      } finally {
        setLoading(false);
      }
    };

    fetchSettings();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const settings = {
        greeting_message: greetingMessage, // Use snake_case for backend
        fallback_reply: fallbackReply,     // Use snake_case for backend
        max_conversation_history: maxConvoHistory,
        confidence_threshold: confidenceThreshold,
      };
      // For now, still using createBotSettings. Update logic will be added later.
      const response = await createBotSettings(settings);
      console.log('Bot settings saved:', response);
      alert('Bot settings saved successfully!');
      setSettingsExist(true); // After saving, settings now exist
    } catch (error) {
      console.error('Failed to save bot settings:', error);
      alert('Failed to save bot settings.');
    }
  };

  if (loading) {
    return <div>Loading bot settings...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div>
      <h1>Bot Settings</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="greetingMessage">Greeting Message</label>
          <input
            type="text"
            id="greetingMessage"
            value={greetingMessage}
            onChange={(e) => setGreetingMessage(e.target.value)}
          />
        </div>
        <div>
          <label htmlFor="fallbackReply">Fallback Reply</label>
          <input
            type="text"
            id="fallbackReply"
            value={fallbackReply}
            onChange={(e) => setFallbackReply(e.target.value)}
          />
        </div>
        <div>
          <label htmlFor="maxConvoHistory">Max Conversation History Length</label>
          <input
            type="number"
            id="maxConvoHistory"
            value={maxConvoHistory}
            onChange={(e) => setMaxConvoHistory(parseInt(e.target.value, 10))}
          />
        </div>
        <div>
          <label htmlFor="confidenceThreshold">Confidence Threshold</label>
          <input
            type="number"
            id="confidenceThreshold"
            step="0.1"
            min="0"
            max="1"
            value={confidenceThreshold}
            onChange={(e) => setConfidenceThreshold(parseFloat(e.target.value))}
          />
        </div>
        <button type="submit">{settingsExist ? "Update Settings" : "Create Settings"}</button>
      </form>
    </div>
  );
};

export default BotSettingsPage;