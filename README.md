# AI-Powered Resume Scanner & Job Matcher

![AI Resume Scanner Showcase](https://your-image-host.com/showcase.gif)  <!-- **IMPORTANT**: Replace with a link to a GIF of your app in action! -->

This is a full-stack web application that provides instant, AI-driven feedback on a user's resume against a specific job description. Users can register, log in, and submit their resume to receive a match score, a summary of their strengths and weaknesses, and actionable advice for improvement.

**Live Demo:** [https://your-live-app-url.com](https://your-live-app-url.com) <!-- **IMPORTANT**: Add this once deployed -->

---

## 🔥 Key Features

-   **Secure User Authentication:** JWT-based registration and login system.
-   **AI-Powered Analysis:** Leverages large language models (via Groq/OpenAI) to provide nuanced feedback.
-   **Dynamic PDF Parsing:** Extracts text directly from uploaded PDF resumes.
-   **Comprehensive Reporting:** Generates a beautiful, easy-to-read report including:
    -   A Match Score (0-100)
    -   An Executive Summary
    -   A list of Strengths & Gaps
    -   Suggested Keywords to add
-   **API Protection:** Implements Redis-based rate limiting to prevent abuse and control costs.
-   **Interactive UI:** A luxurious, responsive frontend built with Next.js, featuring animations and a premium feel.

## 🛠️ Tech Stack

| Category      | Technology                                    |
| ------------- | --------------------------------------------- |
| **Frontend**  | Next.js, React, TypeScript, React Icons       |
| **Backend**   | FastAPI (Python)                              |
| **AI Model**  | Groq (Llama 3) / OpenAI (GPT-3.5)             |
| **Database**  | PostgreSQL                                    |
| **Cache**     | Redis (for Rate Limiting)                     |
| **API Libs**  | SQLAlchemy, Pydantic, Passlib, python-jose    |
| **Containerization** | Docker & Docker Compose                       |

---

## 🚀 Running Locally

This project is fully containerized, making local setup incredibly simple.

### Prerequisites

-   [Docker](https://www.docker.com/products/docker-desktop/) installed and running.
-   An AI provider API Key (e.g., from [Groq](https://console.groq.com/)).

### Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/ai-resume-scanner.git
    cd ai-resume-scanner
    ```

2.  **Create your environment file:**
    Copy the example environment file and fill in your own secret keys and credentials.
    ```bash
    cp .env.example .env
    ```
    You will need to add your `JWT_SECRET_KEY` and your `GROQ_API_KEY`.

3.  **Build and run the application:**
    This single command will build the images for all services and start them.
    ```bash
    docker-compose up --build
    ```

4.  **Access the application:**
    -   **Frontend UI:** [http://localhost:3000](http://localhost:3000)
    -   **Backend API Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🖼️ Screenshots

<table>
  <tr>
    <td><img src="https://your-image-host.com/login-page.png" alt="Login Page"></td>
    <td><img src="https://your-image-host.com/main-app.png" alt="Main Application Page"></td>
  </tr>
  <tr>
    <td colspan="2"><img src="https://your-image-host.com/report.png" alt="Analysis Report"></td>
  </tr>
</table>

<!-- **IMPORTANT**: Add screenshots of your application -->

## Acknowledgment

This project was built step-by-step with guidance, showcasing a full development lifecycle from idea to a polished, deployable application.

Built by Robel Shemeles.