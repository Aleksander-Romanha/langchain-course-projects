# Project 3 — Email Agent (LangChain Foundations)

Short project files and instructions for publishing this project to GitHub.

**Project Purpose:**
- **Description:**: Small email agent demo built during the LangChain Foundations course showing an email automation/agent example.

**Files:**
- **Email agent:**: [project 3/email_agent.py](project%203/email_agent.py)
- **Notebooks:**: See notebooks/module-3 for related walkthroughs and examples.
- **Dependencies:**: See [requirements.txt](requirements.txt)

**Quick Start (Windows)**
- **Create a virtual environment:**: `python -m venv .venv`
- **Activate venv (PowerShell):**: `.\.venv\Scripts\Activate.ps1`
- **Activate venv (cmd):**: `.\.venv\Scripts\activate.bat`
- **Install deps:**: `pip install -r requirements.txt`
- **Run the agent script:**: `python "project 3\email_agent.py"`

Notes:
- If `email_agent.py` expects environment variables (API keys, SMTP credentials), create a `.env` file or set env vars before running. The repository root contains `example.env` as a template.
- Notebooks contain interactive explanations — run them in Jupyter if you want step-by-step context.

**How to publish this project to GitHub**
1. Create a new repo on GitHub (via the website).
2. In your local repo root, initialize git (if needed) and push the `project 3` folder or the entire repo:

```bash
git init
git add .
git commit -m "chore: add project 3 Email Agent"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo>.git
git push -u origin main
```

3. Don't commit secrets — add them to your GitHub repo's Actions/Secrets or local environment.

**License & Credits**
- This code is from the LangChain Academy course materials. Keep attribution as appropriate.

If you want, I can also prepare a minimal `setup.py`/`pyproject.toml` snippet, a standalone `requirements.txt` for this folder, or open a PR-ready commit with these files included.
