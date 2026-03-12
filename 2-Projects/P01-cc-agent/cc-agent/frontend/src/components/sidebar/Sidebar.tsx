import React from 'react';
import { 
  MessageSquare, 
  Settings, 
  ChevronLeft, 
  ChevronRight,
  Trash2
} from 'lucide-react';

interface SidebarProps {
  isCollapsed: boolean;
  onToggle: () => void;
  onOpenSettings: () => void;
  onClearConversation: () => void;
}

const Sidebar: React.FC<SidebarProps> = ({
  isCollapsed,
  onToggle,
  onOpenSettings,
  onClearConversation,
}) => {
  return (
    <div
      className={`h-full bg-secondary border-r border-dark flex flex-col transition-all duration-300 ${
        isCollapsed ? 'w-16' : 'w-64'
      }`}
    >
      <div className="h-14 flex items-center justify-between px-4 border-b border-dark">
        {!isCollapsed && (
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-gold-400 to-gold-600 flex items-center justify-center">
              <MessageSquare className="w-5 h-5 text-dark-950" />
            </div>
            <span className="text-gold font-semibold text-lg">1052 Agent</span>
          </div>
        )}
        {isCollapsed && (
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-gold-400 to-gold-600 flex items-center justify-center mx-auto">
            <MessageSquare className="w-5 h-5 text-dark-950" />
          </div>
        )}
      </div>

      <div className="flex-1 flex flex-col justify-end">
        <div className="p-3">
          <button
            onClick={onClearConversation}
            className={`w-full flex items-center gap-3 p-2.5 rounded-lg hover:bg-red-500/10 transition-all text-gray-400 hover:text-red-400 ${
              isCollapsed ? 'justify-center' : ''
            }`}
            title="清除对话"
          >
            <Trash2 className="w-5 h-5" />
            {!isCollapsed && <span className="text-sm font-medium">清除对话</span>}
          </button>
        </div>
      </div>

      <div className="p-3 border-t border-dark">
        <button
          onClick={onOpenSettings}
          className={`w-full flex items-center gap-3 p-2.5 rounded-lg hover:bg-tertiary transition-all text-gray-400 hover:text-gold ${
            isCollapsed ? 'justify-center' : ''
          }`}
        >
          <Settings className="w-5 h-5" />
          {!isCollapsed && <span className="text-sm font-medium">设置</span>}
        </button>
      </div>

      <button
        onClick={onToggle}
        className="absolute -right-3 top-20 w-6 h-6 bg-card border border-gold/30 rounded-full flex items-center justify-center text-gold hover:bg-gold hover:text-dark-950 transition-all shadow-lg"
      >
        {isCollapsed ? (
          <ChevronRight className="w-4 h-4" />
        ) : (
          <ChevronLeft className="w-4 h-4" />
        )}
      </button>
    </div>
  );
};

export default Sidebar;
