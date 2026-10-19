# NOU e-Gyan LMS — NextGen 🎓

### Enhanced Learning Management System | Django | Python

An enhanced, full-stack Learning Management System (LMS) inspired by the NOU e-Gyan Portal. This project aims to bring academic administration, digital learning resources, assignments, online assessments, attendance tracking, virtual classes, and programming practice into one centralized web application.

> **Project Status:** 🚧 Active Development  
> **Version:** 2.0 — Enhanced Edition

---

## 📌 About the Project

NOU e-Gyan LMS — NextGen is the enhanced version of my previously developed NOU e-Gyan Portal project.

The basic version established the foundation for a Django-based learning management system. This enhanced version focuses on expanding academic workflows, improving the user interface, strengthening authentication and authorization, and organizing features for maintainability and future deployment.

The system provides dedicated interfaces for Super Admins, Teachers, and Students, with functionality tailored to their respective responsibilities.

The long-term goal is to evolve the project into a maintainable, secure, and deployment-ready academic management platform.

## 🎯 Project Objectives

- Digitize academic administration and learning activities.
- Provide centralized management of courses, subjects, teachers, and students.
- Make digital study materials accessible to authorized students.
- Simplify assignment submission, grading, and feedback.
- Support online MCQ assessments and automated result calculation.
- Maintain attendance records and academic reports.
- Facilitate online classes and programming practice.
- Improve communication through announcements and notifications.
- Build a modular foundation for future enhancements and deployment.

## ✨ Key Features

### 🔐 1. Authentication & Access Management
- Unified login interface for supported user types.
- Role-specific dashboards for Super Admin, Teacher, and Student.
- Session management and logout functionality.
- Access control based on user roles.
- Email-based delivery of account credentials.

### 🏛️ 2. Super Admin Dashboard
- Manage academic sessions, courses, and subjects.
- Create and manage teacher and student records.
- Map teachers to academic subjects.
- Upload multiple student records using CSV files.
- Manage study materials, assignments, and online tests.
- Review academic results and attendance reports.
- Manage announcements and notifications.
- Schedule online classes.

### 👨‍🏫 3. Teacher Dashboard
- View assigned courses and subjects.
- Upload course-wise and subject-wise study materials.
- Create assignments with deadlines and instructions.
- Review student submissions and provide marks and feedback.
- Create MCQ tests and manage question banks.
- Import test questions through CSV files.
- Mark attendance and review relevant records.
- Schedule online classes and access announcements.

### 👨‍🎓 4. Student Dashboard
- Access assigned academic information.
- View and access study materials.
- Submit assignments and track feedback.
- Attempt available MCQ tests.
- View test results and marks.
- Check attendance records.
- Join scheduled online classes.
- Practice programming in the online coding environment.
- Review recent code execution history.
- Access notifications, profile information, and help resources.

### 📚 5. Academic Management
- Academic session management.
- Course and subject management.
- Teacher and student record management.
- Course, semester, and subject mapping.
- Active/inactive status management.

### 📝 6. Assignment & Assessment Management
- Assignment creation and submission.
- Submission status tracking.
- Marks and feedback management.
- MCQ-based online tests.
- Question bank management.
- Bulk question import using CSV.
- Automatic scoring and result records.

### 📊 7. Attendance Management
- Record student attendance by date and subject.
- Associate attendance with the relevant academic records.
- Avoid duplicate entries for the same student, subject, and date.
- Provide authorized attendance reports.
- Allow students to review their attendance.

### 🎥 8. Online Class Integration
- Schedule online classes.
- Associate classes with courses, subjects, and teachers.
- Generate meeting links through Google Meet integration.
- Provide eligible students with access to scheduled classes.

### 💻 9. Student Programming Lab
- Browser-based code editor and execution interface.
- Support for multiple programming languages through Judge0 integration.
- Standard input and output handling.
- Execution status, time, and memory information where available.
- Recent code execution history.

