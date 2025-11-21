# 🎓 Student Management System

A modern, full-stack student management application with a beautiful dark theme UI.

## Features

- ✅ Add, Edit, Delete Students
- ✅ View All Students with Sorting
- ✅ Calculate Percentage & Grades Automatically
- ✅ Modern Dark Theme UI/UX
- ✅ Responsive Design
- ✅ Dummy Data Generator
- ✅ RESTful API

## Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite
- **Server**: Gunicorn

## Local Setup

1. **Install Python 3.11+**
   ```bash
   python --version
   ```

2. **Install Dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Run the Application**
   ```bash
   python app.py
   ```

4. **Access the App**
   - Open browser: `http://127.0.0.1:5000`

## Deployment Options

### 🚀 Option 1: Railway (Recommended - Easiest)

1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub"
4. Select your repository
5. Railway auto-detects Python and deploys!
6. Add environment variable: `PORT` (auto-set by Railway)

**Cost**: Free tier available (500 hours/month)

---

### 🌐 Option 2: Render

1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Click "New" → "Web Service"
4. Connect your GitHub repository
5. Settings:
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `cd backend && gunicorn -w 4 -b 0.0.0.0:$PORT app:app`
   - **Environment**: Python 3
6. Deploy!

**Cost**: Free tier available (spins down after 15 min inactivity)

---

### ⚡ Option 3: Vercel

1. Install Vercel CLI:
   ```bash
   npm i -g vercel
   ```

2. Create `vercel.json`:
   ```json
   {
     "version": 2,
     "builds": [
       {
         "src": "backend/app.py",
         "use": "@vercel/python"
       }
     ],
     "routes": [
       {
         "src": "/(.*)",
         "dest": "backend/app.py"
       }
     ]
   }
   ```

3. Deploy:
   ```bash
   vercel
   ```

**Cost**: Free tier available

---

### 🐳 Option 4: Docker + Any Platform

1. Create `Dockerfile` in root:
   ```dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   COPY backend/requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   WORKDIR /app/backend
   CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]
   ```

2. Deploy to:
   - Railway
   - Render
   - Fly.io
   - DigitalOcean App Platform

---

### ☁️ Option 5: PythonAnywhere

1. Go to [pythonanywhere.com](https://www.pythonanywhere.com)
2. Sign up (free tier available)
3. Upload your code via Git or Files
4. Configure Web App:
   - Source code: `/home/username/student-management/backend`
   - WSGI file: Point to `app.py`
5. Reload!

**Cost**: Free tier available (limited)

---

## Environment Variables

For production, set:
- `PORT`: Server port (auto-set by most platforms)
- `FLASK_DEBUG`: Set to `0` for production

## Project Structure

```
student-management/
├── backend/
│   ├── app.py              # Flask application
│   ├── db.py               # Database setup
│   ├── models.py           # Business logic
│   ├── requirements.txt    # Python dependencies
│   ├── students.db         # SQLite database (auto-created)
│   └── frontend/
│       ├── index.html
│       ├── add.html
│       ├── edit.html
│       └── assets/
│           ├── style.css
│           └── script.js
├── Procfile               # For Railway/Heroku
├── runtime.txt            # Python version
└── README.md
```

## API Endpoints

- `GET /api/students` - Get all students
- `POST /api/students` - Add new student
- `GET /api/students/<roll>` - Get student by roll
- `PUT /api/students/<roll>` - Update student
- `DELETE /api/students/<roll>` - Delete student
- `GET /api/students/sorted` - Get sorted by percentage
- `GET /api/students/count` - Get total count
- `POST /api/students/dummy` - Add dummy data

## License

MIT License - Feel free to use!

## Support

For issues or questions, open an issue on GitHub.

---

**Made with ❤️ using Flask & Modern Web Technologies**

