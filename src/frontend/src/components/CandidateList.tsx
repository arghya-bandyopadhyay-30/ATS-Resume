import React from 'react';
import { CandidateCard } from './CandidateCard';

interface Candidate {
  name: string;
  title?: string;
  score: number;
  badge?: string;
}

interface CandidateListProps {
  candidates: Candidate[];
}

export const CandidateList: React.FC<CandidateListProps> = ({ candidates }) => {
  return (
    <section className="w-full bg-white py-14">
      <div className="max-w-5xl mx-auto px-4">
        <div className="mb-10 text-center">
          <h2 className="text-3xl font-bold mb-2">Results</h2>
          <p className="text-gray-600 text-sm">
            Here are the candidates ranked based on the resumes you submitted.
          </p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {candidates.map((candidate, index) => (
            <CandidateCard key={index} {...candidate} />
          ))}
        </div>
      </div>
    </section>
  );
};
