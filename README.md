<h3 align="center">🛠️ care-privacy</h3>

<div align="center">
  <a href="https://github.com/axentx/care-privacy/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License: MIT"></a>
  <a href="https://github.com/axentx/care-privacy"><img src="https://img.shields.io/github/stars/axentx/care-privacy?style=social" alt="GitHub stars"></a>
  <a href="https://github.com/axentx/care-privacy"><img src="https://img.shields.io/github/actions/workflow/status/axentx/care-privacy/ci.yml?branch=main" alt="Build status"></a>
  <a href="https://github.com/axentx/care-privacy"><img src="https://img.shields.io/github/repo-size/axentx/care-privacy" alt="Repo size"></a>
  <a href="https://github.com/axentx/care-privacy"><img src="https://img.shields.io/github/languages/top/axentx/care-privacy" alt="Language: Python"></a>
</div>

---

# 🚀 care-privacy

**Power developers with a toggle‑based consent form.** A lightweight web app that lets users enable or disable data categories before submitting consent, storing records in‑memory for quick prototyping.

## Why care-privacy?

- **Fast Setup** – 2‑minute bootstrap with pip and Flask.  
- **Toggle‑Based UI** – Users can enable/disable data categories via intuitive switches.  
- **In‑Memory Storage** – Zero‑config persistence; data lives in RAM for instant feedback.  
- **Test‑Ready** – Built‑in pytest suite covering form rendering and submission logic.  
- **Extensible** – Plug‑in your own database or authentication layer with minimal changes.  
- **Open‑Source** – MIT license, community‑friendly contributions.  
- **Built for X** – Researchers and developers prototyping AI consent flows in sandbox environments.

## Feature Overview

| Feature | Description |
|---------|-------------|
| Consent Form UI | Rendered with HTML/CSS, includes toggle switches for each data category. |
| Toggle Switches | JavaScript‑free CSS toggles for quick, accessible interactions. |
| In‑Memory DB | Python dictionary stores consent records during runtime. |
| Form Validation | Server‑side checks for required fields and duplicate submissions. |
| Test Suite | Pytest tests for UI rendering, form submission, and data storage. |