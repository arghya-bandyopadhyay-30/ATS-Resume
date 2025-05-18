# ATS-ASAP Code Custodians

**An internal system to match resumes to open roles and keep resume data updated.**

---

## Testing
Use the following for testing as we have used Mock data, we need to be specific with the format:

- **Staffing Assistant:** [Job Description Sample](Testing%20Samples/Job%20Description%20Sample)

- **Resume Update Notifier:** [Resume Upload Excel Sample.xlsx](Testing%20Samples/Resume%20Upload%20Excel%20Sample.xlsx)

---

## Overview

ATS-ASAP Code Custodians is an intelligent full-stack application designed for internal talent management. It streamlines the process of mapping candidate skillsets to open roles and ensures that resumes stay current through automated reminders.

### Key Features
- **Skill-to-Role Matching**: Matches resumes based on tech stack and years of experience.
- **Automated Resume Maintenance**: Sends reminders for updating resumes every 6 months.
- **Resume Parsing & Skill Extraction**: Extracts and normalizes skills from uploaded resumes.
- **Intelligent Matching Algorithm**: Normalizes candidate attributes for accurate matching to roles.

---

## Tech Stack

### Frontend
- `React` with `TypeScript`
- `Tailwind` CSS
- `Vite`

### Backend
- `Python`
- `FastAPI` + `Uvicorn`
- Email Notification System
- Resume Parsing Module
- Testing with `pytest`

---

## Prerequisites

Ensure the following are installed on your system:
- [Node.js](https://nodejs.org/) (v16 or higher)
- [Python](https://www.python.org/) (3.8 or higher)
- [npm](https://www.npmjs.com/)
- [pip](https://pip.pypa.io/)

---

## Project Setup Guide

### 1. Clone the Repository
```bash
git clone https://github.com/arghya-bandyopadhyay-30/ATS-Resume.git
cd ats-asap-code-custodians
```

---

# Project Setup Guide

## 1. Create and Activate the Virtual Environment

At the root of the project:

```bash
python3 -m venv .venv              # Create virtual environment
```
```bash
source .venv/bin/activate          # For macOS/Linux

.venv\Scripts\activate             # For Windows
```

---

## 2. Configure Environment Variables

At the root of the project:

1. Copy the [environment template](env-template) file:

   ```bash
   cp env-template .env
   ```

2. Update the `.env` file with your credentials:

   ```
   SENDER_EMAIL=your_email@example.com        # Replace with your sender email address (e.g., "christsomalina@gmail.com")
   SENDER_PASSWORD=your_email_password        # Replace with your email's app-specific password (e.g., "mlmd eaxt pdco skgl")
   GROQ_API_KEY=your_groq_api_key             # Get your API key from: https://console.groq.com/keys
   ```

---

## 3. Install Python Dependencies

Install all required Python packages:

```bash
pip install -r requirements.txt
```

---

## 4. Start the Backend Server (Only)

To run the backend server independently:

```bash
cd src/backend
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

---

## Full Application Setup (Frontend + Backend)

### 1. Navigate to Frontend Directory

```bash
cd src/frontend
```

### 2. Install Node.js Dependencies

```bash
npm install
```

### 3. Start the Full Development Server

```bash
npm run dev:all
```

This will start both the frontend and backend servers concurrently in development mode.

---

## Testing

### Backend Tests

To run backend tests for the resume parser:

```bash
python -m pytest src/backend/test_resume_parser -v
```

---

## Project Structure

```
root/
├── docker/                         # Docker setup files
├── src/
│   ├── backend/
│   │   ├── email_sender/           # Email functionality
│   │   ├── resume_parser/          # Resume parsing logic
│   │   ├── test_email_sender/      # Tests for email sender
│   │   ├── test_resume_parser/     # Tests for resume parser
│   │   ├── api.py                  # API routing
│   │   ├── settings.py             
│   │   └── web.py                  
│   └── frontend/
│       ├── node_modules/           # Node dependencies
│       ├── public/                 # Static assets (favicon, etc.)
│       └── src/
│           ├── assets/             # Images, fonts, etc.
│           ├── components/         # React components
│           ├── pages/              # Page-level components
│           ├── App.tsx
│           ├── config.ts
│           ├── index.css
│           ├── main.tsx
│           └── vite-env.d.ts
```

---

## Contributing

1. Fork the repository.
2. Create a new feature branch.
3. Commit your changes with clear and meaningful messages.
4. Push the changes to your forked repository.
5. Open a Pull Request for review and merge.

---

## License

This project is proprietary and confidential. Unauthorized use or distribution is strictly prohibited.

---

## Support

For support, issues, or feature requests, please contact the development team directly.
