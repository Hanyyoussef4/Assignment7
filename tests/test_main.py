import sys
import os
# Ensure project root is on PYTHONPATH so 'import main' works
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import shutil
from pathlib import Path
import pytest

import main


def test_validate_url_accepts_valid():
    url = "https://example.com/path"
    assert main._validate_url(url, "Test") == url


def test_validate_url_rejects_invalid():
    with pytest.raises(ValueError):
        main._validate_url("not_a_url", "Test")


def test_hex_to_rgb_name_and_hex():
    # Named colour
    assert main._hex_to_rgb("red") == (255, 0, 0)
    # Hex code
    assert main._hex_to_rgb("#00ff00") == (0, 255, 0)
    # Invalid length
    with pytest.raises(ValueError):
        main._hex_to_rgb("#123")


def test_generate_and_overwrite_qr(tmp_path, monkeypatch):
    # Prepare temp output dir
    qr_dir = tmp_path / "qr_codes"
    # Use env vars to point to temp
    monkeypatch.setenv("QR_CODE_DIR", str(qr_dir))
    monkeypatch.setenv("GITHUB_URL", "https://example.com/repo")
    monkeypatch.setenv("DOCKER_URL", "https://example.com/image")

    # Change cwd so main writes here
    monkeypatch.chdir(tmp_path)

    # Ensure no pytest args get in
    monkeypatch.setattr(sys, 'argv', ['main.py'])
    # First run creates files
    main.main()
    files1 = sorted(p.name for p in qr_dir.iterdir() if p.suffix == ".png")
    assert files1 == ["docker_qr.png", "github_qr.png"]

    # Create dummy file to ensure overwrite logic works
    dummy = qr_dir / "github_qr.png"
    dummy.write_text("old")
    # Second run should overwrite without error
    main.main()
    files2 = sorted(p.name for p in qr_dir.iterdir() if p.suffix == ".png")
    assert files2 == ["docker_qr.png", "github_qr.png"]

    # Ensure content is QR binary (not the old dummy text)
    assert dummy.read_bytes()[:2] != b"ol"
