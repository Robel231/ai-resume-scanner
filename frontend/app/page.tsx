// frontend/app/page.tsx

'use client';

import { useState, FormEvent, useEffect } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import AnalysisReport from './AnalysisReport';
import { useAuth } from './contexts/AuthContext';

// --- TYPE DEFINITIONS ---
interface AnalysisResult {
  match_score: number;
  summary: string;
  strengths: string[];
  gaps: string[];
  suggested_keywords: string[];
  actionable_feedback: string;
}
interface ApiResponse {
  id: number;
  analysis_result: AnalysisResult;
}
const Spinner = () => (
  <div className="spinner-container">
    <div className="spinner"></div>
    <span>Analyzing...</span>
  </div>
);

// --- HEADER COMPONENT ---
function AppHeader() {
  const { isAuthenticated, logout } = useAuth();
  return (
    <nav className="app-nav">
      <div className="logo">AI Scanner</div>
      <div>
        {isAuthenticated ? (
          <button onClick={logout} className="nav-button">Logout</button>
        ) : (
          <Link href="/login" className="nav-button">Login</Link>
        )}
      </div>
    </nav>
  );
}

// --- MAIN PAGE COMPONENT ---
export default function Home() {
  const { isAuthenticated, token } = useAuth();
  const router = useRouter();
  
  // Form and API State
  const [jobDescription, setJobDescription] = useState('');
  const [resumeFile, setResumeFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [apiResponse, setApiResponse] = useState<ApiResponse | null>(null);

  // --- THIS IS THE MISSING FUNCTION ---
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setResumeFile(e.target.files[0]);
    }
  };
  // ------------------------------------

  // If not authenticated, redirect to login page on the client side
  useEffect(() => {
    // A small delay to allow auth state to initialize from localStorage
    const timer = setTimeout(() => {
        if (!isAuthenticated) {
            router.push('/login');
        }
    }, 100); // 100ms delay
    
    return () => clearTimeout(timer); // Cleanup timer
  }, [isAuthenticated, router]);
  
  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!resumeFile || !jobDescription || !token) {
      setError('An error occurred. Please ensure you are logged in and have provided all fields.');
      return;
    }
    setLoading(true);
    setError(null);
    setApiResponse(null);

    const formData = new FormData();
    formData.append('job_description', jobDescription);
    formData.append('resume_file', resumeFile);

    try {
      const response = await fetch('http://localhost:8000/api/v1/analyze', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}` // Use the auth token
        },
        body: formData,
      });
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'An unknown server error occurred.');
      }
      const result: ApiResponse = await response.json();
      setApiResponse(result);
    } catch (err: unknown) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };
  
  // While redirecting or checking auth, can show a loader
  if (!isAuthenticated) {
    return (
        <div style={{display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh', fontFamily: 'sans-serif'}}>
            Loading Application...
        </div>
    )
  }

  return (
    <>
      <AppHeader />
      <main className="container">
        <header className="header">
          <h1>AI Resume Scanner</h1>
          <p>Elevate your job application with data-driven insights. Get instant, professional feedback.</p>
        </header>
        
        <section className="form-card">
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label htmlFor="job-description">Job Description</label>
              <textarea id="job-description" value={jobDescription} onChange={(e) => setJobDescription(e.target.value)} placeholder="Paste the full job description here..." required />
            </div>
            <div className="form-group">
              <label htmlFor="resume-file">Upload Your Resume (PDF)</label>
              <input id="resume-file" type="file" accept=".pdf" onChange={handleFileChange} required />
            </div>
            <button type="submit" disabled={loading}>
              {loading ? <Spinner /> : 'Analyze My Resume'}
            </button>
          </form>
        </section>

        <section className="results-section">
          {error && <div className="error-box"><strong>Error:</strong> {error}</div>}
          {apiResponse && <AnalysisReport data={apiResponse.analysis_result} />}
        </section>

        <footer className="footer">
          Built by Robel Shemeles
        </footer>
      </main>

      <style jsx global>{`
        /* ... All of your existing global styles ... */
        :root {
          --primary-slate-blue: #5a7d9a; 
          --primary-slate-blue-dark: #48657e;
          --background-main: #f8f8f7; 
          --text-primary: #333333; 
          --text-secondary: #706c6b; 
          --border-graceful-gray: #d1ccc9;
          --accent-soft-blue-bg: #e8f0f8; 
          --accent-soft-blue-text: #5a7d9a;
          --success: #28a745;
          --warning: #ffc107;
          --danger: #dc3545;
          --font-family-sans: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
        }
        
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        @keyframes spin { to { transform: rotate(360deg); } }

        body {
          background-color: var(--background-main);
          background-image: 
            radial-gradient(circle at 50% 0, hsla(208, 26%, 88%, 0.5) 0%, transparent 40%),
            url("data:image/svg+xml,%3Csvg width='20' height='20' viewBox='0 0 20 20' xmlns='http://www.w3.org/2000/svg'%3E%3Ccircle cx='10' cy='10' r='1' fill='%23d1ccc9' fill-opacity='0.4'/%3E%3C/svg%3E");
          color: var(--text-primary);
          font-family: var(--font-family-sans);
          margin: 0;
          padding: 0;
        }
        .container { max-width: 800px; margin: 0 auto; padding: 2rem 1rem; animation: fadeIn 0.5s ease-out; }
        .header { text-align: center; margin-bottom: 2.5rem; }
        .header h1 { font-size: 2.5rem; font-weight: 800; margin-bottom: 0.5rem; }
        .header p { font-size: 1.125rem; color: var(--text-secondary); }
        .form-card { background: #fff; padding: 2rem; border-radius: 12px; border: 1px solid var(--border-graceful-gray); box-shadow: 0 10px 25px -5px rgba(0,0,0,0.07), 0 10px 10px -5px rgba(0,0,0,0.04); }
        .form-group { margin-bottom: 1.5rem; }
        .form-group label { display: block; font-weight: 500; margin-bottom: 0.5rem; color: var(--text-primary); }
        .form-group textarea, .form-group input { width: 100%; padding: 0.75rem; border: 1px solid var(--border-graceful-gray); border-radius: 8px; font-size: 1rem; transition: border-color 0.2s, box-shadow 0.2s; background-color: #fff; }
        .form-group textarea:focus, .form-group input:focus { outline: none; border-color: var(--primary-slate-blue); box-shadow: 0 0 0 3px rgba(90, 125, 154, 0.2); }
        .form-group textarea { min-height: 150px; resize: vertical; }
        button[type="submit"] { width: 100%; padding: 0.875rem; font-size: 1rem; font-weight: 700; color: #fff; background: var(--primary-slate-blue); border: none; border-radius: 8px; cursor: pointer; transition: background-color 0.2s, transform 0.1s; display: flex; justify-content: center; align-items: center; }
        button[type="submit"]:hover { background: var(--primary-slate-blue-dark); }
        button[type="submit"]:active { transform: scale(0.98); }
        button[type="submit"]:disabled { background: var(--text-secondary); cursor: not-allowed; }
        .results-section { margin-top: 2.5rem; }
        .error-box { color: #721c24; background-color: #f8d7da; border: 1px solid #f5c6cb; padding: 1rem; border-radius: 8px; }
        .spinner-container { display: flex; align-items: center; gap: 0.5rem; }
        .spinner { width: 1.25em; height: 1.25em; border: 2px solid rgba(255, 255, 255, 0.3); border-radius: 50%; border-top-color: #fff; animation: spin 1s ease-in-out infinite; }
        .footer { text-align: center; margin-top: 4rem; padding-top: 2rem; border-top: 1px solid var(--border-graceful-gray); color: var(--text-secondary); font-size: 0.875rem; }
        
        .app-nav { display: flex; justify-content: space-between; align-items: center; padding: 1rem 2rem; background: white; border-bottom: 1px solid var(--border-graceful-gray); }
        .logo { font-weight: 700; font-size: 1.2rem; }
        .nav-button { background: var(--primary-slate-blue); color: white; border: none; padding: 0.5rem 1rem; border-radius: 8px; cursor: pointer; text-decoration: none; }
      `}</style>
    </>
  );
}