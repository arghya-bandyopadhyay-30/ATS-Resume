import React from 'react';

export const Header: React.FC = () => (
  <header className="bg-white py-8">
    <div className="max-w-5xl mx-auto px-4">
      <div className="text-xl font-bold">ASAP - AST</div>
      <div className="mt-8 text-center">
        <h1 className="text-3xl font-bold">What would you like to do today?</h1>
        <p className="mt-2 text-gray-600">
          ASAP – AST is your intelligent AI assistant that helps you rank resumes efficiently.
        </p>
      </div>
    </div>
  </header>
);
