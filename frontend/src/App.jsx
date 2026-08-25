import { useState } from 'react'
import ReactMarkdown from 'react-markdown'
import { researchTopic } from './services/researchApi'
import './App.css'

function App() {
  const [topic, setTopic] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')

  const handleResearch = async () => {
    const cleanTopic = topic.trim()

    if (cleanTopic.length < 3) {
      setError('Please enter a research topic with at least 3 characters.')
      return
    }

    setLoading(true)
    setError('')
    setResult(null)

    try {
      const data = await researchTopic(cleanTopic)

      if (!data.success) {
        setError(data.error || 'Research failed.')
        return
      }

      setResult(data)
    } catch (err) {
      setError(
        err.message ||
        'Unable to connect to the AI Research Agent API.'
      )
    } finally {
      setLoading(false)
    }
  }
  return (
    <div className="app">
      {/* Header */}
      <header className="header">
        <div className="brand">
          <div className="brand-icon">AI</div>

          <div>
            <h1>AI Research Agent</h1>
            <p>Autonomous Research Platform</p>
          </div>
        </div>

        <div className="api-status">
          <span className="status-dot"></span>
          API Online
        </div>
      </header>

      {/* Main Dashboard */}
      <main className="dashboard">

        {/* Hero */}
        <section className="hero-section">
          <span className="eyebrow">INTELLIGENT RESEARCH</span>

          <h2>
            Research anything.
            <br />
            <span>Let AI do the work.</span>
          </h2>

          <p className="hero-description">
            Enter a research topic and let the AI Research Agent
            investigate, analyze, write, review, and generate a
            comprehensive report.
          </p>
        </section>

        {/* Research Input */}
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
  onChange={(e) => setTopic(e.target.value)}
  onKeyDown={(e) => {
    if (e.key === 'Enter') {
      handleResearch()
    }
  }}
  placeholder="e.g. Artificial Intelligence, Quantum Computing..."
  disabled={loading}
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

        {/* Status */}
        <section className="status-card">

          <div className="status-header">
            <div>
              <h3>Research Status</h3>
              <p>Agent execution status will appear here.</p>
            </div>

            <span className="ready-badge">
              ● Ready
            </span>
          </div>

          <div className="status-placeholder">
  <div className="status-icon">
  {loading ? '...' : '✓'}
  </div>

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
        ? 'The AI Research Agent is researching, planning, writing, and reviewing your topic.'
        : result
          ? 'Your research report has been generated successfully.'
          : 'Enter a topic above to start the research workflow.'}
    </p>
  </div>
</div>

{error && (
  <div className="error-message">
    {error}
  </div>
)}

        </section>

        {/* Report */}
        <section className="report-card">

          <div className="report-header">
            <div>
              <span className="eyebrow">OUTPUT</span>
              <h3>Research Report</h3>
            </div>
          </div>

          <div className="report-placeholder">
  {!result && !loading && (
    <>
      <div className="report-icon">✦</div>

      <h4>Your research report will appear here</h4>

      <p>
        Once the agent completes its research workflow,
        the generated report will be displayed in this area.
      </p>
    </>
  )}

  {loading && (
    <>
      <div className="report-icon">...</div>

      <h4>Generating your research report...</h4>

      <p>
        Please wait while the AI Research Agent completes
        its research workflow.
      </p>
    </>
  )}

  {result && (
    <div className="report-result">
      <p>
        <strong>Topic:</strong> {result.topic}
      </p>

      <div className="report-content">
        <ReactMarkdown>
          {result.report}
        </ReactMarkdown>
      </div>
    </div>
  )}
</div>

        </section>

      </main>

      {/* Footer */}
      <footer className="footer">
        <p>AI Research Agent</p>
        <span>Autonomous Intelligence Platform</span>
      </footer>

    </div>
  )
}

export default App