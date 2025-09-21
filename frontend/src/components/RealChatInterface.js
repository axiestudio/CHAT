import React, { useState, useEffect, useRef } from 'react';
import { toast } from 'react-hot-toast';
import { 
  Send, 
  Download, 
  Loader2, 
  MessageCircle,
  Bot,
  User,
  Trash2,
  Zap
} from 'lucide-react';
import { chatAPI } from '../services/api';

const RealChatInterface = () => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [generatedFlow, setGeneratedFlow] = useState(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Load chat history on component mount
  useEffect(() => {
    loadChatHistory();
  }, []);

  const loadChatHistory = async () => {
    try {
      const response = await chatAPI.getHistory();
      if (response.success && response.history) {
        const formattedMessages = response.history.map(msg => ({
          id: Date.now() + Math.random(),
          role: msg.role,
          content: msg.content,
          timestamp: msg.timestamp,
          flow: msg.flow_data || null
        }));
        setMessages(formattedMessages);
      }
    } catch (error) {
      console.error('Failed to load chat history:', error);
    }
  };

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return;

    const userMessage = {
      id: Date.now(),
      role: 'user',
      content: inputMessage.trim(),
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      const response = await chatAPI.sendMessage(userMessage.content);
      
      if (response.success) {
        const assistantMessage = {
          id: Date.now() + 1,
          role: 'assistant',
          content: response.message,
          timestamp: new Date().toISOString(),
          flow: response.flow,
          intent: response.intent
        };

        setMessages(prev => [...prev, assistantMessage]);

        // If a flow was generated, store it
        if (response.flow) {
          setGeneratedFlow(response.flow);
          toast.success('Flow generated! You can download it below.');
        }
      } else {
        throw new Error(response.message || 'Chat failed');
      }
    } catch (error) {
      console.error('Chat error:', error);
      toast.error(error.response?.data?.detail || error.message || 'Failed to send message');
      
      // Add error message
      const errorMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date().toISOString(),
        isError: true
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const clearChat = async () => {
    try {
      await chatAPI.clearHistory();
      setMessages([]);
      setGeneratedFlow(null);
      toast.success('Chat cleared successfully!');
    } catch (error) {
      console.error('Failed to clear chat:', error);
      toast.error('Failed to clear chat');
    }
  };

  const downloadFlow = () => {
    if (!generatedFlow) return;

    const dataStr = JSON.stringify(generatedFlow, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    
    const link = document.createElement('a');
    link.href = url;
    link.download = `axiestudio_flow_${Date.now()}.json`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
    
    toast.success('Flow downloaded successfully!');
  };

  const MessageBubble = ({ message }) => {
    const isUser = message.role === 'user';
    const isError = message.isError;

    return (
      <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}>
        <div className={`flex max-w-xs lg:max-w-md ${isUser ? 'flex-row-reverse' : 'flex-row'} items-start space-x-2`}>
          {/* Avatar */}
          <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
            isUser 
              ? 'bg-blue-500 text-white' 
              : isError 
                ? 'bg-red-500 text-white'
                : 'bg-gradient-to-r from-purple-500 to-blue-500 text-white'
          }`}>
            {isUser ? <User size={16} /> : <Bot size={16} />}
          </div>

          {/* Message */}
          <div className={`px-4 py-2 rounded-lg ${
            isUser 
              ? 'bg-blue-500 text-white' 
              : isError
                ? 'bg-red-100 text-red-800 border border-red-200'
                : 'bg-white text-gray-800 border border-gray-200 shadow-sm'
          }`}>
            <p className="text-sm whitespace-pre-wrap">{message.content}</p>
            
            {/* Flow indicator */}
            {message.flow && (
              <div className="mt-2 p-2 bg-green-50 border border-green-200 rounded text-xs text-green-700">
                <Zap size={12} className="inline mr-1" />
                Flow generated: {message.flow.name || 'Untitled Flow'}
              </div>
            )}
            
            {/* Timestamp */}
            <div className={`text-xs mt-1 ${isUser ? 'text-blue-100' : 'text-gray-500'}`}>
              {new Date(message.timestamp).toLocaleTimeString()}
            </div>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="max-w-4xl mx-auto h-screen flex flex-col">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 p-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-gradient-to-r from-purple-500 to-blue-500 rounded-full flex items-center justify-center">
              <MessageCircle className="text-white" size={20} />
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-900">Real AxieStudio AI Chat</h1>
              <p className="text-sm text-gray-600">Chat with AI to create authentic AxieStudio flows</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-2">
            {generatedFlow && (
              <button
                onClick={downloadFlow}
                className="flex items-center space-x-2 px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors"
              >
                <Download size={16} />
                <span>Download Flow</span>
              </button>
            )}
            
            <button
              onClick={clearChat}
              className="flex items-center space-x-2 px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors"
            >
              <Trash2 size={16} />
              <span>Clear Chat</span>
            </button>
          </div>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 bg-gray-50">
        {messages.length === 0 ? (
          <div className="text-center py-12">
            <Bot size={48} className="mx-auto text-gray-400 mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">Start a conversation</h3>
            <p className="text-gray-600 mb-4">Ask me to create any AxieStudio flow using natural language!</p>
            <div className="text-sm text-gray-500 space-y-1">
              <p>Try: "Create a chatbot that can answer questions about PDF documents"</p>
              <p>Or: "Build a research agent that can search the web"</p>
            </div>
          </div>
        ) : (
          <>
            {messages.map((message) => (
              <MessageBubble key={message.id} message={message} />
            ))}
            {isLoading && (
              <div className="flex justify-start mb-4">
                <div className="flex items-center space-x-2">
                  <div className="w-8 h-8 bg-gradient-to-r from-purple-500 to-blue-500 rounded-full flex items-center justify-center">
                    <Bot size={16} className="text-white" />
                  </div>
                  <div className="bg-white border border-gray-200 rounded-lg px-4 py-2">
                    <Loader2 size={16} className="animate-spin text-gray-500" />
                  </div>
                </div>
              </div>
            )}
          </>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="bg-white border-t border-gray-200 p-4">
        <div className="flex items-center space-x-4">
          <div className="flex-1">
            <textarea
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Describe the AxieStudio flow you want to create..."
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
              rows="2"
              disabled={isLoading}
            />
          </div>
          <button
            onClick={handleSendMessage}
            disabled={!inputMessage.trim() || isLoading}
            className="flex items-center justify-center w-12 h-12 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {isLoading ? (
              <Loader2 size={20} className="animate-spin" />
            ) : (
              <Send size={20} />
            )}
          </button>
        </div>
      </div>
    </div>
  );
};

export default RealChatInterface;
