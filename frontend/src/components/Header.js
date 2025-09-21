import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Zap, Info } from 'lucide-react';

const Header = () => {
  const location = useLocation();

  return (
    <header className="bg-white shadow-sm border-b">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo and Title */}
          <Link to="/" className="flex items-center space-x-3">
            <div className="bg-blue-600 p-2 rounded-lg">
              <Zap className="h-6 w-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-900">
                AxieStudio AI Flow Generator
              </h1>
              <p className="text-sm text-gray-500">
                Create powerful flows with natural language
              </p>
            </div>
          </Link>

          {/* Navigation */}
          <nav className="flex items-center space-x-6">
            <Link
              to="/"
              className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                location.pathname === '/'
                  ? 'bg-blue-100 text-blue-700'
                  : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
              }`}
            >
              Generator
            </Link>
            <Link
              to="/about"
              className={`px-3 py-2 rounded-md text-sm font-medium transition-colors flex items-center space-x-1 ${
                location.pathname === '/about'
                  ? 'bg-blue-100 text-blue-700'
                  : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
              }`}
            >
              <Info className="h-4 w-4" />
              <span>About</span>
            </Link>
          </nav>
        </div>
      </div>
    </header>
  );
};

export default Header;
