import React from 'react';
import { ContributorCard } from '../components/ContributorCard';
import arghyaImg from '../assets/arghya.png';
import cursorImg from '../assets/cursor.png';
import copilotImg from '../assets/github_copilot.png';
import continueDevImg from '../assets/continue_dev.png';
import haivenImg from '../assets/haiven_tw.png';
import chatgptImg from '../assets/chatgpt.png';
import figmaImg from '../assets/figma.png';
import gemmaImg from '../assets/gemma.png';

export const Home: React.FC = () => {
  const features = [
    {
      title: 'Identify Employees Without Resume Updates',
      desc: 'Spot employees who haven’t uploaded resumes to Jigsaw in the last 6 months and may be missing from staffing consideration.',
    },
    {
      title: 'Encourage Resume Compliance',
      desc: 'Drive 100% resume compliance by sending automated, timely reminder emails.',
    },
    {
      title: 'AI-Driven Skills Analysis',
      desc: 'Use AI to analyze resumes and extract key capabilities aligned with job requirements.',
    },
    {
      title: 'Highlight Relevant Skills for Fitment',
      desc: 'Showcase the most recent and relevant skills of each candidate to determine job-role fitment efficiently.',
    },
  ];

  const contributors = [
    {
      name: 'Arghya Banerjee',
      email: 'arghya.bandyopadhyay.official1@gmail.com',
      role: 'Application Developer',
      image: arghyaImg,
    },
    {
      name: 'Cursor',
      email: 'https://www.cursor.sh/',
      role: 'AI IDE (Generated code and project structure)',
      image: cursorImg,
    },
    {
      name: 'GitHub Copilot',
      email: 'https://github.com/features/copilot',
      role: 'Code Refactoring, Bug Fixing',
      image: copilotImg,
    },
    {
      name: 'Continue.dev',
      email: 'https://continue.dev/',
      role: 'Prompt Generation',
      image: continueDevImg,
    },
    {
      name: 'Haiven (ThoughtWorks)',
      email: 'https://www.thoughtworks.com/', // General TW website since Haiven is internal
      role: 'Story Building',
      image: haivenImg,
    },
    {
      name: 'ChatGPT',
      email: 'https://chat.openai.com/',
      role: 'Docker Files, Mock File Generation, README Authoring',
      image: chatgptImg,
    },
    {
      name: 'Figma AI',
      email: 'https://www.figma.com/',
      role: 'UI Design',
      image: figmaImg,
    },
    {
      name: 'Gemma 2-9B-IT',
      email: 'https://ai.google.dev/gemma',
      role: 'LLM Model for Resume Parsing and Skill Extraction',
      image: gemmaImg,
    },
  ];

  return (
    <div>
      {/* Hero Section */}
      <section className="bg-light-gray py-12 text-center">
        <h1 className="text-3xl font-bold text-primary">Welcome to ASAP</h1>
        <p className="mt-3 text-secondary max-w-3xl mx-auto text-base">
          <strong>ASAP</strong> stands for <strong>AI-powered Staffing & Applicant Platform</strong> —
          a smart assistant designed to bridge the gap between outdated resume data and real-time skill visibility.
        </p>
      </section>

      {/* Problem Statement */}
      <section className="bg-white py-12">
        <div className="max-w-5xl mx-auto px-4 text-center">
          <h2 className="text-2xl font-bold text-primary mb-2">Problem Statement</h2>
          <p className="text-secondary max-w-3xl mx-auto">
            ThoughtWorks relies on Jigsaw or Pathways data to make staffing decisions.
            However, outdated resumes and missing skill insights can lead to misalignment and the underutilization of available talent.
            <br />
            <br />
            ASAP solves this by intelligently identifying resume gaps, prompting employees to update their profiles, and analyzing those resumes to match individuals to roles based on real-time, AI-inferred skillsets.
          </p>
        </div>
      </section>

      {/* Features + Contributors */}
      <section className="bg-white py-12 border-t border-medium">
        <div className="max-w-6xl mx-auto px-4 grid md:grid-cols-2 gap-8 items-start">
          {/* Left: Features */}
          <div className="flex flex-col h-full pr-4 border-r border-medium">
            <h3 className="text-xl font-semibold text-primary mb-2">Key Capabilities</h3>
            <p className="text-secondary mb-4">
              As part of our hackathon initiative, ASAP is built to streamline staffing readiness with AI-powered automation.
            </p>
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

          {/* Right: Contributors */}
          <div className="flex flex-col h-full pl-4 space-y-4">
            <h3 className="text-xl font-semibold text-primary mb-2">Contributors</h3>
            {contributors.map((contributor, index) => (
              <ContributorCard
                key={index}
                image={contributor.image}
                name={contributor.name}
                email={contributor.email}
                role={contributor.role}
              />
            ))}
          </div>
        </div>
      </section>
    </div>
  );
};
