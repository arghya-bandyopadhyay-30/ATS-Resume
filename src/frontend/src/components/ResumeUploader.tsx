import React, { useState } from 'react';
import '../index.css';

interface ResumeUploaderProps {
  onSubmit: (text: string) => void;
  onReset: () => void;
  isLoading: boolean;
}

export const ResumeUploader: React.FC<ResumeUploaderProps> = ({ onSubmit, onReset, isLoading }) => {
  const [resumeText, setResumeText] = useState('');

  const handleSubmit = (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    onSubmit(resumeText);
  };

  const handleReset = () => {
    setResumeText('');
    onReset();
  };

  return (
    <section className="w-full bg-white py-10 border-t border-b border-medium">
      <div className="max-w-3xl mx-auto px-4">
        <form className="flex flex-col space-y-4" onSubmit={handleSubmit}>
          <textarea
            className="w-full p-4 text-sm border border-medium rounded-md focus:outline-none focus:ring-2 focus:ring-sapphire focus:border-transparent min-h-[200px]"
            placeholder="Paste job description here..."
            value={resumeText}
            onChange={(e) => setResumeText(e.target.value)}
            disabled={isLoading}
          />

          <div className="flex justify-end space-x-4">
            <button
              type="submit"
              className={`bg-dark-blue text-white px-6 py-2 text-sm rounded transition-colors ${
                isLoading ? 'opacity-50 cursor-not-allowed' : 'hover:bg-sapphire'
              }`}
              disabled={isLoading}
            >
              {isLoading ? 'Processing...' : 'Search Candidates'}
            </button>

            <button
              type="button"
              onClick={handleReset}
              className={`bg-gray-500 text-white px-6 py-2 text-sm rounded transition-colors ${
                isLoading ? 'opacity-50 cursor-not-allowed' : 'hover:bg-gray-600'
              }`}
              disabled={isLoading}
            >
              Clear
            </button>
          </div>
        </form>
      </div>
    </section>
  );
};
