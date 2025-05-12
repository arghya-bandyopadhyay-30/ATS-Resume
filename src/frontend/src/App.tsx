import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Header } from './components/Header';
import { Footer } from './components/Footer';
import { Home } from './pages/Home';
import { ReminderSender } from './pages/ReminderSender';
import { ResumeRanker } from './pages/ResumeRanker';
export const App: React.FC = () => {
  return (
    <Router>
      <div className="min-h-screen flex flex-col bg-gray-50">
        <Header />
        <main className="flex-grow">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/staffing-assistant" element={<ResumeRanker />} />
            <Route path="/resume-update-notifier" element={<ReminderSender />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
};
