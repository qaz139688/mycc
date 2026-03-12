import React, { useState, useEffect } from 'react';
import {
  X,
  Key,
  Globe,
  Zap,
  Cpu,
  BookOpen,
  Brain,
  UserCircle,
  Info,
  ChevronRight,
  Save,
  Search,
  Database,
  MessageCircle,
  Network
} from 'lucide-react';

interface Settings {
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

interface SettingsPanelProps {
  isOpen: boolean;
  onClose: () => void;
  settings: Settings;
  onSave: (settings: Settings) => void;
}

type SettingsTab = 
  | 'api' 
  | 'social'
  | 'acp'
  | 'websearch' 
  | 'skill' 
  | 'mcp' 
  | 'knowledge' 
  | 'memory' 
  | 'personality' 
  | 'about';

const tabs: { id: SettingsTab; label: string; icon: React.ReactNode }[] = [
  { id: 'api', label: 'API 密钥', icon: <Key style={{ width: '16px', height: '16px' }} /> },
  { id: 'social', label: '社交能力', icon: <MessageCircle style={{ width: '16px', height: '16px' }} /> },
  { id: 'acp', label: 'ACP 通信', icon: <Network style={{ width: '16px', height: '16px' }} /> },
  { id: 'websearch', label: '联网搜索', icon: <Globe style={{ width: '16px', height: '16px' }} /> },
  { id: 'skill', label: 'SKILL', icon: <Zap style={{ width: '16px', height: '16px' }} /> },
  { id: 'mcp', label: 'MCP', icon: <Cpu style={{ width: '16px', height: '16px' }} /> },
  { id: 'knowledge', label: '知识库', icon: <BookOpen style={{ width: '16px', height: '16px' }} /> },
  { id: 'memory', label: '记忆', icon: <Brain style={{ width: '16px', height: '16px' }} /> },
  { id: 'personality', label: '人格文件', icon: <UserCircle style={{ width: '16px', height: '16px' }} /> },
  { id: 'about', label: '关于', icon: <Info style={{ width: '16px', height: '16px' }} /> },
];

const SettingsPanel: React.FC<SettingsPanelProps> = ({
  isOpen,
  onClose,
  settings,
  onSave,
}) => {
  const [activeTab, setActiveTab] = useState<SettingsTab>('api');
  const [localSettings, setLocalSettings] = useState<Settings>(settings);
  const [isCollapsed, setIsCollapsed] = useState(false);

  useEffect(() => {
    setLocalSettings(settings);
  }, [settings]);

  const handleSave = () => {
    onSave(localSettings);
  };

  const updateSetting = <K extends keyof Settings>(key: K, value: Settings[K]) => {
    setLocalSettings((prev) => ({ ...prev, [key]: value }));
  };

  if (!isOpen) return null;

  const inputStyle: React.CSSProperties = {
    width: '100%',
    padding: '8px 12px',
    backgroundColor: '#1a1a1a',
    border: '1px solid #2a2a2a',
    borderRadius: '6px',
    color: '#e7e7e7',
    fontSize: '14px',
    outline: 'none'
  };

  const labelStyle: React.CSSProperties = {
    display: 'block',
    fontSize: '14px',
    color: '#888888',
    marginBottom: '8px'
  };

  const cardStyle: React.CSSProperties = {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: '16px',
    backgroundColor: '#141414',
    borderRadius: '8px'
  };

  const renderToggle = (checked: boolean, onChange: (checked: boolean) => void) => (
    <label style={{ position: 'relative', display: 'inline-flex', alignItems: 'center', cursor: 'pointer' }}>
      <input
        type="checkbox"
        checked={checked}
        onChange={(e) => onChange(e.target.checked)}
        style={{ position: 'absolute', opacity: 0, width: 0, height: 0 }}
      />
      <div style={{
        width: '44px',
        height: '24px',
        backgroundColor: checked ? '#d49a2e' : '#1a1a1a',
        borderRadius: '12px',
        position: 'relative',
        transition: 'background-color 0.2s'
      }}>
        <div style={{
          width: '20px',
          height: '20px',
          backgroundColor: '#fff',
          borderRadius: '50%',
          position: 'absolute',
          top: '2px',
          left: checked ? '22px' : '2px',
          transition: 'left 0.2s'
        }} />
      </div>
    </label>
  );

  return (
    <div style={{
      position: 'fixed',
      inset: 0,
      zIndex: 50,
      display: 'flex'
    }}>
      <div
        style={{
          flex: 1,
          backgroundColor: 'rgba(0, 0, 0, 0.5)',
          backdropFilter: 'blur(4px)'
        }}
        onClick={onClose}
      />

      <div style={{ display: 'flex', height: '100%', backgroundColor: '#0a0a0a', boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.5)' }}>
        <div style={{
          height: '100%',
          backgroundColor: '#141414',
          borderRight: '1px solid #2a2a2a',
          display: 'flex',
          flexDirection: 'column',
          transition: 'width 0.3s',
          width: isCollapsed ? '64px' : '224px'
        }}>
          <div style={{
            height: '56px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            padding: '0 16px',
            borderBottom: '1px solid #2a2a2a'
          }}>
            {!isCollapsed && (
              <span style={{ color: '#d49a2e', fontWeight: 600, fontSize: '18px' }}>设置</span>
            )}
            <button
              onClick={() => setIsCollapsed(!isCollapsed)}
              style={{
                padding: '6px',
                borderRadius: '8px',
                backgroundColor: 'transparent',
                border: 'none',
                color: '#888888',
                cursor: 'pointer'
              }}
            >
              {isCollapsed ? (
                <ChevronRight style={{ width: '20px', height: '20px' }} />
              ) : (
                <X style={{ width: '20px', height: '20px' }} />
              )}
            </button>
          </div>

          <div style={{ flex: 1, overflowY: 'auto', padding: '8px 0' }}>
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                style={{
                  width: '100%',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '12px',
                  padding: '12px 16px',
                  backgroundColor: activeTab === tab.id ? 'rgba(212, 154, 46, 0.2)' : 'transparent',
                  color: activeTab === tab.id ? '#d49a2e' : '#888888',
                  border: 'none',
                  borderRight: activeTab === tab.id ? '2px solid #d49a2e' : 'none',
                  cursor: 'pointer',
                  justifyContent: isCollapsed ? 'center' : 'flex-start'
                }}
              >
                {tab.icon}
                {!isCollapsed && <span style={{ fontSize: '14px' }}>{tab.label}</span>}
              </button>
            ))}
          </div>

