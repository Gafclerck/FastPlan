# FastPlan — CS50 Final Project

FastPlan is a role-based timetable management web application designed to help educational institutions organize academic scheduling in a centralized system. The platform allows administrators to manage professors, courses, classes, and weekly schedules while providing professors and students with personalized views of their academic information.

This project was developed as the **final project for Harvard's CS50 course** using a lightweight but structured full-stack architecture based on **Flask**, **Jinja**, and **SQLAlchemy Core**.

The application is designed for French-speaking academic environments, therefore the **user interface is mostly in French**, while the **codebase remains in English** to maintain clarity and good development practices.

---

# Project Overview

FastPlan simplifies timetable management by providing a centralized system where different actors within a school can interact with scheduling data according to their responsibilities.

The system defines **three main user roles**:

- **Manager (Gestionnaire)** — the administrator who manages the academic structure and schedules
- **Professor** — teachers who manage their availability and consult their timetable
- **Student** — users who can view their assigned courses and class timetable

Each role has access to a dedicated interface adapted to its needs.

---

# Features

## Manager Features

The **manager** acts as the administrator of the platform and has full control over the academic organization.

Main capabilities include:

- Creating and managing **professors**
- Creating and managing **classes**
- Creating **courses**
- Assigning **courses to professors**
- Assigning **courses to classes**
- Creating **teaching sessions (seances)**
- Building and viewing **class timetables**
- Viewing **professor availability**
- Monitoring the system through a **dashboard summary**

The manager dashboard provides quick insights such as:

- recently created professors
- newly created classes
- course assignments
- timetable overview

---

## Professor Features

Professors interact with the platform to manage their teaching schedule and availability.

A professor can:

- View their **weekly timetable**
- Declare **weekly availability**
- See the **courses they teach**
- See the **classes assigned to them**

The availability system allows professors to indicate when they are available to teach during the week. This information helps the manager schedule sessions efficiently.

---

## Student Features

Students have a **read-only interface** focused on viewing information related to their academic schedule.

Students can:

- View the **courses assigned to their class**
- View their **weekly timetable**

Students cannot modify data in the system.

---

# Authentication

FastPlan includes a secure authentication system.

Users must log in to access the application according to their role.

Authentication features include:

- Login system
- Student self-registration
- Password hashing
- Session-based authentication
- Flash messages for feedback

Flask utilities such as `session` and `flash` are used to manage authentication flow and user notifications.

---

# Technology Stack

## Backend

- **Flask** — web framework
- **Jinja** — server-side HTML templating
- **SQLAlchemy Core** — database access layer
- **SQLite** — default database engine

Instead of using SQLAlchemy's ORM layer, the project uses **SQLAlchemy Core** in order to:

- keep SQL queries explicit
- maintain full control over database interactions
- stay closer to raw SQL logic
- centralize query logic inside repositories

---

## Frontend

The interface is built with:

- **Bootstrap 5** for layout and responsive design
- **Custom CSS** for dashboard styling
- **Custom JavaScript** for small UI interactions

Bootstrap was chosen both for its productivity and as an opportunity to practice building interfaces with a modern CSS framework.

---

# Application Architecture

The application follows a **layered architecture** that separates concerns between routing, business logic, data access, and validation.

The main layers are:

### Blueprints

Routes are grouped into **Flask blueprints** based on user roles:

- `auth`
- `manager`
- `professor`
- `student`

This keeps routing logic modular and organized.

---

### Controllers

Controllers contain the **application logic**.  
They validate inputs, orchestrate operations, and call repository functions to interact with the database.

Examples:

- authentication logic
- course assignment logic
- timetable generation
- availability management

---

### Repositories

Repositories contain **database queries written with SQLAlchemy Core**.

They provide a clean abstraction layer between the controllers and the database by centralizing SQL queries.

---

### Validators

Validators ensure that user inputs are valid before being processed by the system.

Examples include validation for:

- user data
- courses
- classes
- professors
- students

---

# Scheduling Model

The scheduling system is built around three core entities:

