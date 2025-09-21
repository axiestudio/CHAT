import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Sparkles, Info, Github, ExternalLink } from 'lucide-react';

const Header = () => {
  const location = useLocation();

  return (
    <header className="bg-white/80 backdrop-blur-xl shadow-lg border-b border-white/20 sticky top-0 z-50">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-20">
          {/* Logo and Title */}
          <Link to="/" className="flex items-center space-x-4 group">
            <div className="relative">
              <div className="absolute inset-0 bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl blur opacity-75 group-hover:opacity-100 transition-opacity"></div>
              <div className="relative bg-gradient-to-r from-blue-600 to-purple-600 p-3 rounded-xl">
                <img
                  src="/logo.svg"
                  alt="AxieStudio Logo"
                  className="h-8 w-8 text-white"
                  onError={(e) => {
                    e.target.style.display = 'none';
                    e.target.nextElementSibling.style.display = 'block';
                  }}
                />
                <Sparkles className="h-8 w-8 text-white hidden" />
              </div>
            </div>
            <div>
              <h1 className="text-2xl font-bold bg-gradient-to-r from-gray-900 via-blue-800 to-purple-800 bg-clip-text text-transparent">
                AxieStudio AI Flow Generator
              </h1>
              <p className="text-sm text-gray-600 font-medium">
                Create powerful flows with natural language ✨
              </p>
            </div>
          </Link>

          {/* Navigation */}
          <nav className="flex items-center space-x-2">
            <Link
              to="/"
              className={`px-6 py-3 rounded-xl text-sm font-semibold transition-all duration-200 ${
                location.pathname === '/'
                  ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white shadow-lg shadow-blue-500/25 transform scale-105'
                  : 'text-gray-700 hover:text-gray-900 hover:bg-white/60 hover:shadow-md'
              }`}
            >
              Generator
            </Link>
            <Link
              to="/about"
              className={`px-6 py-3 rounded-xl text-sm font-semibold transition-all duration-200 flex items-center space-x-2 ${
                location.pathname === '/about'
                  ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white shadow-lg shadow-blue-500/25 transform scale-105'
                  : 'text-gray-700 hover:text-gray-900 hover:bg-white/60 hover:shadow-md'
              }`}
            >
              <Info className="h-4 w-4" />
              <span>About</span>
            </Link>

            {/* GitHub Link */}
            <a
              href="https://github.com/axiestudio/CHAT"
              target="_blank"
              rel="noopener noreferrer"
              className="p-3 text-gray-700 hover:text-gray-900 hover:bg-white/60 rounded-xl transition-all duration-200 hover:shadow-md"
              title="View on GitHub"
            >
              <Github className="h-5 w-5" />
            </a>
          </nav>
        </div>
      </div>
    </header>
  );
};

export default Header;
