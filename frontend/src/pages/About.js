import React from 'react';
import {
  Zap,
  Brain,
  Database,
  Rocket,
  Github,
  ExternalLink,
  Sparkles,
  Star,
  Code,
  Globe,
  Shield,
  Cpu
} from 'lucide-react';

const About = () => {
  return (
    <div className="max-w-6xl mx-auto space-y-12">
      {/* Hero Header */}
      <div className="text-center space-y-8">
        <div className="space-y-4">
          <div className="inline-flex items-center space-x-2 bg-gradient-to-r from-purple-100 to-blue-100 px-4 py-2 rounded-full text-sm font-medium text-purple-800 border border-purple-200">
            <Sparkles className="h-4 w-4" />
            <span>About Our AI-Powered Platform</span>
          </div>

          <h1 className="text-5xl md:text-6xl font-bold bg-gradient-to-r from-gray-900 via-purple-800 to-blue-800 bg-clip-text text-transparent leading-tight">
            AxieStudio AI
            <br />
            <span className="bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">
              Flow Generator ✨
            </span>
          </h1>

          <p className="text-xl text-gray-600 max-w-4xl mx-auto leading-relaxed">
            Transform natural language descriptions into production-ready AxieStudio flows
            using advanced AI and real AxieStudio templates. Built by developers, for developers.
          </p>
        </div>

        {/* Stats */}
        <div className="flex flex-wrap justify-center gap-8 text-center">
          <div className="space-y-1">
            <div className="text-3xl font-bold text-blue-600">294</div>
            <div className="text-sm text-gray-600">Components Indexed</div>
          </div>
          <div className="space-y-1">
            <div className="text-3xl font-bold text-purple-600">31</div>
            <div className="text-sm text-gray-600">Flow Templates</div>
          </div>
          <div className="space-y-1">
            <div className="text-3xl font-bold text-green-600">2-5s</div>
            <div className="text-sm text-gray-600">Generation Time</div>
          </div>
          <div className="space-y-1">
            <div className="text-3xl font-bold text-orange-600">100%</div>
            <div className="text-sm text-gray-600">Compatible</div>
          </div>
        </div>
      </div>

      {/* Features */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div className="bg-white/80 backdrop-blur-xl rounded-3xl shadow-xl border border-white/20 p-8 relative overflow-hidden group hover:shadow-2xl transition-all duration-300">
          <div className="absolute top-0 right-0 w-24 h-24 bg-blue-400/10 rounded-full blur-2xl group-hover:bg-blue-400/20 transition-colors"></div>
          <div className="relative z-10">
            <div className="flex items-center space-x-4 mb-6">
              <div className="p-3 bg-gradient-to-r from-blue-500 to-blue-600 rounded-2xl shadow-lg">
                <Brain className="h-8 w-8 text-white" />
              </div>
              <h3 className="text-2xl font-bold text-gray-900">AI-Powered Generation</h3>
            </div>
            <p className="text-gray-600 leading-relaxed">
              Uses OpenAI GPT-4 to understand your natural language descriptions and
              intelligently select the best components and flow structure with unprecedented accuracy.
            </p>
          </div>
        </div>

        <div className="bg-white/80 backdrop-blur-xl rounded-3xl shadow-xl border border-white/20 p-8 relative overflow-hidden group hover:shadow-2xl transition-all duration-300">
          <div className="absolute top-0 right-0 w-24 h-24 bg-green-400/10 rounded-full blur-2xl group-hover:bg-green-400/20 transition-colors"></div>
          <div className="relative z-10">
            <div className="flex items-center space-x-4 mb-6">
              <div className="p-3 bg-gradient-to-r from-green-500 to-green-600 rounded-2xl shadow-lg">
                <Database className="h-8 w-8 text-white" />
              </div>
              <h3 className="text-2xl font-bold text-gray-900">Real AxieStudio Data</h3>
            </div>
            <p className="text-gray-600 leading-relaxed">
              Built using actual AxieStudio components and starter project templates,
              ensuring 100% compatibility with your production AxieStudio application.
            </p>
          </div>
        </div>

        <div className="bg-white/80 backdrop-blur-xl rounded-3xl shadow-xl border border-white/20 p-8 relative overflow-hidden group hover:shadow-2xl transition-all duration-300">
          <div className="absolute top-0 right-0 w-24 h-24 bg-purple-400/10 rounded-full blur-2xl group-hover:bg-purple-400/20 transition-colors"></div>
          <div className="relative z-10">
            <div className="flex items-center space-x-4 mb-6">
              <div className="p-3 bg-gradient-to-r from-purple-500 to-purple-600 rounded-2xl shadow-lg">
                <Zap className="h-8 w-8 text-white" />
              </div>
              <h3 className="text-2xl font-bold text-gray-900">Lightning Fast</h3>
            </div>
            <p className="text-gray-600 leading-relaxed">
              Generate complete flows in 2-5 seconds using pre-optimized templates
              and intelligent component selection rules powered by advanced algorithms.
            </p>
          </div>
        </div>

        <div className="bg-white/80 backdrop-blur-xl rounded-3xl shadow-xl border border-white/20 p-8 relative overflow-hidden group hover:shadow-2xl transition-all duration-300">
          <div className="absolute top-0 right-0 w-24 h-24 bg-orange-400/10 rounded-full blur-2xl group-hover:bg-orange-400/20 transition-colors"></div>
          <div className="relative z-10">
            <div className="flex items-center space-x-4 mb-6">
              <div className="p-3 bg-gradient-to-r from-orange-500 to-orange-600 rounded-2xl shadow-lg">
                <Rocket className="h-8 w-8 text-white" />
              </div>
              <h3 className="text-2xl font-bold text-gray-900">Production Ready</h3>
            </div>
            <p className="text-gray-600 leading-relaxed">
              Generated flows include all necessary metadata, proper edge connections,
              and component configurations required by AxieStudio for immediate deployment.
            </p>
          </div>
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
