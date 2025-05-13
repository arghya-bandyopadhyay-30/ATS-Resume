# ATS-ASAP Code Custodians

## Project Overview
ATS-ASAP is an intelligent system designed to streamline the internal talent matching process. The application efficiently matches candidates with suitable skill sets to open job roles and ensures resume data remains current through automated reminders.

### Key Features
- Intelligent skill-to-role matching based on multiple criteria:
  - Technology stack
  - Years of experience
- Automated resume maintenance:
  - Proactive reminders for resume updates
  - 6-month update cycle monitoring
  - Resume parsing and skill extraction
- Smart matching algorithm:
  - Normalized skill descriptions
  - Intelligent parsing of requirements
  - Accurate candidate-role matching

## Tech Stack
### Frontend
- React with TypeScript
- Tailwind CSS for styling
- Vite as build tool

### Backend
- Python-based API
- Resume parsing module
- Email notification system
- Automated testing suite

## Prerequisites
- Node.js (v16 or higher)
- Python 3.8 or higher
- pip (Python package manager)
- npm

Here is the updated and clean version of your **Project Setup Guide**, now with the **step to create a `.venv`** added at the top:

---

# Project Setup Guide

## 1. Create and Activate the Virtual Environment

At the root of the project:

```bash
python3 -m venv .venv              # Create virtual environment
```
```bash
source .venv/bin/activate          # For macOS/Linux
````
#### OR
```bash
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
   SENDER_EMAIL=your_email@example.com
   SENDER_PASSWORD=your_email_password
   GROQ_API_KEY=your_groq_api_key
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
