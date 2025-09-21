import React from 'react';
import { Link } from 'react-router-dom';
import { Github, ExternalLink } from 'lucide-react';

const Header = () => {
  return (
    <header className="bg-white shadow-sm border-b">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo and Title */}
          <Link to="/" className="flex items-center space-x-3">
            <img
              src="/logo.svg"
              alt="AxieStudio Logo"
              className="h-10 w-10 object-contain"
              onError={(e) => {
                // Fallback to text logo if SVG fails to load
                e.currentTarget.style.display = 'none';
                e.currentTarget.nextElementSibling.style.display = 'flex';
              }}
            />
            <div
              className="h-10 w-10 bg-blue-600 rounded-lg flex items-center justify-center text-white font-bold text-lg"
              style={{ display: 'none' }}
            >
              AX
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-900">
                AxieStudio AI Chat
              </h1>
              <p className="text-sm text-gray-500">
                Real conversational AI for authentic AxieStudio flows
              </p>
            </div>
          </Link>

          {/* Navigation */}
          <nav className="flex items-center space-x-4">
            <a
              href="https://worthwhile-pelican-axiestudio-7ed1c7d6.koyeb.app/"
              target="_blank"
              rel="noopener noreferrer"
              className="px-3 py-2 rounded-md text-sm font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-100 transition-colors flex items-center space-x-1"
            >
              <ExternalLink className="h-4 w-4" />
              <span>API</span>
            </a>
            <a
              href="https://github.com/axiestudio/CHAT"
              target="_blank"
              rel="noopener noreferrer"
              className="px-3 py-2 rounded-md text-sm font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-100 transition-colors flex items-center space-x-1"
            >
              <Github className="h-4 w-4" />
              <span>GitHub</span>
            </a>
          </nav>
        </div>
      </div>
    </header>
  );
};

export default Header;
