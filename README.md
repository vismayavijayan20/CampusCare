# 🏫 CampusCare – College Complaint Management System

A web-based College Complaint Management System designed to simplify communication between students and college administrators. CampusCare enables students to submit complaints, track their status, and receive notifications about updates.

## 📌 Project Overview

CampusCare is a centralized complaint management platform that helps educational institutions manage student complaints efficiently. Administrators can review complaints, assign priorities, update complaint statuses, and monitor their resolution.

## ✨ Features

### 👨‍🎓 Student Module
- Student registration and login.
- Submit new complaints.
- Upload supporting images.
- Track complaint status.
- View complaint history.
- Receive notifications when complaint status changes.
- View complaint statistics.

### 👨‍💼 Administrator Module
- Secure administrator login.
- View all student complaints.
- Monitor complaint statistics.
- Update complaint status.
- Change complaint priority.
- View uploaded complaint images.
- Manage complaint resolution.

### 🔔 Notification System
- Automatic notifications when complaint status changes.
- Notifications displayed on the student dashboard.
- Complaint update timestamps.

## 🛠️ Technology Stack

| Component | Technology |
|---|---|
| Frontend | HTML5, CSS3, Bootstrap 5 |
| Backend | Python, Flask |
| Database | SQLite |
| ORM | Flask-SQLAlchemy |
| Version Control | Git and GitHub |
| Development Environment | Visual Studio Code |

## 📂 Project Structure

```text
CampusCare/
│
├── instance/
│
├── models/
│   ├── __init__.py
│   └── complaint.py
│
├── static/
│   └── uploads/
│
├── templates/
│   ├── admin_dashboard.html
│   ├── login.html
│   ├── register.html
│   ├── student_dashboard.html
│   └── submit_complaint.html
│
├── app.py
├── config.py
├── create_admin.py
├── requirements.txt
├── .gitignore
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/vismayavijayan20/CampusCare.git
```

### 2. Navigate to the Project Directory

```bash
cd CampusCare
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

For Windows:

```bash
venv\Scripts\activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the Application

```bash
python app.py
```

### 