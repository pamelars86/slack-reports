import React, { useState } from 'react';
import { ChatBubbleLeftRightIcon, SparklesIcon } from '@heroicons/react/24/outline';
import { LLMProvider } from '../types';

interface SummaryFormProps {
  onGenerateSummary: (data: {
    channel_id: string;
    thread_ts: string;
    llm_provider: LLMProvider;
    model: string;
  }) => void;
}

const SummaryForm: React.FC<SummaryFormProps> = ({ onGenerateSummary }) => {
  const [channelId, setChannelId] = useState('');
  const [threadTs, setThreadTs] = useState('');
  const [llmProvider, setLlmProvider] = useState<LLMProvider>('openai');
  const [model, setModel] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!channelId || !threadTs || !model) {
      alert('Please fill in all required fields');
      return;
    }

    setIsSubmitting(true);
    try {
      await onGenerateSummary({
        channel_id: channelId,
        thread_ts: threadTs,
        llm_provider: llmProvider,
        model: model
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  const getModelPlaceholder = (provider: LLMProvider) => {
    switch (provider) {
      case 'openai':
        return 'e.g., gpt-4, gpt-3.5-turbo, gpt-4o';
      case 'ollama':
        return 'e.g., deepseek-r1:latest, llama3:latest';
      default:
        return 'Enter model name';
    }
  };

  const handleProviderChange = (provider: LLMProvider) => {
    setLlmProvider(provider);
    // Clear model when provider changes
    setModel('');
  };

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <div className="mb-8">
        <div className="flex items-center space-x-3 mb-4">
          <SparklesIcon className="h-8 w-8 text-purple-600" />
          <h1 className="text-3xl font-bold text-gray-800">Thread Summarization</h1>
        </div>
        <p className="text-gray-600">
          Generate AI-powered summaries of Slack thread conversations using OpenAI or Ollama.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow-md p-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Channel ID */}
          <div>
            <label htmlFor="channelId" className="block text-sm font-medium text-gray-700 mb-2">
              Channel ID *
            </label>
            <input
              type="text"
              id="channelId"
              value={channelId}
              onChange={(e) => setChannelId(e.target.value)}
              placeholder="C1234567890"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
              required
            />
            <p className="text-xs text-gray-500 mt-1">
              The Slack channel ID where the thread is located
            </p>
          </div>

          {/* Thread Timestamp */}
          <div>
            <label htmlFor="threadTs" className="block text-sm font-medium text-gray-700 mb-2">
              Thread Timestamp *
            </label>
            <input
              type="text"
              id="threadTs"
              value={threadTs}
              onChange={(e) => setThreadTs(e.target.value)}
              placeholder="1748458889.115369"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
              required
            />
            <p className="text-xs text-gray-500 mt-1">
              The timestamp of the main thread message
            </p>
          </div>

          {/* LLM Provider */}
          <div>
            <label htmlFor="llmProvider" className="block text-sm font-medium text-gray-700 mb-2">
              LLM Provider *
            </label>
            <select
              id="llmProvider"
              value={llmProvider}
              onChange={(e) => handleProviderChange(e.target.value as LLMProvider)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
              required
            >
              <option value="openai">OpenAI</option>
              <option value="ollama">Ollama</option>
            </select>
            <p className="text-xs text-gray-500 mt-1">
              Choose the AI provider for generating summaries
            </p>
          </div>

          {/* Model */}
          <div>
            <label htmlFor="model" className="block text-sm font-medium text-gray-700 mb-2">
              Model *
            </label>
            <input
              type="text"
              id="model"
              value={model}
              onChange={(e) => setModel(e.target.value)}
              placeholder={getModelPlaceholder(llmProvider)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
              required
            />
            <p className="text-xs text-gray-500 mt-1">
              Enter the model name for the selected provider
            </p>
          </div>
        </div>

        {/* Submit Button */}
        <div className="mt-8 flex justify-center">
          <button
            type="submit"
            disabled={isSubmitting}
            className={`flex items-center space-x-2 px-8 py-3 rounded-md font-medium transition-colors ${
              isSubmitting
                ? 'bg-gray-400 cursor-not-allowed'
                : 'bg-purple-600 hover:bg-purple-700 text-white'
            }`}
          >
            <ChatBubbleLeftRightIcon className="h-5 w-5" />
            <span>{isSubmitting ? 'Generating Summary...' : 'Generate Summary'}</span>
          </button>
        </div>
      </form>
    </div>
  );
};

export default SummaryForm; 