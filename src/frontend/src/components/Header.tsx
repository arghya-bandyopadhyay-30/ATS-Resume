import React from 'react';
import '../index.css';
import twLogo from '../assets/thoughtworks.png';  // ← your ThoughtWorks logo asset

export const Header: React.FC = () => (
  <header>
    {/* Top nav bar */}
    <div className="bg-dark-blue h-16 flex items-center px-4">
      <img src={twLogo} alt="Thoughtworks" className="h-8 w-auto mr-3" />
      <span className="mx-2 text-white">|</span>
      <span className="text-white font-semibold text-lg">ASAP - AST</span>
    </div>
    {/* Hero section */}
    <div className="bg-light-gray py-12">
      <div className="max-w-5xl mx-auto px-4 text-center">
        <h1 className="text-3xl font-bold text-primary">
          What would you like to do today?
        </h1>
        <p className="mt-2 text-secondary">
          ASAP – AST is your intelligent AI assistant that helps you rank resumes efficiently.
        </p>
      </div>
    </div>
  </header>
);
