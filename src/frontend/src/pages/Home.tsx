import React from 'react';

export const Home: React.FC = () => {
  const features = [
    {
      title: 'Identify Employees Without Resume Updates',
      desc: 'Identify employees who haven’t uploaded resumes to Jigsaw in the last 6 months.'
    },
    {
      title: 'Encourage Resume Compliance',
      desc: 'Encourage 100% resume compliance via timely reminders.'
    },
    {
      title: 'AI Skills Analysis',
      desc: 'Use AI to analyze resumes and infer key skills.'
    },
    {
      title: 'Highlight Relevant Skills',
      desc: 'Highlight the most recently used and relevant skills to determine fitment.'
    }
  ];

  return (
    <div>
      {/* Hero Section with Light Gray */}
      <section className="bg-light-gray py-12 text-center">
        <h1 className="text-3xl font-bold text-primary">Problem Statement</h1>
        <p className="mt-2 text-secondary max-w-2xl mx-auto">
          This app helps identify people with proper skillsets for a given open role using AI,
          especially when Jigsaw/Pathways data is outdated.
        </p>
      </section>

      {/* Main Content with White Background */}
      <section className="bg-white py-12">
        <div className="max-w-5xl mx-auto px-4 grid md:grid-cols-2 gap-8 items-center">
          <div>
            <h3 className="text-xl font-semibold text-primary mb-2">Why this matters</h3>
            <p className="text-secondary">
              As part of this hackathon initiative, we aim to:
            </p>
          </div>

          <div className="space-y-4">
            {features.map(({ title, desc }, index) => (
              <div
                key={index}
                className="bg-white shadow border border-medium rounded-lg p-4"
              >
                <h4 className="text-sm font-semibold text-primary mb-1">{title}</h4>
                <p className="text-secondary text-sm">{desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
};
