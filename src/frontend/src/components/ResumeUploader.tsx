import React, { useState } from 'react';

interface ResumeUploaderProps {
  onSubmit: (text: string) => void;
}

export const ResumeUploader: React.FC<ResumeUploaderProps> = ({ onSubmit }) => {
  const [resumeText, setResumeText] = useState('');

  const handleSubmit = (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    onSubmit(resumeText);
  };

  return (
    <section className="w-full bg-white py-10 border-t border-b border-gray-100">
      <div className="max-w-3xl mx-auto px-4">
        <h2 className="text-2xl font-semibold mb-4">Paste your resumes below</h2>
        <form className="flex items-center space-x-4" onSubmit={handleSubmit}>
          <input
            className="flex-1 p-4 text-sm border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="Paste resumes here"
            value={resumeText}
            onChange={(e) => setResumeText(e.target.value)}
            type="text"
          />
          <button
            type="submit"
            className="px-6 py-2 bg-black text-white text-sm rounded hover:bg-gray-900 transition-colors"
          >
            Submit
          </button>
        </form>
      </div>
    </section>
  );
};
