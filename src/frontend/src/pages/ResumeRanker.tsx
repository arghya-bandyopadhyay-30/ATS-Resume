import React, { useState } from 'react';
import { ResumeUploader } from '../components/ResumeUploader';
import { CandidateList } from '../components/CandidateList';
import { BASE_URL } from '../config';

interface BackendCandidate {
  rank: number;
  candidate_name: string;
  role: string;
  score: number;
  recommendation_label?: string;
}

export const ResumeRanker: React.FC = () => {
  const [candidates, setCandidates] = useState<BackendCandidate[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchRankings = async () => {
    try {
      const response = await fetch(`${BASE_URL}/rankings`);
      const data: BackendCandidate[] = await response.json();
      setCandidates(data);
      setError(null);
    } catch (err) {
      console.error('Failed to fetch rankings:', err);
      setError('Failed to fetch rankings. Please try again.');
    }
  };

  const handleReset = async () => {
    try {
      await fetch(`${BASE_URL}/reset-output`, { method: 'POST' });
      setCandidates([]);
      setError(null);
    } catch (err) {
      console.error('Failed to reset output:', err);
      setError('Failed to reset data. Please try again.');
    }
  };

  const handleResumeSubmit = async (text: string) => {
    if (!text.trim()) {
      setError('Please enter a job description');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch(`${BASE_URL}/analyze-jd`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ jd_text: text }),
      });

      if (!response.ok) throw new Error('Failed to analyze job description');
      await fetchRankings();
    } catch (err) {
      console.error('Failed to submit job description:', err);
      setError('Failed to process job description. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="bg-white">
      {/* Hero Section */}
      <section className="bg-light-gray py-12">
        <div className="max-w-5xl mx-auto px-4 text-center">
          <h1 className="text-3xl font-bold text-primary">What would you like to do today?</h1>
          <p className="mt-2 text-secondary">
            ASAP is your intelligent AI assistant that helps you manage skill fitment.
          </p>
        </div>
      </section>

      <main className="flex-grow">
        <ResumeUploader
          onSubmit={handleResumeSubmit}
          onReset={handleReset}
          isLoading={isLoading}
        />

        {error && (
          <div className="max-w-3xl mx-auto px-4 mt-4">
            <p className="text-red-500 text-sm">{error}</p>
          </div>
        )}

        <CandidateList
          candidates={candidates.map(c => ({
            rank: c.rank,
            name: c.candidate_name,
            title: c.role,
            score: c.score,
            recommendation_label: c.recommendation_label,
          }))}
        />
      </main>
    </div>
  );
};