- **time_slot**
- **seances**
- **class_seance**

Each **seance** occupies a single time slot.

If a course requires multiple consecutive slots, it is represented as **multiple seances**.

This design simplifies the timetable grid while keeping the scheduling logic flexible.

---

# Database Model

The main tables used in the system include:

- `users`
- `profs`
- `students`
- `classes`
- `courses`
- `course_class`
- `time_slot`
- `availability`
- `seances`
- `class_seance`

These tables allow the system to represent:

- user roles
- academic structure
- professor availability
- course assignments
- class schedules

---

# Setup and Installation

The project uses Python virtual environments and installs dependencies from `requirements.txt`.

### Create a virtual environment

```powershell
python -m venv env
```

### Activate the environment

```powershell
.\env\Scripts\Activate.ps1
```

### Install dependencies

```powershell
pip install -r requirements.txt
```

### Run the Flask application

```powershell
$env:FLASK_APP = "app"
flask run
```

The application will automatically create the database tables on startup and store data in:

```
database.db
```

---

# Seeding Time Slots

To initialize the weekly timetable grid, run:

```powershell
python seed_time_slots.py
```

This script seeds the following schedule:

Days:

- Monday → Sunday

Time slots:

- 08:00 – 10:00
- 10:00 – 12:00
- 13:00 – 15:00
- 15:00 – 17:00
- 17:00 – 19:00

---

# Configuration

Default configuration can be overridden with environment variables:

- `DATABASE_URL`
- `SECRET_KEY`

These values can also be defined inside:

```
app/instance/config.py
```

---

# Project Structure

```
FastPlan
│
├── README.md
├── requirements.txt
├── .gitignore
├── instance
│   └── config.py
    |   database.db
├── seed_time_slots.py
├── app
│
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│
│
│   ├── blueprints
│   │   ├── auth
│   │   │   └── auth.py
│   │   │
│   │   ├── manager
│   │   │   ├── prof.py
│   │   │   └── routes.py
│   │   │
│   │   ├── professor
│   │   │   └── routes.py
│   │   │
│   │   └── student
│   │       └── routes.py
│
│   ├── controllers
│   │   ├── auth_controller.py
│   │   ├── availability_controller.py
│   │   ├── class_controller.py
│   │   ├── course_controller.py
│   │   ├── prof_controller.py
│   │   ├── seance_controller.py
│   │   └── student_controller.py
│
│   ├── repositories
│   │   ├── user_repo.py
│   │   ├── student_repo.py
│   │   ├── professor_repo.py
│   │   ├── course_repo.py
│   │   ├── class_repo.py
│   │   ├── availability_repo.py
│   │   └── seance_repo.py
│
│   ├── validators
│   │   ├── user_validator.py
│   │   ├── student_validator.py
│   │   ├── prof_validator.py
│   │   ├── course_validator.py
│   │   └── class_validator.py
│
│   ├── models
│   │   ├── user.py
│   │   ├── student.py
│   │   ├── professor.py
│   │   ├── course.py
│   │   └── classe.py
│
│   ├── static
│   │   ├── style.css
│   │   └── script.js
│
│   └── templates
│       ├── auth
│       ├── manager
│       ├── professor
│       └── student
```

---

# Design Decisions

Several architectural decisions were made to keep the project both educational and realistic:

- **SQLAlchemy Core instead of ORM** to maintain full control over SQL queries.
- **Repository pattern** to centralize database logic.
- **Blueprints by role** to keep the application modular.
- **Server-rendered templates** to keep the scope manageable for a CS50 project.
- **Slot-based scheduling model** to simplify timetable visualization.

---

# Future Improvements

Possible extensions include:

- Automatic timetable generation algorithms
- Conflict detection between professors and classes
- Drag-and-drop timetable editing
- API endpoints for integration with other systems
- Notifications for schedule changes
- Role-based permissions management
- Moving to SqlAlchemy ORM

---

# Author

**Amadou Abdoul-Gafar**

CS50 Final Project

``