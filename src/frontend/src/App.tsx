import React, { useState, useEffect } from 'react';
import { Header } from './components/Header';
import { ResumeUploader } from './components/ResumeUploader';
import { CandidateList } from './components/CandidateList';
import { Footer } from './components/Footer';

interface Candidate {
  candidate_name: string;
  score: number;
}

export const App: React.FC = () => {
  const [candidates, setCandidates] = useState<Candidate[]>([]);

  useEffect(() => {
    fetch('http://localhost:8000/rankings')
      .then((res) => res.json())
      .then((data) => {
        setCandidates(data);
      })
      .catch((err) => console.error('Failed to fetch rankings:', err));
  }, []);

  const handleResumeSubmit = (text: string) => {
    console.log('Submitted resumes:', text);
    // Optional: re-trigger fetch after processing resumes
    // fetchCandidates();
  };

  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      <Header />
      <main className="flex-grow">
        <ResumeUploader onSubmit={handleResumeSubmit} />
        <CandidateList candidates={candidates.map(c => ({
          name: c.candidate_name,
          score: c.score
        }))} />
      </main>
      <Footer />
    </div>
  );
};
