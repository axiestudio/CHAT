import React, { useState, useEffect } from 'react';
import { toast } from 'react-hot-toast';
import {
  Sparkles,
  Download,
  Loader2,
  CheckCircle,
  AlertCircle,
  Cpu,
  Network,
  Clock,
  Zap,
  Brain,
  Rocket,
  Star,
  ArrowRight,
  Copy,
  ExternalLink
} from 'lucide-react';
import { flowAPI, healthCheck } from '../services/api';

const FlowGenerator = () => {
  const [description, setDescription] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedFlow, setGeneratedFlow] = useState(null);
  const [apiStatus, setApiStatus] = useState(null);

  // Check API status on component mount
  useEffect(() => {
    checkApiStatus();
  }, []);

  const checkApiStatus = async () => {
    try {
      const status = await healthCheck();
      setApiStatus(status);
    } catch (error) {
      console.error('API health check failed:', error);
      setApiStatus({ status: 'unhealthy' });
    }
  };

  const handleGenerate = async () => {
    if (!description.trim()) {
      toast.error('Please enter a description for your flow');
      return;
    }

    if (!apiStatus?.openai_configured) {
      toast.error('OpenAI API key not configured on the backend');
      return;
    }

    setIsGenerating(true);
    setGeneratedFlow(null);

    try {
      const result = await flowAPI.generateFlow({
        description: description.trim(),
        use_ai: true,
        model: 'gpt-4'
      });

      if (result.success) {
        setGeneratedFlow(result);
        toast.success('Flow generated successfully!');
      } else {
        throw new Error(result.error || 'Generation failed');
      }
    } catch (error) {
      console.error('Generation error:', error);
      toast.error(error.response?.data?.detail || error.message || 'Failed to generate flow');
    } finally {
      setIsGenerating(false);
    }
  };

  const handleDownload = () => {
    if (!generatedFlow) return;

    const dataStr = JSON.stringify(generatedFlow.flow_data, null, 2);
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

  return (
    <div className="max-w-6xl mx-auto space-y-12">
      {/* Hero Section */}
      <div className="text-center space-y-8">
        <div className="space-y-4">
          <div className="inline-flex items-center space-x-2 bg-gradient-to-r from-blue-100 to-purple-100 px-4 py-2 rounded-full text-sm font-medium text-blue-800 border border-blue-200">
            <Star className="h-4 w-4" />
            <span>Production-Ready AI Flow Generator</span>
          </div>

          <h1 className="text-5xl md:text-6xl font-bold bg-gradient-to-r from-gray-900 via-blue-800 to-purple-800 bg-clip-text text-transparent leading-tight">
            Generate AxieStudio Flows
            <br />
            <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              with AI Magic ✨
            </span>
          </h1>

          <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
            Transform your ideas into production-ready AxieStudio flows using natural language.
            Our AI understands your requirements and creates complete, importable workflows in seconds.
          </p>
        </div>

        {/* Feature Pills */}
        <div className="flex flex-wrap justify-center gap-3">
          <div className="flex items-center space-x-2 bg-white/60 backdrop-blur-sm px-4 py-2 rounded-full text-sm font-medium text-gray-700 border border-gray-200 shadow-sm">
            <Brain className="h-4 w-4 text-blue-600" />
            <span>GPT-4 Powered</span>
          </div>
          <div className="flex items-center space-x-2 bg-white/60 backdrop-blur-sm px-4 py-2 rounded-full text-sm font-medium text-gray-700 border border-gray-200 shadow-sm">
            <Rocket className="h-4 w-4 text-purple-600" />
            <span>Production Ready</span>
          </div>
          <div className="flex items-center space-x-2 bg-white/60 backdrop-blur-sm px-4 py-2 rounded-full text-sm font-medium text-gray-700 border border-gray-200 shadow-sm">
            <Zap className="h-4 w-4 text-yellow-600" />
            <span>Instant Generation</span>
          </div>
        </div>
      </div>

      {/* API Status */}
      {apiStatus && (
        <div className={`relative overflow-hidden rounded-2xl border backdrop-blur-sm ${
          apiStatus.status === 'healthy'
            ? 'bg-gradient-to-r from-green-50/80 to-emerald-50/80 border-green-200/50 shadow-lg shadow-green-500/10'
            : 'bg-gradient-to-r from-red-50/80 to-rose-50/80 border-red-200/50 shadow-lg shadow-red-500/10'
        }`}>
          <div className="p-6">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                {apiStatus.status === 'healthy' ? (
                  <div className="p-2 bg-green-100 rounded-xl">
                    <CheckCircle className="h-6 w-6 text-green-600" />
                  </div>
                ) : (
                  <div className="p-2 bg-red-100 rounded-xl">
                    <AlertCircle className="h-6 w-6 text-red-600" />
                  </div>
                )}
                <div>
                  <span className={`text-lg font-semibold ${
                    apiStatus.status === 'healthy' ? 'text-green-800' : 'text-red-800'
                  }`}>
                    Backend Status: {apiStatus.status === 'healthy' ? 'Connected' : 'Disconnected'}
                  </span>
                  <div className="flex items-center space-x-4 mt-1">
                    <span className={`text-sm font-medium ${
                      apiStatus.openai_configured ? 'text-green-700' : 'text-red-700'
                    }`}>
                      OpenAI: {apiStatus.openai_configured ? '✅ Configured' : '❌ Not configured'}
                    </span>
                    {apiStatus.status === 'healthy' && (
                      <span className="text-sm text-green-600 font-medium">
                        🚀 Ready to generate flows
                      </span>
                    )}
                  </div>
                </div>
              </div>

              {apiStatus.status === 'healthy' && (
                <div className="flex items-center space-x-2 text-green-600">
                  <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                  <span className="text-sm font-medium">Live</span>
                </div>
              )}
            </div>
          </div>

          {/* Animated background */}
          <div className={`absolute inset-0 opacity-20 ${
            apiStatus.status === 'healthy' ? 'bg-gradient-to-r from-green-400 to-emerald-400' : 'bg-gradient-to-r from-red-400 to-rose-400'
          }`}></div>
        </div>
      )}

      {/* Input Section */}
      <div className="relative">
        <div className="bg-white/80 backdrop-blur-xl rounded-3xl shadow-2xl border border-white/20 p-8 relative overflow-hidden">
          {/* Background decoration */}
          <div className="absolute top-0 right-0 w-32 h-32 bg-gradient-to-br from-blue-400/10 to-purple-600/10 rounded-full blur-2xl"></div>
          <div className="absolute bottom-0 left-0 w-24 h-24 bg-gradient-to-br from-indigo-400/10 to-pink-600/10 rounded-full blur-2xl"></div>

          <div className="relative z-10">
            <div className="mb-6">
              <label htmlFor="description" className="block text-lg font-semibold text-gray-800 mb-3">
                ✨ Describe your flow
              </label>
              <p className="text-sm text-gray-600 mb-4">
                Be specific about what you want to build. The more details you provide, the better your flow will be!
              </p>
            </div>

            <div className="relative">
              <textarea
                id="description"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="Example: Create a chatbot that answers questions about PDF documents using RAG with OpenAI embeddings and Pinecone vector store"
                className="w-full h-40 px-6 py-4 bg-gray-50/50 border-2 border-gray-200 rounded-2xl focus:outline-none focus:ring-4 focus:ring-blue-500/20 focus:border-blue-500 resize-none text-gray-800 placeholder-gray-500 text-lg leading-relaxed transition-all duration-200"
                disabled={isGenerating}
                maxLength={500}
              />

              {/* Character count */}
              <div className="absolute bottom-4 right-4 text-sm text-gray-400 bg-white/80 px-2 py-1 rounded-lg">
                {description.length}/500
              </div>
            </div>

            <div className="mt-8 flex flex-col sm:flex-row justify-between items-center gap-4">
              {/* Example suggestions */}
              <div className="flex flex-wrap gap-2">
                <button
                  onClick={() => setDescription("Create a chatbot that answers questions about PDF documents using RAG")}
                  className="text-xs px-3 py-1 bg-blue-100 text-blue-700 rounded-full hover:bg-blue-200 transition-colors"
                  disabled={isGenerating}
                >
                  📄 PDF Q&A Bot
                </button>
                <button
                  onClick={() => setDescription("Build a sentiment analysis pipeline for social media posts")}
                  className="text-xs px-3 py-1 bg-purple-100 text-purple-700 rounded-full hover:bg-purple-200 transition-colors"
                  disabled={isGenerating}
                >
                  😊 Sentiment Analysis
                </button>
                <button
                  onClick={() => setDescription("Create a web scraper that extracts data and stores it in a database")}
                  className="text-xs px-3 py-1 bg-green-100 text-green-700 rounded-full hover:bg-green-200 transition-colors"
                  disabled={isGenerating}
                >
                  🕷️ Web Scraper
                </button>
              </div>

              {/* Generate button */}
              <button
                onClick={handleGenerate}
                disabled={isGenerating || !description.trim() || !apiStatus?.openai_configured}
                className="group relative px-8 py-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-2xl hover:from-blue-700 hover:to-purple-700 focus:outline-none focus:ring-4 focus:ring-blue-500/20 disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-3 font-semibold text-lg shadow-xl shadow-blue-500/25 transition-all duration-200 transform hover:scale-105 disabled:hover:scale-100"
              >
                {isGenerating ? (
                  <>
                    <Loader2 className="h-6 w-6 animate-spin" />
                    <span>Generating Magic...</span>
                  </>
                ) : (
                  <>
                    <Sparkles className="h-6 w-6" />
                    <span>Generate Flow</span>
                    <ArrowRight className="h-5 w-5 group-hover:translate-x-1 transition-transform" />
                  </>
                )}

                {/* Button glow effect */}
                <div className="absolute inset-0 bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl blur opacity-30 group-hover:opacity-50 transition-opacity -z-10"></div>
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Results Section */}
      {generatedFlow && (
        <div className="relative">
          {/* Success animation */}
          <div className="absolute -top-4 left-1/2 transform -translate-x-1/2 z-20">
            <div className="bg-gradient-to-r from-green-500 to-emerald-500 text-white px-6 py-2 rounded-full text-sm font-semibold shadow-lg animate-bounce">
              🎉 Flow Generated Successfully!
            </div>
          </div>

          <div className="bg-white/90 backdrop-blur-xl rounded-3xl shadow-2xl border border-white/20 p-8 relative overflow-hidden mt-8">
            {/* Background decoration */}
            <div className="absolute top-0 right-0 w-40 h-40 bg-gradient-to-br from-green-400/10 to-blue-600/10 rounded-full blur-3xl"></div>
            <div className="absolute bottom-0 left-0 w-32 h-32 bg-gradient-to-br from-purple-400/10 to-pink-600/10 rounded-full blur-3xl"></div>

            <div className="relative z-10">
              <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between mb-8 gap-4">
                <div>
                  <h2 className="text-3xl font-bold bg-gradient-to-r from-gray-900 to-gray-700 bg-clip-text text-transparent mb-2">
                    🚀 Your Flow is Ready!
                  </h2>
                  <p className="text-gray-600">
                    Production-ready AxieStudio flow generated with AI precision
                  </p>
                </div>

                <div className="flex items-center space-x-3">
                  <button
                    onClick={() => {
                      navigator.clipboard.writeText(JSON.stringify(generatedFlow.flow_data, null, 2));
                      toast.success('Flow JSON copied to clipboard!');
                    }}
                    className="px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-xl transition-colors flex items-center space-x-2 font-medium"
                  >
                    <Copy className="h-4 w-4" />
                    <span>Copy JSON</span>
                  </button>

                  <button
                    onClick={handleDownload}
                    className="group px-6 py-3 bg-gradient-to-r from-green-600 to-emerald-600 text-white rounded-xl hover:from-green-700 hover:to-emerald-700 focus:outline-none focus:ring-4 focus:ring-green-500/20 flex items-center space-x-2 font-semibold shadow-lg shadow-green-500/25 transition-all duration-200 transform hover:scale-105"
                  >
                    <Download className="h-5 w-5" />
                    <span>Download JSON</span>
                    <ExternalLink className="h-4 w-4 group-hover:translate-x-1 transition-transform" />
                  </button>
                </div>
              </div>

              {/* Flow Stats */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                <div className="bg-gradient-to-br from-blue-50 to-blue-100/50 p-6 rounded-2xl border border-blue-200/50 relative overflow-hidden">
                  <div className="absolute top-0 right-0 w-16 h-16 bg-blue-400/10 rounded-full blur-xl"></div>
                  <div className="relative z-10">
                    <div className="flex items-center space-x-3 mb-3">
                      <div className="p-2 bg-blue-500 rounded-xl">
                        <Cpu className="h-6 w-6 text-white" />
                      </div>
                      <span className="font-semibold text-blue-900">Components</span>
                    </div>
                    <div className="text-3xl font-bold text-blue-600">
                      {generatedFlow.components?.length || 0}
                    </div>
                    <div className="text-sm text-blue-700 mt-1">
                      AI-selected modules
                    </div>
                  </div>
                </div>

                <div className="bg-gradient-to-br from-green-50 to-green-100/50 p-6 rounded-2xl border border-green-200/50 relative overflow-hidden">
                  <div className="absolute top-0 right-0 w-16 h-16 bg-green-400/10 rounded-full blur-xl"></div>
                  <div className="relative z-10">
                    <div className="flex items-center space-x-3 mb-3">
                      <div className="p-2 bg-green-500 rounded-xl">
                        <Network className="h-6 w-6 text-white" />
                      </div>
                      <span className="font-semibold text-green-900">Connections</span>
                    </div>
                    <div className="text-3xl font-bold text-green-600">
                      {generatedFlow.flow_data?.data?.edges?.length || 0}
                    </div>
                    <div className="text-sm text-green-700 mt-1">
                      Smart connections
                    </div>
                  </div>
                </div>

                <div className="bg-gradient-to-br from-purple-50 to-purple-100/50 p-6 rounded-2xl border border-purple-200/50 relative overflow-hidden">
                  <div className="absolute top-0 right-0 w-16 h-16 bg-purple-400/10 rounded-full blur-xl"></div>
                  <div className="relative z-10">
                    <div className="flex items-center space-x-3 mb-3">
                      <div className="p-2 bg-purple-500 rounded-xl">
                        <Clock className="h-6 w-6 text-white" />
                      </div>
                      <span className="font-semibold text-purple-900">Generation Time</span>
                    </div>
                    <div className="text-3xl font-bold text-purple-600">
                      {generatedFlow.generation_time?.toFixed(2)}s
                    </div>
                    <div className="text-sm text-purple-700 mt-1">
                      Lightning fast
                    </div>
                  </div>
                </div>
              </div>

              {/* Components List */}
              {generatedFlow.components && generatedFlow.components.length > 0 && (
                <div className="mb-8">
                  <h3 className="text-2xl font-bold text-gray-900 mb-6 flex items-center space-x-2">
                    <span>🧩 Components Used</span>
                  </h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {generatedFlow.components.map((component, index) => (
                      <div key={index} className="bg-gradient-to-r from-gray-50 to-gray-100/50 p-5 rounded-2xl border border-gray-200/50 hover:shadow-lg transition-all duration-200 group">
                        <div className="flex items-start space-x-3">
                          <div className="p-2 bg-blue-500 rounded-lg group-hover:bg-blue-600 transition-colors">
                            <Cpu className="h-4 w-4 text-white" />
                          </div>
                          <div className="flex-1">
                            <div className="font-semibold text-gray-900 mb-1">{component.display_name}</div>
                            <div className="text-sm text-gray-600 leading-relaxed">{component.description}</div>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Success Message */}
              <div className="bg-gradient-to-r from-green-50 to-emerald-50 border-2 border-green-200/50 rounded-2xl p-6 relative overflow-hidden">
                <div className="absolute top-0 right-0 w-24 h-24 bg-green-400/10 rounded-full blur-2xl"></div>
                <div className="relative z-10">
                  <div className="flex items-center space-x-3 mb-3">
                    <div className="p-2 bg-green-500 rounded-xl">
                      <CheckCircle className="h-6 w-6 text-white" />
                    </div>
                    <span className="text-xl font-bold text-green-800">Ready for AxieStudio! 🎉</span>
                  </div>
                  <p className="text-green-700 leading-relaxed">
                    Your flow has been generated using real AxieStudio templates and is ready to import
                    into your production AxieStudio application. Simply download the JSON file and import
                    it directly into AxieStudio to start building amazing AI workflows!
                  </p>

                  <div className="mt-4 flex items-center space-x-4 text-sm text-green-600">
                    <div className="flex items-center space-x-1">
                      <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                      <span>Production Ready</span>
                    </div>
                    <div className="flex items-center space-x-1">
                      <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                      <span>Fully Compatible</span>
                    </div>
                    <div className="flex items-center space-x-1">
                      <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                      <span>AI Optimized</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default FlowGenerator;
