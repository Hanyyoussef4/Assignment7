# 🚀 QR Code Generator App

[![CI Status](https://github.com/Hanyyoussef4/Assignment7/actions/workflows/ci.yml/badge.svg)](https://github.com/Hanyyoussef4/Assignment7/actions/workflows/ci.yml)
[![Docker Hub](https://img.shields.io/docker/v/hany25/qr-code-generator-app?label=docker%20hub)](https://hub.docker.com/r/hany25/qr-code-generator-app)

A robust CLI tool and Dockerized application that generates two QR codes—one linking to your GitHub repository and one to your Docker Hub image—automatically overwriting previous codes on each run. Perfect for seamlessly sharing your project endpoints.

---

## 📋 Table of Contents

1. [Features](#features)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Usage](#usage)

   * [Local (Host)](#local-host)
   * [Docker](#docker)
   * [Docker Compose](#via-docker-compose)
5. [Testing & Coverage](#testing--coverage)
6. [Configuration](#configuration)
7. [CI/CD Workflow](#cicd-workflow)
8. [Reflection & Academic Integrity](#reflection--academic-integrity)
9. [Quick Links](#quick-links)

---

## ✨ Features

* **Dual QR Generation**: Outputs `github_qr.png` and `docker_qr.png` in a configurable directory.
* **Overwrite Safety**: Automatically removes old QR files before each run.
* **Flexible Inputs**: Accepts URLs via CLI flags (`--github`, `--docker`) or environment variables.
* **Color Customization**: `FILL_COLOR` and `BACK_COLOR` support named colors or hex codes (default: red on white).
* **Docker-Ready**: Fully containerized for consistent performance across environments.
* **Comprehensive Testing**: Unit and smoke tests ensure ≥ 90% coverage on core functionality.

---

## 🛠️ Prerequisites

* **Python 3.10+**
* **pip**
* **Docker** (for container execution)

---

## 📥 Installation

```bash
# Clone the repository
git clone https://github.com/Hanyyoussef4/Assignment7.git
cd Assignment7

# (Optional) Create & activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate    # macOS/Linux
# .\.venv\Scripts\activate   # Windows

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 💻 Usage

### Local (Host)

Generate both QR codes in a single command:

```bash
python main.py \
  --github https://github.com/Hanyyoussef4/Assignment7 \
  --docker https://hub.docker.com/r/hany25/qr-code-generator-app
```

Or rely on environment variables:

```bash
export GITHUB_URL=https://github.com/Hanyyoussef4/Assignment7
export DOCKER_URL=https://hub.docker.com/r/hany25/qr-code-generator-app
python main.py
```

**Output directory structure:**

```
qr_codes/
├── github_qr.png
└── docker_qr.png
```

### Docker

1. **Pull** from Docker Hub

   ```bash
   docker pull hany25/qr-code-generator-app:latest
   ```

2. **Build & Tag** (if making local changes)

   ```bash
   docker build -t hany25/qr-code-generator-app:latest .
   ```

3. **Push** to Docker Hub

   ```bash
   docker push hany25/qr-code-generator-app:latest
   ```

4. **Run**

   ```bash
   docker run --rm \
     -v "$(pwd)/qr_codes":/app/qr_codes \
     hany25/qr-code-generator-app:latest \
     --github "https://github.com/Hanyyoussef4/Assignment7" \
     --docker "https://hub.docker.com/r/hany25/qr-code-generator-app"
   ```

### Via Docker Compose

```yaml
services:
  qrgen:
    image: hany25/qr-code-generator-app:latest
    volumes:
      - ./qr_codes:/app/qr_codes
    environment:
      GITHUB_URL: https://github.com/Hanyyoussef4/Assignment7
      DOCKER_URL: https://hub.docker.com/r/hany25/qr-code-generator-app
```

```bash
docker compose up
docker compose down
```

---

## 🧪 Testing & Coverage

* **Unit Tests:** `tests/test_main.py` validates URL parsing, color parsing, and overwrite logic.
* **Docker Smoke Test:** `tests/test_dockerfile.py` ensures the container generates both QR codes.

Run tests with coverage:

```bash
pytest --maxfail=1 --disable-warnings --cov=.
```

Generate HTML report:

```bash
pytest --cov-report=html
open htmlcov/index.html
```

Aim for **≥ 90%** coverage on `main.py`.

---

## ⚙️ Configuration

| Variable      | Description          | Default        |
| ------------- | -------------------- | -------------- |
| `GITHUB_URL`  | GitHub repo URL      | Script default |
| `DOCKER_URL`  | Docker Hub image URL | Script default |
| `QR_CODE_DIR` | Output directory     | `qr_codes`     |
| `FILL_COLOR`  | QR foreground color  | `red`          |
| `BACK_COLOR`  | QR background color  | `white`        |

Supports named colors or hex codes.

---

## 🔄 CI/CD Workflow

This repository uses GitHub Actions for automated testing and Docker builds. See the status badge at the top for current health. The workflow file is located at `.github/workflows/ci.yml`.

```yaml
name: CI
on: [push, pull_request]
jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      - run: |
          docker build -t qr-code-generator-app:test .
      - run: |
          pytest --maxfail=1 --disable-warnings --cov=.
```

---

## 🔗 Quick Links

* [GitHub Repository](https://github.com/Hanyyoussef4/Assignment7)
* [Docker Hub Image](https://hub.docker.com/r/hany25/qr-code-generator-app)
* [pytest Documentation](https://docs.pytest.org/)
* [GitHub Actions](https://github.com/features/actions)
* [Homebrew](https://brew.sh/)

---

*Happy QR’ing!*
