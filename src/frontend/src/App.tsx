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
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchRankings = async () => {
    try {
      const response = await fetch('http://localhost:8000/rankings');
      const data = await response.json();
      setCandidates(data);
      setError(null);
    } catch (err) {
      console.error('Failed to fetch rankings:', err);
      setError('Failed to fetch rankings. Please try again.');
    }
  };

  useEffect(() => {
    fetchRankings();
  }, []);

  const handleResumeSubmit = async (text: string) => {
    if (!text.trim()) {
      setError('Please enter a job description');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      // Send job description to backend
      const response = await fetch('http://localhost:8000/analyze-jd', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ jd_text: text }),
      });

      if (!response.ok) {
        throw new Error('Failed to analyze job description');
      }

      // Refresh rankings after successful analysis
      await fetchRankings();
    } catch (err) {
      console.error('Failed to submit job description:', err);
      setError('Failed to process job description. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      <Header />
      <main className="flex-grow">
        <ResumeUploader onSubmit={handleResumeSubmit} isLoading={isLoading} />
        {error && (
          <div className="max-w-3xl mx-auto px-4 mt-4">
            <p className="text-red-500 text-sm">{error}</p>
          </div>
        )}
        <CandidateList candidates={candidates.map(c => ({
          name: c.candidate_name,
          score: c.score
        }))} />
      </main>
      <Footer />
    </div>
  );
};
