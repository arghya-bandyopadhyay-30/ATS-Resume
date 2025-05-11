import React from 'react';
import thoughtworksLogo from '../assets/thoughtworks.jpg';

export const Header: React.FC = () => {
  return (
    <header className="w-full bg-white border-b border-gray-200">
      <div className="flex items-center justify-between max-w-7xl mx-auto px-6 py-4">
        <div className="flex items-center space-x-3">
          <img
            src={thoughtworksLogo}
            alt="Thoughtworks Logo"
            className="w-8 h-8 object-contain"
          />
          <span className="font-bold text-xl">ASAP - AST</span>
        </div>
      </div>

      <div className="max-w-3xl mx-auto px-4 py-10 text-center">
        <h1 className="text-4xl font-bold mb-4">What would you like to do today?</h1>
        <p className="text-lg text-gray-600">
          ASAP – AST is your intelligent AI assistant that helps you rank resumes efficiently.
        </p>
      </div>
    </header>
  );
};
