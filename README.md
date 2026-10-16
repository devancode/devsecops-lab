# DevSecOps + AI Security Lab

> ⚠️ **Intentionally vulnerable training project.** `app/app.py` contains deliberately planted security bugs for learning purposes. Do **not** deploy it or reuse its code. The hardcoded password is a fake placeholder.

A hands-on lab that builds a **CI/CD pipeline with security gates** using open-source tools: Jenkins runs a SAST scan on every build and **fails the build automatically when a High-severity vulnerability is found**. Later phases extend the same pipeline to **AI/LLM security testing**.

## What this project demonstrates

- **Jenkins in Docker**: a reproducible Jenkins setup (custom image with Python, Node.js and pipeline plugins)
- **Pipeline as code**: a Declarative `Jenkinsfile` stored in Git
- **SAST with Bandit**: static code analysis of the Python app
- **Report vs. gate pattern**:
  - *Report stage*: always scans everything and archives `bandit.json` / `bandit.txt` as build artifacts (never blocks)
  - *Security gate*: `bandit -r app -lll` fails the build on **High** severity findings via a non-zero exit code
- **Change control lesson**: a commit that disabled the gate (`|| true`) and its `git revert` are kept in history to show why pipeline files need review

## Pipeline

```
git commit → Jenkins → Install → SAST report (Bandit, archived) → Security gate (fail on High)
```

Current state: the build is **intentionally red**. The gate catches a command-injection bug (Bandit B602, CWE-78).

## Planted vulnerabilities

| ID | Vulnerability | Location | Detected by |
|---|---|---|---|
| VULN-1 | Hardcoded secret | `app/app.py` | Bandit B105 (Low) |
| VULN-2 | SQL injection via string building | `GET /notes/<owner>` | Bandit B608 (Medium) |
| VULN-3 | OS command injection (`shell=True` with user input) | `GET /ping` | Bandit B602 (**High**, fails the build) |

## Project structure

```
devsecops-lab/
├── Jenkinsfile               # the pipeline
├── requirements.txt          # Python dependencies (pinned)
├── app/app.py                # deliberately vulnerable Flask API
├── tests/                    # test package
└── jenkins/
    ├── Dockerfile            # Jenkins LTS + Python + Node.js + plugins
    └── docker-compose.yml    # runs Jenkins on http://localhost:8080
```

## Run it locally

Requirements: Docker, Git, Python 3.

```bash
# 1. Start Jenkins
cd jenkins
docker compose up -d --build
docker exec jenkins-lab cat /var/jenkins_home/secrets/initialAdminPassword

# 2. Run the security scan yourself
cd ..
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt bandit==1.9.4
bandit -r app -lll ; echo "Exit code: $?"   # 1 = High issue found → build would fail
```

In Jenkins: **New Item → Pipeline → Pipeline script from SCM → Git**, point it at this repo, script path `Jenkinsfile`, then **Build Now**.

## Roadmap

- [x] Jenkins in Docker
- [x] Vulnerable Python app
- [x] Bandit SAST report + High-severity security gate
- [ ] Prompt-injection testing of an LLM app with **Promptfoo** in the pipeline
- [ ] LLM vulnerability scanning with **Garak**
- [ ] Tracing with **LangSmith**
- [ ] AI-SBOM with **cdxgen** (CycloneDX)
- [ ] Additional scanners: Semgrep, pip-audit, Gitleaks

## Tools

Jenkins · Docker · Python / Flask · Bandit · Git