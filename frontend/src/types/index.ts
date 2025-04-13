export interface TaskResponse {
  task_id: string;
  status: string;
}

export interface TaskStatus {
  status: 'PENDING' | 'SUCCESS' | 'FAILURE';
  error?: string;
  data?: Message[] | TopReplier[];
  task_name?: string;
}

export interface Message {
  author: string;
  date: string;
  message: string;
  post_id: string;
  reactions: { [key: string]: number };
  replies: Reply[];
  subtype: string | null;
  url: string;
}

export interface Reply {
  author: string;
  date: string;
  message: string;
  post_id: string;
  url: string;
}

export interface TopReplier {
  user: string;
  count: number;
}

export type ReportData = Message[] | TopReplier[];

export interface ApiError {
  error: string;
}