import React from 'react';

export const Footer: React.FC = () => (
  <footer className="bg-white py-6">
    <div className="max-w-5xl mx-auto px-4 flex justify-between text-gray-600 text-sm">
      <span>© 2025 ASAP – AST</span>
      <div className="space-x-4">
        <a href="#" className="hover:underline">Privacy Policy</a>
        <a href="#" className="hover:underline">Terms of Service</a>
      </div>
    </div>
  </footer>
);
