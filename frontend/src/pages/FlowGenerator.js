import React, { useState, useEffect } from 'react';
import { toast } from 'react-hot-toast';
import { 
  Zap, 
  Download, 
  Loader2, 
  CheckCircle, 
  AlertCircle,
  Cpu,
  Network,
  Clock
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
    <div className="max-w-4xl mx-auto space-y-8">
      {/* Header */}
      <div className="text-center">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">
          Generate AxieStudio Flows with AI
        </h1>
        <p className="text-lg text-gray-600 max-w-2xl mx-auto">
          Describe what you want to build in natural language, and our AI will create 
          a complete AxieStudio flow ready for import.
        </p>
      </div>

      {/* API Status */}
      {apiStatus && (
        <div className={`p-4 rounded-lg border ${
          apiStatus.status === 'healthy' 
            ? 'bg-green-50 border-green-200' 
            : 'bg-red-50 border-red-200'
        }`}>
          <div className="flex items-center space-x-2">
            {apiStatus.status === 'healthy' ? (
              <CheckCircle className="h-5 w-5 text-green-600" />
            ) : (
              <AlertCircle className="h-5 w-5 text-red-600" />
            )}
            <span className={`font-medium ${
              apiStatus.status === 'healthy' ? 'text-green-800' : 'text-red-800'
            }`}>
              Backend Status: {apiStatus.status === 'healthy' ? 'Connected' : 'Disconnected'}
            </span>
          </div>
          <div className="mt-2 text-sm text-gray-600">
            OpenAI: {apiStatus.openai_configured ? '✅ Configured' : '❌ Not configured'}
          </div>
        </div>
      )}

      {/* Input Section */}
      <div className="bg-white rounded-lg shadow-sm border p-6">
        <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-2">
          Describe your flow
        </label>
        <textarea
          id="description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Example: Create a chatbot that answers questions about PDF documents using RAG"
          className="w-full h-32 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
          disabled={isGenerating}
        />
        
        <div className="mt-4 flex justify-between items-center">
          <div className="text-sm text-gray-500">
            {description.length}/500 characters
          </div>
          <button
            onClick={handleGenerate}
            disabled={isGenerating || !description.trim() || !apiStatus?.openai_configured}
            className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
          >
            {isGenerating ? (
              <>
                <Loader2 className="h-4 w-4 animate-spin" />
                <span>Generating...</span>
              </>
            ) : (
              <>
                <Zap className="h-4 w-4" />
                <span>Generate Flow</span>
              </>
            )}
          </button>
        </div>
      </div>

      {/* Results Section */}
      {generatedFlow && (
        <div className="bg-white rounded-lg shadow-sm border p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold text-gray-900">Generated Flow</h2>
            <button
              onClick={handleDownload}
              className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 flex items-center space-x-2"
            >
              <Download className="h-4 w-4" />
              <span>Download JSON</span>
            </button>
          </div>

          {/* Flow Stats */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <div className="bg-blue-50 p-4 rounded-lg">
              <div className="flex items-center space-x-2">
                <Cpu className="h-5 w-5 text-blue-600" />
                <span className="font-medium text-blue-900">Components</span>
              </div>
              <div className="text-2xl font-bold text-blue-600 mt-1">
                {generatedFlow.components?.length || 0}
              </div>
            </div>
            
            <div className="bg-green-50 p-4 rounded-lg">
              <div className="flex items-center space-x-2">
                <Network className="h-5 w-5 text-green-600" />
                <span className="font-medium text-green-900">Connections</span>
              </div>
              <div className="text-2xl font-bold text-green-600 mt-1">
                {generatedFlow.flow_data?.data?.edges?.length || 0}
              </div>
            </div>
            
            <div className="bg-purple-50 p-4 rounded-lg">
              <div className="flex items-center space-x-2">
                <Clock className="h-5 w-5 text-purple-600" />
                <span className="font-medium text-purple-900">Generation Time</span>
              </div>
              <div className="text-2xl font-bold text-purple-600 mt-1">
                {generatedFlow.generation_time?.toFixed(2)}s
              </div>
            </div>
          </div>

          {/* Components List */}
          {generatedFlow.components && generatedFlow.components.length > 0 && (
            <div className="mb-6">
              <h3 className="text-lg font-medium text-gray-900 mb-3">Components Used</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {generatedFlow.components.map((component, index) => (
                  <div key={index} className="bg-gray-50 p-3 rounded-md">
                    <div className="font-medium text-gray-900">{component.display_name}</div>
                    <div className="text-sm text-gray-600">{component.description}</div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Success Message */}
          <div className="bg-green-50 border border-green-200 rounded-md p-4">
            <div className="flex items-center space-x-2">
              <CheckCircle className="h-5 w-5 text-green-600" />
              <span className="font-medium text-green-800">Ready for AxieStudio!</span>
            </div>
            <p className="text-sm text-green-700 mt-1">
              Your flow has been generated using real AxieStudio templates and is ready to import 
              into your production AxieStudio application.
            </p>
          </div>
        </div>
      )}
    </div>
  );
};

export default FlowGenerator;
