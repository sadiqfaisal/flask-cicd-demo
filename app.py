from flask import Flask, jsonify, render_template_string
from datetime import datetime, timezone
import os
import platform

app = Flask(__name__)

STARTED_AT = datetime.now(timezone.utc)

HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>DevOps Pulse | Command Center</title>

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">

<style>
:root {
    --bg:#080b14;
    --panel:#101625;
    --panel2:#131d30;
    --border:rgba(148,163,184,.13);
    --muted:#8290a9;
    --white:#f1f5ff;
    --cyan:#36d9f5;
    --purple:#9b82ff;
    --green:#37e6a2;
    --red:#ff6485;
    --mono:'DM Mono',monospace;
    --font:'Manrope',sans-serif;
}
* {box-sizing:border-box}
body {
    margin:0;
    background:
      radial-gradient(ellipse at 75% -10%,rgba(101,73,208,.18),transparent 35%),
      radial-gradient(ellipse at 10% 45%,rgba(25,180,208,.07),transparent 35%),
      var(--bg);
    color:var(--white);
    font-family:var(--font);
    min-height:100vh;
}
button {font-family:inherit;cursor:pointer}
.layout {display:flex;min-height:100vh}
.sidebar {
    width:245px;
    flex-shrink:0;
    padding:28px 19px;
    border-right:1px solid var(--border);
    background:rgba(9,13,24,.85);
    display:flex;
    flex-direction:column;
}
.brand {display:flex;align-items:center;gap:12px;margin-bottom:48px}
.brand-icon {
    width:39px;height:39px;border-radius:12px;
    background:linear-gradient(135deg,#37d9f5,#7761ed);
    display:grid;place-items:center;
    font-size:21px;color:#07111c;font-weight:900;
    box-shadow:0 0 25px rgba(54,217,245,.22);
}
.brand-name {font-size:17px;font-weight:800;letter-spacing:-.7px}
.brand-name span {color:var(--cyan)}
.nav-label {
    color:#65718a;font-size:10px;font-weight:800;
    letter-spacing:1.7px;margin:0 0 14px 10px;
}
.nav-item {
    display:flex;align-items:center;gap:12px;
    padding:12px 13px;border-radius:9px;
    margin-bottom:5px;color:#94a1b8;
    text-decoration:none;font-size:12px;font-weight:700;
    transition:.2s;
}
.nav-item:hover,.nav-item.active {
    color:white;background:linear-gradient(90deg,rgba(54,217,245,.13),rgba(155,130,255,.08));
}
.nav-item.active {border-left:2px solid var(--cyan)}
.nav-icon {font-size:16px;width:19px;text-align:center}
.sidebar-bottom {margin-top:auto}
.profile {
    display:flex;align-items:center;gap:11px;
    padding:14px 5px 0;border-top:1px solid var(--border);
}
.avatar {
    width:35px;height:35px;border-radius:50%;
    display:grid;place-items:center;
    background:linear-gradient(135deg,#8068ed,#32cce7);
    font-size:12px;font-weight:800;color:white;
}
.profile strong {font-size:11px;display:block}
.profile small {font-size:10px;color:var(--muted)}
.main {flex:1;min-width:0;padding:29px 38px 45px}
.topbar {
    display:flex;align-items:center;justify-content:space-between;
    margin-bottom:34px;gap:15px;
}
.breadcrumb {font-size:12px;color:var(--muted)}
.breadcrumb b {color:white}
.top-actions {display:flex;align-items:center;gap:12px}
.clock {font-family:var(--mono);font-size:11px;color:#a8b4ca}
.live-pill {
    display:flex;align-items:center;gap:7px;
    padding:8px 12px;border:1px solid rgba(55,230,162,.2);
    background:rgba(55,230,162,.07);border-radius:30px;
    color:var(--green);font-size:10px;font-weight:800;
}
.dot {width:7px;height:7px;background:var(--green);border-radius:50%;box-shadow:0 0 10px var(--green);animation:pulse 1.7s infinite}
@keyframes pulse {50%{opacity:.35;box-shadow:0 0 2px var(--green)}}
.refresh {
    background:#182238;color:white;border:1px solid var(--border);
    border-radius:9px;padding:9px 13px;font-size:11px;font-weight:700;
}
.refresh:hover {border-color:var(--cyan);color:var(--cyan)}
.hero {
    display:flex;justify-content:space-between;align-items:center;
    gap:25px;margin-bottom:27px;
}
.eyebrow {
    color:var(--cyan);font-size:10px;font-weight:800;
    letter-spacing:2px;margin-bottom:10px;
}
h1 {font-size:clamp(27px,3.4vw,40px);letter-spacing:-2px;line-height:1.15;margin:0 0 10px}
.gradient {
    background:linear-gradient(90deg,#45ddf5,#a68bff);
    -webkit-background-clip:text;background-clip:text;color:transparent;
}
.subtitle {font-size:12px;color:var(--muted);line-height:1.8}
.hero-right {text-align:right;min-width:150px}
.build-label {font-size:10px;color:var(--muted);letter-spacing:1px}
.build-number {font-family:var(--mono);font-size:22px;margin-top:7px}
.build-number span {color:var(--purple)}
.grid {
    display:grid;grid-template-columns:repeat(4,minmax(0,1fr));
    gap:15px;margin-bottom:20px;
}
.metric {
    background:linear-gradient(145deg,rgba(19,29,48,.95),rgba(13,20,34,.95));
    border:1px solid var(--border);border-radius:13px;
    padding:19px;position:relative;overflow:hidden;
}
.metric:after {
    content:"";position:absolute;right:-24px;top:-35px;
    width:95px;height:95px;border-radius:50%;
    background:var(--glow,rgba(54,217,245,.08));filter:blur(30px);
}
.metric-top {display:flex;justify-content:space-between;align-items:center}
.metric-title {font-size:10px;color:var(--muted);font-weight:700;letter-spacing:.5px}
.metric-icon {font-size:18px}
.metric-value {font-size:28px;font-weight:800;letter-spacing:-1.3px;margin:17px 0 4px}
.metric-note {font-size:10px;color:var(--muted)}
.green {color:var(--green)}
.cyan {color:var(--cyan)}
.purple {color:var(--purple)}
.orange {color:#ffbd70}
.content-grid {
    display:grid;grid-template-columns:minmax(0,1.65fr) minmax(270px,1fr);
    gap:17px;margin-bottom:18px;
}
.panel {
    background:rgba(16,22,37,.91);
    border:1px solid var(--border);
    border-radius:13px;padding:21px;
    min-width:0;
}
.panel-heading {
    display:flex;align-items:center;justify-content:space-between;
    gap:10px;margin-bottom:21px;
}
.panel-heading h2 {font-size:13px;margin:0;font-weight:800}
.panel-heading p {font-size:10px;color:var(--muted);margin:5px 0 0}
.tag {
    font-family:var(--mono);font-size:9px;padding:6px 9px;
    border:1px solid var(--border);border-radius:5px;color:#a8b4ca;
}
.pipeline {
    display:grid;grid-template-columns:repeat(4,1fr);
    gap:9px;align-items:stretch;
}
.stage {
    position:relative;text-align:center;
    background:#121d30;border:1px solid var(--border);
    border-radius:10px;padding:17px 7px;
}
.stage-icon {font-size:22px;margin-bottom:10px}
.stage-name {font-size:10px;font-weight:800;margin-bottom:6px}
.stage-status {font-family:var(--mono);font-size:8px;color:var(--green)}
.stage-status.optional {color:#ffbd70}
.pipeline-note {
    margin-top:15px;padding:11px;
    background:rgba(54,217,245,.045);
    border-left:2px solid var(--cyan);
    font-size:10px;color:#9cabc1;line-height:1.7;
}
.activity-list {display:flex;flex-direction:column;gap:17px}
.activity {display:flex;align-items:flex-start;gap:11px}
.activity-icon {
    width:28px;height:28px;flex-shrink:0;border-radius:8px;
    background:#17253a;display:grid;place-items:center;font-size:13px;
}
.activity strong {font-size:10px;display:block;margin:2px 0 4px}
.activity small {font-size:9px;color:var(--muted);line-height:1.5}
.activity-time {margin-left:auto;font-family:var(--mono);font-size:8px;color:#75839b;white-space:nowrap}
.bottom-grid {
    display:grid;grid-template-columns:1fr 1fr;gap:17px;
}
.endpoint {
    display:flex;align-items:center;justify-content:space-between;
    padding:13px 0;border-bottom:1px solid var(--border);
}
.endpoint:last-child {border:0}
.endpoint-name {font-size:11px;font-weight:700}
.endpoint-path {font-family:var(--mono);font-size:9px;color:var(--muted);margin-top:5px}
.endpoint-btn {
    background:rgba(54,217,245,.08);color:var(--cyan);
    border:1px solid rgba(54,217,245,.2);
    border-radius:7px;padding:8px 11px;font-size:9px;font-weight:800;
}
.endpoint-btn:hover {background:rgba(54,217,245,.17)}
.output {
    margin-top:14px;background:#090f1c;border:1px solid var(--border);
    border-radius:8px;padding:12px;min-height:48px;
    font-family:var(--mono);font-size:10px;color:#9eabc2;
    white-space:pre-wrap;overflow-wrap:anywhere;
}
.footer {
    display:flex;justify-content:space-between;gap:15px;
    margin-top:24px;padding-top:18px;border-top:1px solid var(--border);
    color:#63718a;font-size:9px;
}
.footer span {font-family:var(--mono)}
.toast {
    position:fixed;right:25px;bottom:25px;
    background:#17253a;border:1px solid rgba(55,230,162,.3);
    padding:13px 18px;border-radius:9px;
    font-size:11px;opacity:0;transform:translateY(10px);
    transition:.25s;pointer-events:none;z-index:5;
}
.toast.show {opacity:1;transform:translateY(0)}
@media(max-width:1050px) {
    .sidebar{width:190px}
    .main{padding:25px}
    .grid{grid-template-columns:repeat(2,1fr)}
}
@media(max-width:760px) {
    .sidebar{display:none}
    .main{padding:20px 15px}
    .content-grid,.bottom-grid{grid-template-columns:1fr}
    .hero{align-items:flex-start}
    .hero-right{display:none}
    .topbar{flex-wrap:wrap}
    .pipeline{grid-template-columns:repeat(2,1fr)}
    .footer{flex-direction:column}
}
</style>
</head>

<body>
<div class="layout">

<aside class="sidebar">
    <div class="brand">
        <div class="brand-icon">⌘</div>
        <div class="brand-name">DEVOPS<span>PULSE</span></div>
    </div>

    <div class="nav-label">WORKSPACE</div>
    <a href="#overview" class="nav-item active"><span class="nav-icon">◈</span> Overview</a>
    <a href="#pipeline" class="nav-item"><span class="nav-icon">⑂</span> CI/CD Pipeline</a>
    <a href="#activity" class="nav-item"><span class="nav-icon">◷</span> Build Activity</a>
    <a href="#diagnostics" class="nav-item"><span class="nav-icon">⌘</span> Diagnostics</a>

    <div class="sidebar-bottom">
        <div class="nav-label">PROJECT</div>
        <div class="nav-item"><span class="nav-icon">◉</span> Flask Application</div>
        <div class="profile">
            <div class="avatar">DP</div>
            <div>
                <strong>DevOps Project</strong>
                <small>Internship Demo</small>
            </div>
        </div>
    </div>
</aside>

<main class="main" id="overview">

    <header class="topbar">
        <div class="breadcrumb">Workspace / <b>Command Center</b></div>
        <div class="top-actions">
            <div class="clock" id="clock">--:--:--</div>
            <div class="live-pill"><span class="dot"></span> LOCAL APP ONLINE</div>
            <button class="refresh" onclick="refreshDashboard()">↻ Refresh</button>
        </div>
    </header>

    <section class="hero">
        <div>
            <div class="eyebrow">ENGINEERING / AUTOMATION</div>
            <h1>Your deployment.<br><span class="gradient">Under control.</span></h1>
            <div class="subtitle">
                A centralized view of application health, CI/CD automation and build operations.<br>
                Monitor your project from code commit to container image.
            </div>
        </div>
        <div class="hero-right">
            <div class="build-label">PROJECT VERSION</div>
            <div class="build-number">v<span id="versionNumber">1.0.0</span></div>
            <div class="build-label" style="margin-top:7px">FLASK APPLICATION</div>
        </div>
    </section>

    <section class="grid">
        <div class="metric" style="--glow:rgba(55,230,162,.16)">
            <div class="metric-top">
                <div class="metric-title">APPLICATION STATUS</div>
                <div class="metric-icon green">◉</div>
            </div>
            <div class="metric-value green" id="appStatus">ONLINE</div>
            <div class="metric-note" id="statusNote">Waiting for live health check</div>
        </div>

        <div class="metric" style="--glow:rgba(54,217,245,.16)">
            <div class="metric-top">
                <div class="metric-title">CI PIPELINE</div>
                <div class="metric-icon cyan">⑂</div>
            </div>
            <div class="metric-value cyan">READY</div>
            <div class="metric-note">Configured in GitHub Actions</div>
        </div>

        <div class="metric" style="--glow:rgba(155,130,255,.18)">
            <div class="metric-top">
                <div class="metric-title">CONTAINER BUILD</div>
                <div class="metric-icon purple">▣</div>
            </div>
            <div class="metric-value purple">CONFIGURED</div>
            <div class="metric-note">Dockerfile available</div>
        </div>

        <div class="metric" style="--glow:rgba(255,189,112,.14)">
            <div class="metric-top">
                <div class="metric-title">DEPLOYMENT</div>
                <div class="metric-icon orange">⇧</div>
            </div>
            <div class="metric-value orange" style="font-size:20px">NOT CONNECTED</div>
            <div class="metric-note">Cloud deployment not configured</div>
        </div>
    </section>

    <section class="content-grid">
        <div class="panel" id="pipeline">
            <div class="panel-heading">
                <div>
                    <h2>CI/CD PIPELINE ARCHITECTURE</h2>
                    <p>Automated workflow configured for every main branch push</p>
                </div>
                <div class="tag">WORKFLOW / CI.YML</div>
            </div>

            <div class="pipeline">
                <div class="stage">
                    <div class="stage-icon">⌘</div>
                    <div class="stage-name">SOURCE CODE</div>
                    <div class="stage-status">CONFIGURED</div>
                </div>
                <div class="stage">
                    <div class="stage-icon">⚙</div>
                    <div class="stage-name">AUTOMATED TESTS</div>
                    <div class="stage-status">CONFIGURED</div>
                </div>
                <div class="stage">
                    <div class="stage-icon">▣</div>
                    <div class="stage-name">DOCKER BUILD</div>
                    <div class="stage-status">CONFIGURED</div>
                </div>
                <div class="stage">
                    <div class="stage-icon">☁</div>
                    <div class="stage-name">CLOUD RELEASE</div>
                    <div class="stage-status optional">OPTIONAL</div>
                </div>
            </div>

            <div class="pipeline-note">
                <strong>Workflow:</strong> A GitHub push triggers the automation.
                GitHub Actions installs dependencies, runs tests and builds a Docker image.
                Image publishing and cloud deployment require additional configuration.
            </div>
        </div>

        <div class="panel" id="activity">
            <div class="panel-heading">
                <div>
                    <h2>WORKFLOW ACTIVITY</h2>
                    <p>Configured automation stages</p>
                </div>
                <div class="tag">PIPELINE</div>
            </div>

            <div class="activity-list">
                <div class="activity">
                    <div class="activity-icon">⌘</div>
                    <div><strong>Source checkout</strong><small>GitHub Actions retrieves repository code</small></div>
                    <div class="activity-time">01</div>
                </div>
                <div class="activity">
                    <div class="activity-icon">⚙</div>
                    <div><strong>Dependency installation</strong><small>Python environment and packages</small></div>
                    <div class="activity-time">02</div>
                </div>
                <div class="activity">
                    <div class="activity-icon">✓</div>
                    <div><strong>Automated testing</strong><small>Pytest executes application tests</small></div>
                    <div class="activity-time">03</div>
                </div>
                <div class="activity">
                    <div class="activity-icon">▣</div>
                    <div><strong>Container image build</strong><small>Docker builds the application image</small></div>
                    <div class="activity-time">04</div>
                </div>
            </div>
        </div>
    </section>

    <section class="bottom-grid" id="diagnostics">
        <div class="panel">
            <div class="panel-heading">
                <div>
                    <h2>LIVE DIAGNOSTICS</h2>
                    <p>Send requests to your running Flask application</p>
                </div>
                <div class="tag">API</div>
            </div>

            <div class="endpoint">
                <div>
                    <div class="endpoint-name">Application Health</div>
                    <div class="endpoint-path">GET /api/health</div>
                </div>
                <button class="endpoint-btn" onclick="checkHealth()">RUN CHECK ↗</button>
            </div>

            <div class="endpoint">
                <div>
                    <div class="endpoint-name">Build Information</div>
                    <div class="endpoint-path">GET /api/version</div>
                </div>
                <button class="endpoint-btn" onclick="getVersion()">VIEW INFO ↗</button>
            </div>

            <div class="output" id="apiOutput">Select an operation to inspect the live API response...</div>
        </div>

        <div class="panel">
            <div class="panel-heading">
                <div>
                    <h2>PROJECT CONFIGURATION</h2>
                    <p>Application runtime information</p>
                </div>
                <div class="tag">SYSTEM</div>
            </div>

            <div class="endpoint">
                <div><div class="endpoint-name">Framework</div><div class="endpoint-path">Python web framework</div></div>
                <span class="cyan">FLASK</span>
            </div>
            <div class="endpoint">
                <div><div class="endpoint-name">Automation</div><div class="endpoint-path">Continuous integration</div></div>
                <span class="cyan">GITHUB ACTIONS</span>
            </div>
            <div class="endpoint">
                <div><div class="endpoint-name">Containerization</div><div class="endpoint-path">Application packaging</div></div>
                <span class="purple">DOCKER</span>
            </div>
            <div class="endpoint">
                <div><div class="endpoint-name">Test framework</div><div class="endpoint-path">Automated validation</div></div>
                <span class="green">PYTEST</span>
            </div>
        </div>
    </section>

    <footer class="footer">
        <div>DEVOPS PULSE &nbsp;·&nbsp; CI/CD COMMAND CENTER</div>
        <span>BUILT WITH PYTHON + FLASK</span>
        <div>INTERNSHIP PROJECT / 2026</div>
    </footer>
</main>
</div>

<div class="toast" id="toast">Request completed</div>

<script>
function updateClock() {
    document.getElementById("clock").textContent =
        new Date().toLocaleTimeString();
}
updateClock();
setInterval(updateClock, 1000);

function toast(message) {
    const el = document.getElementById("toast");
    el.textContent = message;
    el.classList.add("show");
    setTimeout(() => el.classList.remove("show"), 2600);
}

async function checkHealth() {
    const output = document.getElementById("apiOutput");
    output.textContent = "Connecting to application...";
    try {
        const response = await fetch("/api/health");
        const data = await response.json();
        output.textContent = JSON.stringify(data, null, 2);
        document.getElementById("appStatus").textContent =
            data.status.toUpperCase();
        document.getElementById("statusNote").textContent =
            "Last checked: " + new Date().toLocaleTimeString();
        toast("Health check completed");
    } catch (error) {
        output.textContent = "Health check failed: " + error.message;
        document.getElementById("appStatus").textContent = "ERROR";
        document.getElementById("statusNote").textContent = "API unavailable";
        toast("Health check failed");
    }
}

async function getVersion() {
    const output = document.getElementById("apiOutput");
    output.textContent = "Retrieving build information...";
    try {
        const response = await fetch("/api/version");
        const data = await response.json();
        output.textContent = JSON.stringify(data, null, 2);
        document.getElementById("versionNumber").textContent = data.version;
        toast("Build information retrieved");
    } catch (error) {
        output.textContent = "Request failed: " + error.message;
        toast("Could not retrieve build information");
    }
}

async function refreshDashboard() {
    await checkHealth();
    toast("Dashboard refreshed");
}

document.querySelectorAll(".nav-item[href]").forEach(link => {
    link.addEventListener("click", () => {
        document.querySelectorAll(".nav-item").forEach(item => item.classList.remove("active"));
        link.classList.add("active");
    });
});

checkHealth();
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/api/health")
def api_health():
    return jsonify({
        "status": "healthy",
        "application": "DevOps Pulse",
        "message": "Flask application is responding",
        "checked_at": datetime.now(timezone.utc).isoformat()
    }), 200

@app.route("/api/version")
def api_version():
    return jsonify({
        "application": "DevOps Pulse",
        "version": "1.0.0",
        "framework": "Flask",
        "python_version": platform.python_version(),
        "environment": os.environ.get("APP_ENV", "local")
    }), 200

# Backwards-compatible routes for existing tests
@app.route("/health")
def health():
    return api_health()

@app.route("/version")
def version():
    return api_version()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
