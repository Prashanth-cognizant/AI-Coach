# AI Coach Frontend - Quick Start Guide

## Installation

### 1. Install Dependencies
```bash
npm install
```

### 2. Create Environment File
Create `.env` file in frontend folder:
```
REACT_APP_API_URL=http://localhost:8000/api
```

### 3. Run Development Server
```bash
npm start
```

App opens at: http://localhost:3000

### 4. Build for Production
```bash
npm run build
```

## Pages

- `/login` - User login
- `/register` - New user registration
- `/dashboard` - Main dashboard with stats
- `/sessions` - Log and view coaching sessions
- `/chat` - Chat with AI Coach
- `/profile` - User profile management

## Features

### Dashboard
- Real-time statistics (workouts, calories, weight, mood)
- Weight progress chart
- Workout activity chart
- Recent sessions list

### Sessions
- Log new coaching sessions
- Select session type
- Track exercises and calories
- Mood before/after tracking
- AI recommendations

### AI Chat
- Ask fitness questions
- Get instant coaching tips
- Chat history
- Quick tips sidebar

### Profile
- View and edit user information
- Track weight progress
- View account details
- Calculate BMI and progress

## Authentication

Uses JWT tokens stored in localStorage
- Token expires after 30 minutes
- Auto-redirect to login if token invalid
- Logout clears token and redirects

## Styling

Modern gradient design with:
- Purple gradient theme
- Smooth animations
- Responsive grid layouts
- Mobile-friendly design
- Interactive hover effects

## Components Used

- React Router for navigation
- Axios for API calls
- Recharts for data visualization
- Custom CSS for styling

## Development Tips

- Keep API URL in sync with backend
- Clear browser cache if styles don't update
- Check console for API errors
- Use React DevTools for debugging

## Deployment

Frontend can be deployed to:
- Vercel
- Netlify
- GitHub Pages
- Any static hosting

Just run `npm run build` and deploy the `build` folder.
