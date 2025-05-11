import React from 'react';

interface CandidateCardProps {
  name: string;
  title: string;
  score: number;
  recommendation_label?: string;
}

export const CandidateCard: React.FC<CandidateCardProps> = ({ name, title, score, recommendation_label }) => (
  <div className="bg-white border border-gray-200 rounded-lg p-6 flex space-x-4">
    <div className="w-24 h-24 bg-gray-200 rounded" />
    <div className="flex-1">
      <h3 className="text-lg font-bold">{name}</h3>
      <p className="text-gray-600">{title}</p>
      <p className="mt-2 font-semibold">Score: {score}</p>
      {recommendation_label && (
        <span className="inline-block mt-2 bg-gray-100 text-gray-800 text-xs font-medium px-2 py-1 rounded">
          {recommendation_label}
        </span>
      )}
    </div>
  </div>
);