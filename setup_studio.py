"""Create an isolated project environment and fetch two pinned free voice files."""
from pathlib import Path
import hashlib
import os
import shutil
import subprocess
import sys
import urllib.request
import venv

ROOT = Path(__file__).resolve().parent
BASE = 'https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/'
FILES = {
    'kokoro-v1.0.int8.onnx': '6e742170d309016e5891a994e1ce1559c702a2ccd0075e67ef7157974f6406cb',
    'voices-v1.0.bin': 'bca610b8308e8d99f32e6fe4197e7ec01679264efed0cac9140fe9c29f1fbf7d',
}

def download_models(directory):
    directory.mkdir(parents=True, exist_ok=True)
    def digest(path):
        with path.open('rb') as source:
            return hashlib.file_digest(source, 'sha256').hexdigest()
    for name, expected in FILES.items():
        path = directory/name
        if path.exists() and digest(path) == expected:
            continue
        part = path.with_suffix('.partial')
        try:
            with urllib.request.urlopen(BASE+name, timeout=120) as source, part.open('wb') as out:
                shutil.copyfileobj(source, out)
            if digest(part) != expected:
                raise ValueError(f'Incomplete or different model: {name}. Rerun setup.')
            part.replace(path)
        finally:
            part.unlink(missing_ok=True)

def main():
    if not (3, 11) <= sys.version_info[:2] <= (3, 12):
        raise SystemExit('Use Python 3.11 or 3.12 for the tested dependency range.')
    env = ROOT/'.venv'
    python = env/('Scripts/python.exe' if os.name == 'nt' else 'bin/python')
    if not python.exists():
        venv.EnvBuilder(with_pip=True).create(env)
    subprocess.run([str(python), '-m', 'pip', 'install','-r',str(ROOT/'requirements.txt')], check=True)
    download_models(ROOT/'models')
    subprocess.run([str(python), str(ROOT/'studio/render.py'), '--doctor'],check=True)

if __name__ == '__main__':
    main()
