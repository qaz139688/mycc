const API_BASE_URL = 'http://localhost:10053';

export interface Message {
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: number;
}

export interface Conversation {
  id: string;
  title: string;
  messages: Message[];
  created_at: number;
  updated_at: number;
}

export interface Settings {
  api_key: string;
  api_base_url: string;
  model_name: string;
  telegram_token: string;
  telegram_chat_id: string;
  metaso_api_key: string;
  user_custom_prompt: string;
  user_preferences: string;
  personality_file: string;
  personality_content: string;
  feishu_app_id: string;
  feishu_app_secret: string;
  feishu_encrypt_key: string;
  feishu_verification_token: string;
  feishu_chat_id: string;
  acp_enabled: boolean;
  acp_data_path: string;
  acp_seed_password: string;
  acp_access_point: string;
  acp_agent_name: string;
  acp_aid: string;
  acp_debug: boolean;
}

export interface StreamCallbacks {
  onConversationId: (id: string) => void;
  onUserMessage: (message: Message, conversationId: string) => void;
  onChunk: (content: string) => void;
  onDone: (message: Message, conversationId: string) => void;
  onError: (error: string) => void;
}

async function fetchAPI<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
    throw new Error(error.detail || `HTTP error! status: ${response.status}`);
  }

  return response.json();
}

export const api = {
  async getConversation(): Promise<Conversation> {
    return fetchAPI<Conversation>('/api/conversation');
  },

  async clearConversation(): Promise<void> {
    await fetchAPI('/api/conversation', { method: 'DELETE' });
  },

  async sendMessageStream(
    content: string,
    callbacks: StreamCallbacks
  ): Promise<void> {
    const response = await fetch(`${API_BASE_URL}/api/chat/stream`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        content,
      }),
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
      callbacks.onError(error.detail || `HTTP error! status: ${response.status}`);
      return;
    }

    const reader = response.body?.getReader();
    if (!reader) {
      callbacks.onError('No response body');
      return;
    }

    const decoder = new TextDecoder();
    let buffer = '';

    try {
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop() || '';

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const jsonStr = line.slice(6);
              const data = JSON.parse(jsonStr);
              
              switch (data.type) {
                case 'conversation_id':
                  callbacks.onConversationId(data.conversation_id);
                  break;
                case 'user_message':
                  callbacks.onUserMessage(data.message, data.conversation_id);
                  break;
                case 'chunk':
                  callbacks.onChunk(data.content);
                  break;
                case 'tool_call':
                  console.log('Tool call:', data.tool_call);
                  break;
                case 'tool_result':
                  console.log('Tool result:', data.tool_call_id, data.result);
                  break;
                case 'done':
                  callbacks.onDone(data.message, data.conversation_id);
                  break;
                case 'error':
                  callbacks.onError(data.error);
                  break;
              }
            } catch (e) {
              console.error('Parse error:', e);
            }
          }
        }
      }
    } finally {
      reader.releaseLock();
    }
  },

  async getSettings(): Promise<Settings> {
    return fetchAPI<Settings>('/api/settings');
  },

  async updateSettings(settings: Partial<Settings>): Promise<Settings> {
    return fetchAPI<Settings>('/api/settings', {
      method: 'POST',
      body: JSON.stringify(settings),
    });
  },
};
