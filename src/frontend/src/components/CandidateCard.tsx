// src/components/CandidateCard.tsx
import React from 'react';
import '../index.css';
import silhouette from '../assets/user-icon.png';  // silhouette placeholder asset

interface CandidateCardProps {
  name: string;
  title: string;
  score: number;
  recommendation_label?: string;
}

export const CandidateCard: React.FC<CandidateCardProps> = ({
  name,
  title,
  score,
  recommendation_label,
}) => {
  // Determine badge color based on score tiers
  const getBadgeStyle = () => {
    if (score >= 90) {
      return { backgroundColor: 'var(--color-jade-green)', color: '#ffffff' };
    } else if (score >= 75) {
      return { backgroundColor: 'var(--color-sapphire)', color: '#ffffff' };
    } else if (score >= 60) {
      return { backgroundColor: 'var(--color-amethyst-purple)', color: '#ffffff' };
    } else {
      return { backgroundColor: 'var(--color-flamingo)', color: '#ffffff' };
    }
  };

  return (
    <div className="bg-white border border-medium rounded-2xl p-6 flex space-x-6 shadow-sm">
      {/* Profile silhouette */}
      <div className="w-24 h-24 bg-light-gray rounded-full flex items-center justify-center">
        <img
          src={silhouette}
          alt="Profile placeholder"
          className="w-12 h-12 text-secondary"
        />
      </div>

      {/* Candidate details */}
      <div className="flex-1">
        <h3 className="text-lg font-bold text-primary">{name}</h3>
        <p className="text-secondary">{title}</p>
        <p className="mt-2 font-semibold text-primary">Score: {score}</p>
        {recommendation_label && (
          <span
            className="inline-block mt-3 px-3 py-1 text-xs rounded-full font-semibold"
            style={getBadgeStyle()}
          >
            {recommendation_label}
          </span>
        )}
      </div>
    </div>
  );
};
