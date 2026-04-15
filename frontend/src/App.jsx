import { useState, useEffect } from "react";

const DEFAULT_API = "http://localhost:8000";

const SERVICES = [
  { value: "enterprise", label: "Enterprise Solutions" },
  { value: "saas", label: "SaaS Platform" },
  { value: "consulting", label: "Consulting Services" },
  { value: "support", label: "Technical Support" },
  { value: "training", label: "Training & Education" }
];

export default function App() {
  const apiBase = import.meta.env.VITE_API_BASE_URL || DEFAULT_API;

  // Auth state
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [apiToken, setApiToken] = useState("");
  const [loginError, setLoginError] = useState("");

  // App state
  const [activeTab, setActiveTab] = useState("view");
  const [objectionText, setObjectionText] = useState("");
  const [selectedService, setSelectedService] = useState("enterprise");
  const [objections, setObjections] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [createdObjection, setCreatedObjection] = useState(null);

  // Check for stored token on mount
  useEffect(() => {
    const storedToken = localStorage.getItem("api_token");
    if (storedToken) {
      setApiToken(storedToken);
      setIsAuthenticated(true);
    }
  }, []);

  // Login handler
  const handleLogin = async (e) => {
    e.preventDefault();
    setLoginError("");
    
    // Test the token by making a request
    try {
      const response = await fetch(`${apiBase}/objections/`, {
        headers: {
          "Authorization": `Bearer ${apiToken}`
        }
      });

      if (response.ok) {
        // Token is valid
        localStorage.setItem("api_token", apiToken);
        setIsAuthenticated(true);
        setLoginError("");
      } else if (response.status === 401) {
        setLoginError("Invalid API token. Please check and try again.");
      } else {
        setLoginError("Unable to verify token. Please try again.");
      }
    } catch (err) {
      setLoginError("Cannot connect to server. Please ensure the backend is running.");
    }
  };

  // Logout handler
  const handleLogout = () => {
    localStorage.removeItem("api_token");
    setApiToken("");
    setIsAuthenticated(false);
    setObjections([]);
    setCreatedObjection(null);
    setError(null);
    setSuccess(null);
  };

  // Fetch objections function
  const fetchObjections = async () => {
    if (!apiToken) return;
    
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`${apiBase}/objections/`, {
        headers: {
          "Authorization": `Bearer ${apiToken}`
        }
      });
      if (!response.ok) {
        if (response.status === 401) {
          setError("Session expired. Please login again.");
          handleLogout();
          return;
        }
        throw new Error("Failed to fetch objections");
      }
      const data = await response.json();
      setObjections(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Fetch objections when authenticated and on view tab
  useEffect(() => {
    if (isAuthenticated && activeTab === "view" && apiToken) {
      fetchObjections();
    }
  }, [activeTab, isAuthenticated, apiToken]);

  const createObjection = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setSuccess(null);
    setCreatedObjection(null);

    try {
      const response = await fetch(`${apiBase}/objections/`, {
        method: "POST",
        headers: { 
          "Content-Type": "application/json",
          "Authorization": `Bearer ${apiToken}`
        },
        body: JSON.stringify({ objection_text: objectionText })
      });

      if (!response.ok) {
        if (response.status === 401) {
          setError("Session expired. Please login again.");
          handleLogout();
          return;
        }
        const errorData = await response.json();
        throw new Error(errorData.detail || "Failed to create objection");
      }

      const data = await response.json();
      setSuccess(`Objection created successfully! (ID: ${data.id})`);
      setCreatedObjection(data);
      setObjectionText("");
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Show login page if not authenticated
  if (!isAuthenticated) {
    return (
      <div className="app login-page">
        <div className="login-container">
          <div className="login-card">
            <div className="login-header">
              <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
                <path d="M7 11V7a5 5 0 0 1 10 0v4" />
              </svg>
              <h1>Sales Objection Handler</h1>
              <p>Enter your API token to continue</p>
            </div>

            <form onSubmit={handleLogin} className="login-form">
              <div className="form-group">
                <label htmlFor="api-token">API Token</label>
                <input
                  id="api-token"
                  type="password"
                  value={apiToken}
                  onChange={(e) => setApiToken(e.target.value)}
                  placeholder="Enter your API token"
                  className="login-input"
                  required
                  autoFocus
                />
                <p className="help-text">
                  Default token: <code>supersecret007</code>
                </p>
              </div>

              {loginError && (
                <div className="alert alert-error">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <circle cx="12" cy="12" r="10" />
                    <line x1="15" y1="9" x2="9" y2="15" />
                    <line x1="9" y1="9" x2="15" y2="15" />
                  </svg>
                  {loginError}
                </div>
              )}

              <button type="submit" className="btn-primary btn-large btn-full">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4" />
                  <polyline points="10 17 15 12 10 7" />
                  <line x1="15" y1="12" x2="3" y2="12" />
                </svg>
                Login
              </button>
            </form>

            <div className="login-footer">
              <p>Need help? Check the <code>.env</code> file for the API token.</p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="app">
      <header className="header">
        <div className="container">
          <div className="header-content">
            <div>
              <h1 className="title">Sales Objection Handler</h1>
              <p className="subtitle">AI-powered B2B SaaS objection response system</p>
            </div>
            <button onClick={handleLogout} className="btn-logout">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
                <polyline points="16 17 21 12 16 7" />
                <line x1="21" y1="12" x2="9" y2="12" />
              </svg>
              Logout
            </button>
          </div>
        </div>
      </header>

      <main className="main">
        <div className="container">
          <div className="tabs">
            <button
              className={`tab ${activeTab === "view" ? "active" : ""}`}
              onClick={() => setActiveTab("view")}
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" />
                <polyline points="9 22 9 12 15 12 15 22" />
              </svg>
              View All Data
            </button>
            <button
              className={`tab ${activeTab === "create" ? "active" : ""}`}
              onClick={() => setActiveTab("create")}
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <line x1="12" y1="5" x2="12" y2="19" />
                <line x1="5" y1="12" x2="19" y2="12" />
              </svg>
              Create Objection
            </button>
          </div>

          {error && (
            <div className="alert alert-error">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <circle cx="12" cy="12" r="10" />
                <line x1="15" y1="9" x2="9" y2="15" />
                <line x1="9" y1="9" x2="15" y2="15" />
              </svg>
              {error}
            </div>
          )}

          {success && (
            <div className="alert alert-success">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <polyline points="20 6 9 17 4 12" />
              </svg>
              {success}
            </div>
          )}

          {activeTab === "view" && (
            <div className="content">
              <div className="section-header">
                <h2>All Objections</h2>
                <button onClick={fetchObjections} disabled={loading} className="btn-refresh">
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <polyline points="23 4 23 10 17 10" />
                    <polyline points="1 20 1 14 7 14" />
                    <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15" />
                  </svg>
                  Refresh
                </button>
              </div>

              {loading ? (
                <div className="loading">
                  <div className="spinner"></div>
                  <p>Loading objections...</p>
                </div>
              ) : objections.length === 0 ? (
                <div className="empty-state">
                  <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                    <path d="M9 11l3 3L22 4" />
                    <path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11" />
                  </svg>
                  <h3>No objections yet</h3>
                  <p>Create your first objection to get started</p>
                  <button onClick={() => setActiveTab("create")} className="btn-primary">
                    Create Objection
                  </button>
                </div>
              ) : (
                <div className="objections-grid">
                  {objections.map((obj) => (
                    <div key={obj.id} className="objection-card">
                      <div className="card-header">
                        <span className="card-id">#{obj.id}</span>
                        <span className={`badge badge-${obj.severity.toLowerCase()}`}>
                          {obj.severity}
                        </span>
                      </div>
                      <div className="card-body">
                        <div className="field">
                          <label>Objection</label>
                          <p className="objection-text">{obj.objection_text}</p>
                        </div>
                        <div className="field">
                          <label>AI Response</label>
                          <p className="response-text">{obj.response}</p>
                        </div>
                        <div className="card-footer">
                          <span className="category-tag">{obj.category}</span>
                          <span className="timestamp">
                            {new Date(obj.created_at).toLocaleDateString()}
                          </span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {activeTab === "create" && (
            <div className="content">
              <div className="section-header">
                <h2>Create New Objection</h2>
              </div>

              <form onSubmit={createObjection} className="form">
                <div className="form-group">
                  <label htmlFor="service">Service Type</label>
                  <select
                    id="service"
                    value={selectedService}
                    onChange={(e) => setSelectedService(e.target.value)}
                    className="select"
                  >
                    {SERVICES.map((service) => (
                      <option key={service.value} value={service.value}>
                        {service.label}
                      </option>
                    ))}
                  </select>
                  <p className="help-text">Select the service related to this objection</p>
                </div>

                <div className="form-group">
                  <label htmlFor="objection">Objection Text</label>
                  <textarea
                    id="objection"
                    value={objectionText}
                    onChange={(e) => setObjectionText(e.target.value)}
                    placeholder="Enter the sales objection here... (e.g., 'Your product is too expensive')"
                    rows={6}
                    required
                    className="textarea"
                  />
                  <p className="help-text">
                    Describe the customer's objection or concern
                  </p>
                </div>

                <div className="form-actions">
                  <button
                    type="submit"
                    disabled={loading || !objectionText.trim()}
                    className="btn-primary btn-large"
                  >
                    {loading ? (
                      <>
                        <div className="spinner-small"></div>
                        Processing...
                      </>
                    ) : (
                      <>
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                          <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z" />
                          <polyline points="17 21 17 13 7 13 7 21" />
                          <polyline points="7 3 7 8 15 8" />
                        </svg>
                        Submit Objection
                      </>
                    )}
                  </button>
                  <button
                    type="button"
                    onClick={() => {
                      setObjectionText("");
                      setError(null);
                      setSuccess(null);
                      setCreatedObjection(null);
                    }}
                    className="btn-secondary"
                    disabled={loading}
                  >
                    Clear Form
                  </button>
                </div>
              </form>

              {createdObjection && (
                <div className="result-section">
                  <h3 className="result-title">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
                      <polyline points="22 4 12 14.01 9 11.01" />
                    </svg>
                    AI-Generated Response
                  </h3>
                  
                  <div className="result-card">
                    <div className="result-header">
                      <span className="result-id">Objection #{createdObjection.id}</span>
                      <span className={`badge badge-${createdObjection.severity.toLowerCase()}`}>
                        {createdObjection.severity}
                      </span>
                    </div>

                    <div className="result-body">
                      <div className="result-field">
                        <label>Your Objection</label>
                        <p className="result-objection">{createdObjection.objection_text}</p>
                      </div>

                      <div className="result-field">
                        <label>AI Response</label>
                        <div className="result-response">
                          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
                          </svg>
                          <p>{createdObjection.response}</p>
                        </div>
                      </div>

                      <div className="result-footer">
                        <div className="result-meta">
                          <span className="meta-item">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
                              <circle cx="12" cy="7" r="4" />
                            </svg>
                            Category: <strong>{createdObjection.category}</strong>
                          </span>
                          <span className="meta-item">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                              <circle cx="12" cy="12" r="10" />
                              <polyline points="12 6 12 12 16 14" />
                            </svg>
                            {new Date(createdObjection.created_at).toLocaleString()}
                          </span>
                        </div>
                        <button
                          onClick={() => setActiveTab("view")}
                          className="btn-view-all"
                        >
                          View All Objections
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </main>

      <footer className="footer">
        <div className="container">
          <p>API Base: <strong>{apiBase}</strong></p>
        </div>
      </footer>
    </div>
  );
}
