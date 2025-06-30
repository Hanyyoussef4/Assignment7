import os
import subprocess
import pytest

def test_docker_build_and_run(tmp_path):
    image = "qr-code-generator-app:test"
    # Prepare an isolated output directory
    qr_dir = tmp_path / "qr_codes"
    qr_dir.mkdir()

    # Run the container, mounting tmp_path as /app
    run = subprocess.run(
        [
            "docker", "run", "--rm",
            "-v", f"{qr_dir}:/app/qr_codes",
            image,
            # pass both URLs via new flags
            "--github", "https://example.com",
            "--docker", "https://example.com",
        ],
        capture_output=True,
        text=True,
        timeout=30
    )

    # Should exit cleanly
    assert run.returncode == 0, run.stderr

    # Two QR files should be generated and overwritten each run
    files = list(qr_dir.iterdir())
    # Expect exactly two .png files
    pngs = [f for f in files if f.name.lower().endswith(".png")]
    assert len(pngs) == 2, f"Expected 2 PNGs, found {len(pngs)}: {files!r}"

    # Filenames match our defaults
    names = sorted(f.name for f in pngs)
    assert names == ["docker_qr.png", "github_qr.png"]
