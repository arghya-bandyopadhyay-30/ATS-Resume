import React from 'react';
import userIcon from '../assets/user-icon.png';

interface CandidateCardProps {
  name: string;
  title?: string;
  score: number;
}

export const CandidateCard: React.FC<CandidateCardProps> = ({
  name,
  title,
  score,
}) => {
  return (
    <div className="flex items-start p-6 bg-white rounded-xl border border-gray-200 shadow-sm">
      <img
        src={userIcon}
        alt="User Icon"
        className="w-14 h-14 rounded-md mr-5 object-cover"
      />
      <div>
        <h3 className="text-lg font-bold text-gray-900 mb-1">{name}</h3>
        {title && <p className="text-sm text-gray-600 mb-1">{title}</p>}
        <p className="text-sm font-medium text-gray-800 mb-1">Score: {score}</p>
      </div>
    </div>
  );
};
