# Gemini Workspace Documentation

This document provides an overview of the project structure, technologies used, and key configurations to assist Gemini in understanding and interacting with this workspace.

## Project Overview

This project is a customer support bot with a web-based frontend for user interaction, an admin dashboard for management, and a Python-based backend that leverages AI and machine learning for customer support.

## Technologies

### Backend (`./backend`)

- **Framework:** Django
- **API:** Django REST Framework
- **AI & Machine Learning:**
  - `langgraph`
  - `langchain` (including `langchain-openai`, `langchain-community`)
  - `pinecone` (for vector storage)
- **Dependencies:** `django-cors-headers`, `djangorestframework-simplejwt`, `drf-spectacular`, `nltk`
- **Python Version:** 3.13

### Frontend (`./frontend`)

- **Framework:** Next.js (v15.4.5)
- **Language:** TypeScript
- **UI:** React (v19.1.0)
- **Styling:** Tailwind CSS
- **Dependencies:** `axios`, `react-icons`, `react-markdown`

### Admin App (`./admin-app`)

- **Framework:** Next.js (v15.4.6)
- **Language:** TypeScript
- **UI:** React (v19.1.0)
- **Styling:** Tailwind CSS

## Project Structure

The project is a monorepo with three main components:

- **`admin-app/`**: A Next.js application for the admin dashboard.
- **`backend/`**: A Django application that serves the API and handles the AI/ML logic.
- **`frontend/`**: A Next.js application for the main user-facing chat interface.

## Key Files

- **`backend/manage.py`**: The Django management script for running the server, migrations, and other administrative tasks.
- **`backend/core/settings.py`**: The main Django settings file.
- **`backend/Pipfile`**: Defines the Python dependencies for the backend.
- **`frontend/package.json`**: Defines the dependencies and scripts for the frontend application.
- **`admin-app/package.json`**: Defines the dependencies and scripts for the admin dashboard application.
- **`frontend/src/app/page.tsx`**: The main page for the user-facing chat interface.
- **`admin-app/src/app/page.tsx`**: The main page for the admin dashboard.

## Common Commands

### Backend

- **Run the development server:**
  ```bash
  cd backend
  pipenv run python manage.py runserver
  ```
- **Apply database migrations:**
  ```bash
  cd backend
  pipenv run python manage.py migrate
  ```

### Frontend & Admin App

- **Run the development server:**
  ```bash
  # For the frontend
  cd frontend
  npm run dev

  # For the admin app
  cd admin-app
  npm run dev
  ```
- **Build for production:**
  ```bash
  # For the frontend
  cd frontend
  npm run build

  # For the admin app
  cd admin-app
  npm run build
  ```
- **Run linters:**
  ```bash
  # For the frontend
  cd frontend
  npm run lint

  # For the admin app
  cd admin-app
  npm run lint
  ```