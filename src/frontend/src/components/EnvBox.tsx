export const EnvBox: React.FC<{ label: string; desc: string }> = ({ label, desc }) => (
  <div className="border border-medium p-4 rounded bg-gray-50">
    <div className="text-xs font-semibold text-gray-600 mb-1">{label}</div>
    <div className="text-sm text-gray-800">{desc}</div>
  </div>
);