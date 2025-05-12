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
- npm or yarn

## Installation

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd src/backend
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd src/frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   # or
   yarn install
   ```

## Running the Application

### Start Backend Server
1. Activate the virtual environment (if not already activated):
   ```bash
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Start the backend server:
   ```bash
   run.sh
   ```
   The backend server will run on `http://localhost:5000`

### Start Frontend Development Server
1. In a new terminal, navigate to the frontend directory:
   ```bash
   cd src/frontend
   ```

2. Start the development server:
   ```bash
   npm run dev
   # or
   yarn dev
   ```
   The frontend will be available at `http://localhost:5173`

## Testing
### Backend Tests
```bash
cd src/backend
python -m pytest
```

### Frontend Tests
```bash
cd src/frontend
npm run test
# or
yarn test
```

## Project Structure
```
src/
├── frontend/           # React frontend application
│   ├── src/            # Source files
│   ├── public/         # Static assets
│   └── package.json    # Frontend dependencies
│
├── backend/            # Python backend application
│   ├── api.py          # Main API endpoints
│   ├── resume_parser/  # Resume parsing module
│   ├── email_sender/   # Email notification system
│   └── settings.py     # Configuration settings
│
└── utils/              # Shared utilities
```

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License
This project is proprietary and confidential.

## Support
For support and questions, please contact the development team.