          <div style={{ padding: '16px', borderTop: '1px solid #2a2a2a' }}>
            <button
              onClick={handleSave}
              style={{
                width: '100%',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '8px',
                padding: '10px 16px',
                background: 'linear-gradient(135deg, #d49a2e 0%, #b87f24 100%)',
                color: '#0a0a0a',
                fontWeight: 600,
                borderRadius: '8px',
                border: 'none',
                cursor: 'pointer'
              }}
            >
              <Save style={{ width: '16px', height: '16px' }} />
              {!isCollapsed && <span>保存设置</span>}
            </button>
          </div>
        </div>

        <div style={{ width: '384px', backgroundColor: '#0a0a0a', display: 'flex', flexDirection: 'column' }}>
          <div style={{
            height: '56px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'flex-end',
            padding: '0 16px',
            borderBottom: '1px solid #2a2a2a'
          }}>
            <button
              onClick={onClose}
              style={{
                padding: '8px',
                borderRadius: '8px',
                backgroundColor: 'transparent',
                border: 'none',
                color: '#888888',
                cursor: 'pointer'
              }}
            >
              <X style={{ width: '20px', height: '20px' }} />
            </button>
          </div>

          <div style={{ flex: 1, overflowY: 'auto', padding: '24px' }}>
            {activeTab === 'api' && (
              <div>
                <h2 style={{ fontSize: '20px', fontWeight: 600, color: '#d49a2e', marginBottom: '24px' }}>API 配置</h2>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                  <div>
                    <label style={labelStyle}>API 密钥</label>
                    <input
                      type="password"
                      value={localSettings.apiKey}
                      onChange={(e) => updateSetting('apiKey', e.target.value)}
                      placeholder="输入你的 API 密钥"
                      style={inputStyle}
                    />
                  </div>
                  <div>
                    <label style={labelStyle}>API 基础 URL</label>
                    <input
                      type="text"
                      value={localSettings.apiBaseUrl}
                      onChange={(e) => updateSetting('apiBaseUrl', e.target.value)}
                      placeholder="https://api.openai.com/v1"
                      style={inputStyle}
                    />
                  </div>
                  <div>
                    <label style={labelStyle}>模型名称</label>
                    <input
                      type="text"
                      value={localSettings.modelName}
                      onChange={(e) => updateSetting('modelName', e.target.value)}
                      placeholder="gpt-4"
                      style={inputStyle}
                    />
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'social' && (
              <div>
                <h2 style={{ fontSize: '20px', fontWeight: 600, color: '#d49a2e', marginBottom: '24px' }}>社交能力</h2>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                  <div style={{ padding: '16px', backgroundColor: '#141414', borderRadius: '8px' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '16px' }}>
                      <MessageCircle style={{ width: '24px', height: '24px', color: '#0088cc' }} />
                      <span style={{ fontSize: '16px', fontWeight: 500, color: '#e7e7e7' }}>Telegram</span>
                    </div>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                      <div>
                        <label style={labelStyle}>Bot Token</label>
                        <input
                          type="password"
                          value={localSettings.telegramToken}
                          onChange={(e) => updateSetting('telegramToken', e.target.value)}
                          placeholder="123456789:ABCdefGHIjklMNOpqrsTUVwxyz"
                          style={inputStyle}
                        />
                      </div>
                      <div>
                        <label style={labelStyle}>Chat ID</label>
                        <input
                          type="text"
                          value={localSettings.telegramChatId}
                          onChange={(e) => updateSetting('telegramChatId', e.target.value)}
                          placeholder="123456789"
                          style={inputStyle}
                        />
                      </div>
                      <div style={{ fontSize: '12px', color: '#666666', marginTop: '8px' }}>
                        <p style={{ marginBottom: '4px' }}>获取方式：</p>
                        <p>1. 在 Telegram 中搜索 @BotFather 创建机器人获取 Token</p>
                        <p>2. 在 Telegram 中搜索 @userinfobot 获取你的 Chat ID</p>
                      </div>
                    </div>
                  </div>
                  
                  <div style={{ padding: '16px', backgroundColor: '#141414', borderRadius: '8px' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '16px' }}>
                      <svg style={{ width: '24px', height: '24px' }} viewBox="0 0 24 24" fill="none">
                        <path d="M6.5 6.5h11v11h-11z" fill="#3370ff"/>
                        <path d="M4 4h4v4H4zM16 4h4v4h-4zM4 16h4v4H4zM16 16h4v4h-4z" fill="#3370ff"/>
                      </svg>
                      <span style={{ fontSize: '16px', fontWeight: 500, color: '#e7e7e7' }}>飞书</span>
                    </div>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                      <div>
                        <label style={labelStyle}>App ID</label>
                        <input
                          type="text"
                          value={localSettings.feishuAppId}
                          onChange={(e) => updateSetting('feishuAppId', e.target.value)}
                          placeholder="cli_xxxxxxxxxxxx"
                          style={inputStyle}
                        />
                      </div>
                      <div>
                        <label style={labelStyle}>App Secret</label>
                        <input
                          type="password"
                          value={localSettings.feishuAppSecret}
                          onChange={(e) => updateSetting('feishuAppSecret', e.target.value)}
                          placeholder="输入 App Secret"
                          style={inputStyle}
                        />
                      </div>
                      <div>
                        <label style={labelStyle}>Encrypt Key (可选)</label>
                        <input
                          type="password"
                          value={localSettings.feishuEncryptKey}
                          onChange={(e) => updateSetting('feishuEncryptKey', e.target.value)}
                          placeholder="用于消息加密"
                          style={inputStyle}
                        />
                      </div>
                      <div>
                        <label style={labelStyle}>Verification Token (可选)</label>
                        <input
                          type="text"
                          value={localSettings.feishuVerificationToken}
                          onChange={(e) => updateSetting('feishuVerificationToken', e.target.value)}
                          placeholder="用于验证请求"
                          style={inputStyle}
                        />
                      </div>
                      <div>
                        <label style={labelStyle}>默认 Chat ID</label>
                        <input
                          type="text"
                          value={localSettings.feishuChatId}
                          onChange={(e) => updateSetting('feishuChatId', e.target.value)}
                          placeholder="oc_xxxxxxxxxxxx"
                          style={inputStyle}
                        />
                      </div>
                      <div style={{ fontSize: '12px', color: '#666666', marginTop: '8px' }}>
                        <p style={{ marginBottom: '4px' }}>配置步骤：</p>
                        <p>1. 访问 <a href="https://open.feishu.cn/" target="_blank" rel="noopener noreferrer" style={{ color: '#d49a2e' }}>飞书开放平台</a> 创建企业自建应用</p>
                        <p>2. 在应用详情页获取 App ID 和 App Secret</p>
                        <p>3. 在事件订阅中配置请求地址: /api/feishu/webhook</p>
                        <p>4. 添加消息接收权限: im:message</p>
                        <p>5. 发布应用并添加到群聊或单聊</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'acp' && (
              <div>
                <h2 style={{ fontSize: '20px', fontWeight: 600, color: '#d49a2e', marginBottom: '24px' }}>ACP 通信协议</h2>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                  <div style={{ padding: '16px', backgroundColor: '#141414', borderRadius: '8px' }}>
                    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px' }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                        <Network style={{ width: '24px', height: '24px', color: '#d49a2e' }} />
                        <span style={{ fontSize: '16px', fontWeight: 500, color: '#e7e7e7' }}>启用 ACP</span>
                      </div>
                      <div style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: '6px',
                        padding: '4px 10px',
                        borderRadius: '12px',
                        backgroundColor: localSettings.acpEnabled ? 'rgba(34, 197, 94, 0.2)' : 'rgba(239, 68, 68, 0.2)',
                        fontSize: '12px',
                        color: localSettings.acpEnabled ? '#22c55e' : '#ef4444'
                      }}>
                        <div style={{
                          width: '6px',
                          height: '6px',
                          borderRadius: '50%',
                          backgroundColor: localSettings.acpEnabled ? '#22c55e' : '#ef4444'
                        }} />
                        {localSettings.acpEnabled ? '已启用' : '未启用'}
                      </div>
                    </div>
                    {renderToggle(localSettings.acpEnabled, (v) => updateSetting('acpEnabled', v))}
                  </div>

                  <div style={{ padding: '16px', backgroundColor: '#141414', borderRadius: '8px' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '16px' }}>
                      <span style={{ fontSize: '16px', fontWeight: 500, color: '#e7e7e7' }}>基本配置</span>
                    </div>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                      <div>
                        <label style={labelStyle}>接入点 (Access Point)</label>
                        <select
                          value={localSettings.acpAccessPoint}
                          onChange={(e) => updateSetting('acpAccessPoint', e.target.value)}
                          style={{
                            width: '100%',
                            padding: '8px 12px',
                            backgroundColor: '#1a1a1a',
                            border: '1px solid #2a2a2a',
                            borderRadius: '6px',
                            color: '#e7e7e7',
                            fontSize: '14px',
                            outline: 'none',
                            cursor: 'pointer'
                          }}
                        >
                          <option value="agentid.pub">agentid.pub</option>
                          <option value="agencp.io">agencp.io</option>
                        </select>
                        <p style={{ fontSize: '12px', color: '#666666', marginTop: '4px' }}>选择 ACP 网络接入点</p>
                      </div>
                      <div>
                        <label style={labelStyle}>Agent 名称</label>
                        <input
                          type="text"
                          value={localSettings.acpAgentName}
                          onChange={(e) => updateSetting('acpAgentName', e.target.value)}
                          placeholder="myagent"
                          style={inputStyle}
                        />
                        <p style={{ fontSize: '12px', color: '#666666', marginTop: '4px' }}>用于创建新的 Agent 身份</p>
                      </div>
                      <div>
                        <label style={labelStyle}>已有 AID (可选)</label>
                        <input
                          type="text"
                          value={localSettings.acpAid}
                          onChange={(e) => updateSetting('acpAid', e.target.value)}
                          placeholder="myagent.agentunion.cn"
                          style={inputStyle}
                        />
                        <p style={{ fontSize: '12px', color: '#666666', marginTop: '4px' }}>如果已有 AID，填写此项将直接加载</p>
                      </div>
                    </div>
                  </div>

                  <div style={{ padding: '16px', backgroundColor: '#141414', borderRadius: '8px' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '16px' }}>
                      <span style={{ fontSize: '16px', fontWeight: 500, color: '#e7e7e7' }}>高级配置</span>
                    </div>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                      <div>
                        <label style={labelStyle}>数据存储路径 (可选)</label>
                        <input
                          type="text"
                          value={localSettings.acpDataPath}
                          onChange={(e) => updateSetting('acpDataPath', e.target.value)}
                          placeholder="留空使用默认路径"
                          style={inputStyle}
                        />
                      </div>
                      <div>
                        <label style={labelStyle}>加密种子密码</label>
                        <input
                          type="password"
                          value={localSettings.acpSeedPassword}
                          onChange={(e) => updateSetting('acpSeedPassword', e.target.value)}
                          placeholder="用于私钥加密"
                          style={inputStyle}
                        />
                      </div>
                      <div style={{ ...cardStyle, backgroundColor: '#1a1a1a' }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                          <span style={{ fontSize: '14px', color: '#e7e7e7' }}>调试模式</span>
                        </div>
                        {renderToggle(localSettings.acpDebug, (v) => updateSetting('acpDebug', v))}
                      </div>
                    </div>
                  </div>

                  <div style={{ padding: '12px', backgroundColor: 'rgba(212, 154, 46, 0.1)', borderRadius: '8px', border: '1px solid rgba(212, 154, 46, 0.2)' }}>
                    <p style={{ fontSize: '12px', color: '#d49a2e', margin: 0, marginBottom: '8px' }}>
                      💡 ACP (智能体通信协议) 说明：
                    </p>
                    <p style={{ fontSize: '12px', color: '#888888', margin: 0, lineHeight: '1.6' }}>
                      ACP 是一个开放协议，用于解决 Agent 互相通信协作的问题。启用后，您的 Agent 可以与其他 Agent 进行安全通信。
                      访问 <a href="https://agentunion.cn" target="_blank" rel="noopener noreferrer" style={{ color: '#d49a2e' }}>agentunion.cn</a> 了解更多。
                    </p>
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'websearch' && (
              <div>
                <h2 style={{ fontSize: '20px', fontWeight: 600, color: '#d49a2e', marginBottom: '24px' }}>联网搜索</h2>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                  <div style={{ padding: '16px', backgroundColor: '#141414', borderRadius: '8px' }}>
                    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px' }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                        <Search style={{ width: '24px', height: '24px', color: '#d49a2e' }} />
                        <span style={{ fontSize: '16px', fontWeight: 500, color: '#e7e7e7' }}>密塔AI搜索</span>
                      </div>
                      <div style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: '6px',
                        padding: '4px 10px',
                        borderRadius: '12px',
                        backgroundColor: localSettings.metasoApiKey ? 'rgba(34, 197, 94, 0.2)' : 'rgba(239, 68, 68, 0.2)',
                        fontSize: '12px',
                        color: localSettings.metasoApiKey ? '#22c55e' : '#ef4444'
                      }}>
                        <div style={{
                          width: '6px',
                          height: '6px',
                          borderRadius: '50%',
                          backgroundColor: localSettings.metasoApiKey ? '#22c55e' : '#ef4444'
                        }} />
                        {localSettings.metasoApiKey ? '已启用' : '未启用'}
                      </div>
                    </div>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                      <div>
                        <label style={labelStyle}>API 密钥</label>
                        <input
                          type="password"
                          value={localSettings.metasoApiKey}
                          onChange={(e) => updateSetting('metasoApiKey', e.target.value)}
                          placeholder="输入密塔AI搜索 API 密钥"
                          style={inputStyle}
                        />
                      </div>
                      <div style={{ fontSize: '12px', color: '#666666', marginTop: '8px' }}>
                        <p style={{ marginBottom: '4px' }}>获取方式：</p>
                        <p>1. 访问 <a href="https://metaso.cn/search-api/api-keys" target="_blank" rel="noopener noreferrer" style={{ color: '#d49a2e' }}>密塔AI搜索API管理页</a></p>
                        <p>2. 登录后创建并复制 API 密钥</p>
                        <p>3. 将密钥粘贴到上方输入框中</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'skill' && (
              <div>
                <h2 style={{ fontSize: '20px', fontWeight: 600, color: '#d49a2e', marginBottom: '24px' }}>SKILL 配置</h2>
                <div style={cardStyle}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                    <Zap style={{ width: '20px', height: '20px', color: '#d49a2e' }} />
                    <div>
                      <div style={{ fontSize: '14px', fontWeight: 500, color: '#e7e7e7' }}>启用 SKILL</div>
                      <div style={{ fontSize: '12px', color: '#888888' }}>启用自定义技能功能</div>
                    </div>
                  </div>
                  {renderToggle(localSettings.enableSkill, (v) => updateSetting('enableSkill', v))}
                </div>
              </div>
            )}

            {activeTab === 'mcp' && (
              <div>
                <h2 style={{ fontSize: '20px', fontWeight: 600, color: '#d49a2e', marginBottom: '24px' }}>MCP 配置</h2>
                <div style={cardStyle}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                    <Cpu style={{ width: '20px', height: '20px', color: '#d49a2e' }} />
                    <div>
                      <div style={{ fontSize: '14px', fontWeight: 500, color: '#e7e7e7' }}>启用 MCP</div>
                      <div style={{ fontSize: '12px', color: '#888888' }}>启用模型上下文协议</div>
                    </div>
                  </div>
                  {renderToggle(localSettings.enableMCP, (v) => updateSetting('enableMCP', v))}
                </div>
              </div>
            )}

            {activeTab === 'knowledge' && (
              <div>
                <h2 style={{ fontSize: '20px', fontWeight: 600, color: '#d49a2e', marginBottom: '24px' }}>知识库</h2>
                <div style={cardStyle}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                    <Database style={{ width: '20px', height: '20px', color: '#d49a2e' }} />
                    <div>
                      <div style={{ fontSize: '14px', fontWeight: 500, color: '#e7e7e7' }}>启用知识库</div>
                      <div style={{ fontSize: '12px', color: '#888888' }}>允许 Agent 访问知识库</div>
                    </div>
                  </div>
                  {renderToggle(localSettings.enableKnowledgeBase, (v) => updateSetting('enableKnowledgeBase', v))}
                </div>
              </div>
            )}

            {activeTab === 'memory' && (
              <div>
                <h2 style={{ fontSize: '20px', fontWeight: 600, color: '#d49a2e', marginBottom: '24px' }}>记忆与偏好</h2>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                  <div style={{ padding: '16px', backgroundColor: '#141414', borderRadius: '8px' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '12px' }}>
                      <UserCircle style={{ width: '20px', height: '20px', color: '#d49a2e' }} />
                      <span style={{ fontSize: '16px', fontWeight: 500, color: '#e7e7e7' }}>用户自定义提示词</span>
                    </div>
                    <p style={{ fontSize: '12px', color: '#888888', marginBottom: '12px' }}>
                      设置你希望AI始终遵循的指令，例如回答风格、格式要求等。
                    </p>
                    <textarea
                      value={localSettings.userCustomPrompt}
                      onChange={(e) => updateSetting('userCustomPrompt', e.target.value)}
                      placeholder="例如：请用简洁的方式回答，每次回答都给出要点总结..."
                      style={{
                        ...inputStyle,
                        minHeight: '100px',
                        resize: 'vertical',
                        fontFamily: 'inherit'
                      }}
                    />
                  </div>
                  
                  <div style={{ padding: '16px', backgroundColor: '#141414', borderRadius: '8px' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '12px' }}>
                      <Brain style={{ width: '20px', height: '20px', color: '#d49a2e' }} />
                      <span style={{ fontSize: '16px', fontWeight: 500, color: '#e7e7e7' }}>用户偏好</span>
                    </div>
                    <p style={{ fontSize: '12px', color: '#888888', marginBottom: '12px' }}>
                      告诉AI你的个人偏好，例如语言、专业领域、兴趣爱好等。
                    </p>
                    <textarea
                      value={localSettings.userPreferences}
                      onChange={(e) => updateSetting('userPreferences', e.target.value)}
                      placeholder="例如：我是程序员，偏好使用Python，对AI和机器学习感兴趣..."
                      style={{
                        ...inputStyle,
                        minHeight: '100px',
                        resize: 'vertical',
                        fontFamily: 'inherit'
                      }}
                    />
                  </div>
                  
                  <div style={{ padding: '12px', backgroundColor: 'rgba(212, 154, 46, 0.1)', borderRadius: '8px', border: '1px solid rgba(212, 154, 46, 0.2)' }}>
                    <p style={{ fontSize: '12px', color: '#d49a2e', margin: 0 }}>
                      💡 提示：以上设置会在每次对话中自动添加到系统提示词中，AI会根据这些信息调整回答方式。
                    </p>
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'personality' && (
              <div>
                <h2 style={{ fontSize: '20px', fontWeight: 600, color: '#d49a2e', marginBottom: '24px' }}>人格文件</h2>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                  <div>
                    <label style={labelStyle}>人格名称</label>
                    <input
                      type="text"
                      value={localSettings.personalityFile}
                      onChange={(e) => updateSetting('personalityFile', e.target.value)}
                      placeholder="输入人格名称"
                      style={inputStyle}
                    />
                  </div>
                  <div>
                    <label style={labelStyle}>人格描述</label>
                    <textarea
                      value={localSettings.personalityContent}
                      onChange={(e) => updateSetting('personalityContent', e.target.value)}
                      placeholder="描述这个人格的特点、语气、行为方式..."
                      rows={8}
                      style={{ ...inputStyle, resize: 'none' }}
                    />
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'about' && (
              <div>
                <h2 style={{ fontSize: '20px', fontWeight: 600, color: '#d49a2e', marginBottom: '24px' }}>关于</h2>
                <div style={{ padding: '24px', backgroundColor: '#141414', borderRadius: '8px', textAlign: 'center' }}>
                  <div style={{
                    width: '64px',
                    height: '64px',
                    margin: '0 auto 16px',
                    borderRadius: '12px',
                    background: 'linear-gradient(135deg, #e5b24a 0%, #d49a2e 50%, #b87f24 100%)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center'
                  }}>
                    <Zap style={{ width: '32px', height: '32px', color: '#0a0a0a' }} />
                  </div>
                  <h3 style={{ fontSize: '18px', fontWeight: 600, marginBottom: '8px', color: '#e7e7e7' }}>AI Agent</h3>
                  <p style={{ fontSize: '14px', color: '#888888', marginBottom: '16px' }}>版本 1.0.0</p>
                  <p style={{ fontSize: '12px', color: '#666666' }}>
                    一个功能强大的 AI 助手，支持多种功能和自定义配置。
                  </p>
                </div>
                <div style={{ marginTop: '16px' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '14px', padding: '8px 0', borderBottom: '1px solid #2a2a2a' }}>
                    <span style={{ color: '#888888' }}>开发者</span>
                    <span style={{ color: '#e7e7e7' }}>黎夏</span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '14px', padding: '8px 0', borderBottom: '1px solid #2a2a2a' }}>
                    <span style={{ color: '#888888' }}>许可证</span>
                    <span style={{ color: '#e7e7e7' }}>MIT</span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '14px', padding: '8px 0', borderBottom: '1px solid #2a2a2a' }}>
                    <span style={{ color: '#888888' }}>技术栈</span>
                    <span style={{ color: '#e7e7e7' }}>React + TypeScript + Python</span>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default SettingsPanel;
