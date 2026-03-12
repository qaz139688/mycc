import { useState, useCallback, useEffect } from 'react';
import Sidebar from './components/sidebar/Sidebar';
import SettingsPanel from './components/settings/SettingsPanel';
import Chat from './components/Chat';
import { api, type Conversation } from './services/api';

interface LocalSettings {
  apiKey: string;
  apiBaseUrl: string;
  modelName: string;
  enableWebSearch: boolean;
  enableSkill: boolean;
  enableMCP: boolean;
  enableKnowledgeBase: boolean;
  enableMemory: boolean;
  personalityFile: string;
  personalityContent: string;
  language: string;
  theme: 'dark' | 'light';
  telegramToken: string;
  telegramChatId: string;
  metasoApiKey: string;
  userCustomPrompt: string;
  userPreferences: string;
  feishuAppId: string;
  feishuAppSecret: string;
  feishuEncryptKey: string;
  feishuVerificationToken: string;
  feishuChatId: string;
  acpEnabled: boolean;
  acpDataPath: string;
  acpSeedPassword: string;
  acpAccessPoint: string;
  acpAgentName: string;
  acpAid: string;
  acpDebug: boolean;
}

const defaultSettings: LocalSettings = {
  apiKey: '',
  apiBaseUrl: 'https://api.openai.com/v1',
  modelName: 'gpt-4',
  enableWebSearch: false,
  enableSkill: false,
  enableMCP: false,
  enableKnowledgeBase: false,
  enableMemory: false,
  personalityFile: '',
  personalityContent: '',
  language: 'zh-CN',
  theme: 'dark',
  telegramToken: '',
  telegramChatId: '',
  metasoApiKey: '',
  userCustomPrompt: '',
  userPreferences: '',
  feishuAppId: '',
  feishuAppSecret: '',
  feishuEncryptKey: '',
  feishuVerificationToken: '',
  feishuChatId: '',
  acpEnabled: false,
  acpDataPath: '',
  acpSeedPassword: '123456',
  acpAccessPoint: 'agentid.pub',
  acpAgentName: '',
  acpAid: '',
  acpDebug: false,
};

