// frontend/app/register/page.tsx

'use client';

import { useState, FormEvent, useEffect, useRef } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { FiMail, FiLock } from 'react-icons/fi';

const Spinner = () => (
  <div className="spinner-container">
    <div className="spinner"></div>
    <span>Please wait...</span>
  </div>
);

export default function RegisterPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const cardRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const card = cardRef.current;
    if (!card) return;
    const handleMouseMove = (e: MouseEvent) => {
      const { left, top, width, height } = card.getBoundingClientRect();
      const x = (e.clientX - left) / width;
      const y = (e.clientY - top) / height;
      card.style.setProperty('--mouse-x', `${x * 100}%`);
      card.style.setProperty('--mouse-y', `${y * 100}%`);
    };
    document.addEventListener('mousemove', handleMouseMove);
    return () => document.removeEventListener('mousemove', handleMouseMove);
  }, []);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const response = await fetch('http://localhost:8000/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to register');
      }
      router.push('/login?registered=true');
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <div className="auth-container">
        <div className="auth-card" ref={cardRef}>
          <div className="card-content">
            <h2>Create an Account</h2>
            <p className="subtitle">Join us and start optimizing your career.</p>
            <form onSubmit={handleSubmit}>
              {error && <p className="message error-text">{error}</p>}
              <div className="input-group">
                <input type="email" id="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
                <label htmlFor="email"><FiMail /> Email Address</label>
              </div>
              <div className="input-group">
                <input type="password" id="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
                <label htmlFor="password"><FiLock /> Password</label>
              </div>
              <button type="submit" disabled={loading}>
                {loading ? <Spinner /> : 'Create My Account'}
              </button>
            </form>
            <p className="switch-text">
              Already have an account? <Link href="/login">Log In</Link>
            </p>
          </div>
        </div>
      </div>
      {/* Re-using the same global styles as the login page for consistency */}
      <style jsx global>{`
        :root {
          --primary-slate-blue: #5a7d9a; 
          --primary-slate-blue-dark: #48657e;
          --background-main: #f0f2f5; 
          --text-primary: #1a202c; 
          --text-secondary: #4a5568; 
          --border-color: rgba(255, 255, 255, 0.2);
          --font-family-sans: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
        }
        @keyframes fadeIn { from { opacity: 0; transform: scale(0.95); } to { opacity: 1; transform: scale(1); } }
        @keyframes spin { to { transform: rotate(360deg); } }
        .auth-container { display: flex; align-items: center; justify-content: center; min-height: 100vh; font-family: var(--font-family-sans); padding: 1rem; background-color: var(--background-main); background-image: radial-gradient(circle at 10% 20%, hsla(210, 30%, 80%, 0.3), transparent 50%), radial-gradient(circle at 80% 90%, hsla(210, 30%, 80%, 0.3), transparent 50%); overflow: hidden; }
        .auth-card { position: relative; width: 100%; max-width: 420px; border-radius: 16px; animation: fadeIn 0.6s ease-out forwards; background: rgba(255, 255, 255, 0.6); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); border: 1px solid var(--border-color); box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1); overflow: hidden; }
        .auth-card::before { content: ''; position: absolute; top: var(--mouse-y, 50%); left: var(--mouse-x, 50%); width: 300px; height: 300px; background: radial-gradient(circle, rgba(255, 255, 255, 0.4) 0%, transparent 70%); transform: translate(-50%, -50%); transition: top 0.3s ease, left 0.3s ease; pointer-events: none; opacity: 0.5; }
        .card-content { padding: 2.5rem; text-align: center; }
        h2 { font-size: 1.8rem; margin-bottom: 0.5rem; color: var(--text-primary); font-weight: 700; }
        .subtitle { color: var(--text-secondary); margin-bottom: 2.5rem; }
        .input-group { position: relative; margin-bottom: 2rem; }
        .input-group input { width: 100%; padding: 0.8rem 0.5rem; border: none; border-bottom: 2px solid var(--text-secondary); background-color: transparent; font-size: 1rem; color: var(--text-primary); position: relative; z-index: 1; }
        .input-group label { position: absolute; top: 0.8rem; left: 0.5rem; color: var(--text-secondary); pointer-events: none; transition: all 0.2s ease; display: flex; align-items: center; gap: 0.5rem; z-index: 0; }
        .input-group input:focus + label, .input-group input:valid + label { top: -1.2rem; left: 0; font-size: 0.8rem; color: var(--primary-slate-blue); }
        .input-group input:focus { outline: none; border-bottom-color: var(--primary-slate-blue); }
        button[type="submit"] { width: 100%; padding: 0.875rem; font-weight: 600; font-size: 1rem; color: #fff; background: var(--primary-slate-blue); border: none; border-radius: 8px; cursor: pointer; transition: all 0.2s; display: flex; align-items: center; justify-content: center; min-height: 48px; box-shadow: 0 4px 15px rgba(90, 125, 154, 0.3); }
        button[type="submit"]:hover { background: var(--primary-slate-blue-dark); transform: translateY(-3px); box-shadow: 0 7px 20px rgba(90, 125, 154, 0.4); }
        button:disabled { background: var(--text-secondary); cursor: not-allowed; box-shadow: none; transform: none; }
        .message { padding: 0.75rem; border-radius: 8px; margin-bottom: 1.5rem; animation: fadeIn 0.3s; font-size: 0.9rem; }
        .error-text { color: #721c24; background-color: #f8d7da; }
        .switch-text { font-size: 0.9rem; margin-top: 1.5rem; color: var(--text-secondary); }
        .switch-text a { color: var(--primary-slate-blue); text-decoration: none; font-weight: 600; }
        .spinner-container { display: flex; align-items: center; gap: 0.75rem; }
        .spinner { width: 1.25em; height: 1.25em; border: 2px solid rgba(255, 255, 255, 0.3); border-radius: 50%; border-top-color: #fff; animation: spin 1s ease-in-out infinite; }
      `}</style>
    </>
  );
}