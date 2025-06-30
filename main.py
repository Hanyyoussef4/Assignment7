"""CLI utility to generate QR codes for your GitHub repository and Docker Hub image.

Each run cleans up old QR files so that `github_qr.png` and `docker_qr.png` are overwritten with fresh codes.
By default, QR codes are generated in **red** on a white background.
"""
from __future__ import annotations

import argparse
import logging
import os
import sys
from pathlib import Path
from typing import Final

import qrcode  # pip install qrcode[pil]
import validators  # pip install validators
from dotenv import load_dotenv  # pip install python-dotenv

###############################################################################
# Configuration & defaults
###############################################################################
load_dotenv()

DEFAULT_GITHUB_URL: Final[str] = os.getenv("GITHUB_URL", "https://github.com/Hanyyoussef4/Assignment7")
DEFAULT_DOCKER_URL: Final[str] = os.getenv("DOCKER_URL", "https://hub.docker.com/r/hany25/qr-code-generator-app")

QR_DIRECTORY: Final[str] = os.getenv("QR_CODE_DIR", "qr_codes")
FILL_COLOR: Final[str] = os.getenv("FILL_COLOR", "blue")    # default red fill
BACK_COLOR: Final[str] = os.getenv("BACK_COLOR", "white") # default white back

GITHUB_QR_FILE: Final[str] = "github_qr.png"
DOCKER_QR_FILE: Final[str] = "docker_qr.png"

###############################################################################
# Logging
###############################################################################
def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )

###############################################################################
# Helpers
###############################################################################

def _validate_url(url: str, label: str) -> str:
    if not validators.url(url):
        raise ValueError(f"{label} URL is not valid: {url!r}")
    return url


def _hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    names = {
        "black": "#000000",
        "white": "#ffffff",
        "red":   "#ff0000",
        "green": "#00ff00",
        "blue":  "#0000ff",
        "navy":  "#000080",
    }
    hex_code = names.get(hex_color.lower(), hex_color).lstrip("#")
    if len(hex_code) != 6:
        raise ValueError(f"Invalid colour {hex_color!r}")
    return tuple(int(hex_code[i : i + 2], 16) for i in (0, 2, 4))


def _apply_colour(img):
    img = img.convert("RGB")
    fg = _hex_to_rgb(FILL_COLOR)
    bg = _hex_to_rgb(BACK_COLOR)
    px = img.load()
    w, h = img.size
    for x in range(w):
        for y in range(h):
            px[x, y] = fg if px[x, y] == (0, 0, 0) else bg
    return img


def _generate_qr(url: str, path: Path) -> None:
    qr = qrcode.make(url)
    qr = _apply_colour(qr)
    qr.save(path)

###############################################################################
# Main
###############################################################################

def main() -> None:
    setup_logging()
    parser = argparse.ArgumentParser(
        description="Generate two QR codes, overwriting old ones.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--github", "-g", default=DEFAULT_GITHUB_URL,
                        help="GitHub repository URL (overrides env)")
    parser.add_argument("--docker", "-d", default=DEFAULT_DOCKER_URL,
                        help="Docker-Hub image URL (overrides env)")
    opts = parser.parse_args()

    out_dir = Path(QR_DIRECTORY)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Cleanup existing files before generation
    for fname in (GITHUB_QR_FILE, DOCKER_QR_FILE):
        try:
            (out_dir / fname).unlink()
        except FileNotFoundError:
            pass

    logging.info("Saving QR codes to %s", out_dir.resolve())

    # GitHub QR
    try:
        url = _validate_url(opts.github, "GitHub")
        _generate_qr(url, out_dir / GITHUB_QR_FILE)
        logging.info("Overwrote %s", GITHUB_QR_FILE)
    except ValueError as e:
        logging.error(e)

    # Docker-Hub QR
    try:
        url = _validate_url(opts.docker, "Docker-Hub")
        _generate_qr(url, out_dir / DOCKER_QR_FILE)
        logging.info("Overwrote %s", DOCKER_QR_FILE)
    except ValueError as e:
        logging.error(e)

    logging.info("Done.")


if __name__ == "__main__":
    main()