### 📢 10. Announcements & Notifications
- Publish announcements for relevant audiences.
- Organize notifications by module and audience.
- Display relevant updates on user dashboards.

*Feature availability may vary while the enhanced version is under development.*

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Django | Web framework and application logic |
| Django ORM | Database operations |
| SQLite | Development database |
| HTML5 | Page structure |
| CSS3 | Styling and responsive layouts |
| JavaScript | Client-side interactivity |
| Bootstrap | Responsive UI components |
| Google OAuth 2.0 / Google Meet API | Online class integration |
| Judge0 API | Online code execution |
| SMTP / Django Email | Email delivery |
| Visual Studio Code | Development environment |
| Git & GitHub | Version control and source management |

**Database note:** SQLite is used during the current development phase. A production deployment may require a more suitable database configuration based on the application's operational requirements.

## 🏗️ Application Architecture

The application follows Django's model-template-view approach.

- **Models:** Define academic entities and database relationships.
- **Views:** Handle requests, validation, permissions, and application logic.
- **Templates:** Render dashboards, forms, tables, and other user interfaces.
- **URLs:** Route requests to the appropriate views.
- **Static files:** Store CSS, JavaScript, icons, and other frontend assets.
- **Media files:** Store uploaded study materials and assignment attachments.

The application is being developed as a modular Django web application, with an emphasis on separating responsibilities and keeping the code maintainable.

## 📂 Project Modules

| Module | Purpose |
|---|---|
| Authentication | Login, logout, and session handling |
| Academic Sessions | Manage academic years/sessions |
| Courses & Subjects | Organize academic offerings |
| Teacher Management | Manage teacher records and assignments |
| Student Management | Manage enrollment and student records |
| Study Materials | Publish digital learning resources |
| Assignments | Submission, grading, and feedback |
| Online Tests | MCQ assessments and results |
| Attendance | Attendance records and reports |
| Online Classes | Scheduling and meeting links |
| Programming Lab | Code execution and history |
| Announcements | Academic updates and notices |
| Notifications | Relevant user notifications |
| Profiles & Help | User information and student support |
| Email Management | Account credential delivery |

## 📁 Project Structure

```text
nouLMS/
│
├── myapp/
│   ├── migrations/
│   ├── static/
│   │   ├── css/
│   │   ├── images/
│   │   └── js/
│   │
│   ├── templates/
│   │   ├── admin/
│   │   │   └── add_course.html
│   │   │   └── session.html
│   │   │   └── adminbase.html
│   │   │   └── admindash.html
│   │   │   └── delete_course.html
│   │   │   └── delete_session.html
│   │   │   └── edit_course.html
│   │   │   └── edit_session.html
│   │   │   └── view_courses.html
│   │   │   └── view_session.html
│   │   ├── teacher/
│   │   │   └── teacherdash.html
│   │   └── index.html
│   │
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
│
├── nouLMS/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── db.sqlite3
├── manage.py
└── README.md
```

### Folder & File Description

