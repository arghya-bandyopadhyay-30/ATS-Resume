import React, { useState } from 'react';
import { BASE_URL } from '../config';
import { EnvBox } from '../components/EnvBox';

interface EmailResult {
  email: string;
  date: string;
  email_sent: boolean;
}

export const ReminderSender: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [results, setResults] = useState<EmailResult[]>([]);
  const [totalRecords, setTotalRecords] = useState(0);
  const [processedRecords, setProcessedRecords] = useState(0);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFile(e.target.files?.[0] || null);
    setResults([]);
    setError(null);
    setTotalRecords(0);
    setProcessedRecords(0);
  };

  const handleSubmit = async () => {
    if (!file) {
      setError('Please upload a .xlsx file.');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch(`${BASE_URL}/process-emails`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const { detail } = await response.json();
        throw new Error(detail || 'Failed to process file.');
      }

      const data = await response.json();
      setResults(data.results || []);
      setTotalRecords(data.total_records || 0);
      setProcessedRecords(data.processed_records || 0);
    } catch (err: any) {
      setError(err.message || 'Unexpected error occurred.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-white px-6 py-12">
      {/* Required Environment Variables */}
      <div className="max-w-6xl mx-auto mb-12">
        <h2 className="text-xl font-bold text-primary mb-2">⚠️ Required Environment Variables</h2>
        <p className="text-secondary text-sm mb-4">Make sure you have the required variables set up.</p>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <EnvBox label="SENDER_EMAIL" desc="Your Gmail or SMTP-enabled sender address." />
          <EnvBox label="SENDER_PASSWORD" desc="App-specific password or email token." />
        </div>
      </div>

      {/* Upload Reminder Sheet */}
      <div className="max-w-6xl mx-auto bg-gray-50 border border-gray-300 rounded-lg p-6 mb-12 shadow-sm">
        <h2 className="text-2xl font-bold text-primary mb-2">Upload Reminder Sheet</h2>
        <p className="text-secondary text-sm mb-6">
          Upload an Excel file to send reminder emails in bulk.
        </p>

        <div className="flex flex-col md:flex-row md:items-center gap-4">
          <input
            type="file"
            accept=".xlsx"
            onChange={handleFileChange}
            disabled={isLoading}
            className="flex-1 border border-gray-300 rounded px-4 py-2 text-sm bg-white"
          />
          <button
            onClick={handleSubmit}
            disabled={!file || isLoading}
            className={`px-6 py-2 text-sm text-white rounded ${
              file && !isLoading
                ? 'bg-dark-blue hover:bg-sapphire'
                : 'bg-gray-400 cursor-not-allowed'
            }`}
          >
            {isLoading ? 'Sending...' : 'Send Reminder Emails'}
          </button>
        </div>

        {file && (
          <p className="text-secondary text-sm mt-2">Selected file: <strong>{file.name}</strong></p>
        )}

        {error && <p className="text-red-500 text-sm mt-4">{error}</p>}
      </div>

      {/* Submission Output */}
      <div className="max-w-6xl mx-auto">
        <h2 className="text-xl font-bold text-primary mb-2">Submission Output</h2>
        <p className="text-secondary text-sm mb-4">Check the results of your submission.</p>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
          <EnvBox label="Total Records" desc={`${totalRecords}`} />
          <EnvBox label="Processed Records" desc={`${processedRecords}`} />
          <EnvBox label="Emails Sent" desc={`${results.filter(r => r.email_sent).length}`} />
        </div>

        {results.length > 0 && (
          <div className="border-t pt-4 overflow-x-auto">
            <table className="min-w-full text-sm text-left border-collapse">
              <thead className="bg-light-gray text-primary border-b border-medium">
                <tr>
                  <th className="px-4 py-2">Email</th>
                  <th className="px-4 py-2">Last Upload</th>
                  <th className="px-4 py-2">Status</th>
                </tr>
              </thead>
              <tbody>
                {results.map((res, idx) => (
                  <tr key={idx} className="border-b border-gray-100">
                    <td className="px-4 py-2">{res.email}</td>
                    <td className="px-4 py-2">{res.date}</td>
                    <td className="px-4 py-2 font-medium">
                      <span className={res.email_sent ? 'text-green-600' : 'text-red-500'}>
                        {res.email_sent ? '✅ Sent' : '❌ Failed'}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};
