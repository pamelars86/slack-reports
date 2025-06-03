import React from 'react';
import { DocumentTextIcon, ChartBarIcon, ChatBubbleLeftRightIcon } from '@heroicons/react/24/outline';

interface SidebarProps {
  activeTab: 'reports' | 'tasks' | 'summaries' | 'summary-tasks';
  onTabChange: (tab: 'reports' | 'tasks' | 'summaries' | 'summary-tasks') => void;
}

const Sidebar: React.FC<SidebarProps> = ({ activeTab, onTabChange }) => {
  return (
    <div className="w-64 bg-white shadow-md">
      <div className="p-4">
        <h2 className="text-lg font-semibold text-gray-800 mb-4">Slack Reports</h2>
        <nav className="space-y-2">
          <button
            onClick={() => onTabChange('reports')}
            className={`flex items-center space-x-2 w-full px-4 py-2 rounded-md transition-colors ${
              activeTab === 'reports'
                ? 'bg-blue-50 text-blue-600'
                : 'text-gray-600 hover:bg-gray-50'
            }`}
          >
            <DocumentTextIcon className="h-5 w-5" />
            <span>Generate Reports</span>
          </button>
          <button
            onClick={() => onTabChange('tasks')}
            className={`flex items-center space-x-2 w-full px-4 py-2 rounded-md transition-colors ${
              activeTab === 'tasks'
                ? 'bg-blue-50 text-blue-600'
                : 'text-gray-600 hover:bg-gray-50'
            }`}
          >
            <ChartBarIcon className="h-5 w-5" />
            <span>Report Status</span>
          </button>
          <button
            onClick={() => onTabChange('summaries')}
            className={`flex items-center space-x-2 w-full px-4 py-2 rounded-md transition-colors ${
              activeTab === 'summaries'
                ? 'bg-blue-50 text-blue-600'
                : 'text-gray-600 hover:bg-gray-50'
            }`}
          >
            <ChatBubbleLeftRightIcon className="h-5 w-5" />
            <span>Thread Summaries</span>
          </button>
          <button
            onClick={() => onTabChange('summary-tasks')}
            className={`flex items-center space-x-2 w-full px-4 py-2 rounded-md transition-colors ${
              activeTab === 'summary-tasks'
                ? 'bg-blue-50 text-blue-600'
                : 'text-gray-600 hover:bg-gray-50'
            }`}
          >
            <ChatBubbleLeftRightIcon className="h-5 w-5" />
            <span>Summary Status</span>
          </button>
        </nav>
      </div>
    </div>
  );
};

export default Sidebar;