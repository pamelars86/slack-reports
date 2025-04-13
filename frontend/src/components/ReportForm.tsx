import React, { useState } from 'react';
import { ChatBubbleLeftIcon, UserGroupIcon } from '@heroicons/react/24/outline';

interface ReportFormProps {
  onGenerateReport: (type: 'messages' | 'repliers', data: {
    channel_id: string;
    start_date: string;
    end_date: string;
    top_n?: number;
  }) => void;
}

const ReportForm: React.FC<ReportFormProps> = ({ onGenerateReport }) => {
  const [channelId, setChannelId] = useState('');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [topN, setTopN] = useState<number>(5);
  const [reportType, setReportType] = useState<'messages' | 'repliers'>('messages');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (reportType === 'messages') {
      onGenerateReport('messages', {
        channel_id: channelId,
        start_date: startDate,
        end_date: endDate
      });
    } else {
      onGenerateReport('repliers', {
        channel_id: channelId,
        start_date: startDate,
        end_date: endDate,
        top_n: topN
      });
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-6">
      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
          <button
            type="button"
            onClick={() => setReportType('messages')}
            className={`p-6 rounded-lg border-2 transition-all ${
              reportType === 'messages'
                ? 'border-blue-500 bg-blue-50'
                : 'border-gray-200 hover:border-blue-300'
            }`}
          >
            <div className="flex flex-col items-center space-y-2">
              <ChatBubbleLeftIcon className="h-12 w-12 text-blue-500" />
              <h3 className="text-lg font-medium">Get Messages</h3>
              <p className="text-sm text-gray-500 text-center">
                Retrieve all messages from a channel within a date range
              </p>
            </div>
          </button>

          <button
            type="button"
            onClick={() => setReportType('repliers')}
            className={`p-6 rounded-lg border-2 transition-all ${
              reportType === 'repliers'
                ? 'border-blue-500 bg-blue-50'
                : 'border-gray-200 hover:border-blue-300'
            }`}
          >
            <div className="flex flex-col items-center space-y-2">
              <UserGroupIcon className="h-12 w-12 text-blue-500" />
              <h3 className="text-lg font-medium">Top Repliers</h3>
              <p className="text-sm text-gray-500 text-center">
                Get the most active users in a channel within a date range
              </p>
            </div>
          </button>
        </div>

        <div className="space-y-4">
          <div>
            <label htmlFor="channelId" className="block text-sm font-medium text-gray-700">
              Channel ID
            </label>
            <input
              type="text"
              id="channelId"
              value={channelId}
              onChange={(e) => setChannelId(e.target.value)}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 py-2 px-3"
              required
            />
          </div>

          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <div>
              <label htmlFor="startDate" className="block text-sm font-medium text-gray-700">
                Start Date
              </label>
              <input
                type="date"
                id="startDate"
                value={startDate}
                onChange={(e) => setStartDate(e.target.value)}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 py-2 px-3"
                required
              />
            </div>

            <div>
              <label htmlFor="endDate" className="block text-sm font-medium text-gray-700">
                End Date
              </label>
              <input
                type="date"
                id="endDate"
                value={endDate}
                onChange={(e) => setEndDate(e.target.value)}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 py-2 px-3"
                required
              />
            </div>
          </div>

          {reportType === 'repliers' && (
            <div>
              <label htmlFor="topN" className="block text-sm font-medium text-gray-700">
                Number of Top Repliers
              </label>
              <input
                type="number"
                id="topN"
                value={topN}
                onChange={(e) => setTopN(Number(e.target.value))}
                min="1"
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 py-2 px-3"
                required
              />
            </div>
          )}
        </div>

        <div className="flex justify-center">
          <button
            type="submit"
            className="px-6 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
          >
            Generate Report
          </button>
        </div>
      </form>
    </div>
  );
};

export default ReportForm;