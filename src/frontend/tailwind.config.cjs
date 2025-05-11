// src/frontend/tailwind.config.cjs
module.exports = {
  // tell Tailwind where your template files live:
  content: [
    './index.html',
    './src/**/*.{js,jsx,ts,tsx}',
  ],
  theme: {
    extend: {},    // you can drop in custom colors & spacing here later
  },
  plugins: [],
}
