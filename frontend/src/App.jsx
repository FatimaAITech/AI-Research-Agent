// ```jsx
import { useEffect, useState } from 'react'
import ReactMarkdown from 'react-markdown'
import {
  researchTopic,
  getSavedReports,
  getSavedReport,
  getSimilarTopics,
} from './services/researchApi'
import './App.css'

function App() {
  const [topic, setTopic] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')
  const [reports, setReports] = useState([])
  const [reportsLoading, setReportsLoading] = useState(false)
  const [reportsError, setReportsError] = useState('')
  const [selectedReport, setSelectedReport] = useState(null)
  const [similarTopics, setSimilarTopics] = useState([])
  const [similarLoading, setSimilarLoading] = useState(false)
  const [similarError, setSimilarError] = useState('')

  const loadReports = async () => {
    setReportsLoading(true)
    setReportsError('')

    try {
      const data = await getSavedReports()
      setReports(data.reports || [])
    } catch (err) {
      setReportsError(err.message || 'Unable to load saved reports.')
    } finally {
      setReportsLoading(false)
    }
  }

  const searchSimilarTopics = async (searchTopic) => {
    if (!searchTopic?.trim()) return

    setSimilarLoading(true)
    setSimilarError('')
    setSimilarTopics([])

    try {
      const data = await getSimilarTopics(searchTopic.trim())
      setSimilarTopics(data.matches || [])
    } catch (err) {
      setSimilarError(err.message || 'Unable to search previous research.')
    } finally {
      setSimilarLoading(false)
    }
  }

  const openReport = async (filename) => {
    setReportsError('')

    try {
      const data = await getSavedReport(filename)
      setSelectedReport(data)
    } catch (err) {
      setReportsError(err.message || 'Unable to open this report.')
    }
  }

  useEffect(() => {
    loadReports()
  }, [])

  const handleResearch = async () => {
    const cleanTopic = topic.trim()

    if (cleanTopic.length < 3) {
      setError('Please enter a research topic with at least 3 characters.')
      return
    }

    setLoading(true)
    setError('')
    setResult(null)
    setSelectedReport(null)

    try {
      await searchSimilarTopics(cleanTopic)
      const data = await researchTopic(cleanTopic)

      if (!data.success) {
        setError(data.error || 'Research failed.')
        return
      }

      setResult(data)
      await loadReports()
    } catch (err) {
      setError(err.message || 'Unable to connect to the AI Research Agent API.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <header className="header">
        <div className="brand">
          <div className="brand-icon">AI</div>
          <div>
            <h1>AI Research Agent</h1>
            <p>Autonomous Research Platform</p>
          </div>
        </div>

        <div className="api-status">
          <span className="status-dot" />
          API Online
        </div>
      </header>

      <main className="dashboard">
        <section className="hero-section">
          <span className="eyebrow">INTELLIGENT RESEARCH</span>
          <h2>
            Research anything.
            <br />
            <span>Let AI do the work.</span>
          </h2>
          <p className="hero-description">
            Research, analyze, review, and generate structured reports.
          </p>
        </section>

        <section className="research-card">
          <div className="card-header">
            <div>
              <h3>Start New Research</h3>
              <p>What would you like the agent to research?</p>
            </div>
          </div>

          <div className="input-wrapper">
            <input
              type="text"
              value={topic}
              onChange={(event) => setTopic(event.target.value)}
              onKeyDown={(event) => {
                if (event.key === 'Enter' && !loading) handleResearch()
              }}
              placeholder="e.g. Artificial Intelligence, Quantum Computing..."
              disabled={loading}
              maxLength={500}
            />
            <button
              type="button"
              onClick={handleResearch}
              disabled={loading}
            >
              {loading ? 'Researching...' : 'Start Research'}
            </button>
          </div>
        </section>

        <section className="status-card">
          <div className="status-header">
            <div>
              <h3>Research Status</h3>
              <p>Agent execution status</p>
            </div>
            <span className="ready-badge">
              {loading ? 'Researching' : result ? 'Completed' : 'Ready'}
            </span>
          </div>

          <div className="status-placeholder">
            <div className="status-icon">{loading ? '...' : '✓'}</div>
            <div>
              <strong>
                {loading
                  ? 'Research in progress...'
                  : result
                    ? 'Research completed'
                    : 'Ready to research'}
              </strong>
              <p>
                {loading
                  ? 'The agent is processing your request.'
                  : result
                    ? 'Your report is ready.'
                    : 'Enter a topic to begin.'}
              </p>
            </div>
          </div>

          {error && <div className="error-message">{error}</div>}
        </section>

        <section className="report-card">
          <div className="report-header">
            <div>
              <span className="eyebrow">OUTPUT</span>
              <h3>Research Report</h3>
            </div>
          </div>

          <div className="report-placeholder">
            {loading && <p>Generating your report. Please wait...</p>}

            {!result && !loading && (
              <p>Your new research report will appear here.</p>
            )}

            {result && (
              <div className="report-result">
                <p><strong>Topic:</strong> {result.topic}</p>
                <div className="report-content">
                  <ReactMarkdown>{result.report}</ReactMarkdown>
                </div>
              </div>
            )}
          </div>
        </section>

        <section className="research-card">
          <div className="card-header">
            <div>
              <h3>Similar Topics / Previous Research</h3>
              <p>Related topics found in research memory.</p>
            </div>
          </div>

          {similarLoading && <p>Searching previous research...</p>}
          {similarError && <div className="error-message">{similarError}</div>}

          {!similarLoading && !similarError && similarTopics.length === 0 && (
            <p>No similar topics found for the latest search.</p>
          )}

          {similarTopics.length > 0 && (
            <ul>
              {similarTopics.map((item, index) => (
                <li key={`${item.topic}-${index}`}>
                  <strong>{item.topic}</strong>
                  {' — '}
                  {Math.round(item.score * 100)}% similarity
                  <button
                    type="button"
                    onClick={() => {
                      setTopic(item.topic)
                      searchSimilarTopics(item.topic)
                    }}
                  >
                    Search related
                  </button>
                </li>
              ))}
            </ul>
          )}
        </section>

        <section className="research-card">
          <div className="card-header">
            <div>
              <h3>Saved Reports</h3>
              <p>Previously generated Markdown reports.</p>
            </div>
            <button
              type="button"
              onClick={loadReports}
              disabled={reportsLoading}
            >
              {reportsLoading ? 'Refreshing...' : 'Refresh'}
            </button>
          </div>

          {reportsError && <div className="error-message">{reportsError}</div>}
          {reportsLoading && <p>Loading saved reports...</p>}

          {!reportsLoading && reports.length === 0 && (
            <p>No saved reports found.</p>
          )}

          <ul>
            {reports.map((report) => (
              <li key={report.filename}>
                <button
                  type="button"
                  onClick={() => openReport(report.filename)}
                >
                  {report.title
                    .replace(/_[a-f0-9]{8,}$/i, '')
                   .replace(/_/g, ' ')
                   .replace(/\b\w/g, (char) => char.toUpperCase())}
                </button>
              </li>
            ))}
          </ul>

          {selectedReport && (
            <div className="report-content">
              <h4>{selectedReport.filename}</h4>
              <ReactMarkdown>{selectedReport.content}</ReactMarkdown>
            </div>
          )}
        </section>
      </main>

      <footer className="footer">
        <p>AI Research Agent</p>
        <span>Autonomous Intelligence Platform</span>
      </footer>
    </div>
  )
}

export default App
