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

