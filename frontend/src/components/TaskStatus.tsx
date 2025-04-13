import React from 'react';
import { ArrowPathIcon, CheckCircleIcon, XCircleIcon, ArrowDownTrayIcon } from '@heroicons/react/24/outline';
import { TaskStatus as TaskStatusType } from '../types';

interface TaskStatusProps {
  taskId: string;
  status: TaskStatusType;
  onRefresh: (taskName: string) => void;
  onDownload: (format: 'csv' | 'json') => void;
  channel_id: string;
  start_date: string;
  end_date: string;
  top_n?: number;
  type: 'messages' | 'repliers';
  last_updated: Date;
}

const TaskStatus: React.FC<TaskStatusProps> = ({
  taskId,
  status,
  onRefresh,
  onDownload,
  channel_id,
  start_date,
  end_date,
  top_n,
  type,
  last_updated
}) => {
  const formatDate = (date: string) => {
    return new Date(date).toLocaleDateString();
  };

  return (
    <div className="bg-white p-4 rounded-lg shadow">
      <div className="flex justify-between items-start mb-4">
        <div>
          <h3 className="text-lg font-semibold">
            {type === 'messages' ? 'Reporte de Mensajes' : 'Reporte de Top Repliers'} - ID: {taskId}
          </h3>
          <p className="text-sm text-gray-600">
            Canal: {channel_id}
          </p>
          <p className="text-sm text-gray-600">
            Período: {formatDate(start_date)} - {formatDate(end_date)}
          </p>
          {top_n && (
            <p className="text-sm text-gray-600">
              Top {top_n} repliers
            </p>
          )}
        </div>
        <div className="text-sm text-gray-500">
          Última actualización: {last_updated.toLocaleTimeString()}
        </div>
      </div>

      <div className="mb-4">
        {status.status === 'PENDING' && (
          <div className="text-yellow-600">
            <div className="font-semibold">Estado: Pendiente</div>
          </div>
        )}
        {status.status === 'SUCCESS' && (
          <div className="text-green-600">
            <div className="font-semibold">Estado: Completado</div>
            {status.data && (
              <div className="text-xs text-gray-500 mt-1">
                Datos disponibles: {Array.isArray(status.data) ? `${status.data.length} registros` : '1 registro'}
              </div>
            )}
          </div>
        )}
        {status.status === 'FAILURE' && (
          <div className="text-red-600">
            <div className="font-semibold">Estado: Error</div>
            <div className="text-sm mt-1">Error: {status.error || 'Error desconocido'}</div>
          </div>
        )}
      </div>

      <div className="flex justify-between items-center">
        {status.status !== 'SUCCESS' && (
          <button
            onClick={() => {
              const taskName = status.task_name || (type === 'messages' ? 'fetch_messages' : 'top_repliers');
              console.log('Refreshing status for task:', taskId, 'with name:', taskName);
              onRefresh(taskName);
            }}
            className="flex items-center space-x-2 bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition-colors"
            title="Click to refresh task status"
          >
            <ArrowPathIcon className="h-5 w-5" />
            <span>Actualizar Estado</span>
          </button>
        )}

        {status.status === 'SUCCESS' && status.data && (
          <div className="flex items-center space-x-2">
            <button
              onClick={() => onDownload('csv')}
              className="flex items-center space-x-2 bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600 transition-colors"
            >
              <ArrowDownTrayIcon className="h-5 w-5" />
              <span>Download CSV</span>
            </button>
            <button
              onClick={() => onDownload('json')}
              className="flex items-center space-x-2 bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600 transition-colors"
            >
              <ArrowDownTrayIcon className="h-5 w-5" />
              <span>Download JSON</span>
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default TaskStatus;