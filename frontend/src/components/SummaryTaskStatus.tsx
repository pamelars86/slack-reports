import React from 'react';
import {
  ClockIcon,
  CheckCircleIcon,
  XCircleIcon,
  ArrowPathIcon,
  DocumentArrowDownIcon,
  SparklesIcon,
  ChatBubbleLeftRightIcon
} from '@heroicons/react/24/outline';
import { SummaryTaskStatus as SummaryTaskStatusType } from '../types';

interface SummaryTaskStatusProps {
  taskId: string;
  status: SummaryTaskStatusType;
  onRefresh: () => void;
  onDownload: () => void;
  channel_id: string;
  thread_ts: string;
  llm_provider: 'openai' | 'ollama';
  model: string;
  last_updated: Date;
}

const SummaryTaskStatus: React.FC<SummaryTaskStatusProps> = ({
  taskId,
  status,
  onRefresh,
  onDownload,
  channel_id,
  thread_ts,
  llm_provider,
  model,
  last_updated
}) => {
  const getStatusIcon = () => {
    switch (status.status) {
      case 'PENDING':
        return <ClockIcon className="h-5 w-5 text-yellow-500" />;
      case 'SUCCESS':
        return <CheckCircleIcon className="h-5 w-5 text-green-500" />;
      case 'FAILURE':
        return <XCircleIcon className="h-5 w-5 text-red-500" />;
      default:
        return <ClockIcon className="h-5 w-5 text-gray-500" />;
    }
  };

  const getStatusColor = () => {
    switch (status.status) {
      case 'PENDING':
        return 'border-yellow-200 bg-yellow-50';
      case 'SUCCESS':
        return 'border-green-200 bg-green-50';
      case 'FAILURE':
        return 'border-red-200 bg-red-50';
      default:
        return 'border-gray-200 bg-gray-50';
    }
  };

  const formatDate = (date: Date) => {
    return date.toLocaleString();
  };

  return (
    <div className={`border rounded-lg p-6 ${getStatusColor()}`}>
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center space-x-3">
          {getStatusIcon()}
          <div>
            <h3 className="font-semibold text-gray-800 flex items-center space-x-2">
              <SparklesIcon className="h-4 w-4" />
              <span>Thread Summary</span>
            </h3>
            <p className="text-sm text-gray-600">Task ID: {taskId}</p>
          </div>
        </div>
        <div className="flex space-x-2">
          <button
            onClick={onRefresh}
            className="p-2 text-gray-600 hover:text-blue-600 hover:bg-blue-50 rounded-md transition-colors"
            title="Refresh status"
          >
            <ArrowPathIcon className="h-4 w-4" />
          </button>
          {status.status === 'SUCCESS' && status.data && (
            <button
              onClick={onDownload}
              className="p-2 text-gray-600 hover:text-green-600 hover:bg-green-50 rounded-md transition-colors"
              title="Download JSON"
            >
              <DocumentArrowDownIcon className="h-4 w-4" />
            </button>
          )}
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
        <div>
          <p className="text-sm font-medium text-gray-700">Channel ID:</p>
          <p className="text-sm text-gray-600 font-mono">{channel_id}</p>
        </div>
        <div>
          <p className="text-sm font-medium text-gray-700">Thread Timestamp:</p>
          <p className="text-sm text-gray-600 font-mono">{thread_ts}</p>
        </div>
        <div>
          <p className="text-sm font-medium text-gray-700">LLM Provider:</p>
          <div className="flex items-center space-x-1">
            <ChatBubbleLeftRightIcon className="h-4 w-4 text-purple-500" />
            <span className="text-sm text-gray-600 capitalize">{llm_provider}</span>
          </div>
        </div>
        <div>
          <p className="text-sm font-medium text-gray-700">Model:</p>
          <p className="text-sm text-gray-600">{model}</p>
        </div>
      </div>

      {status.status === 'SUCCESS' && status.data && (
        <div className="border-t pt-4 mt-4">
          <div className="mb-3">
            <h4 className="font-medium text-gray-800 flex items-center space-x-2">
              <SparklesIcon className="h-4 w-4 text-purple-500" />
              <span>AI Summary</span>
            </h4>
          </div>
          <div className="bg-white border rounded-lg p-4">
            <p className="text-gray-700 leading-relaxed whitespace-pre-wrap">
              {status.data.summary}
            </p>
          </div>
          <div className="mt-3 grid grid-cols-1 md:grid-cols-3 gap-3 text-sm text-gray-600">
            <div>
              <span className="font-medium">Total Messages:</span> {status.data.thread_data.total_messages}
            </div>
            <div>
              <span className="font-medium">Replies:</span> {status.data.thread_data.replies.length}
            </div>
            <div>
              <span className="font-medium">Generated:</span> {new Date(status.data.generated_at).toLocaleString()}
            </div>
          </div>
        </div>
      )}

      {status.status === 'FAILURE' && status.error && (
        <div className="border-t pt-4 mt-4">
          <div className="bg-red-50 border border-red-200 rounded-lg p-3">
            <p className="text-red-700 text-sm">
              <strong>Error:</strong> {status.error}
            </p>
          </div>
        </div>
      )}

      <div className="flex justify-between items-center text-xs text-gray-500 mt-4 pt-4 border-t">
        <span>Status: <span className="font-medium capitalize">{status.status.toLowerCase()}</span></span>
        <span>Last updated: {formatDate(last_updated)}</span>
      </div>
    </div>
  );
};

export default SummaryTaskStatus; 