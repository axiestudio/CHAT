import React from 'react';
import { 
  Zap, 
  Brain, 
  Database, 
  Rocket, 
  Github, 
  ExternalLink 
} from 'lucide-react';

const About = () => {
  return (
    <div className="max-w-4xl mx-auto space-y-8">
      {/* Header */}
      <div className="text-center">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">
          About AxieStudio AI Flow Generator
        </h1>
        <p className="text-lg text-gray-600 max-w-2xl mx-auto">
          Transform natural language descriptions into production-ready AxieStudio flows 
          using advanced AI and real AxieStudio templates.
        </p>
      </div>

      {/* Features */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow-sm border p-6">
          <div className="flex items-center space-x-3 mb-4">
            <div className="bg-blue-100 p-2 rounded-lg">
              <Brain className="h-6 w-6 text-blue-600" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900">AI-Powered Generation</h3>
          </div>
          <p className="text-gray-600">
            Uses OpenAI GPT-4 to understand your natural language descriptions and 
            intelligently select the best components and flow structure.
          </p>
        </div>

        <div className="bg-white rounded-lg shadow-sm border p-6">
          <div className="flex items-center space-x-3 mb-4">
            <div className="bg-green-100 p-2 rounded-lg">
              <Database className="h-6 w-6 text-green-600" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900">Real AxieStudio Data</h3>
          </div>
          <p className="text-gray-600">
            Built using actual AxieStudio components and starter project templates, 
            ensuring 100% compatibility with your production AxieStudio application.
          </p>
        </div>

        <div className="bg-white rounded-lg shadow-sm border p-6">
          <div className="flex items-center space-x-3 mb-4">
            <div className="bg-purple-100 p-2 rounded-lg">
              <Zap className="h-6 w-6 text-purple-600" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900">Lightning Fast</h3>
          </div>
          <p className="text-gray-600">
            Generate complete flows in 2-5 seconds using pre-optimized templates 
            and intelligent component selection rules.
          </p>
        </div>

        <div className="bg-white rounded-lg shadow-sm border p-6">
          <div className="flex items-center space-x-3 mb-4">
            <div className="bg-orange-100 p-2 rounded-lg">
              <Rocket className="h-6 w-6 text-orange-600" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900">Production Ready</h3>
          </div>
          <p className="text-gray-600">
            Generated flows include all necessary metadata, proper edge connections, 
            and component configurations required by AxieStudio.
          </p>
        </div>
      </div>

      {/* How It Works */}
      <div className="bg-white rounded-lg shadow-sm border p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">How It Works</h2>
        
        <div className="space-y-6">
          <div className="flex items-start space-x-4">
            <div className="bg-blue-100 text-blue-600 rounded-full p-2 font-bold text-sm min-w-[2rem] h-8 flex items-center justify-center">
              1
            </div>
            <div>
              <h3 className="font-semibold text-gray-900 mb-2">Natural Language Input</h3>
              <p className="text-gray-600">
                Describe what you want to build in plain English. For example: 
                "Create a chatbot that answers questions about PDF documents"
              </p>
            </div>
          </div>

          <div className="flex items-start space-x-4">
            <div className="bg-blue-100 text-blue-600 rounded-full p-2 font-bold text-sm min-w-[2rem] h-8 flex items-center justify-center">
              2
            </div>
            <div>
              <h3 className="font-semibold text-gray-900 mb-2">AI Analysis</h3>
              <p className="text-gray-600">
                OpenAI GPT-4 analyzes your description to understand the intent and 
                determines the best flow type (basic chat, RAG system, agent tools, etc.)
              </p>
            </div>
          </div>

          <div className="flex items-start space-x-4">
            <div className="bg-blue-100 text-blue-600 rounded-full p-2 font-bold text-sm min-w-[2rem] h-8 flex items-center justify-center">
              3
            </div>
            <div>
              <h3 className="font-semibold text-gray-900 mb-2">Template Selection</h3>
              <p className="text-gray-600">
                The system selects the most appropriate template from 31 real AxieStudio 
                starter projects and customizes it for your specific use case.
              </p>
            </div>
          </div>

          <div className="flex items-start space-x-4">
            <div className="bg-blue-100 text-blue-600 rounded-full p-2 font-bold text-sm min-w-[2rem] h-8 flex items-center justify-center">
              4
            </div>
            <div>
              <h3 className="font-semibold text-gray-900 mb-2">Flow Generation</h3>
              <p className="text-gray-600">
                A complete AxieStudio-compatible JSON file is generated with proper 
                component configurations, edge connections, and metadata.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Technical Details */}
      <div className="bg-white rounded-lg shadow-sm border p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Technical Architecture</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h3 className="font-semibold text-gray-900 mb-3">Backend (FastAPI)</h3>
            <ul className="space-y-2 text-gray-600">
              <li>• FastAPI REST API</li>
              <li>• OpenAI GPT-4 integration</li>
              <li>• 294 indexed AxieStudio components</li>
              <li>• 31 real flow templates</li>
              <li>• Production-ready deployment</li>
            </ul>
          </div>
          
          <div>
            <h3 className="font-semibold text-gray-900 mb-3">Frontend (React)</h3>
            <ul className="space-y-2 text-gray-600">
              <li>• Modern React application</li>
              <li>• Tailwind CSS styling</li>
              <li>• Real-time API communication</li>
              <li>• Responsive design</li>
              <li>• Vercel deployment ready</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Deployment */}
      <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg border p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">Deployment Ready</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h3 className="font-semibold text-gray-900 mb-2">Frontend → Vercel</h3>
            <p className="text-gray-600 text-sm">
              The React frontend is optimized for Vercel deployment with automatic 
              builds and global CDN distribution.
            </p>
          </div>
          <div>
            <h3 className="font-semibold text-gray-900 mb-2">Backend → Render/Railway</h3>
            <p className="text-gray-600 text-sm">
              The FastAPI backend can be deployed to any hosting service that supports 
              Python applications, including Render, Railway, or Heroku.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default About;
