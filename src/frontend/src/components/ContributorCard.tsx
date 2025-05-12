import React from 'react';

interface ContributorCardProps {
  image: string;
  name: string;
  email: string;
  role: string;
}

export const ContributorCard: React.FC<ContributorCardProps> = ({ image, name, email, role }) => {
  return (
    <div className="flex items-center p-4 border border-medium rounded-lg shadow bg-white space-x-4">
      <img
        src={image}
        alt={name}
        className="w-14 h-14 rounded-full object-cover border border-gray-300"
      />
      <div>
        <h4 className="text-sm font-semibold text-primary">{name}</h4>
        <a href={`mailto:${email}`} className="text-xs text-sapphire underline">
          {email}
        </a>
        <p className="text-xs text-gray-500 italic">Role: {role}</p>
      </div>
    </div>
  );
};
