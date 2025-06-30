# 🚀 QR Code Generator App

A simple CLI utility and Dockerized application that generates two QR codes—one for your GitHub repository and one for your Docker Hub image—overwriting old codes each time it runs. Ideal for sharing quick links to your project.

---

## 📋 Table of Contents

1. [Features](#features)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Usage](#usage)

   * [Host (Local)](#host-local)
   * [Docker](#docker)
5. [Testing & Coverage](#testing--coverage)
6. [Configuration](#configuration)
7. [Development & Contribution](#development--contribution)
8. [Academic Integrity](#academic-integrity)

---

## ✨ Features

* Generates **two** QR codes (`github_qr.png` and `docker_qr.png`) in a configurable output directory.
* **Overwrites** existing codes on each run to keep your folder clean.
* Supports **dual-URL mode** via CLI flags `--github` and `--docker`, or environment variables.
* **Colour customization** using `FILL_COLOR` and `BACK_COLOR` (defaults: red on white).
* **Dockerized** for consistent behavior across environments.
* **Comprehensive tests** with pytest and Docker smoke tests, achieving >90% coverage.

---

## 🛠️ Prerequisites

* **Python 3.10+**
* **pip**
* **Docker** (for container usage)

---

## 📥 Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/Hanyyoussef4/Assignment7.git
   cd Assignment7
   ```

2. **Create & activate a virtual environment** (optional but recommended)

   ```bash
   python3 -m venv .venv  # macOS/Linux
   source .venv/bin/activate
   # Windows
   .\.venv\Scripts\activate
   ```

3. **Install Python dependencies**

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

---

## 💻 Usage

### Host (Local)

Generate both QR codes in one go:

```bash
python main.py \
  --github https://github.com/Hanyyoussef4/Assignment7 \
  --docker https://hub.docker.com/r/hany25/qr-code-generator-app
```

Or rely on defaults (baked into the script):

```bash
export GITHUB_URL="https://github.com/Hanyyoussef4/Assignment7"
export DOCKER_URL="https://hub.docker.com/r/hany25/qr-code-generator-app"
python main.py
```

Generated files:

```
qr_codes/github_qr.png
qr_codes/docker_qr.png
```

### Docker

#### Build & Push to Docker Hub

1. **Log in** to Docker Hub:

   ```bash
   docker login
   ```
2. **Build** the image and tag it for your Hub repository:

   ```bash
   docker build -t hany25/qr-code-generator-app:latest .
   ```
3. **Push** the image to your Docker Hub repository:

   ```bash
   docker push hany25/qr-code-generator-app:latest
   ```

   > **What is `docker push`?**
   > The `docker push` command uploads your local Docker image (tagged with your repository name) to Docker Hub, so it can be downloaded and run by others. Without pushing, the image only exists on your machine.

#### Running the Container Locally

Build locally (optional) or pull from Hub:

```bash
# If you just pushed, pull latest
docker pull hany25/qr-code-generator-app:latest
```

Run the container (mounting local `qr_codes` for output):

```bash
docker run --rm \
  -v "$(pwd)/qr_codes:/app/qr_codes" \
  hany25/qr-code-generator-app:latest \
  --github https://github.com/Hanyyoussef4/Assignment7 \
  --docker https://hub.docker.com/r/hany25/qr-code-generator-app
```

Or use Docker Compose:

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

Build the Docker image:

```bash
docker build -t qr-code-generator-app:latest .
```

Run the container (mounting local `qr_codes` for output):

```bash
docker run --rm \
  -v "$(pwd)/qr_codes:/app/qr_codes" \
  qr-code-generator-app:latest \
  --github https://github.com/Hanyyoussef4/Assignment7 \
  --docker https://hub.docker.com/r/hany25/qr-code-generator-app
```

Or use Docker Compose:

```yaml
services:
  qrgen:
    build: .
    volumes:
      - ./qr_codes:/app/qr_codes
    environment:
      GITHUB_URL: https://github.com/Hanyyoussef4/Assignment7
      DOCKER_URL: https://hub.docker.com/r/hany25/qr-code-generator-app
```

```bash
docker compose up --build
docker compose down
```

---

## 🧪 Testing & Coverage

Tests are written with **pytest** and include:

* **Unit tests** (`tests/test_main.py`) validating URL parsing, colour conversion, file overwrite logic.
* **Docker smoke test** (`tests/test_dockerfile.py`) ensuring the container generates both QR codes.

Run all tests with coverage report:

```bash
pytest --maxfail=1 --disable-warnings --cov=.
```

Generate an HTML coverage report:

```bash
pytest --cov=.
pytest --cov-report=html
open htmlcov/index.html
```

Aim for **≥90%** coverage on `main.py`.

---

## ⚙️ Configuration

| Variable      | Description           | Default          |
| ------------- | --------------------- | ---------------- |
| `GITHUB_URL`  | GitHub repository URL | *script default* |
| `DOCKER_URL`  | Docker Hub image URL  | *script default* |
| `QR_CODE_DIR` | Output directory      | `qr_codes`       |
| `FILL_COLOR`  | QR foreground colour  | `red`            |
| `BACK_COLOR`  | QR background colour  | `white`          |

Colors support hex codes (`#rrggbb`) or common names (`red`, `blue`, `navy`).

---

## 🚧 Development & Contribution

1. Fork the repo and create a feature branch:

   ```bash
   git checkout -b feature/my-change
   ```
2. Make changes, add tests, ensure coverage:

   ```bash
   git add . && git commit -m 'feat: …'
   pytest --cov=.
   ```
3. Push and open a Pull Request.

---

## 📜 Academic Integrity

I certify that this submission is my own work. I have neither given nor received unauthorized help on this assignment, and I have not submitted the same work in a previous course.

---

## 🔗 Quick Links

* [Homebrew](https://brew.sh/)
* [Python Downloads](https://www.python.org/downloads/)
* [Docker Desktop](https://www.docker.com/products/docker-desktop/)
* [pytest Documentation](https://docs.pytest.org/)
* [GitHub Actions](https://github.com/features/actions)
