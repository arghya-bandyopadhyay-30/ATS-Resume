import React from 'react';
import '../index.css';

export const Footer: React.FC = () => (
  <footer className="bg-light-gray border-t border-medium py-6">
    <div className="max-w-5xl mx-auto px-4 flex flex-col md:flex-row items-center justify-between text-secondary text-sm">
      <span>© 2025 ASAP – AST</span>
      <div className="mt-3 md:mt-0 space-x-4">
        <a href="#" className="hover:text-sapphire">
          Privacy Policy
        </a>
        <a href="#" className="hover:text-sapphire">
          Terms of Service
        </a>
      </div>
    </div>
  </footer>
);