- **myapp/** — Contains application logic, models, views, templates, static assets, and migrations.
- **myapp/templates/** — Contains HTML templates for different sections of the application.
- **myapp/static/** — Stores CSS, JavaScript, and image assets.
- **myapp/models.py** — Defines database models.
- **myapp/views.py** — Handles application views and request processing.
- **myapp/admin.py** — Registers models with Django Admin.
- **nouLMS/settings.py** — Contains Django project configuration.
- **nouLMS/urls.py** — Defines project-level URL routing.
- **nouLMS/asgi.py** and **nouLMS/wsgi.py** — Provide ASGI and WSGI application entry points.
- **manage.py** — Provides Django management commands.
- **db.sqlite3** — SQLite database file used by the project.


## ⚙️ Getting Started

Follow these steps to run the project locally after cloning the repository.

### Prerequisites

Install the following tools:

- Python
- Git
- Visual Studio Code or another code editor

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/nou-egyan-lms-nextgen.git
cd nou-egyan-lms-nextgen
```

Replace `YOUR-USERNAME` with your GitHub username.

### 2. Create a Virtual Environment

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

If a `requirements.txt` file is available:

```bash
pip install -r requirements.txt
```

If it has not been created yet, generate and review it from the project's working environment before publishing the repository.

### 4. Configure Environment Variables

Create a local `.env` file for sensitive configuration such as:

- Django secret key
- Debug settings
- Database configuration, if applicable
- Email/SMTP credentials
- Google OAuth credentials
- Judge0 API configuration

Use the environment variable names expected by the application. Never commit real credentials or production secrets to GitHub.

### 5. Apply Database Migrations

```bash
python manage.py migrate
```

### 6. Create a Superuser

```bash
python manage.py createsuperuser
```

### 7. Run the Development Server

```bash
python manage.py runserver
```

Open the local development URL displayed by Django in your terminal.

> **Note:** These instructions assume a conventional Django project layout. Additional configuration or setup steps may be required depending on the current repository structure and third-party integrations.

## 🔒 Security & Development Practices

The enhanced version aims to follow these practices:

- Enforce server-side authorization for protected operations.
- Keep secrets and API credentials outside version control.
- Validate user input and uploaded files.
- Use Django's password handling and authentication mechanisms appropriately.
- Configure production settings separately from development settings.
- Use HTTPS and secure cookie settings in production.
- Review third-party API access, error handling, and rate limits.
- Add automated tests for critical workflows.
- Maintain database migrations and document configuration requirements.

These are development goals and configuration requirements; they should be verified before the application is described as production-ready.

## 🗺️ Development Roadmap

- [x] Complete the initial basic version of the NOU e-Gyan Portal.
- [x] Establish the initial Django application and academic workflows.
- [ ] Organize and enhance the application architecture.
- [ ] Improve the visual consistency of dashboards and forms.
- [ ] Strengthen role-based access control and session handling.
- [ ] Refine academic session, course, subject, teacher, and student workflows.
- [ ] Enhance assignment submission and grading workflows.
- [ ] Refine online assessment and result management.
- [ ] Improve attendance reporting and validation.
- [ ] Complete and verify Google Meet integration.
- [ ] Complete and verify Judge0 code execution integration.
- [ ] Improve automated testing and error handling.
- [ ] Finalize environment-based configuration and deployment settings.
- [ ] Evaluate production database and hosting options.
- [ ] Prepare deployment documentation.

*Update the checklist as each feature is implemented and tested.*

## 🚀 Future Enhancements

Potential improvements include:

- PostgreSQL support for production deployments.
- More comprehensive automated tests.
- Improved logging and monitoring.
- Better reporting and academic analytics.
- Notification and email reliability improvements.
- Cloud deployment and scalable file storage.
- Mobile-friendly enhancements and possible mobile application support.
- CI/CD workflows for automated checks and deployment.

## 🎓 Learning Outcomes

This project provides practical experience in:

- Python and Django web development.
- Relational database design and ORM operations.
- Authentication, sessions, and access control.
- Full-stack integration using HTML, CSS, JavaScript, and Bootstrap.
- Academic workflow design and implementation.
- REST/API integrations and external service configuration.
- File uploads, CSV processing, and validation.
- Git, GitHub, debugging, and iterative software development.

## 👨‍💻 Developer

**Sandeep Shahu**

B.Tech Computer Science (AI & ML) Student | Python & Django Developer

- GitHub: [@sandeepshahu33](https://github.com/sandeepshahu33)
- Portfolio: [View Portfolio](https://sandeepshahu33.github.io/Portfolio/)

## 🤝 Contributions

Suggestions, bug reports, and improvement ideas are welcome. For substantial changes, consider opening an issue before submitting a pull request.

## 📄 License

A license has not yet been specified. Add an appropriate license file before permitting reuse or redistribution of the source code.

---

**NOU e-Gyan LMS — NextGen**  
*Building a better digital learning experience, one feature at a time.*
