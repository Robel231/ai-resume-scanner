# AI-Powered Resume Scanner & Job Matcher

![AI Resume Scanner Showcase](httpshttps://github.com/Robel231/ai-resume-scanner/blob/main/showcase.gif?raw=true)

This is a full-stack web application designed to demystify the job application process. It provides users with instant, AI-driven feedback on how their resume aligns with a specific job description.

The application is built with a modern, scalable, and production-ready architecture. It features a secure authentication system, a robust FastAPI backend that orchestrates AI analysis and data persistence, and a luxurious, fully interactive frontend built with Next.js.

The goal of this project was to build a complete, end-to-end product that solves a real-world problem for job seekers, demonstrating skills in backend development, frontend design, AI integration, and DevOps.

---

## 🔥 Key Features

-   **Secure User Authentication:** JWT-based registration and login system with password hashing.
-   **AI-Powered Analysis:** Leverages large language models (via Groq/OpenAI) to provide nuanced feedback.
-   **Dynamic PDF Parsing:** Extracts text directly from uploaded PDF resumes using PyMuPDF.
-   **Comprehensive Reporting:** Generates a beautiful, easy-to-read report including a match score, strengths, gaps, and actionable advice.
-   **API Protection:** Implements Redis-based rate limiting to prevent abuse and control costs.
-   **Interactive UI:** A luxurious, responsive frontend built with Next.js, featuring animations, glassmorphism, and a premium feel.

## 🛠️ Tech Stack

| Category      | Technology                                    |
| ------------- | --------------------------------------------- |
| **Frontend**  | Next.js, React, TypeScript, React Icons       |
| **Backend**   | FastAPI (Python)                              |
| **AI Model**  | Groq (Llama 3) / OpenAI (GPT-3.5)             |
| **Database**  | PostgreSQL                                    |
| **Cache**     | Redis (for Rate Limiting)                     |
| **API Libs**  | SQLAlchemy, Pydantic, Passlib, python-jose, SlowAPI |
| **Containerization** | Docker & Docker Compose                       |

---

## 🚀 Running Locally

This project is fully containerized, making local setup incredibly simple and reliable.

### Prerequisites

-   [Docker](https://www.docker.com/products/docker-desktop/) installed and running.
-   An AI provider API Key (e.g., from [Groq](https://console.groq.com/)).

### Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Robel231/ai-resume-scanner.git
    cd ai-resume-scanner
    ```

2.  **Create your environment file:**
    Copy the example environment file. This file contains all the necessary variables your application needs.
    ```bash
    cp .env.example .env
    ```

3.  **Fill in your secrets:**
    Open the newly created `.env` file and add your own secret keys for `JWT_SECRET_KEY` and your `GROQ_API_KEY`.

4.  **Build and run the application:**
    This single command will build the images for all services (API, frontend, DB, Redis) and start them in a networked environment.
    ```bash
    docker-compose up --build
    ```

5.  **Access the application:**
    -   **Frontend UI:** [http://localhost:3000](http://localhost:3000)
    -   **Backend API Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Acknowledgment

This project was built step-by-step with guidance, showcasing a full development lifecycle from an idea in a brain dump to a polished, containerized application.

Built by Robel Shemeles.