function App() {
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(false);
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [settings, setSettings] = useState<LocalSettings>(defaultSettings);
  const [conversation, setConversation] = useState<Conversation | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [streamingContent, setStreamingContent] = useState<string>('');

  const toggleSidebar = useCallback(() => {
    setIsSidebarCollapsed((prev) => !prev);
  }, []);

  const loadConversation = useCallback(async () => {
    try {
      const conv = await api.getConversation();
      setConversation(conv);
    } catch (error) {
      console.error('Failed to load conversation:', error);
    }
  }, []);

  const loadSettings = useCallback(async () => {
    try {
      const apiSettings = await api.getSettings();
      setSettings(prev => ({
        ...prev,
        apiKey: apiSettings.api_key,
        apiBaseUrl: apiSettings.api_base_url,
        modelName: apiSettings.model_name,
        telegramToken: apiSettings.telegram_token || '',
        telegramChatId: apiSettings.telegram_chat_id || '',
        metasoApiKey: apiSettings.metaso_api_key || '',
        userCustomPrompt: apiSettings.user_custom_prompt || '',
        userPreferences: apiSettings.user_preferences || '',
        personalityFile: apiSettings.personality_file || '',
        personalityContent: apiSettings.personality_content || '',
        feishuAppId: apiSettings.feishu_app_id || '',
        feishuAppSecret: apiSettings.feishu_app_secret || '',
        feishuEncryptKey: apiSettings.feishu_encrypt_key || '',
        feishuVerificationToken: apiSettings.feishu_verification_token || '',
        feishuChatId: apiSettings.feishu_chat_id || '',
        acpEnabled: apiSettings.acp_enabled || false,
        acpDataPath: apiSettings.acp_data_path || '',
        acpSeedPassword: apiSettings.acp_seed_password || '123456',
        acpAccessPoint: apiSettings.acp_access_point || 'agentunion.cn',
        acpAgentName: apiSettings.acp_agent_name || '',
        acpAid: apiSettings.acp_aid || '',
        acpDebug: apiSettings.acp_debug || false,
      }));
    } catch (error) {
      console.error('Failed to load settings:', error);
    }
  }, []);

  useEffect(() => {
    loadConversation();
    loadSettings();
  }, [loadConversation, loadSettings]);

  const handleClearConversation = useCallback(async () => {
    if (confirm('确定要清除所有对话记录吗？此操作不可恢复。')) {
      try {
        await api.clearConversation();
        setConversation(null);
      } catch (error) {
        console.error('Failed to clear conversation:', error);
      }
    }
  }, []);

  const handleSendMessage = useCallback(async (content: string) => {
    setIsLoading(true);
    setStreamingContent('');

    try {
      await api.sendMessageStream(content, {
        onConversationId: (id) => {
          console.log('[App] onConversationId:', id);
        },
        onUserMessage: (msg) => {
          setConversation((prev) => {
            if (!prev) {
              return {
                id: 'main',
                title: '对话池',
                messages: [msg],
                created_at: msg.timestamp,
                updated_at: msg.timestamp,
              };
            }
            const hasMessage = prev.messages.some(m => m.timestamp === msg.timestamp);
            if (hasMessage) return prev;
            return {
              ...prev,
              messages: [...prev.messages, msg],
            };
          });
        },
        onChunk: (chunk) => {
          setStreamingContent((prev) => prev + chunk);
        },
        onDone: (message) => {
          setStreamingContent('');
          setConversation((prev) => {
            if (!prev) return prev;
            const hasAssistant = prev.messages.some(m => m.role === 'assistant' && m.timestamp === message.timestamp);
            if (hasAssistant) return prev;
            return {
              ...prev,
              messages: [...prev.messages, message],
              updated_at: message.timestamp,
            };
          });
        },
        onError: (error) => {
          console.error('[App] Stream error:', error);
          setStreamingContent('');
          alert(error);
        },
      });
    } catch (error) {
      console.error('[App] Failed to send message:', error);
      alert(error instanceof Error ? error.message : '发送消息失败');
    } finally {
      setIsLoading(false);
    }
  }, []);

  const handleSaveSettings = useCallback(async (newSettings: LocalSettings) => {
    try {
      await api.updateSettings({
        api_key: newSettings.apiKey,
        api_base_url: newSettings.apiBaseUrl,
        model_name: newSettings.modelName,
        telegram_token: newSettings.telegramToken,
        telegram_chat_id: newSettings.telegramChatId,
        metaso_api_key: newSettings.metasoApiKey,
        user_custom_prompt: newSettings.userCustomPrompt,
        user_preferences: newSettings.userPreferences,
        personality_file: newSettings.personalityFile,
        personality_content: newSettings.personalityContent,
        feishu_app_id: newSettings.feishuAppId,
        feishu_app_secret: newSettings.feishuAppSecret,
        feishu_encrypt_key: newSettings.feishuEncryptKey,
        feishu_verification_token: newSettings.feishuVerificationToken,
        feishu_chat_id: newSettings.feishuChatId,
        acp_enabled: newSettings.acpEnabled,
        acp_data_path: newSettings.acpDataPath,
        acp_seed_password: newSettings.acpSeedPassword,
        acp_access_point: newSettings.acpAccessPoint,
        acp_agent_name: newSettings.acpAgentName,
        acp_aid: newSettings.acpAid,
        acp_debug: newSettings.acpDebug,
      });
      setSettings(newSettings);
      setIsSettingsOpen(false);
    } catch (error) {
      console.error('Failed to save settings:', error);
      alert(error instanceof Error ? error.message : '保存设置失败');
    }
  }, []);

  return (
    <div className="flex h-screen w-screen bg-primary overflow-hidden">
      <div className="relative">
        <Sidebar
          isCollapsed={isSidebarCollapsed}
          onToggle={toggleSidebar}
          onOpenSettings={() => setIsSettingsOpen(true)}
          onClearConversation={handleClearConversation}
        />
      </div>

      <div className="flex-1 flex flex-col min-w-0">
        <Chat
          conversation={conversation}
          onSendMessage={handleSendMessage}
          isLoading={isLoading}
          streamingContent={streamingContent}
        />
      </div>

      <SettingsPanel
        isOpen={isSettingsOpen}
        onClose={() => setIsSettingsOpen(false)}
        settings={settings}
        onSave={handleSaveSettings}
      />
    </div>
  );
}

export default App;
