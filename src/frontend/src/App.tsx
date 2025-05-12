import React, { useState, useEffect } from 'react';
import { Header } from './components/Header';
import { ResumeUploader } from './components/ResumeUploader';
import { CandidateList } from './components/CandidateList';
import { Footer } from './components/Footer';

interface BackendCandidate {
  candidate_name: string;
  role: string;
  score: number;
  recommendation_label?: string;
}

export const App: React.FC = () => {
  const [candidates, setCandidates] = useState<BackendCandidate[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchRankings = async () => {
    try {
      const response = await fetch('http://localhost:8000/rankings');
      const data: BackendCandidate[] = await response.json();
      setCandidates(data);
      setError(null);
    } catch (err) {
      console.error('Failed to fetch rankings:', err);
      setError('Failed to fetch rankings. Please try again.');
    }
  };

  // Reset output folder and fetch rankings once on load
  useEffect(() => {
    const resetOutputAndFetch = async () => {
      try {
        await fetch('http://localhost:8000/reset-output', { method: 'POST' });
        await fetchRankings();  // Fetch after clearing the output folder
      } catch (err) {
        console.error('Failed to reset output or fetch rankings:', err);
        setError('Failed to reset data. Please try again.');
      }
    };

    resetOutputAndFetch();
  }, []);

  const handleResumeSubmit = async (text: string) => {
    if (!text.trim()) {
      setError('Please enter a job description');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch('http://localhost:8000/analyze-jd', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ jd_text: text }),
      });

      if (!response.ok) throw new Error('Failed to analyze job description');
      await fetchRankings();  // Fetch updated results after JD analysis
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

        <CandidateList
          candidates={candidates.map(c => ({
            name: c.candidate_name,
            title: c.role,
            score: c.score,
            recommendation_label: c.recommendation_label,
          }))}
        />
      </main>
      <Footer />
    </div>
  );
};
