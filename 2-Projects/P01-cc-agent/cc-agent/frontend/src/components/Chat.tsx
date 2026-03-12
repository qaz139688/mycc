import { useState, useRef, useEffect } from 'react';
import { Send, User, Bot, Sparkles } from 'lucide-react';
import { type Conversation, type Message } from '../services/api';

interface ChatProps {
  conversation: Conversation | null;
  onSendMessage: (content: string) => void;
  isLoading: boolean;
  streamingContent?: string;
}

const Chat: React.FC<ChatProps> = ({ conversation, onSendMessage, isLoading, streamingContent = '' }) => {
  const [input, setInput] = useState('');
  const [displayedTitle, setDisplayedTitle] = useState('');
  const [displayedSubtitle, setDisplayedSubtitle] = useState('');
  const [showCursor, setShowCursor] = useState(true);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const fullTitle = '今天有什么可以帮你的？';
  const fullSubtitle = '我是1052AI智能助手，很高兴为你服务。';

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [conversation?.messages, streamingContent]);

  useEffect(() => {
    if (!conversation || conversation?.messages?.length === 0) {
      setDisplayedTitle('');
      setDisplayedSubtitle('');
      
      const titleInterval = setInterval(() => {
        setDisplayedTitle(prev => {
          if (prev.length < fullTitle.length) {
            return fullTitle.slice(0, prev.length + 1);
          }
          clearInterval(titleInterval);
          return prev;
        });
      }, 80);

      const subtitleTimeout = setTimeout(() => {
        const subtitleInterval = setInterval(() => {
          setDisplayedSubtitle(prev => {
            if (prev.length < fullSubtitle.length) {
              return fullSubtitle.slice(0, prev.length + 1);
            }
            clearInterval(subtitleInterval);
            return prev;
          });
        }, 50);
      }, fullTitle.length * 80 + 200);

      const cursorTimeout = setTimeout(() => {
        setShowCursor(false);
      }, fullTitle.length * 80 + fullSubtitle.length * 50 + 500);

      return () => {
        clearInterval(titleInterval);
        clearTimeout(subtitleTimeout);
        clearTimeout(cursorTimeout);
      };
    }
  }, [conversation?.messages?.length]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (input.trim() && !isLoading) {
      onSendMessage(input.trim());
      setInput('');
      if (textareaRef.current) {
        textareaRef.current.style.height = 'auto';
      }
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInput(e.target.value);
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 200)}px`;
    }
  };

  const formatTime = (timestamp: number) => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString('zh-CN', { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  const quickPrompts = ['帮我写一段代码', '解释一个概念', '分析数据', '创意写作'];

  return (
    <div className="flex flex-col h-full bg-primary">
      <div className="flex-1 overflow-y-auto px-4 py-6">
        {!conversation || conversation?.messages?.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-center">
            <div className="w-20 h-20 mb-6 rounded-2xl bg-gradient-to-br from-gold-400 to-gold-600 flex items-center justify-center shadow-lg shadow-gold/20 icon-appear">
              <Sparkles className="w-10 h-10 text-dark-950" />
            </div>
            <h2 className="text-2xl font-bold text-gradient-gold mb-2 min-h-[2.5rem]">
              {displayedTitle}
              {showCursor && displayedTitle.length < fullTitle.length && (
                <span className="inline-block w-0.5 h-6 bg-gold ml-1 animate-pulse" />
              )}
            </h2>
            <p className="text-muted max-w-md min-h-[1.5rem]">
              {displayedSubtitle}
              {showCursor && displayedTitle.length === fullTitle.length && displayedSubtitle.length < fullSubtitle.length && (
                <span className="inline-block w-0.5 h-4 bg-gold ml-1 animate-pulse" />
              )}
            </p>
            
            <div className="mt-8 grid grid-cols-2 gap-3 max-w-lg">
              {quickPrompts.map((prompt, index) => (
                <button
                  key={index}
                  onClick={() => {
                    setInput(prompt);
                    textareaRef.current?.focus();
                  }}
                  className="petal-bloom px-4 py-3 bg-secondary hover:bg-tertiary border border-dark hover:border-gold/30 rounded-lg text-sm text-gray-300 transition-all text-left hover:scale-105 hover:shadow-lg hover:shadow-gold/10"
                  style={{ animationDelay: `${0.3 + index * 0.1}s` }}
                >
                  {prompt}
                </button>
              ))}
            </div>
          </div>
        ) : (
          <div className="max-w-4xl mx-auto space-y-6">
            {conversation.messages.map((message: Message, index: number) => (
              <div
                key={index}
                className={`flex gap-4 ${
                  message.role === 'user' ? 'flex-row-reverse' : ''
                }`}
              >
                <div
                  className={`w-10 h-10 rounded-full flex-shrink-0 flex items-center justify-center ${
                    message.role === 'user'
                      ? 'bg-gold text-dark-950'
                      : 'bg-gradient-to-br from-gold-400 to-gold-600 text-dark-950'
                  }`}
                >
                  {message.role === 'user' ? (
                    <User className="w-5 h-5" />
                  ) : (
                    <Bot className="w-5 h-5" />
                  )}
                </div>

                <div className={`flex-1 ${message.role === 'user' ? 'flex flex-col items-end' : ''}`}>
                  <div
                    className={`inline-block px-4 py-3 rounded-2xl max-w-[85%] ${
                      message.role === 'user'
                        ? 'bg-gold text-dark-950 rounded-tr-sm'
                        : 'bg-secondary text-gray-200 rounded-tl-sm border border-dark'
                    }`}
                  >
                    <p className="whitespace-pre-wrap leading-relaxed text-left">
                      {message.content}
                    </p>
                  </div>
                  <div className={`mt-1 text-xs text-muted ${message.role === 'user' ? 'text-right' : ''}`}>
                    {formatTime(message.timestamp)}
                  </div>
                </div>
              </div>
            ))}
            
            {(isLoading || streamingContent) && (
              <div className="flex gap-4">
                <div className="w-10 h-10 rounded-full bg-gradient-to-br from-gold-400 to-gold-600 flex-shrink-0 flex items-center justify-center">
                  <Bot className="w-5 h-5 text-dark-950" />
                </div>
                <div className="flex-1">
                  <div className="inline-block px-4 py-3 rounded-2xl bg-secondary text-gray-200 rounded-tl-sm border border-dark max-w-[85%]">
                    {streamingContent ? (
                      <p className="whitespace-pre-wrap leading-relaxed">{streamingContent}</p>
                    ) : (
                      <div className="flex gap-1">
                        <span className="w-2 h-2 bg-gold rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                        <span className="w-2 h-2 bg-gold rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                        <span className="w-2 h-2 bg-gold rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                      </div>
                    )}
                  </div>
                </div>
              </div>
            )}
            
            <div ref={messagesEndRef} />
          </div>
        )}
      </div>

      <div className="border-t border-dark bg-secondary px-4 py-4">
        <div className="max-w-4xl mx-auto">
          <form onSubmit={handleSubmit} className="relative">
            <textarea
              ref={textareaRef}
              value={input}
              onChange={handleInputChange}
              onKeyDown={handleKeyDown}
              placeholder="输入消息... (Shift + Enter 换行)"
              rows={1}
              className="w-full pr-14 py-3.5 pl-4 bg-tertiary border border-dark rounded-xl resize-none overflow-hidden focus:border-gold focus:ring-1 focus:ring-gold/30 transition-all"
              style={{ minHeight: '52px', maxHeight: '200px' }}
            />
            <button
              type="submit"
              disabled={!input.trim() || isLoading}
              className="absolute right-2 bottom-2 p-2 bg-gold text-dark-950 rounded-lg hover:bg-gold-light disabled:opacity-50 disabled:cursor-not-allowed transition-all"
            >
              <Send className="w-5 h-5" />
            </button>
          </form>
          <div className="mt-2 text-center text-xs text-muted">
            AI 生成的内容可能存在错误，请仔细核对重要信息。
          </div>
        </div>
      </div>
    </div>
  );
};

export default Chat;
