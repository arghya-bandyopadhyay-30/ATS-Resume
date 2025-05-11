import React from 'react';

export const Footer: React.FC = () => (
  <footer className="w-full bg-white border-t border-gray-200 py-8 mt-12">
    <div className="max-w-4xl mx-auto px-4 flex flex-col md:flex-row items-center justify-between text-gray-500 text-sm space-y-2 md:space-y-0">
      <div>© 2023 ASAP – AST</div>
      <div className="flex space-x-6">
        <a href="#" className="hover:underline">Privacy Policy</a>
        <a href="#" className="hover:underline">Terms of Service</a>
      </div>
    </div>
  </footer>
); 