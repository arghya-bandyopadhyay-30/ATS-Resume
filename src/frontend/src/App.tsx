import React, { useState } from 'react';
import { Header } from './components/Header';
import { ResumeUploader } from './components/ResumeUploader';
import { CandidateList } from './components/CandidateList';
import { Footer } from './components/Footer';

const initialCandidates = [
  { name: 'Candidate A', title: 'Software Engineer', score: 85},
  { name: 'Candidate B', title: 'Data Analyst', score: 78},
  { name: 'Candidate C', title: 'Web Developer', score: 90},
  { name: 'Candidate D', title: 'Project Manager', score: 75},
];

export const App: React.FC = () => {
  const [candidates, setCandidates] = useState(initialCandidates);

  const handleResumeSubmit = (text: string) => {
    // Placeholder: In a real app, process resumes and update candidates
    // For now, just log the text
    console.log('Submitted resumes:', text);
  };

  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      <Header />
      <main className="flex-grow">
        <ResumeUploader onSubmit={handleResumeSubmit} />
        <CandidateList candidates={candidates} />
      </main>
      <Footer />
    </div>
  );
};
