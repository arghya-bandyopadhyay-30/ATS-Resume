import React from 'react';
import '../index.css';

export const Footer: React.FC = () => (
  <footer className="bg-light-gray border-t border-gray-300 text-center text-xs text-secondary py-4">
    <div className="max-w-5xl mx-auto flex justify-between items-center px-4">
      <p>© {new Date().getFullYear()} ASAP</p>
      <div>
        <a href="#" className="text-secondary hover:underline mr-4">Privacy Policy</a>
        <a href="#" className="text-secondary hover:underline">Terms of Service</a>
      </div>
    </div>
  </footer>
);
