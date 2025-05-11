// src/components/CandidateList.tsx
import React from 'react';
import { CandidateCard } from './CandidateCard';
import '../index.css';

export interface Candidate {
  name: string;
  title: string;
  score: number;
  recommendation_label?: string;
}

interface CandidateListProps {
  candidates: Candidate[];
}

export const CandidateList: React.FC<CandidateListProps> = ({ candidates }) => (
  <section className="bg-white py-12 border-t border-b border-medium">
    <div className="max-w-5xl mx-auto px-4">
      <div className="text-center mb-10">
        <h2 className="text-3xl font-bold text-primary">Results</h2>
        <p className="text-secondary mt-2">
          Here are the candidates ranked based on the resumes you submitted.
        </p>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {candidates.map(candidate => (
          <CandidateCard
            key={candidate.name}
            name={candidate.name}
            title={candidate.title}
            score={candidate.score}
            recommendation_label={candidate.recommendation_label}
          />
        ))}
      </div>
    </div>
  </section>
);
