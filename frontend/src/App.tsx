import React, { useState } from 'react';
import Sidebar from './components/Sidebar';
import ReportForm from './components/ReportForm';
import TaskStatus from './components/TaskStatus';
import { TaskResponse, TaskStatus as TaskStatusType } from './types';
import { CheckCircleIcon } from '@heroicons/react/24/outline';

const API_URL = 'http://localhost:5000';

interface Task {
  id: string;
  status: TaskStatusType;
  type: 'messages' | 'repliers';
  created_at: Date;
  last_updated: Date;
  channel_id: string;
  start_date: string;
  end_date: string;
  top_n?: number;
}

const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'reports' | 'tasks'>('reports');
  const [tasks, setTasks] = useState<Task[]>([]);
  const [notification, setNotification] = useState<{ message: string; taskId: string } | null>(null);

  const generateReport = async (type: 'messages' | 'repliers', data: {
    channel_id: string;
    start_date: string;
    end_date: string;
    top_n?: number;
  }) => {
    try {
      const endpoint = type === 'messages' ? 'fetch-messages' : 'top-repliers';
      const taskName = type === 'messages' ? 'fetch_messages' : 'top_repliers';
      const response = await fetch(`${API_URL}/${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      const result: TaskResponse = await response.json();
      const now = new Date();
      const newTask: Task = {
        id: result.task_id,
        status: {
          status: 'PENDING' as const,
          task_name: taskName
        },
        type,
        created_at: now,
        last_updated: now,
        channel_id: data.channel_id,
        start_date: data.start_date,
        end_date: data.end_date,
        top_n: data.top_n
      };

      setTasks(prev => [newTask, ...prev]);
      setNotification({ message: `Task ${result.task_id} generated successfully`, taskId: result.task_id });

      setTimeout(() => setNotification(null), 5000);
    } catch (error) {
      console.error('Error generating report:', error);
      setNotification({ message: 'Error generating task', taskId: '' });
      setTimeout(() => setNotification(null), 5000);
    }
  };

  const checkTaskStatus = async (taskId: string, taskName: string) => {
    try {
      console.log('Checking status for task:', taskId, 'with name:', taskName);
      const response = await fetch(`${API_URL}/task-status/${taskId}?task_name=${taskName}`);

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const newStatus: TaskStatusType = await response.json();
      console.log('Received status:', newStatus);

      if (!newStatus || !newStatus.status) {
        throw new Error('Invalid status response from server');
      }

      setTasks(prev => prev.map(task => {
        if (task.id === taskId) {
          console.log('Updating task status from:', task.status.status, 'to:', newStatus.status);
          return {
            ...task,
            status: {
              ...newStatus,
              task_name: task.status.task_name
            },
            last_updated: new Date()
          };
        }
        return task;
      }));

      let notificationMessage = '';
      if (newStatus.status === 'SUCCESS') {
        notificationMessage = `Task ${taskId} completed successfully`;
      } else if (newStatus.status === 'FAILURE') {
        notificationMessage = `Error in task ${taskId}: ${newStatus.error || 'Unknown error'}`;
      } else {
        notificationMessage = `Task ${taskId} is still pending`;
      }

      setNotification({
        message: notificationMessage,
        taskId
      });
      setTimeout(() => setNotification(null), 5000);
    } catch (error) {
      console.error('Error checking task status:', error);
      setNotification({
        message: `Error checking status: ${error instanceof Error ? error.message : 'Unknown error'}`,
        taskId
      });
      setTimeout(() => setNotification(null), 5000);
    }
  };

  const downloadData = (taskId: string, format: 'csv' | 'json') => {
    const task = tasks.find(t => t.id === taskId);
    if (!task?.status.data) return;

    const data = task.status.data;
    let content: string;
    let mimeType: string;
    let extension: string;

    if (format === 'csv') {
      const processedData = data.map(item => {
        if ('reactions' in item && 'replies' in item) {
          const { post_id, reactions, replies, ...rest } = item;
          return {
            ...rest,
            reactions_count: Object.values(reactions || {}).reduce((a, b) => a + b, 0),
            reactions_list: Object.entries(reactions || {}).map(([name, count]) => `${name}:${count}`).join('; '),
            replies_count: replies?.length || 0,
            replies_list: replies?.map(reply => `${reply.author}: ${reply.message}`).join('; ') || ''
          };
        } else {
          return item;
        }
      });

      const headers = Object.keys(processedData[0]);
      const rows = processedData.map(item =>
        headers.map(header => {
          const value = (item as Record<string, any>)[header];
          if (value === null || value === undefined) {
            return '';
          }
          if (typeof value === 'object') {
            return `"${JSON.stringify(value).replace(/"/g, '""')}"`;
          }
          const stringValue = String(value).replace(/"/g, '""');
          const escapedValue = stringValue.replace(/[\n\r]/g, ' ');
          return /[",\n\r]/.test(escapedValue) ? `"${escapedValue}"` : escapedValue;
        }).join(',')
      );
      content = [headers.join(','), ...rows].join('\n');
      mimeType = 'text/csv;charset=utf-8;';
      extension = 'csv';
    } else {
      content = JSON.stringify(data, null, 2);
      mimeType = 'application/json';
      extension = 'json';
    }

    const blob = new Blob([content], { type: mimeType });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `${task.type}_${taskId}.${extension}`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="flex h-screen bg-gray-100">
      <Sidebar activeTab={activeTab} onTabChange={setActiveTab} />
      <main className="flex-1 overflow-auto">
        {notification && (
          <div className="fixed top-4 right-4 bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded flex items-center space-x-2">
            <CheckCircleIcon className="h-5 w-5" />
            <span>{notification.message}</span>
          </div>
        )}
        {activeTab === 'reports' ? (
          <ReportForm onGenerateReport={generateReport} />
        ) : tasks.length > 0 ? (
          <div className="p-6 space-y-6">
            <h2 className="text-xl font-semibold">Generated Reports</h2>
            {tasks.map(task => (
              <TaskStatus
                key={task.id}
                taskId={task.id}
                status={task.status}
                onRefresh={(taskName) => checkTaskStatus(task.id, taskName)}
                onDownload={(format) => downloadData(task.id, format)}
                channel_id={task.channel_id}
                start_date={task.start_date}
                end_date={task.end_date}
                top_n={task.top_n}
                type={task.type}
                last_updated={task.last_updated}
              />
            ))}
          </div>
        ) : (
          <div className="p-6">
            <h2 className="text-xl font-semibold">No reports generated</h2>
            <p className="text-gray-600">Generate a report to see its status.</p>
          </div>
        )}
      </main>
    </div>
  );
};

export default App;