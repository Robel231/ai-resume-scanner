// frontend/app/AnalysisReport.tsx

'use client';

import { FiCheckCircle, FiXCircle, FiKey, FiMessageSquare, FiTrendingUp } from 'react-icons/fi';

// --- TYPE DEFINITION (Unchanged) ---
interface AnalysisResult {
  match_score: number;
  summary: string;
  strengths: string[];
  gaps: string[];
  suggested_keywords: string[];
  actionable_feedback: string;
}
interface ReportProps {
  data: AnalysisResult;
}

// --- HELPER FUNCTION (Unchanged) ---
const getScoreStyle = (score: number) => {
  if (score >= 85) return { color: 'var(--success)', name: 'Excellent Match' };
  if (score >= 60) return { color: 'var(--warning)', name: 'Good Match' };
  return { color: 'var(--danger)', name: 'Needs Improvement' };
};

export default function AnalysisReport({ data }: ReportProps) {
  const { color, name } = getScoreStyle(data.match_score);

  return (
    <>
      <div className="report-card">
        <h2 className="report-title">Analysis Report</h2>

        <div className="score-wrapper">
          <div className="score-circle" style={{ borderColor: color }}>
            <span className="score-number" style={{ color }}>{data.match_score}</span>
            <span className="score-label">Match Score</span>
          </div>
          <div className="score-verdict" style={{ color: name === 'Excellent Match' ? 'var(--success)' : name === 'Good Match' ? 'var(--warning)' : 'var(--danger)' }}>{name}</div>
        </div>

        <div className="report-section">
          <h3><FiMessageSquare /> Executive Summary</h3>
          <p>{data.summary}</p>
        </div>

        <div className="columns">
          <div className="report-section">
            <h3><FiCheckCircle style={{ color: 'var(--success)' }} /> Strengths</h3>
            <ul>{data.strengths.map((item, i) => <li key={i}>{item}</li>)}</ul>
          </div>
          <div className="report-section">
            <h3><FiXCircle style={{ color: 'var(--danger)' }} /> Gaps & Improvements</h3>
            <ul>{data.gaps.map((item, i) => <li key={i}>{item}</li>)}</ul>
          </div>
        </div>

        <div className="report-section">
          <h3><FiKey /> Suggested Keywords</h3>
          <div className="keywords-container">
            {data.suggested_keywords.map((keyword, i) => <span key={i} className="keyword-pill">{keyword}</span>)}
          </div>
        </div>
        
        <div className="report-section">
          <h3><FiTrendingUp /> Actionable Feedback</h3>
          <p>{data.actionable_feedback}</p>
        </div>
      </div>

      {/* --- UPDATED COMPONENT-SPECIFIC STYLES --- */}
      <style jsx>{`
        @keyframes pulse {
          0%, 100% { transform: scale(1); }
          50% { transform: scale(1.05); }
        }
        .report-card {
          background: #fff;
          padding: 2.5rem;
          border-radius: 12px;
          border: 1px solid var(--border-graceful-gray);
          box-shadow: 0 4px 12px -2px rgba(0,0,0,0.06);
          animation: fadeIn 0.5s ease-out;
        }
        .report-title {
          text-align: center;
          font-size: 1.875rem;
          font-weight: 700;
          margin-bottom: 2rem;
          color: var(--text-primary);
        }

        .score-wrapper {
          text-align: center;
          margin-bottom: 2.5rem;
        }
        .score-circle {
          width: 160px;
          height: 160px;
          margin: 0 auto;
          border-radius: 50%;
          border-width: 10px;
          border-style: solid;
          display: flex;
          flex-direction: column;
          justify-content: center;
          align-items: center;
          background-color: var(--background-main);
          animation: pulse 2.5s infinite ease-in-out;
        }
        .score-number {
          font-size: 4rem;
          font-weight: 800;
        }
        .score-label {
          font-size: 0.875rem;
          text-transform: uppercase;
          color: var(--text-secondary);
          letter-spacing: 0.5px;
        }
        .score-verdict {
          margin-top: 1rem;
          font-size: 1.25rem;
          font-weight: 700;
        }

        .report-section {
          margin-bottom: 2rem;
        }
        .report-section:last-child {
          margin-bottom: 0;
        }
        .report-section h3 {
          display: flex;
          align-items: center;
          gap: 0.75rem;
          font-size: 1.25rem;
          font-weight: 700;
          padding-bottom: 0.5rem;
          border-bottom: 1px solid var(--border-graceful-gray);
          margin-bottom: 1rem;
          color: var(--text-primary);
        }
        .report-section p, .report-section li {
          line-height: 1.6;
          color: var(--text-secondary);
        }
        .report-section ul {
          padding-left: 1.25rem;
          margin: 0;
        }
        .report-section li {
          margin-bottom: 0.5rem;
        }
        
        .columns {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
          gap: 2rem;
        }
        
        .keywords-container {
          display: flex;
          flex-wrap: wrap;
          gap: 0.75rem;
        }
        .keyword-pill {
          background-color: var(--accent-soft-blue-bg);
          color: var(--accent-soft-blue-text);
          padding: 0.5rem 1rem;
          border-radius: 9999px;
          font-size: 0.875rem;
          font-weight: 500;
          transition: transform 0.2s;
        }
        .keyword-pill:hover {
          transform: translateY(-2px);
        }
      `}</style>
    </>
  );
}