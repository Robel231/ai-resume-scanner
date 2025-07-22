# System Architecture

This document outlines the architecture of the AI Resume Scanner application. The system is designed as a microservices-style architecture, containerized with Docker, and orchestrated with Docker Compose for local development.

## Architecture Diagram
Use code with caution.
Markdown
+------------------+ +------------------+
| User Browser |----->| Next.js |
+------------------+ | (Frontend @:3000) |
+--------+---------+
| (API Calls)
v
+----------------------------------+----------------------------------+
| Backend Network |
| |
| +-----------------------------------------------------------------+ |
| | FastAPI API (@:8000) | |
| +-----------------------------------------------------------------+ |
| | | | | |
| | | (Auth/Rate Limit) | | (Analysis) |
| v v v v |
| +--------+ +--------+ +-----------+ +------------+ |
| | Redis | | PostgreSQL |----->| OpenAI API | |
| | (@:6379) | | (DB @:5432) | +-----------+ +------------+ |
| +--------+ +--------+ |
| |
+----------------------------------------------------------------------+
Generated code
## Component Breakdown

1.  **Client (Next.js):**
    -   **Framework:** Next.js with React/TypeScript.
    -   **Role:** Provides the complete UI/UX. Handles user registration/login, file uploads, and renders the analysis results.
    -   **Communication:** Interacts with the FastAPI backend via REST API calls.

2.  **API Server (FastAPI):**
    -   **Framework:** FastAPI (Python).
    -   **Role:** The core business logic engine.
    -   **Responsibilities:**
        -   **Authentication:** Manages JWT creation and validation.
        -   **PDF Processing:** Extracts text from uploaded PDF resumes.
        -   **AI Integration:** Constructs prompts and communicates with the OpenAI API.
        -   **Database Interaction:** Stores user data and analysis history in PostgreSQL.
        -   **Rate Limiting:** Uses Redis to control API usage per user.

3.  **Database (PostgreSQL):**
    -   **Role:** The primary data store for persistent data.
    -   **Data Stored:** User accounts (with hashed passwords), job descriptions, and historical analysis results.

4.  **Cache (Redis):**
    -   **Role:** High-speed, in-memory data store.
    -   **Primary Use:** Caching frequently accessed data and tracking API requests for rate-limiting purposes.

5.  **Containerization (Docker & Docker Compose):**
    -   **Role:** Ensures a consistent and reproducible development environment.
    -   **`Dockerfile`:** Each service (frontend, backend) has its own Dockerfile defining its image.
    -   **`docker-compose.yml`:** Defines and links all the services (`api`, `frontend`, `db`, `redis`) so they can be run with a single command.