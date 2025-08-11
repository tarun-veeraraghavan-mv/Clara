"use client";
import React, { useState } from 'react';
import { createBotSettings } from '@/services/botSettingsService';

const BotSettingsPage = () => {
  const [greetingMessage, setGreetingMessage] = useState('');
  const [fallbackReply, setFallbackReply] = useState('');
  const [maxConvoHistory, setMaxConvoHistory] = useState(10);
  const [confidenceThreshold, setConfidenceThreshold] = useState(0.8);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const settings = {
        greetingMessage,
        fallbackReply,
        maxConvoHistory,
        confidenceThreshold,
      };
      const response = await createBotSettings(settings);
      console.log('Bot settings created:', response);
      alert('Bot settings saved successfully!');
    } catch (error) {
      console.error('Failed to save bot settings:', error);
      alert('Failed to save bot settings.');
    }
  };

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
        <button type="submit">Submit</button>
      </form>
    </div>
  );
};

export default BotSettingsPage;
